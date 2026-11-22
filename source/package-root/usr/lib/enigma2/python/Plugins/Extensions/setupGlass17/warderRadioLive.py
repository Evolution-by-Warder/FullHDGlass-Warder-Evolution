"""Optional live Radio Browser bouquets and demand-loaded Enigma2 radio picons.

The live bouquet replaces the managed legacy entry in the radio index but leaves the old source file untouched as a recovery fallback.
Only this module's own files may be replaced. No network calls run in the GUI.
Radio Warder Evolution supplies the catalogue and the validated logo downloader.
"""
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import signal
import sys
import tempfile
import time
import unicodedata
from urllib.parse import quote, urlsplit
from uuid import UUID

DIRECTORY = Path('/etc/enigma2')
FILE = 'userbouquet.warder.live.radio'
LEGACY_FILE = 'userbouquet.warder.radio'
LEGACY_HEADER = b'#NAME Warder Radio Streams\n'
HEADER = b'#NAME Warder Radio Live\n'
INDEX_LINE = ('#SERVICE 1:7:2:0:0:0:0:0:0:0:FROM BOUQUET "' + FILE + '" ORDER BY bouquet\n').encode()
DATA_FILE = 'warder-radio-live-stations.json'
STATE_FILE = 'warder-radio-live-state.json'
ICON_STATE = 'warder-radio-live-picons.json'
DIAG_FILE = 'warder-radio-live-diagnostics.json'
DAY = 24 * 3600
RETRY = 6 * 3600
INITIAL_RETRY = 15 * 60
BOOTSTRAP_GENERATION = 'live126-world'
MAX_PAGES = 3
MAX_STATIONS = 4000  # Per-country staging, not a global station limit
COUNTRIES_PER_PASS = 2
WORLD_REFRESH_INTERVAL = 7 * DAY
WORLD_STEP_INTERVAL = 5 * 60
PENDING_FILE = 'warder-radio-live-pending.json'
MAX_ICONS = 640  # bounded on-demand cache, not an entire world picon archive
MIN_FREE = 16 * 1024 * 1024
ICON_RETRY_SECONDS = 15 * 60
COUNTRIES = ('SK', 'CZ')
_controller = None


def _plugin():
    # The standalone worker is invoked directly, outside Enigma's Python path.
    plugins_root = str(Path(__file__).resolve().parents[3])
    if plugins_root not in sys.path:
        sys.path.insert(0, plugins_root)
    from Plugins.Extensions.WarderRadio.radio_browser import RadioBrowser
    from Plugins.Extensions.WarderRadio.station_logos import StationLogos
    return RadioBrowser, StationLogos


def _read_json(path, default, limit=1024 * 1024):
    try:
        if path.is_symlink():
            return default
        with path.open('rb') as handle:
            data = handle.read(limit + 1)
        if len(data) > limit:
            return default
        return json.loads(data.decode('utf-8'))
    except (ValueError, UnicodeError, OSError):
        return default


def _write(path, data):
    if path.is_symlink() or (path.exists() and not path.is_file()):
        raise OSError('Unsafe managed path')
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(dir=str(path.parent), prefix='.warder-live-',
                                         delete=False) as handle:
            temporary = Path(handle.name)
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        os.chmod(str(temporary), 0o644)
        os.replace(str(temporary), str(path))
        temporary = None
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def _json_bytes(data):
    return json.dumps(data, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode('utf-8')


def _lock(path):
    return os.fdopen(os.open(str(path), os.O_WRONLY | os.O_CREAT | os.O_NOFOLLOW, 0o600), 'w')


def _safe_file(path):
    return not path.is_symlink() and (not path.exists() or path.is_file())


def _countries(plugin_dir):
    countries = list(COUNTRIES)
    settings = _read_json(plugin_dir / 'state.json', {})
    selected = settings.get('online_country') if isinstance(settings, dict) else ''
    if isinstance(selected, str) and re.fullmatch(r'[A-Za-z]{2}', selected):
        selected = selected.upper()
        if selected not in countries:
            countries.append(selected)
    return countries


def service_stem(uuid):
    """Stable picon/service identity: independent of mutable stream URLs."""
    if not isinstance(uuid, str) or not re.fullmatch(
            r'(?:[0-9a-fA-F]{32}|[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-'
            r'[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12})', uuid):
        raise ValueError('Missing or malformed Radio Browser UUID')
    try:
        canonical = str(UUID(uuid))
    except (ValueError, AttributeError, TypeError):
        raise ValueError('Missing or malformed Radio Browser UUID')
    digest = hashlib.sha256(canonical.encode('ascii')).hexdigest().upper()
    fields = ('4097', '0', '2', digest[:4], digest[4:8], digest[8:12],
              digest[12:20], '0', '0', '0')
    return '_'.join(fields)


def _entry(row):
    uuid, url, name = row.get('stationuuid'), row.get('url'), row.get('name')
    if not isinstance(url, str) or len(url) > 4096 or any(ord(char) < 32 for char in url):
        raise ValueError('Invalid radio URL')
    try:
        parsed = urlsplit(url)
        if (parsed.scheme.lower() not in ('http', 'https') or not parsed.hostname or
                parsed.username is not None or parsed.password is not None):
            raise ValueError('Invalid radio URL')
        _ = parsed.port
    except (ValueError, AttributeError):
        raise ValueError('Invalid radio URL')
    if not isinstance(name, str) or not name.strip():
        raise ValueError('Invalid radio name')
    name = ' '.join(name.split())[:140]
    if not name:
        raise ValueError('Empty radio name')
    stem = service_stem(uuid)
    return {'stem': stem, 'stationuuid': str(UUID(uuid)), 'name': name,
            'url': url, 'favicon': row.get('favicon', ''),
            'homepage': row.get('homepage', '')}


def _service(item):
    fields = item['stem'].replace('_', ':')
    return ('#SERVICE ' + fields + ':' + quote(item['url'], safe='/') +
            '\n#DESCRIPTION ' + item['name'] + '\n')


def _bouquet(groups):
    lines = [HEADER.decode()]
    for code, stations in groups:
        lines.append('#SERVICE 1:64:2:0:0:0:0:0:0:0:\n#DESCRIPTION ' + code + '\n')
        lines.extend(_service(station) for station in stations)
    return ''.join(lines).encode('utf-8')


def _sections(raw):
    """Extract well-formed groups without altering the station reference bytes."""
    if not isinstance(raw, bytes) or not raw.startswith((HEADER, LEGACY_HEADER)):
        return {}
    lines = raw.splitlines(keepends=True)
    groups = {}
    name, content = None, []
    for i in range(1, len(lines)):
        line = lines[i]
        if (line.startswith(b'#SERVICE 1:64:') and i + 1 < len(lines)
                and lines[i + 1].startswith(b'#DESCRIPTION ')):
            if name is not None and name not in groups:
                groups[name] = b''.join(content)
            try:
                name = lines[i + 1][len(b'#DESCRIPTION '):].decode('utf-8').strip()
            except UnicodeError:
                return {}
            if not name or len(name) > 120:
                return {}
            content = [line]
            # The description gets appended by the next iteration.
        elif name is not None:
            content.append(line)
    if name is not None and name not in groups:
        groups[name] = b''.join(content)
    return groups


def _group_name(code, labels):
    """Preserve the classic Slovak/Czech headings across radio generations."""
    preferred = {'SK': 'Slovensko', 'CZ': 'Čechy'}.get(code)
    if preferred and preferred in labels:
        return preferred
    if code in labels:
        return code
    # Historical world bouquets used localized names for some countries;
    # reuse their exact existing heading rather than adding duplicates.
    aliases = {
        'DE': ('Deutschland', 'Germany', 'Nemecko'),
        'FR': ('France', 'Francúzsko'),
        'AT': ('Österreich', 'Austria', 'Rakúsko'),
        'CH': ('Schweiz', 'Switzerland', 'Švajčiarsko'),
        'IT': ('Italia', 'Italy', 'Taliansko'),
        'ES': ('España', 'Spain', 'Španielsko'),
        'GB': ('United Kingdom', 'Great Britain', 'Veľká Británia'),
        'US': ('United States', 'USA', 'Spojené štáty'),
        'PL': ('Polska', 'Poland', 'Poľsko'),
        'HU': ('Magyarország', 'Hungary', 'Maďarsko'),
    }
    for name in aliases.get(code, ()):
        if name in labels:
            return name
    try:
        from Plugins.Extensions.WarderRadio.radio_browser import country_name
        name = country_name(code)
    except (ImportError, ValueError, OSError):
        name = code
    return name if name in labels else (preferred or name)


def _country_sort_key(label):
    """SK, CZ first; remaining displayed country labels sorted accent-insensitively."""
    folded = unicodedata.normalize('NFKD', label.casefold())
    plain = ''.join(char for char in folded if not unicodedata.combining(char))
    normalized = ' '.join(plain.split())
    if normalized in ('slovensko', 'slovakia'):
        return (0, '', label)
    if normalized in ('cechy', 'cesko', 'ceska republika', 'czechia', 'czech republic'):
        return (1, '', label)
    return (2, normalized, label.casefold())


def _station_sort_key(value):
    """Natural, stable, accent-insensitive alphabetic order for displayed names."""
    folded = unicodedata.normalize('NFKD', value.casefold())
    plain = ''.join(char for char in folded if not unicodedata.combining(char))
    return (' '.join(plain.split()), value.casefold())


def _sorted_country_section(section):
    """Sort station records within one country without modifying their bytes.

    Each station is a complete #SERVICE / #DESCRIPTION pair, with optional
    additional metadata attached. If the original layout is unfamiliar, keep
    it untouched rather than risk losing or corrupting receiver services.
    """
    lines = section.splitlines(keepends=True)
    if (len(lines) < 2 or not lines[0].startswith(b'#SERVICE 1:64:')
            or not lines[1].startswith(b'#DESCRIPTION ')):
        return section
    heading = b''.join(lines[:2])
    remaining = lines[2:]
    if not remaining:
        return section
    records = []
    offset = 0
    while offset < len(remaining):
        if (not remaining[offset].startswith(b'#SERVICE ')
                or offset + 1 >= len(remaining)
                or not remaining[offset + 1].startswith(b'#DESCRIPTION ')):
            return section
        try:
            name = remaining[offset + 1][len(b'#DESCRIPTION '):].decode('utf-8').strip()
        except UnicodeError:
            return section
        if not name:
            return section
        finish = offset + 2
        while finish < len(remaining) and not remaining[finish].startswith(b'#SERVICE '):
            finish += 1
        block = b''.join(remaining[offset:finish])
        records.append((_station_sort_key(name), len(records), block))
        offset = finish
    records.sort(key=lambda item: (item[0], item[1]))
    ordered = heading + b''.join(item[2] for item in records)
    if len(ordered) != len(section):
        raise ValueError('Radio sort changed byte count')
    return ordered


def _combined(legacy, current, updates=None):
    """Keep every old country and service, sorting only country-group order."""
    old = _sections(legacy) if legacy is not None else {}
    live = _sections(current) if current is not None else {}
    output = dict(old)
    for name, section in live.items():
        canonical = {'SK': 'Slovensko', 'CZ': 'Čechy'}.get(name, name)
        # Migration: an original world group wins over a partial test124/125
        # country. After source deletion, the full live group is authoritative.
        if canonical not in output:
            if name == 'SK':
                section = section.replace(b'#DESCRIPTION SK\n',
                                          '#DESCRIPTION Slovensko\n'.encode('utf-8'), 1)
            elif name == 'CZ':
                section = section.replace(b'#DESCRIPTION CZ\n',
                                          '#DESCRIPTION Čechy\n'.encode('utf-8'), 1)
            output[canonical] = section
    for name, section in (updates or {}).items():
        output[name] = section
    # Sort all countries and the intact station records inside each one.
    # Never rewrite URLs, Enigma service references or station names.
    names = sorted(output, key=_country_sort_key)
    return HEADER + b''.join(_sorted_country_section(output[name]) for name in names)


def _country_codes(browser, state):
    """Fetch full Radio Browser country inventory once; never filter to SK/CZ."""
    known = state.get('world_countries')
    if isinstance(known, list) and known:
        countries = [value for value in known
                     if isinstance(value, str) and re.fullmatch(r'[A-Z]{2}', value)]
        if countries:
            return list(dict.fromkeys(countries))
    if not hasattr(browser, 'facets'):
        return list(COUNTRIES)
    facets = browser.facets()
    if facets.offline:
        raise OSError('Country inventory unavailable')
    countries = [code for code in facets.countries
                 if isinstance(code, str) and re.fullmatch(r'[A-Z]{2}', code)]
    countries = list(dict.fromkeys([*COUNTRIES, *countries]))
    if len(countries) < 2:
        raise ValueError('Unexpected empty country inventory')
    state['world_countries'] = countries
    return countries


def _managed_legacy(directory):
    """Only the original Warder-managed radio file may be hidden from the index."""
    source = directory / LEGACY_FILE
    if source.is_symlink() or not source.is_file():
        return None
    try:
        if source.stat().st_size > 4 * 1024 * 1024:
            return None
        raw = source.read_bytes()
        return raw if raw.startswith(LEGACY_HEADER) else None
    except OSError:
        return None


def _retire_legacy(directory):
    """Reclaim original Warder radio bytes only after exact migration proof.

    The old managed file and its one managed .bak are deleted only after every
    original country *section* is byte-identical in the registered live file.
    Never delete unknown or user-owned files; never follow symlinks.
    """
    source = directory / LEGACY_FILE
    target = directory / FILE
    original = _managed_legacy(directory)
    if original is None or target.is_symlink() or not target.is_file():
        return False
    old_sections = _sections(original)
    current = target.read_bytes()
    new_sections = _sections(current)
    if (not old_sections or
            len(old_sections) != original.count(b'#SERVICE 1:64:') or
            not all(new_sections.get(name) == _sorted_country_section(body)
                    for name, body in old_sections.items())):
        return False
    # Check registration before deleting any recoverable source data.
    index = directory / 'bouquets.radio'
    if not index.is_file() or index.is_symlink():
        return False
    indexed = index.read_bytes()
    if (INDEX_LINE.strip() not in indexed or
            LEGACY_FILE.encode('ascii') in indexed):
        return False
    metadata = _read_json(directory / STATE_FILE, {})
    if (not isinstance(metadata, dict) or
            metadata.get('bouquet_sha256') != hashlib.sha256(current).hexdigest()):
        return False
    if source.is_symlink() or source.read_bytes() != original:
        return False
    source.unlink()
    # A package-generated previous-version copy is obsolete after the world
    # inventory was preserved byte-for-byte in the new managed live bouquet.
    backup = directory / (LEGACY_FILE + '.bak')
    try:
        if backup.is_file() and not backup.is_symlink() and backup.stat().st_size <= 4 * 1024 * 1024:
            if backup.read_bytes().startswith(LEGACY_HEADER):
                backup.unlink()
    except OSError:
        pass
    return True


def _register(directory):
    """Put the live bouquet first; retire ONLY a verified Warder legacy entry.

    All other radio-bouquet references and their relative order are preserved.
    Rewriting uses a complete atomic file rather than in-place truncation.
    """
    index = directory / 'bouquets.radio'
    if not _safe_file(index):
        raise OSError('Unsafe radio index')
    if index.exists() and index.stat().st_size > 512 * 1024:
        raise ValueError('Oversized radio index')
    before = index.read_bytes() if index.exists() else b''
    if before and b'\x00' in before:
        raise ValueError('Invalid radio index')
    lines = before.splitlines(keepends=True)
    legacy_state = _read_json(directory / STATE_FILE, {})
    legacy_owned = (_managed_legacy(directory) is not None or
                    isinstance(legacy_state, dict) and
                    legacy_state.get('legacy_retired') is True)
    path_re = re.compile(rb'^#SERVICE[ \t]+[^\r\n]*FROM BOUQUET "([^"\r\n]+)"')
    kept = []
    for line in lines:
        match = path_re.match(line)
        if match and (match.group(1) == FILE.encode('ascii') or
                      (legacy_owned and match.group(1) == LEGACY_FILE.encode('ascii'))):
            continue
        kept.append(line)
    # Put the new bouquet immediately after the radio-index heading.
    # Preserve every other byte, apart from a necessary newline for insertion.
    if kept and kept[0].startswith(b'#NAME '):
        first, tail = kept[0], kept[1:]
        ending = b'\r\n' if first.endswith(b'\r\n') else b'\n'
        if not first.endswith(b'\n'):
            first += ending
        result = first + INDEX_LINE + b''.join(tail)
    else:
        result = b'#NAME Bouquets (Radio)\n' + INDEX_LINE + b''.join(kept)
    if result == before:
        return False
    if index.exists() and index.read_bytes() != before:
        raise OSError('Concurrent radio index edit')
    _write(index, result)
    return True


def bootstrap(directory=DIRECTORY):
    """Local-only first-paint preparation, no online or Enigma2 imports.

    The preexisting managed streams, if any, seed the new filename until the
    background Radio Browser refresh replaces them. Their original file remains
    untouched for rollback and must no longer be registered as another bouquet.
    """
    directory = Path(directory)
    target = directory / FILE
    state_path = directory / STATE_FILE
    index = directory / 'bouquets.radio'
    if not all(_safe_file(p) for p in (target, state_path, index)):
        return {'changed': False, 'skipped': 'unsafe-path'}
    with _lock(directory / (STATE_FILE + '.lock')) as handle:
        try:
            fcntl.flock(handle, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            return {'changed': False, 'skipped': 'busy'}
        existing = target.read_bytes() if target.exists() else None
        if existing is not None and not existing.startswith(HEADER):
            return {'changed': False, 'skipped': 'unmanaged'}
        state = _read_json(state_path, {})
        if not isinstance(state, dict):
            state = {}
        created = False
        legacy = _managed_legacy(directory)
        if existing is not None:
            expected = state.get('bouquet_sha256')
            if not isinstance(expected, str) or hashlib.sha256(existing).hexdigest() != expected:
                return {'changed': False, 'skipped': 'owner-modified'}
        if existing is None and legacy is None:
            raw = HEADER + (
                '#SERVICE 1:64:2:0:0:0:0:0:0:0:\n'
                '#DESCRIPTION Načítavanie rádií…\n'
            ).encode('utf-8')
            origin = 'empty-fallback'
        else:
            raw = _combined(legacy, existing)
            origin = 'legacy-world' if legacy else 'current-live'
        if raw != existing:
            if len(raw) > 12 * 1024 * 1024:
                raise ValueError('World radio bouquet exceeds safe size')
            _write(target, raw)
            created = True
            state['bouquet_sha256'] = hashlib.sha256(raw).hexdigest()
        if state.get('bootstrap_generation') != BOOTSTRAP_GENERATION:
            state['bootstrap_generation'] = BOOTSTRAP_GENERATION
            state.pop('success', None)
            state.pop('attempt', None)
            state['world_cursor'] = 0
            state['seed_origin'] = origin
            _write(state_path, _json_bytes(state))
        elif created:
            _write(state_path, _json_bytes(state))
        moved = _register(directory)
        retired = _retire_legacy(directory)
        if retired:
            state['legacy_retired'] = True
            _write(state_path, _json_bytes(state))
        return {'changed': created or moved, 'created': created,
                'legacy_retired': retired, 'legacy_hidden': retired or
                _managed_legacy(directory) is not None}


def refresh(directory=DIRECTORY, now=None, browser=None):
    """Incrementally refresh every Radio Browser country, preserving old groups.

    Only two countries and up to three pages per country are processed in one
    worker. A larger country's staged pages are resumed on the next pass.
    The legacy world bouquet remains fully usable during the entire cycle.
    """
    directory = Path(directory)
    now = time.time() if now is None else now
    if now < 1700000000:
        return {'changed': False, 'skipped': 'clock'}
    target = directory / FILE
    index = directory / 'bouquets.radio'
    data = directory / DATA_FILE
    pending_path = directory / PENDING_FILE
    state_path = directory / STATE_FILE
    if not all(_safe_file(path) for path in (target, index, data, state_path,
                                              pending_path)):
        return {'changed': False, 'skipped': 'unsafe-path'}
    before = target.read_bytes() if target.exists() else None
    if before is not None and not before.startswith(HEADER):
        return {'changed': False, 'skipped': 'unmanaged'}
    with _lock(directory / (STATE_FILE + '.lock')) as handle:
        try:
            fcntl.flock(handle, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            return {'changed': False, 'skipped': 'busy'}
        state = _read_json(state_path, {})
        if not isinstance(state, dict):
            state = {}
        if before is None and state.get('bootstrap_generation') != BOOTSTRAP_GENERATION:
            state['bootstrap_generation'] = BOOTSTRAP_GENERATION
            state.pop('attempt', None)
        if before is not None:
            expected = state.get('bouquet_sha256', '')
            if (not isinstance(expected, str) or
                    not re.fullmatch(r'[0-9a-f]{64}', expected) or
                    hashlib.sha256(before).hexdigest() != expected):
                return {'changed': False, 'skipped': 'owner-modified'}
        success, attempt = state.get('success', 0), state.get('attempt', 0)
        complete = state.get('world_complete', False) is True
        if before is not None and complete and success and 0 <= now-success < WORLD_REFRESH_INTERVAL:
            changed = _register(directory)
            return {'changed': changed, 'skipped': 'not-due'}
        retry = WORLD_STEP_INTERVAL if before is not None else INITIAL_RETRY
        if attempt and 0 <= now-attempt < retry:
            changed = _register(directory) if before is not None else False
            return {'changed': changed, 'skipped': 'not-due'}
        state['attempt'] = now
        _write(state_path, _json_bytes(state))

        if browser is None:
            RadioBrowser, _ = _plugin()
            browser = RadioBrowser('/etc/enigma2/warder-radio')
        codes = _country_codes(browser, state)
        # A selected country should also be included if older Radio Browser
        # inventory data has not listed it yet.
        codes = list(dict.fromkeys([*codes, *_countries(directory / 'warder-radio')]))
        if not codes:
            raise ValueError('Empty world country inventory')
        cursor = state.get('world_cursor', 0)
        if type(cursor) is not int or not 0 <= cursor < len(codes):
            cursor = 0
        staged = _read_json(pending_path, {}, 4 * 1024 * 1024)
        if not isinstance(staged, dict):
            staged = {}
        old_sections = _sections(_managed_legacy(directory))
        current_sections = _sections(before)
        labels = {*old_sections, *current_sections}
        updates, updated_rows = {}, {}
        done = 0
        for _ in range(COUNTRIES_PER_PASS):
            if cursor >= len(codes):
                break
            code = codes[cursor]
            continuing = staged.get('country') == code
            rows = staged.get('rows', []) if continuing else []
            offset = staged.get('offset', 0) if continuing else 0
            if (not isinstance(rows, list) or type(offset) is not int or
                    not 0 <= offset <= MAX_STATIONS or len(rows) > MAX_STATIONS):
                rows, offset = [], 0
            known = {item.get('stationuuid') for item in rows if isinstance(item, dict)}
            more = False
            for _page in range(MAX_PAGES):
                result = browser.page(country=code, offset=offset)
                if result.offline:
                    raise OSError('Radio Browser offline; preserving existing world bouquet')
                for station in result.rows:
                    try:
                        item = _entry(station)
                    except (ValueError, TypeError, AttributeError):
                        continue
                    if item['stationuuid'] in known:
                        continue
                    known.add(item['stationuuid'])
                    rows.append(item)
                offset += 60
                more = bool(result.more)
                if not more:
                    break
                if len(rows) >= MAX_STATIONS:
                    break
            if more and len(rows) < MAX_STATIONS:
                _write(pending_path, _json_bytes({
                    'country': code, 'offset': offset, 'rows': rows[:MAX_STATIONS]
                }))
                break
            # Never publish a truncated country as the complete replacement of
            # its older complete group. Retain previous valid data instead.
            staged = {}
            if rows and not more:
                name = _group_name(code, labels)
                for row in rows:
                    row['countrycode'] = code
                updates[name] = _bouquet([(name, rows)])[len(HEADER):]
                updated_rows[code] = rows
                labels.add(name)
            elif code in COUNTRIES and not before and not old_sections:
                raise ValueError('Empty core country; keep previous bouquet')
            cursor += 1
            done += 1
            _write(pending_path, b'{}')
        finished = cursor >= len(codes)
        if finished:
            state['success'] = now
            state['world_complete'] = True
            state['world_cursor'] = 0
            # Refresh the inventory on the next complete weekly cycle.
            state.pop('world_countries', None)
        else:
            state['world_complete'] = False
            state['world_cursor'] = cursor
        raw = _combined(_managed_legacy(directory), before, updates)
        if not _sections(raw):
            raise ValueError('World radio bouquet has no stations')
        if len(raw) > 16 * 1024 * 1024:
            raise ValueError('World radio bouquet exceeds receiver-safe limit')
        if target.exists() and target.read_bytes() != before:
            raise OSError('Concurrent world bouquet edit')
        mapping = _read_json(data, {}, 24 * 1024 * 1024)
        old_rows = mapping.get('stations', []) if isinstance(mapping, dict) else []
        previous = [row for row in old_rows
                    if isinstance(row, dict) and row.get('countrycode') not in updated_rows]
        saved = previous + [row for rows in updated_rows.values() for row in rows]
        mapping_bytes = _json_bytes({'schema': 1, 'stations': saved})
        if len(mapping_bytes) > 24 * 1024 * 1024:
            raise ValueError('Radio picon mapping exceeds receiver-safe limit')
        if not data.exists() or data.read_bytes() != mapping_bytes:
            _write(data, mapping_bytes)
        changed = raw != before
        if changed:
            if before is not None:
                _write(directory / (FILE + '.bak'), before)
            _write(target, raw)
        registered = _register(directory)
        state['bouquet_sha256'] = hashlib.sha256(raw).hexdigest()
        _write(state_path, _json_bytes(state))
        return {'changed': changed or registered, 'stations': len(saved),
                'countries': len(_sections(raw)),
                'world_total': len(codes), 'world_processed': cursor,
                'world_complete': finished, 'processed_this_run': done}


def _skin_picon_directory():
    """Resolve FullHDGlass PATHS at GUI runtime; never write into Own picons."""
    try:
        from Components.config import config
        from .warderUserPicons import selected_source
        enabled, _ = selected_source(config)
        if enabled:
            return None
        base = config.plugins.setupGlass17.par39.value
        if not isinstance(base, str) or not base.startswith('/') or not base.strip():
            return None
        root = Path(base)
        # A configured PATHS root must be on real external media.
        if root.is_symlink() or not root.is_dir() or os.stat(str(root)).st_dev == os.stat('/').st_dev:
            return None
        directory = root / 'picon'
        if directory.is_symlink():
            return None
        if directory.exists() and (not directory.is_dir() or
                                   not os.access(str(directory), os.W_OK)):
            return None
        # Do not create directories on Enigma's GUI thread. The child process
        # validates the removable-media mount again before creating this one.
        check = directory if directory.exists() else root
        vfs = os.statvfs(str(check))
        if vfs.f_bavail * vfs.f_frsize < MIN_FREE:
            return None
        return str(directory)
    except (AttributeError, ImportError, OSError, TypeError, ValueError):
        return None


def _radio_world_root():
    """Read PATHS for radio bundles without creating folders on the GUI thread."""
    try:
        from Components.config import config
        value = config.plugins.setupGlass17.par39.value
        if not isinstance(value, str) or not value.startswith('/'):
            return None
        root = Path(value)
        if (root.name != 'hdg17_files' or root.is_symlink() or
                not root.is_dir() or root.stat().st_dev == Path('/').stat().st_dev):
            return None
        vfs = os.statvfs(str(root))
        if vfs.f_bavail * vfs.f_frsize < MIN_FREE:
            return None
        return root
    except (AttributeError, ImportError, OSError, TypeError, ValueError):
        return None


def _radio_custom_picons_enabled():
    """Explicit user-owned picon source must not be overwritten by radio ZIP."""
    try:
        from Components.config import config
        from .warderUserPicons import selected_source
        return selected_source(config)[0]
    except (AttributeError, ImportError, TypeError, ValueError):
        return True


def _picon_dir():
    """Use existing picon folder on a truly mounted disk; never fill image flash."""
    root = os.stat('/').st_dev
    for mount in ('/media/hdd', '/media/usb', '/media/mmc'):
        parent = Path(mount)
        try:
            if parent.is_symlink() or not parent.is_dir() or os.stat(str(parent)).st_dev == root:
                continue
            path = parent / 'picon'
            if (path.is_dir() and not path.is_symlink() and
                    os.access(str(path), os.W_OK)):
                vfs = os.statvfs(str(path))
                if vfs.f_bavail * vfs.f_frsize >= MIN_FREE:
                    return path
        except OSError:
            continue
    return None


def _owned(path, entries, directory):
    """True only when this exact unchanged file was generated by this worker."""
    record = entries.get(path.name)
    if not isinstance(record, dict) or record.get('directory') != str(directory):
        return False
    if path.is_symlink() or not path.is_file():
        return False
    try:
        if path.stat().st_size > 512 * 1024:
            return False
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        return digest == record.get('sha256')
    except OSError:
        return False


def _purge_owned(entries, directory, keep):
    """Bound picon count, preserving all unowned or user-modified files."""
    if len(entries) <= MAX_ICONS:
        return
    order = sorted(
        ((name, record) for name, record in entries.items()
         if isinstance(record, dict) and record.get('directory') == str(directory)
         and isinstance(record.get('at'), (int, float))),
        key=lambda pair: pair[1]['at'])
    for name, _ in order:
        if len(entries) <= MAX_ICONS:
            break
        if name in keep or not re.fullmatch(r'(?:4097|1)_[0-9A-F_]+\.png', name):
            continue
        path = directory / name
        if _owned(path, entries, directory):
            try:
                path.unlink()
            except OSError:
                continue
        entries.pop(name, None)


def _picon_png(source, width=220, height=132):
    """Fit the trusted radio logo into a transparent 16:9-ish Enigma2 picon.

    No distortion, letterboxing with alpha, no branding overlay. Executed only
    in the background download worker, never in the main GUI thread.
    """
    import io
    from PIL import Image
    with Image.open(io.BytesIO(source), formats=('PNG',)) as logo:
        if (logo.width < 24 or logo.height < 24 or
                logo.width * logo.height > 1024 * 1024):
            raise ValueError('Unsafe radio logo dimensions')
        image = logo.convert('RGBA')
        image.thumbnail((width, height),
                        Image.Resampling.LANCZOS if hasattr(Image, 'Resampling')
                        else Image.LANCZOS)
        canvas = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        canvas.alpha_composite(image, ((width - image.width) // 2,
                                       (height - image.height) // 2))
        output = io.BytesIO()
        canvas.save(output, 'PNG', compress_level=6)
        return output.getvalue()


def get_icon(stem, directory=DIRECTORY, store=None, destination=None):
    """Download or refresh one logo; never change an unowned native picon.

    The source plugin validates PNG pixels and external HTTP hosts. This worker
    validates the actual cached PNG and limits per-receiver writes.
    """
    directory = Path(directory)
    if not re.fullmatch(r'4097_0_2_(?:[0-9A-F]{1,8}_){6}[0-9A-F]{1,8}', stem):
        return {'changed': False, 'skipped': 'invalid-stem'}
    mapping = _read_json(directory / DATA_FILE, {})
    rows = mapping.get('stations') if isinstance(mapping, dict) else None
    if not isinstance(rows, list):
        return {'changed': False, 'skipped': 'missing-map'}
    item = next((row for row in rows if isinstance(row, dict) and row.get('stem') == stem), None)
    if not item:
        return {'changed': False, 'skipped': 'unknown-station'}
    target_dir = Path(destination) if destination is not None else _picon_dir()
    if target_dir is None or not target_dir.is_dir() or target_dir.is_symlink():
        return {'changed': False, 'skipped': 'no-picon-dir'}
    target = target_dir / (stem + '.png')
    alias = target_dir / ('1' + stem[4:] + '.png')
    state_path = directory / ICON_STATE
    if not _safe_file(state_path):
        return {'changed': False, 'skipped': 'unsafe-state'}
    with _lock(directory / (ICON_STATE + '.lock')) as handle:
        try:
            fcntl.flock(handle, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            return {'changed': False, 'skipped': 'busy'}
        state = _read_json(state_path, {})
        entries = state.get('files', {}) if isinstance(state, dict) else {}
        if not isinstance(entries, dict):
            entries = {}
        paths = (target, alias)
        # A custom/approved picon owns both reference variants. Never mix
        # an online graphic beside an explicitly installed user version.
        if any(p.exists() and not _owned(p, entries, target_dir) or p.is_symlink()
               for p in paths):
            return {'changed': False, 'skipped': 'already-present'}
        now = time.time()
        if all(p.is_file() for p in paths) and all(
                0 <= now - entries[p.name]['at'] < DAY * 7 for p in paths):
            return {'changed': False, 'skipped': 'already-present'}
        if store is None:
            _, StationLogos = _plugin()
            store = StationLogos('/etc/enigma2/warder-radio')
        source = store.get(item)
        if not source or not Path(source).is_file() or Path(source).is_symlink():
            return {'changed': False, 'skipped': 'no-logo'}
        with open(source, 'rb') as inp:
            content = inp.read(512 * 1024 + 1)
        if not content.startswith(b'\x89PNG\r\n\x1a\n') or len(content) > 512 * 1024:
            return {'changed': False, 'skipped': 'bad-logo'}
        try:
            content = _picon_png(content)
        except (ValueError, OSError, ImportError):
            return {'changed': False, 'skipped': 'bad-logo'}
        checksum = hashlib.sha256(content).hexdigest()
        changed = False
        # Two canonical Enigma2 reference names are supported. Keep ownership
        # and individual checksums, so custom replacements always win.
        for p in paths:
            if p.is_file():
                if not _owned(p, entries, target_dir):
                    return {'changed': changed, 'skipped': 'user-modified'}
                if entries[p.name]['sha256'] != checksum:
                    _write(p, content)
                    changed = True
            else:
                try:
                    with os.fdopen(os.open(str(p), os.O_WRONLY | os.O_CREAT |
                                          os.O_EXCL | os.O_NOFOLLOW, 0o644), 'wb') as output:
                        output.write(content)
                        output.flush()
                        os.fsync(output.fileno())
                except FileExistsError:
                    return {'changed': changed, 'skipped': 'user-modified'}
                changed = True
            entries[p.name] = {'directory': str(target_dir), 'sha256': checksum, 'at': now}
        _purge_owned(entries, target_dir, {p.name for p in paths})
        _write(state_path, _json_bytes({'files': entries}))
        return {'changed': changed}


def request_picon(reference):
    """Nonblocking GUI callback for a visible service-list radio row."""
    controller = _controller
    if controller is not None and not getattr(controller, 'local_world_sha', None):
        controller.enqueue_icon(reference)


def cached_country_picon(references, base):
    """Fast in-memory UUID ownership test before reading radio-only PNG path.

    Normal TV/SAT, custom/Own Picons, and unrecognized stations retain their
    existing native lookup. No Radio Browser, JSON or HTTP per rendered row.
    """
    controller = _controller
    if (controller is None or
            not isinstance(base, str) or not base or
            not isinstance(references, (tuple, list))):
        return ''
    known = getattr(controller, 'known_icons', set())
    folder = os.path.join(base, 'picon', 'radio')
    # The selected separate country owns a different UUID map than the legacy
    # single Warder Live bouquet. Cache only that signed country's logo members.
    owner = os.path.join(folder, '.warder-radio-country.json')
    try:
        mtime = os.stat(owner).st_mtime_ns if not os.path.islink(owner) else None
    except OSError:
        mtime = None
    if mtime != getattr(controller, 'country_logo_mtime', None):
        record = _read_json(Path(owner), {}, 4 * 1024 * 1024) if mtime else {}
        valid = isinstance(record, dict) and record.get('owner') == 'WarderRadioLive'
        files = record.get('files') if valid else {}
        controller.country_logo_stems = {
            name[:-4] for name in files if isinstance(name, str)
            and re.fullmatch(r'4097_0_2_(?:[0-9A-F]{1,8}_){6}[0-9A-F]{1,8}\.png', name)
        } if isinstance(files, dict) else set()
        controller.country_logo_mtime = mtime
    known = known | getattr(controller, 'country_logo_stems', set())
    for stem in references:
        if not isinstance(stem, str):
            continue
        exact = '4097' + stem[1:] if stem.startswith('1_') else stem
        if exact in known:
            path = os.path.join(folder, exact + '.png')
            if os.path.isfile(path):
                return path
    # Never use an online/fallback logo to override a signed original. This
    # path is radio-only and bound to the active owned country, never TV/SAT.
    try:
        from . import warderRadioCountryBouquets as country_bouquets
        selected = country_bouquets.selected_country(DIRECTORY)
        if selected:
            online = os.path.join(base, 'picon', 'radio', selected)
            path = os.path.join(online, '.warder-radio-online-source.json')
            mtime = os.stat(path).st_mtime_ns if not os.path.islink(path) else None
            key = (selected, mtime)
            if key != getattr(controller, 'country_online_mtime', None):
                record = _read_json(Path(path), {}, 4 * 1024 * 1024)
                files = (record.get('files') if isinstance(record, dict)
                         and record.get('owner') == 'WarderRadioOnline'
                         and record.get('country') == selected else {})
                controller.country_online_stems = {
                    name[:-4] for name in files
                    if isinstance(name, str) and
                    re.fullmatch(r'4097_0_2_(?:[0-9A-F]{1,8}_){6}[0-9A-F]{1,8}\.png', name)
                } if isinstance(files, dict) else set()
                controller.country_online_mtime = key
            known_online = getattr(controller, 'country_online_stems', set())
            for stem in references:
                if not isinstance(stem, str):
                    continue
                exact = '4097' + stem[1:] if stem.startswith('1_') else stem
                if exact in known_online:
                    asset = os.path.join(online, exact + '.png')
                    if os.path.isfile(asset) and not os.path.islink(asset):
                        return asset
    except (ImportError,AttributeError,OSError,TypeError,ValueError):
        pass
    return ''


class Controller:
    def __init__(self, event_loop=None, reload_bouquets=None, session=None):
        from .warderHelpPreview import _NativeLoop
        self.loop = event_loop or _NativeLoop()
        self.reload = reload_bouquets or self._reload
        self.session = session
        self.radio_refresh_timer = None
        self.pending = self.loop.callLater(25, self.check)
        self.icon_timer = self.loop.callLater(25, self.check_icon)
        self.world_timer = self.loop.callLater(5, self.check_world)
        self.worker = None
        self.icon_worker = None
        self.world_worker = None
        self.timeout = None
        self.world_timeout = None
        self.active_local_key = None
        self.local_worker_key = None
        self.local_world_sha = None
        self.country_logo_stems = set()
        self.country_logo_mtime = None
        self.country_online_mtime = None
        self.country_online_stems = set()
        self.observed_native_country = None
        self.last_bulk_logo = None
        self.closed = False
        self.initial_reload = True
        self.last_icon = None
        self.icon_queue = []
        self.known_icons = set()
        self.icon_requested = {}
        self.map_mtime = None
        self._load_icon_map()

    @staticmethod
    def _reload():
        from enigma import eDVBDB
        eDVBDB.getInstance().reloadBouquets()

    def _spawn(self, action, args, callback):
        from .warderHelpPreview import _Worker
        worker = _Worker(callback)
        path = os.path.abspath(__file__)
        if action in ('refresh', 'local', 'world', 'logo_zip'):
            path = os.path.join(os.path.dirname(path), 'warderRadioCountry.py')
        self.loop.spawnProcess(worker, '/usr/bin/python3', ['/usr/bin/python3', path] + args,
                               env=dict(os.environ))
        return worker

    def request_refresh(self):
        """Immediately schedule a selected-country refresh from the MENU."""
        if self.closed:
            return
        if self.pending is not None and self.pending.active():
            self.pending.cancel()
        self.pending = self.loop.callLater(1 if self.worker is None else 3, self.check)

    def check(self):
        self.pending = None
        if self.closed:
            return
        if self.worker is not None:
            self.pending = self.loop.callLater(3, self.check)
            return
        try:
            root = _radio_world_root()
            from . import warderRadioCountry as country
            selected = country._pending_country(country._choice(DIRECTORY))
            if not selected:
                selected = country.active_country(DIRECTORY)
            from . import warderRadioWorld as world
            digest = world.cached_country(root, selected) if root is not None else None
            if digest:
                self.local_world_sha = digest
                key = (selected, digest)
                if selected == country.active_country(DIRECTORY) and (
                        country._pending_country(country._choice(DIRECTORY)) is None and
                        self.active_local_key == key):
                    self.pending = self.loop.callLater(3600, self.check)
                    return
                self.local_worker_key = key
                self.worker = self._spawn(
                    'local', ['--activate-world', selected, str(root)], self.finished)
            else:
                self.local_world_sha = None
                self.local_worker_key = None
                self.worker = self._spawn('refresh', ['--refresh'], self.finished)
            self.timeout = self.loop.callLater(90, self.timed_out)
        except Exception:
            self.finished(None)

    def check_world(self):
        """Fetch a new world snapshot off the GUI; 14-day successful cadence."""
        self.world_timer = None
        if self.closed:
            return
        root = _radio_world_root()
        if root is None:
            self.world_timer = self.loop.callLater(3600, self.check_world)
            return
        if self.world_worker is not None:
            self.world_timer = self.loop.callLater(60, self.check_world)
            return
        try:
            self.world_worker = self._spawn(
                'world', ['--sync-world', str(root)], self.world_done)
            self.world_timeout = self.loop.callLater(210, self.world_timed_out)
        except Exception:
            self.world_done(None)

    def world_done(self, result):
        self.world_worker = None
        if self.world_timeout is not None and self.world_timeout.active():
            self.world_timeout.cancel()
        self.world_timeout = None
        if self.closed:
            return
        valid = isinstance(result, dict)
        ready = valid and (result.get('changed') or
                           result.get('skipped') == 'already-current')
        if valid and result.get('changed'):
            self.active_local_key = None
            self.request_refresh()
        # An absent/unpublished index is NOT treated as a completed refresh.
        if valid and result.get('pending_source'):
            # A preview country list is NOT a published, signed world.
            delay = 6 * 3600
        elif valid and result.get('skipped') == 'not-due':
            seconds = result.get('retry_after')
            delay = max(60, min(14 * DAY, seconds)) if (
                type(seconds) is int and seconds > 0) else 6 * 3600
        else:
            delay = 14 * DAY if ready else 6 * 3600
        self.world_timer = self.loop.callLater(delay, self.check_world)

    def world_timed_out(self):
        self.world_timeout = None
        if self.world_worker is not None:
            try:
                self.world_worker.transport.kill()
            except Exception:
                pass

    def _refresh_visible_radio_list(self, reset_to_top=True):
        """Refresh an open Enigma2 radio list after a progressive country update.

        DVBDB.reloadBouquets alone does not invalidate the visible ServiceList
        root. The selection window otherwise keeps showing the old country's
        entries until it is closed/reopened.
        """
        self.radio_refresh_timer = None
        if self.closed or self.session is None:
            return False
        try:
            dialog = getattr(self.session, 'current_dialog', None)
            if dialog is None or not getattr(dialog, 'shown', False):
                return False
            if not any(cls.__name__ == 'ChannelSelectionRadio'
                       for cls in type(dialog).__mro__):
                return False
            root = dialog.getRoot()
            path = root.getPath() if root is not None else ''
            if not isinstance(path, str) or not (
                    'FROM BOUQUET "' + FILE + '"' in path or
                    'FROM BOUQUET "bouquets.radio"' in path):
                return False
            listing = dialog.servicelist
            if getattr(listing, 'instance', None) is None:
                return False
            # Enigma2 resetRoot preserves the OLD numeric row index. While
            # background pages are alphabetically inserted, retain the same
            # selected service instead. Only a new country's FIRST page
            # should place the selection at the beginning of the list.
            selected = None
            if not reset_to_top and hasattr(listing, 'getCurrent'):
                selected = listing.getCurrent()
            listing.resetRoot()
            if reset_to_top and 'FROM BOUQUET "' + FILE + '"' in path:
                listing.goTop()
            elif selected is not None and hasattr(listing, 'setCurrent'):
                listing.setCurrent(selected, adjust=False)
            return True
        except (AttributeError, OSError, RuntimeError, TypeError):
            return False

    def finished(self, result):
        self.worker = None
        if self.timeout is not None and self.timeout.active():
            self.timeout.cancel()
        self.timeout = None
        if self.closed:
            return
        has_bouquet = (DIRECTORY / FILE).is_file()
        valid = isinstance(result, dict)
        switched = valid and result.get('changed') and bool(result.get('country'))
        first_page = not valid or result.get('first_page', True)
        if valid and result.get('local') and result.get('country'):
            self.active_local_key = getattr(self, 'local_worker_key', None)
            self._load_icon_map()
            if self.icon_timer is not None and self.icon_timer.active():
                self.icon_timer.cancel()
            self.icon_timer = self.loop.callLater(0.2, self.check_icon)
        if valid and (result.get('changed') or
                      (self.initial_reload and has_bouquet)):
            try:
                self.reload()
                self.initial_reload = False
                if switched:
                    self._refresh_visible_radio_list(reset_to_top=first_page)
                    # The ChoiceBox may be closing as the first cached page
                    # arrives. Retry once without blocking the channel list.
                    if self.radio_refresh_timer is not None and self.radio_refresh_timer.active():
                        self.radio_refresh_timer.cancel()
                    self.radio_refresh_timer = self.loop.callLater(
                        1, lambda: self._refresh_visible_radio_list(
                            reset_to_top=first_page))
            except Exception:
                pass
        preference = _read_json(DIRECTORY / 'warder-radio-live-country.json', {})
        deferred = _read_json(DIRECTORY / 'warder-radio-live-country-request.json', {})
        awaiting_country = ((isinstance(preference, dict) and
                             isinstance(preference.get('pending'), str)) or
                            (isinstance(deferred, dict) and
                             isinstance(deferred.get('country'), str) and
                             re.fullmatch(r'[A-Z]{2}', deferred['country'])))
        partial = valid and (result.get('incomplete') is True or
                             result.get('skipped') == 'country-superseded')
        if self.pending is not None and self.pending.active():
            self.pending.cancel()
        # Resume paginated countries promptly. If the remote catalogue fails,
        # keep the existing stations but revisit the pending choice, rather
        # than going silent for one hour after the first unsuccessful attempt.
        delay = (3 if partial else 60 if awaiting_country else
                 60 if self.initial_reload and not has_bouquet else
                 120 if result is None else 3600)
        self.pending = self.loop.callLater(delay, self.check)

    def timed_out(self):
        self.timeout = None
        if self.worker is not None:
            try:
                self.worker.transport.kill()
            except Exception:
                pass

    def _load_icon_map(self):
        mapping = DIRECTORY / DATA_FILE
        mtime = mapping.stat().st_mtime_ns if mapping.is_file() and not mapping.is_symlink() else None
        if mtime == self.map_mtime:
            return
        self.map_mtime = mtime
        data = _read_json(mapping, {}, 24 * 1024 * 1024) if mtime is not None else {}
        rows = data.get('stations', []) if isinstance(data, dict) else []
        self.known_icons = {row.get('stem') for row in rows if isinstance(row, dict)
                            and isinstance(row.get('stem'), str)}
        self.icon_requested.clear()
        initial, seen = [], {}
        for row in rows:
            if not isinstance(row, dict):
                continue
            code = row.get('countrycode', '')
            seen[code] = seen.get(code, 0) + 1
            # Do not fetch every radio logo in the worldwide catalogue.
            # Radio Browser images are demand-loaded for visible list rows.
            if seen[code] <= 8:
                initial.append(row.get('stem', ''))
        self.icon_queue = [stem for stem in initial if stem in self.known_icons]

    def enqueue_icon(self, reference):
        """Queue one visible radio without doing network or disk I/O per row."""
        if self.closed:
            return
        try:
            fields = (reference if isinstance(reference, str) else
                      reference.toString()).split(':', 10)
            stem = '_'.join(field.upper() for field in fields[:10])
            if len(fields) < 11 or not re.fullmatch(
                    r'4097_0_2_(?:[0-9A-F]{1,8}_){6}[0-9A-F]{1,8}', stem):
                return
            last_attempt = self.icon_requested.get(stem)
            if last_attempt is not None and time.monotonic() - last_attempt < ICON_RETRY_SECONDS:
                return
            # Only the visible live-bouquet identities are accepted.
            if stem not in self.known_icons:
                return
            # A repeated render must not cancel and postpone the same pending
            # download timer. Only elevate a station that is not already first.
            if self.icon_queue and self.icon_queue[0] == stem:
                return
            if stem in self.icon_queue:
                self.icon_queue.remove(stem)
            self.icon_queue.insert(0, stem)
            self.icon_queue = self.icon_queue[:48]
            # The cooldown starts only when the background worker was spawned.
            # A missing/unmounted PATHS directory must never permanently block retry.
            if self.icon_worker is None:
                if self.icon_timer is not None and self.icon_timer.active():
                    self.icon_timer.cancel()
                self.icon_timer = self.loop.callLater(0.3, self.check_icon)
        except (AttributeError, TypeError, ValueError):
            return

    def _observe_country_bouquet(self):
        """Native radio ServiceList focus is authoritative for selected logo ZIP."""
        if self.session is None:
            return None
        try:
            from . import warderRadioCountryBouquets as country_bouquets
            dialog = getattr(self.session, 'current_dialog', None)
            if dialog is None or not getattr(dialog, 'shown', False):
                try:
                    from Screens.InfoBar import InfoBar
                    info = InfoBar.instance
                    dialog = info.servicelist if info is not None else None
                except (ImportError, AttributeError):
                    dialog = None
            if dialog is None:
                return None
            if not any(cls.__name__ in ('ChannelSelectionRadio', 'ChannelSelection')
                       for cls in type(dialog).__mro__):
                return None
            root = dialog.getRoot()
            path = root.getPath() if root is not None else ''
            code = country_bouquets.selected_from_native_path(path)
            if code is not None:
                # Explicit native folder choice is durable across a later GUI
                # restart and OSD-language changes. Entering the bouquet is
                # the user's decision; only that country is activated.
                country_bouquets.remember_selection(DIRECTORY, code)
                if code != self.observed_native_country:
                    self.observed_native_country = code
                    from . import warderRadioCountry as country
                    if country.active_country(DIRECTORY) != code:
                        country.request_country(code, DIRECTORY)
                        self.request_refresh()
            else:
                # Leaving the service list MUST NOT erase the preferred
                # country: the user chose it once and expects it at boot.
                self.observed_native_country = None
            return code
        except (AttributeError, OSError, ValueError, TypeError):
            return None

    def check_icon(self):
        self.icon_timer = None
        if self.closed:
            return
        try:
            if self.icon_worker is None:
                # In the pre-generated mode logos arrive in ONE country ZIP,
                # not as thousands of individual Radio Browser requests.
                root = _radio_world_root()
                chosen_bouquet = self._observe_country_bouquet()
                cached = None
                country_code = None
                if root is not None:
                    from . import warderRadioWorld as world
                    from . import warderRadioCountry as country
                    country_code = chosen_bouquet
                    cached = world.cached_country(root, country_code) if country_code else None
                if cached:
                    self.local_world_sha = cached
                    if not _radio_custom_picons_enabled():
                        key = (country_code, cached)
                        last = self.last_bulk_logo
                        if last is None or last[0] != key or (
                                time.monotonic() - last[1] >= 3600):
                            self.last_bulk_logo = (key, time.monotonic())
                            self.icon_worker = self._spawn(
                                'logo_zip',
                                ['--logos-world', country_code, str(root)],
                                self.icon_done)
                    # In cached-country mode do NOT start old per-station
                    # downloads into the shared TV/SAT picon folder.
                else:
                    self.local_world_sha = None
                    if chosen_bouquet and root is not None:
                        if not _radio_custom_picons_enabled():
                            key = (country_code, 'online-verified-source')
                            last = self.last_bulk_logo
                            if last is None or last[0] != key or (
                                    time.monotonic() - last[1] >= 60):
                                self.last_bulk_logo = (key, time.monotonic())
                                self.icon_worker = self._spawn(
                                    'logo_zip',
                                    ['--logos-online', country_code, str(root)],
                                    self.icon_done)
                    else:
                        # Legacy single-country fallback remains available.
                        self._load_icon_map()
                        from NavigationInstance import instance
                        ref = instance.getCurrentlyPlayingServiceReference() if instance else None
                        fields = ref.toString().split(':') if ref else []
                        stem = '_'.join(field.upper() for field in fields[:10])
                        candidate = None
                        if (len(fields) >= 11 and stem in self.known_icons and
                                stem != self.last_icon):
                            candidate = stem
                        elif self.icon_queue:
                            candidate = self.icon_queue.pop(0)
                        if candidate:
                            destination = _skin_picon_directory()
                            if destination:
                                self.icon_worker = self._spawn(
                                    'icon', ['--icon', candidate, destination], self.icon_done)
                                self.icon_requested[candidate] = time.monotonic()
                                self.last_icon = candidate
        except Exception:
            pass
        self.icon_timer = self.loop.callLater(12, self.check_icon)

    def icon_done(self, result):
        self.icon_worker = None
        if isinstance(result, dict) and result.get('incomplete'):
            # Continue the next bounded country batch without a 1-hour stall.
            self.last_bulk_logo = None
        if isinstance(result, dict) and result.get('skipped') == 'country-catalogue-not-ready':
            self.last_bulk_logo = None
        # Native Enigma2 caches visible ServiceList rows. Redraw only the
        # currently open channel list after a verified new/updated radio picon;
        # never reload all bouquets or stop the playing station.
        if isinstance(result, dict) and result.get('changed') is True:
            try:
                from Screens.InfoBar import InfoBar
                infobar = InfoBar.instance
                screen = infobar.servicelist if infobar is not None else None
                component = screen.servicelist if screen is not None and getattr(
                    screen, 'shown', False) else None
                listing = component.l if component is not None else None
                if listing is not None:
                    listing.refresh()
            except (ImportError, AttributeError, RuntimeError):
                pass

    def close(self):
        self.closed = True
        for call in (self.pending, self.icon_timer, self.timeout,
                     self.radio_refresh_timer, getattr(self, 'world_timer', None),
                     getattr(self, 'world_timeout', None)):
            if call is not None and call.active():
                call.cancel()
        for worker in (self.worker, self.icon_worker,
                       getattr(self, 'world_worker', None)):
            if worker is not None:
                try:
                    worker.transport.kill()
                except Exception:
                    pass



def _safe_status(data, directory=None):
    """Publish sanitized status only; never persist stream addresses or secrets."""
    try:
        target = Path(DIRECTORY if directory is None else directory) / DIAG_FILE
        _write(target, _json_bytes(data))
    except OSError:
        pass


def _radio_picon_diagnostics(directory):
    """Read only known config keys and counts; never expose sensitive settings."""
    config_keys = (
        'config.skin.primary_skin',
        'config.channelSelection.showPicon',
        'config.usage.service_icon_enable',
        'config.plugins.setupGlass17.par125',
        'config.plugins.setupGlass17.par124',
    )
    settings = {}
    source = directory / 'settings'
    try:
        if source.is_file() and not source.is_symlink() and source.stat().st_size <= 1024 * 1024:
            with source.open('r', encoding='utf-8', errors='replace') as handle:
                for line in handle:
                    key, separator, value = line.partition('=')
                    if separator and key in config_keys:
                        settings[key] = value.strip()
    except OSError:
        pass
    current = settings.get('config.plugins.setupGlass17.par125', '/media/usb')
    mount = (settings.get('config.plugins.setupGlass17.par124', '')
             if current == '0' else current)
    base = Path(mount) / 'hdg17_files' if mount.startswith('/') else None
    folder = base / 'picon' if base is not None else None
    count = None
    if folder is not None and folder.is_dir() and not folder.is_symlink():
        try:
            with os.scandir(str(folder)) as scans:
                count = sum(1 for entry in scans if entry.name.lower().endswith('.png')
                            and entry.is_file(follow_symlinks=False))
        except OSError:
            pass
    mapping = _read_json(directory / DATA_FILE, {}, 24 * 1024 * 1024)
    rows = mapping.get('stations', []) if isinstance(mapping, dict) else []
    if not isinstance(rows, list):
        rows = []
    owned = _read_json(directory / ICON_STATE, {})
    tracked = owned.get('files', {}) if isinstance(owned, dict) else {}
    if not isinstance(tracked, dict):
        tracked = {}
    return {
        'online_station_mappings': len(rows),
        'cached_generated_files': len(tracked),
        'picon_folder_png_count': count,
        'picon_folder_exists': folder is not None and folder.is_dir(),
        'skin_active': settings.get('config.skin.primary_skin', '') == 'hd_glass17/skin.xml',
        'native_picon_enabled_legacy': settings.get('config.usage.service_icon_enable'),
        'native_picon_enabled_new': settings.get('config.channelSelection.showPicon'),
    }


def diagnose(directory=DIRECTORY):
    """Read-only receiver diagnostic; no network requests or GUI imports."""
    directory = Path(directory)
    target = directory / FILE
    index = directory / 'bouquets.radio'
    source = Path(__file__).resolve().parent.parent / 'WarderRadio' / 'radio_browser.py'
    state = _read_json(directory / STATE_FILE, {})
    latest = _read_json(directory / DIAG_FILE, {})
    if not isinstance(state, dict):
        state = {}
    if not isinstance(latest, dict):
        latest = {}
    registered = False
    if index.is_file() and not index.is_symlink():
        with index.open('rb') as handle:
            registered = INDEX_LINE.strip() in handle.read(512 * 1024)
    data = {
        'version': 'radio-live-test127',
        'radio_plugin_source_exists': source.is_file(),
        'bouquet_exists': target.is_file() and not target.is_symlink(),
        'registered_in_bouquets_radio': registered,
        'last_attempt': state.get('attempt'),
        'last_success': state.get('success'),
        'last_status': latest,
        'picon_diagnostics': _radio_picon_diagnostics(directory),
    }
    if source.is_file():
        try:
            _plugin()
            data['radio_plugin_import'] = 'ok'
        except ImportError as exc:
            data['radio_plugin_import'] = 'failed'
            data['module'] = getattr(exc, 'name', None) or 'unknown'
        except (OSError, ValueError):
            data['radio_plugin_import'] = 'failed'
            data['module'] = 'unknown'
    else:
        data['radio_plugin_import'] = 'missing'
    return data


def refresh_with_status():
    """Used by the silent installer / controller; record errors for diagnosis."""
    try:
        result = refresh()
    except Exception as exc:
        reason = type(exc).__name__
        message = str(exc)
        if isinstance(exc, ImportError):
            reason = 'radio-plugin-import'
        elif 'Radio Browser' in message:
            reason = 'radio-browser-unavailable'
        elif 'Empty core country' in message:
            reason = 'empty-required-country'
        elif 'Concurrent bouquet edit' in message:
            reason = 'concurrent-edit'
        elif 'Unsafe' in message:
            reason = 'unsafe-path'
        _safe_status({'result': 'failed', 'reason': reason,
                      'timestamp': int(time.time())})
        raise
    _safe_status({'result': 'ready' if (Path(DIRECTORY) / FILE).is_file() else 'not-ready',
                  'changed': bool(result.get('changed')),
                  'skipped': result.get('skipped'),
                  'stations': result.get('stations'),
                  'timestamp': int(time.time())})
    return result


def start(reason=0, session=None):
    global _controller
    if reason == 0 and _controller is None:
        _controller = Controller(session=session)
    elif reason == 0 and session is not None:
        _controller.session = session
    elif reason != 0 and _controller is not None:
        _controller.close()
        _controller = None


if __name__ == '__main__':
    try:
        signal.alarm(90)
        os.nice(10)
        if sys.argv[1:] == ['--bootstrap']:
            result = bootstrap()
        elif sys.argv[1:] == ['--refresh']:
            # The worker may start without an installer (e.g. after a GUI
            # restart); keep index promotion idempotent in both paths.
            bootstrap()
            result = refresh_with_status()
        elif sys.argv[1:] == ['--diagnose']:
            print(json.dumps(diagnose(), ensure_ascii=False))
            sys.exit(0)
        elif len(sys.argv) == 4 and sys.argv[1] == '--icon':
            destination = Path(sys.argv[3])
            # Prevent forged CLI paths from writing to receiver flash.
            parent = destination.parent
            root_device = os.stat('/').st_dev
            if (destination.name != 'picon' or parent.is_symlink() or
                    not parent.is_dir() or os.stat(str(parent)).st_dev == root_device or
                    destination.is_symlink() or
                    (destination.exists() and not destination.is_dir())):
                sys.exit(3)
            if not destination.exists():
                destination.mkdir(mode=0o755)
            if (destination.is_symlink() or not destination.is_dir() or
                    os.stat(str(destination)).st_dev == root_device):
                sys.exit(3)
            result = get_icon(sys.argv[2], destination=destination)
        else:
            sys.exit(2)
        print(json.dumps(result))
    except Exception:
        sys.exit(1)
