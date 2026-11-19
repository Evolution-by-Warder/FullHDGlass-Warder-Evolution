"""Warder Radio Live: one persistent active country, chosen from Radio Browser.

This module never changes personal bouquets, image-owned ChannelSelection.py,
or standalone Radio plugin settings. Network work runs only in subprocesses.
"""
import fcntl
import hashlib
import json
import os
from pathlib import Path
from urllib.parse import unquote_to_bytes
import re
import signal
import sys
import time

# Standalone IPK postinst launches this file by absolute path, so make the
# receiver's Enigma2 plugin root importable without importing the skin plugin.
_ENIGMA_ROOT = str(Path(__file__).resolve().parents[3])
if _ENIGMA_ROOT not in sys.path:
    sys.path.insert(0, _ENIGMA_ROOT)
from Plugins.Extensions.setupGlass17 import warderRadioLive as live

DIRECTORY = Path('/etc/enigma2')
CHOICE_FILE = 'warder-radio-live-country.json'
PAGE_FILE = 'warder-radio-live-country-pending.json'
COUNTRY_RE = re.compile(r'^[A-Z]{2}$')
MAX_PAGES_PER_JOB = 5
MAX_STATIONS = 4000
DAY = 86400
RETRY = 15 * 60
STEP = 2
MAP_LIMIT = 24 * 1024 * 1024
VERSION = 1

LANGUAGE_COUNTRY = {
    'sk': 'SK', 'cs': 'CZ', 'cz': 'CZ',
    'de': 'DE', 'en': 'GB', 'fr': 'FR', 'it': 'IT',
    'pl': 'PL', 'hu': 'HU', 'es': 'ES', 'pt': 'PT',
    'nl': 'NL', 'ro': 'RO', 'ru': 'RU', 'uk': 'UA',
    'tr': 'TR', 'el': 'GR', 'gr': 'GR', 'et': 'EE',
    'lt': 'LT', 'lv': 'LV', 'fi': 'FI', 'sv': 'SE',
    'da': 'DK', 'no': 'NO', 'sq': 'AL', 'al': 'AL',
    'fa': 'IR', 'ar': 'AE', 'zh': 'CN', 'ja': 'JP',
    'ko': 'KR', 'hr': 'HR', 'sl': 'SI', 'bg': 'BG',
    'sr': 'RS', 'he': 'IL', 'id': 'ID', 'th': 'TH',
}


def initial_country(settings=DIRECTORY / 'settings'):
    """Read the user's Enigma2 OSD language, not the box's network location."""
    try:
        p = Path(settings)
        if p.is_symlink() or not p.is_file() or p.stat().st_size > 1024 * 1024:
            return 'SK'
        with p.open('r', encoding='utf-8', errors='replace') as handle:
            for line in handle:
                if line.startswith('config.osd.language='):
                    locale = line.partition('=')[2].strip().lower().replace('-', '_')
                    language = locale.split('_', 1)[0]
                    return LANGUAGE_COUNTRY.get(language, 'SK')
    except OSError:
        pass
    return 'SK'


def _choice(directory):
    p = Path(directory) / CHOICE_FILE
    obj = live._read_json(p, {})
    return obj if isinstance(obj, dict) else {}


def active_country(directory=DIRECTORY):
    obj = _choice(directory)
    candidate = obj.get('active')
    return candidate if isinstance(candidate, str) and COUNTRY_RE.fullmatch(candidate) else initial_country(Path(directory) / 'settings')


def _pending_country(obj):
    candidate = obj.get('pending')
    return candidate if isinstance(candidate, str) and COUNTRY_RE.fullmatch(candidate) else None


def country_name(code):
    try:
        from Plugins.Extensions.WarderRadio.radio_browser import country_name as name
        value = name(code)
        return value if isinstance(value, str) and value else code
    except (ImportError, ValueError, TypeError, OSError):
        return {'SK': 'Slovensko', 'CZ': 'Čechy', 'GB': 'United Kingdom',
                'DE': 'Germany', 'FR': 'France'}.get(code, code)


def _candidate_names(code):
    # Legacy bouquet labels vary by source; never guess which country a
    # complete country section belongs to based on a substring.
    aliases = {
        'SK': ('Slovensko', 'Slovakia'), 'CZ': ('Čechy', 'Česko', 'Czechia'),
        'DE': ('Deutschland', 'Germany', 'Nemecko'),
        'AT': ('Österreich', 'Austria', 'Rakúsko'),
        'GB': ('United Kingdom', 'Great Britain', 'Veľká Británia'),
        'FR': ('France', 'Francúzsko'),
    }
    return tuple(dict.fromkeys((code, country_name(code), *aliases.get(code, ()))))


def _section_for(raw, code):
    sections = live._sections(raw)
    for name in _candidate_names(code):
        if name in sections:
            return sections[name]
    return None


def _single(code, section):
    if section is None:
        name = country_name(code)
        section = (
            '#SERVICE 1:64:2:0:0:0:0:0:0:0:\n'
            '#DESCRIPTION ' + name[:100] + '\n'
        ).encode('utf-8')
    return live.HEADER + live._sorted_country_section(section)


def _normalized_receiver_bouquet(raw):
    """Normalize *only* transport formatting Enigma2 may rewrite on save.

    Accept BOM, CRLF and header trailing whitespace, but not arbitrary
    content edits. All service rows are still compared byte-for-byte against
    the trusted mapping and its stored checksum before any recovery write.
    """
    if not isinstance(raw, bytes) or not raw or len(raw) > 12 * 1024 * 1024:
        return None
    clean = raw.replace(b'\r\n', b'\n')
    if b'\r' in clean or b'\x00' in clean:
        return None
    if not clean.endswith(b'\n'):
        clean += b'\n'
    parts = clean.split(b'\n')
    header = parts[0]
    if header.startswith(b'\xef\xbb\xbf'):
        header = header[3:]
    if header.rstrip(b' \t') != live.HEADER[:-1]:
        return None
    parts[0] = live.HEADER[:-1]
    return b'\n'.join(parts)


def _owner_valid(directory, original, state):
    if original is None:
        return True
    normalized = _normalized_receiver_bouquet(original)
    if normalized is None:
        return False
    checksum = hashlib.sha256(normalized).hexdigest()
    current = state.get('sha256')
    old = live._read_json(Path(directory) / live.STATE_FILE, {})
    old_sha = old.get('bouquet_sha256') if isinstance(old, dict) else None
    return checksum in (current, old_sha)


def _reference_key(raw):
    """Normalize the numeric Enigma2 identity (not its changing URL/name)."""
    try:
        source = raw.removeprefix(b'#SERVICE ').strip().split(b':', 10)
        if len(source) != 11 or not source[0].isdigit() or not source[1].isdigit():
            return None
        fields = (int(source[0]), int(source[1]),
                  *(int(value, 16) for value in source[2:10]))
        return fields, source[10]
    except (ValueError, TypeError, OverflowError):
        return None


def _trusted_service_matches(service_line, item):
    """Compare a saved Enigma2 reference to the authoritative exact map row.

    Enigma2's toString() uses lowercase percent escapes and can append the
    #DESCRIPTION name to #SERVICE. Neither means the stream URL changed.
    Require the full numeric service ID, decoded URL and any appended name to
    match the existing trusted catalogue; don't trust a bare UUID/name match.
    """
    parsed = _reference_key(service_line)
    if parsed is None:
        return False
    fields, tail = parsed
    try:
        stem = item['stem'].split('_')
        intended = (int(stem[0]), int(stem[1]),
                    *(int(value, 16) for value in stem[2:10]))
        if fields != intended:
            return False
        path, separator, label = tail.partition(b':')
        if unquote_to_bytes(path) != item['url'].encode('utf-8'):
            return False
        if separator and unquote_to_bytes(label) != item['name'].encode('utf-8'):
            return False
        return True
    except (KeyError, ValueError, AttributeError, UnicodeError, TypeError):
        return False


def _alt_group_filename(line):
    """No arbitrary filesystem paths, only Enigma2's own alternative group."""
    record = line.removeprefix(b'#SERVICE ').strip()
    matched = re.fullmatch(
        rb'1:134:2:0:0:0:0:0:0:0:FROM BOUQUET '
        rb'"(alternatives\.[a-z0-9_][a-z0-9_.-]{0,178}\.radio)" '
        rb'ORDER BY bouquet', record)
    if not matched:
        return None
    name = matched.group(1).decode('ascii')
    if '..' in name:
        return None
    return name


def _alt_contains_missing(directory, filename, item):
    """The missing published station must belong to this exact alt bouquet."""
    alt = Path(directory) / filename
    try:
        if alt.is_symlink() or not alt.is_file() or alt.stat().st_size > 128 * 1024:
            return False
        content = alt.read_bytes().replace(b'\r\n', b'\n')
    except OSError:
        return False
    if not content.startswith(b'#NAME '):
        return False
    for line in content.splitlines():
        if line.startswith(b'#SERVICE ') and _trusted_service_matches(line, item):
            return True
    return False


def _recover_enigma_alternative(directory, original, state, inspect_only=False):
    """Recover exactly one native Alternative Edit, with full trust checks.

    The original receiver file is backed up unchanged. Never adopt an unknown
    playlist, renamed station, changed URL or unverified alternative group.
    """
    directory = Path(directory)
    normalized = _normalized_receiver_bouquet(original)
    if (normalized is None or
            not isinstance(state.get('sha256'), str) or
            not re.fullmatch(r'[0-9a-f]{64}', state['sha256'])):
        return False
    country = state.get('active')
    if not isinstance(country, str) or not COUNTRY_RE.fullmatch(country):
        return False
    mapping = live._read_json(directory / live.DATA_FILE, {}, MAP_LIMIT)
    rows = mapping.get('stations') if isinstance(mapping, dict) else None
    if not isinstance(rows, list) or len(rows) < 2 or len(rows) > MAX_STATIONS:
        return False
    if any(not isinstance(row, dict) or row.get('countrycode') != country for row in rows):
        return False
    # Require the catalogue itself to match the previously published checksum.
    try:
        original_catalogue = live._bouquet([(country_name(country), rows)])
        original_catalogue = live.HEADER + live._sorted_country_section(
            original_catalogue[len(live.HEADER):])
    except (ValueError, KeyError, AttributeError, TypeError):
        return False
    if hashlib.sha256(original_catalogue).hexdigest() != state['sha256']:
        return False

    data = normalized.splitlines(keepends=True)
    if (len(data) < 6 or data[0] != live.HEADER or
            data[1] != b'#SERVICE 1:64:2:0:0:0:0:0:0:0:\n' or
            data[2] != ('#DESCRIPTION ' + country_name(country) + '\n').encode('utf-8')):
        return False
    # Map stable numeric identities once, keeping verification linear even
    # for countries with several thousand stations.
    indexed = {}
    for position, row in enumerate(rows):
        stem_ref = b'#SERVICE ' + row['stem'].replace('_', ':').encode('ascii') + b':'
        parsed_stem = _reference_key(stem_ref)
        if parsed_stem is None or parsed_stem[0] in indexed:
            return False
        indexed[parsed_stem[0]] = (position, row)
    found = set()
    alternative = None
    index = 3
    while index < len(data):
        service = data[index]
        if not service.startswith(b'#SERVICE '):
            return False
        has_description = (index + 1 < len(data) and
                           data[index + 1].startswith(b'#DESCRIPTION '))
        description = data[index + 1] if has_description else None
        index += 2 if has_description else 1
        filename = _alt_group_filename(service)
        if filename is not None:
            if alternative is not None:
                return False
            alternative = (filename, description)
            continue
        if description is None:
            return False
        parsed = _reference_key(service)
        match = indexed.get(parsed[0]) if parsed is not None else None
        if match is None:
            return False
        position, row = match
        if (position in found or not _trusted_service_matches(service, row) or
                description != ('#DESCRIPTION ' + row['name'] + '\n').encode('utf-8')):
            return False
        found.add(position)

    absent = set(range(len(rows))) - found
    if alternative is None or len(absent) != 1 or len(found) != len(rows) - 1:
        return False
    filename, description = alternative
    missing = rows[next(iter(absent))]
    if (description is not None and
            description != ('#DESCRIPTION ' + missing['name'] + '\n').encode('utf-8')):
        return False
    if not _alt_contains_missing(directory, filename, missing):
        return False

    target = directory / live.FILE
    if target.is_symlink() or not target.is_file() or target.read_bytes() != original:
        return False
    backup = directory / (live.FILE + '.enigma-alternatives.bak')
    if not live._safe_file(backup) or backup.exists():
        return False
    if inspect_only:
        return True
    live._write(backup, original)
    live._write(target, original_catalogue)
    state['sha256'] = hashlib.sha256(original_catalogue).hexdigest()
    state['recovered_alternative_edit'] = True
    _save_choice(directory, state)
    return True


def _pending_country_switch_backup_allowed(directory, original, state):
    """A user-selected NEW country may replace this owned live bouquet.

    This is not a generic checksum bypass. Require a distinct explicit pending
    country, a source map signed by the previous active-country SHA256, and the
    exact set of original service identities (optionally with ONE native
    alternative) in the current radio file. Native Enigma2 may re-encode
    stream URL strings, descriptions or CRLF on save, so don't require raw-byte
    equality. Always back up the untouched receiver file before replacement.
    """
    directory = Path(directory)
    active, pending = state.get('active'), _pending_country(state)
    if (not isinstance(active, str) or not COUNTRY_RE.fullmatch(active) or
            pending is None or pending == active or
            not isinstance(state.get('sha256'), str) or
            not re.fullmatch(r'[0-9a-f]{64}', state['sha256'])):
        return False
    raw = _normalized_receiver_bouquet(original)
    if raw is None:
        return False
    rows_obj = live._read_json(directory / live.DATA_FILE, {}, MAP_LIMIT)
    rows = rows_obj.get('stations') if isinstance(rows_obj, dict) else None
    if (not isinstance(rows, list) or not rows or len(rows) > MAX_STATIONS or
            any(not isinstance(row, dict) or row.get('countrycode') != active
                for row in rows)):
        return False
    try:
        catalogue = live._bouquet([(country_name(active), rows)])
        catalogue = live.HEADER + live._sorted_country_section(
            catalogue[len(live.HEADER):])
        if hashlib.sha256(catalogue).hexdigest() != state['sha256']:
            return False
        permitted = set()
        for row in rows:
            key = _reference_key(
                b'#SERVICE ' + row['stem'].replace('_', ':').encode('ascii') + b':')
            if key is None or key[0] in permitted:
                return False
            permitted.add(key[0])
    except (ValueError, KeyError, TypeError, AttributeError, UnicodeError):
        return False

    lines = raw.splitlines(keepends=True)
    if (len(lines) < 5 or lines[0] != live.HEADER or
            lines[1] != b'#SERVICE 1:64:2:0:0:0:0:0:0:0:\n' or
            lines[2] != ('#DESCRIPTION ' + country_name(active) + '\n').encode('utf-8')):
        return False
    seen, alternative_count = set(), 0
    index = 3
    while index < len(lines):
        line = lines[index]
        if not line.startswith(b'#SERVICE '):
            return False
        if _alt_group_filename(line) is not None:
            alternative_count += 1
            if alternative_count > 1:
                return False
        else:
            key = _reference_key(line)
            if (key is None or key[0] not in permitted or
                    key[0] in seen or key[0][0] != 4097):
                return False
            seen.add(key[0])
        index += 1
        if index < len(lines) and lines[index].startswith(b'#DESCRIPTION '):
            index += 1
    if len(seen) + alternative_count != len(rows):
        return False
    # A previous safeguard may already have created a backup. Do not ever
    # overwrite it; the user can inspect/delete it deliberately if necessary.
    backup = directory / (live.FILE + '.before-country-switch.bak')
    return live._safe_file(backup) and not backup.exists()


def _save_choice(directory, data):
    live._write(Path(directory) / CHOICE_FILE, live._json_bytes(data))


def _lock(directory):
    return live._lock(Path(directory) / (CHOICE_FILE + '.lock'))


def bootstrap(directory=DIRECTORY):
    """Convert an existing world list to the language-selected single country.

    No network calls. An already saved user country is never reset from OSD
    language, including when OSD language changes after installation.
    """
    directory = Path(directory)
    path = directory / live.FILE
    preference = directory / CHOICE_FILE
    index = directory / 'bouquets.radio'
    if not all(live._safe_file(p) for p in (path, preference, index)):
        return {'changed': False, 'skipped': 'unsafe-path'}
    with _lock(directory) as handle:
        try:
            fcntl.flock(handle, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            return {'changed': False, 'skipped': 'busy'}
        state = _choice(directory)
        country = active_country(directory)
        original = path.read_bytes() if path.exists() else None
        if not _owner_valid(directory, original, state):
            return {'changed': False, 'skipped': 'owner-modified'}
        legacy = live._managed_legacy(directory)
        section = _section_for(original, country)
        if section is None:
            section = _section_for(legacy, country)
        # Retain a previously validated, single-country active list even when
        # its source country's heading has since been renamed.
        if section is None and original is not None and state.get('active') == country:
            blocks = live._sections(original)
            if len(blocks) == 1:
                section = next(iter(blocks.values()))
        raw = _single(country, section)
        if len(raw) > 12 * 1024 * 1024:
            raise ValueError('Active-country bouquet exceeds safe limit')
        changed = original != raw
        if changed:
            live._write(path, raw)
        state.update({'schema': VERSION, 'active': country,
                      'sha256': hashlib.sha256(raw).hexdigest()})
        _save_choice(directory, state)
        registered = live._register(directory)
        return {'changed': changed or registered, 'country': country,
                'pending': _pending_country(state)}


def request_country(country, directory=DIRECTORY):
    """Queue a country switch without changing the currently playable list."""
    if not isinstance(country, str) or not COUNTRY_RE.fullmatch(country):
        return {'accepted': False, 'reason': 'invalid-country'}
    directory = Path(directory)
    if not live._safe_file(directory / CHOICE_FILE):
        return {'accepted': False, 'reason': 'unsafe-path'}
    with _lock(directory) as handle:
        try:
            fcntl.flock(handle, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            return {'accepted': False, 'reason': 'busy'}
        state = _choice(directory)
        if country == state.get('active') and not state.get('pending'):
            return {'accepted': True, 'already_active': True}
        state.update({'schema': VERSION, 'pending': country,
                      'pending_started': int(time.time()), 'last_attempt': 0,
                      'last_error': None, 'downloaded': 0})
        _save_choice(directory, state)
        page = directory / PAGE_FILE
        if live._safe_file(page):
            live._write(page, b'{}')
        return {'accepted': True, 'already_active': False}


def _station_rows(browser, country, offset, saved):
    seen = {row.get('stationuuid') for row in saved if isinstance(row, dict)}
    rows = list(saved)
    more = False
    for _ in range(MAX_PAGES_PER_JOB):
        page = browser.page(country=country, offset=offset)
        if page.offline:
            raise OSError('Radio Browser country unavailable')
        for item in page.rows:
            try:
                entry = live._entry(item)
            except (TypeError, AttributeError, ValueError):
                continue
            if entry['stationuuid'] in seen:
                continue
            seen.add(entry['stationuuid'])
            entry['countrycode'] = country
            rows.append(entry)
        more = bool(page.more)
        offset += 60
        if not more or len(rows) >= MAX_STATIONS:
            break
    return rows, offset, more


def refresh(directory=DIRECTORY, now=None, browser=None):
    """Fetch only the selected country and commit a switch when fully valid."""
    directory = Path(directory)
    now = time.time() if now is None else now
    if now < 1700000000:
        return {'changed': False, 'skipped': 'clock'}
    target = directory / live.FILE
    state_path = directory / CHOICE_FILE
    staging = directory / PAGE_FILE
    mapping = directory / live.DATA_FILE
    if not all(live._safe_file(p) for p in (target, state_path, staging, mapping)):
        return {'changed': False, 'skipped': 'unsafe-path'}
    before = target.read_bytes() if target.exists() else None
    with _lock(directory) as lock:
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            return {'changed': False, 'skipped': 'busy'}
        state = _choice(directory)
        # The GUI or setup may have changed the active country while a worker
        # was still running; the worker reads the choice under this lock.
        pending_backup_required = False
        if not _owner_valid(directory, before, state):
            # The exact native Alternative Edit can still take the original
            # strict recovery path and keep its existing recovery-backup name.
            if _recover_enigma_alternative(directory, before, state):
                before = target.read_bytes()
            else:
                # An explicit *different* country selection replaces only this
                # owned bouquet, after exact inventory checks and an untouched
                # backup made once the new country has fully downloaded.
                pending_backup_required = _pending_country_switch_backup_allowed(
                    directory, before, state)
                if not pending_backup_required:
                    return {'changed': False, 'skipped': 'owner-modified'}
        country = _pending_country(state) or active_country(directory)
        if not COUNTRY_RE.fullmatch(country):
            return {'changed': False, 'skipped': 'invalid-country'}
        pending = _pending_country(state)
        since = state.get('last_success', 0)
        attempt = state.get('last_attempt', 0)
        page = live._read_json(staging, {}, 4 * 1024 * 1024)
        continuing = isinstance(page, dict) and page.get('country') == country
        if not pending and not continuing and since and 0 <= now-since < DAY:
            return {'changed': False, 'skipped': 'not-due'}
        if attempt and 0 <= now-attempt < (STEP if continuing else RETRY):
            return {'changed': False, 'skipped': 'not-due',
                    'incomplete': bool(continuing)}
        state['last_attempt'] = now
        _save_choice(directory, state)
        if browser is None:
            RadioBrowser, _ = live._plugin()
            browser = RadioBrowser('/etc/enigma2/warder-radio')
        rows = page.get('rows', []) if continuing else []
        offset = page.get('offset', 0) if continuing else 0
        if (not isinstance(rows, list) or not isinstance(offset, int) or
                offset < 0 or offset > MAX_STATIONS or len(rows) > MAX_STATIONS):
            rows, offset = [], 0
        try:
            collected, offset, more = _station_rows(browser, country, offset, rows)
        except (OSError, ValueError):
            state['last_error'] = 'radio-browser-unavailable'
            _save_choice(directory, state)
            return {'changed': False, 'skipped': 'radio-browser-unavailable'}
        if more:
            if len(collected) >= MAX_STATIONS:
                state['last_error'] = 'too-many-stations'
                _save_choice(directory, state)
                return {'changed': False, 'skipped': 'too-many-stations'}
            staging_data = {'country': country, 'rows': collected, 'offset': offset}
            encoded = live._json_bytes(staging_data)
            if len(encoded) > 4 * 1024 * 1024:
                state['last_error'] = 'country-too-large'
                _save_choice(directory, state)
                return {'changed': False, 'skipped': 'country-too-large'}
            live._write(staging, encoded)
            state['downloaded'] = len(collected)
            state['last_error'] = None
            _save_choice(directory, state)
            return {'changed': False, 'incomplete': True, 'country': country,
                    'downloaded': len(collected)}
        if not collected:
            state['last_error'] = 'empty-country'
            _save_choice(directory, state)
            return {'changed': False, 'skipped': 'empty-country'}
        collected.sort(key=lambda row: live._station_sort_key(row['name']))
        raw = live._bouquet([(country_name(country), collected)])
        if len(raw) > 12 * 1024 * 1024:
            raise ValueError('Active country too large')
        payload = live._json_bytes({'schema': VERSION, 'stations': collected})
        if len(payload) > MAP_LIMIT:
            raise ValueError('Country icon mapping too large')
        if target.exists() and target.read_bytes() != before:
            raise OSError('Concurrent managed bouquet edit')
        if pending_backup_required:
            backup = directory / (live.FILE + '.before-country-switch.bak')
            if not live._safe_file(backup) or backup.exists():
                return {'changed': False, 'skipped': 'backup-exists'}
            # Save the exact byte representation, including Enigma2's custom
            # formatting and alternative list, before installing new stations.
            live._write(backup, before)
        if not mapping.exists() or mapping.read_bytes() != payload:
            live._write(mapping, payload)
        changed = raw != before
        if changed:
            live._write(target, raw)
        state.update({'active': country, 'sha256': hashlib.sha256(raw).hexdigest(),
                      'last_success': now, 'last_attempt': now,
                      'last_error': None, 'downloaded': len(collected)})
        state.pop('pending', None)
        state.pop('pending_started', None)
        _save_choice(directory, state)
        live._write(staging, b'{}')
        registered = live._register(directory)
        # Remove old owned world data only after a new, complete online
        # selected country was installed. Unrelated bouquets stay untouched.
        legacy = live._managed_legacy(directory)
        index = directory / 'bouquets.radio'
        if legacy is not None and index.is_file() and not index.is_symlink():
            index_bytes = index.read_bytes()
            if (live.INDEX_LINE.strip() in index_bytes and
                    b'FROM BOUQUET "userbouquet.warder.radio"' not in index_bytes):
                old = directory / live.LEGACY_FILE
                if not old.is_symlink() and old.read_bytes() == legacy:
                    old.unlink()
                    backup = directory / (live.LEGACY_FILE + '.bak')
                    if (backup.is_file() and not backup.is_symlink()
                            and backup.stat().st_size <= 4 * 1024 * 1024):
                        if backup.read_bytes().startswith(live.LEGACY_HEADER):
                            backup.unlink()
        return {'changed': changed or registered or bool(pending),
                'country': country, 'stations': len(collected)}


def _start_selected_country_refresh(session):
    """Guarantee that a saved country selection actually schedules a worker.

    A plugin context menu can remain usable even when the GUI-side controller
    was not initialized at session start. Never silently report success while
    its asynchronous download scheduler is missing.
    """
    controller = live._controller
    if controller is None or getattr(controller, 'closed', False):
        live.start(0, session=session)
        controller = live._controller
    if controller is None or getattr(controller, 'closed', False):
        return False
    controller.request_refresh()
    return True


def diagnose(directory=DIRECTORY):
    """Read-only debug status for receiver tests; never display stream URLs."""
    directory = Path(directory)
    info = _choice(directory)
    staging = live._read_json(directory / PAGE_FILE, {}, 4 * 1024 * 1024)
    stations = live._read_json(directory / live.DATA_FILE, {}, MAP_LIMIT)
    raw_path = directory / live.FILE
    try:
        raw = (raw_path.read_bytes() if raw_path.is_file() and
               not raw_path.is_symlink() and raw_path.stat().st_size <= 12 * 1024 * 1024
               else None)
    except OSError:
        raw = None
    normalized = _normalized_receiver_bouquet(raw)
    sections = live._sections(normalized)
    live_state = live._read_json(directory / live.STATE_FILE, {})
    if not isinstance(live_state, dict):
        live_state = {}
    expected = _choice(directory).get('sha256')
    old_expected = live_state.get('bouquet_sha256')
    actual = hashlib.sha256(raw).hexdigest() if raw is not None else None
    normalized_sha = (hashlib.sha256(normalized).hexdigest()
                      if normalized is not None else None)
    return {
        'bouquet_exists': raw is not None,
        'bouquet_bytes': len(raw) if raw is not None else 0,
        'bouquet_header_valid': bool(normalized),
        'bouquet_format_normalizable': normalized is not None,
        'bouquet_line_endings': 'crlf' if raw and b'\r\n' in raw else 'lf_or_other',
        'bouquet_group_markers': raw.count(b'#SERVICE 1:64:') if raw else 0,
        'bouquet_stream_entries': sum(line.startswith(b'#SERVICE 4097:')
                                      for line in raw.splitlines()) if raw else 0,
        'bouquet_owned_checksum_valid': bool(normalized_sha and
                                              normalized_sha in (expected, old_expected)),
        'enigma_alternative_recovery_possible': bool(
            raw is not None and normalized_sha not in (expected, old_expected) and
            _recover_enigma_alternative(directory, raw, _choice(directory),
                                       inspect_only=True)),
        'pending_country_switch_safe': bool(
            raw is not None and normalized_sha not in (expected, old_expected) and
            _pending_country_switch_backup_allowed(directory, raw, info)),
        'active': active_country(directory),
        'pending': _pending_country(info),
        'downloaded': info.get('downloaded', 0),
        'pending_pages': staging.get('offset', 0) // 60
        if isinstance(staging, dict) and isinstance(staging.get('offset', 0), int)
        else 0,
        'last_attempt': info.get('last_attempt'),
        'last_success': info.get('last_success'),
        'last_error': info.get('last_error'),
        'visible_country_sections': list(sections),
        'mapped_stations': len(stations.get('stations', []))
        if isinstance(stations, dict) and isinstance(stations.get('stations'), list)
        else 0,
    }


def country_options():
    """Local catalog from the installed Radio plugin; no network on GUI thread."""
    source = Path(__file__).resolve().parent.parent / 'WarderRadio' / 'country-names.json'
    names = live._read_json(source, {}, 48 * 1024)
    if not isinstance(names, dict) or not names:
        names = {code: name for code, name in
                 [('SK', 'Slovensko'), ('CZ', 'Čechy'), ('DE', 'Germany'),
                  ('GB', 'United Kingdom'), ('FR', 'France'),
                  ('IT', 'Italy'), ('PL', 'Poland'), ('ES', 'Spain')]}
    return sorted([(name, code) for code, name in names.items()
                   if isinstance(code, str) and COUNTRY_RE.fullmatch(code)
                   and isinstance(name, str) and name],
                  key=lambda row: live._country_sort_key(row[0]))


def is_live_service(service):
    """Only show the MENU entry for stations in our own Warder Live bouquet."""
    try:
        reference = service.toString() if hasattr(service, 'toString') else service
        if not isinstance(reference, str):
            return False
        fields = reference.split(':', 10)
        if len(fields) < 11:
            return False
        # Native list sometimes rewrites 4097 to type 1: compare stable
        # service identity fields, not the IPTV URL.
        identity = ':'.join(fields[1:10]).upper()
        path = DIRECTORY / live.FILE
        if path.is_symlink() or not path.is_file() or path.stat().st_size > 12 * 1024 * 1024:
            return False
        with path.open('rb') as stream:
            for line in stream:
                if not line.startswith(b'#SERVICE '):
                    continue
                parts = line[9:].decode('utf-8', 'replace').split(':', 10)
                if len(parts) >= 11 and ':'.join(parts[1:10]).upper() == identity:
                    return True
    except (OSError, ValueError, UnicodeError):
        pass
    return False


def _is_live_bouquet_selected(csel):
    """Only the highlighted Warder Radio Live folder in radio bouquets."""
    try:
        current = csel.getCurrentSelection()
        root = csel.getRoot()
        if current is None or root is None:
            return False
        current_path = current.getPath()
        root_path = root.getPath()
        return (isinstance(current_path, str) and
                'FROM BOUQUET "' + live.FILE + '"' in current_path and
                isinstance(root_path, str) and
                'FROM BOUQUET "bouquets.radio"' in root_path)
    except (AttributeError, TypeError, ValueError):
        return False


def install_root_country_menu():
    """Optional in-memory root-bouquet context action for OpenATV/OpenPLi.

    Enigma2 exposes plugin context actions for playable services but not for
    folder rows in the radio bouquet root. Extend only the specific native
    menu instance when Warder Radio Live is highlighted. All standard actions
    remain in their original order, untouched for other bouquets.
    """
    try:
        from Screens.ChannelSelection import ChannelContextMenu
        from Components.ChoiceList import ChoiceEntryComponent
        from .warderUiText import ui_text
    except (ImportError, AttributeError):
        return False

    original = ChannelContextMenu.__init__
    if getattr(original, '_warder_live_country_root_menu', False):
        return False

    def context_init(menu, session, csel, *args, **kwargs):
        original(menu, session, csel, *args, **kwargs)
        if not _is_live_bouquet_selected(csel):
            return
        try:
            widget = menu['menu']
            entries = list(widget.getList())
            if any(isinstance(item, (tuple, list)) and item and
                   isinstance(item[0], (tuple, list)) and item[0] and
                   'Warder Radio Live' in str(item[0][0])
                   for item in entries):
                return

            def select_country():
                # Match the native runPlugin flow: open the next screen and
                # then close the context menu, leaving normal radio navigation.
                open_country_selector(session)
                menu.close(False)

            entry = ChoiceEntryComponent(
                text=(ui_text('Select country (Warder Radio Live)'),
                      select_country))
            entries.insert(1 if entries else 0, entry)
            widget.setList(entries)
        except (AttributeError, KeyError, TypeError, IndexError, ValueError):
            # Unsupported image variants keep their stock context menu.
            pass

    context_init._warder_live_country_root_menu = True
    ChannelContextMenu.__init__ = context_init
    return True


def open_country_selector(session, service=None, **kwargs):
    """Native Channel Selection MENU callback; runs no HTTP in the GUI."""
    try:
        from Screens.ChoiceBox import ChoiceBox
        from Screens.MessageBox import MessageBox
        from .warderUiText import ui_text
    except ImportError:
        return
    current = active_country()
    choices = country_options()
    if not choices:
        session.open(MessageBox, ui_text("Country list is unavailable."),
                     type=MessageBox.TYPE_INFO, timeout=5)
        return

    def chosen(answer):
        if not answer:
            return
        code = answer[1]
        result = request_country(code)
        if not result.get('accepted'):
            session.open(MessageBox, ui_text("Country selection could not be saved."),
                         type=MessageBox.TYPE_INFO, timeout=5)
            return
        if result.get('already_active'):
            return
        scheduled = False
        try:
            scheduled = _start_selected_country_refresh(session)
        except (AttributeError, ImportError, OSError, RuntimeError, TypeError):
            scheduled = False
        if not scheduled:
            session.open(MessageBox,
                         ui_text("Country saved, but background radio update did not start."),
                         type=MessageBox.TYPE_INFO, timeout=6)
        else:
            session.open(MessageBox,
                         ui_text("Loading radio stations for the selected country."),
                         type=MessageBox.TYPE_INFO, timeout=4)

    # Keep the active choice first in the user-facing menu.
    ordered = sorted(choices, key=lambda row: row[1] != current)
    session.openWithCallback(chosen, ChoiceBox, title=ui_text("Select country (Warder Radio Live)"),
                             list=[(name + (' ' + ui_text('(current)') if code == current else ''), code)
                                   for name, code in ordered])


if __name__ == '__main__':
    try:
        signal.alarm(90)
        os.nice(10)
        if sys.argv[1:] == ['--bootstrap']:
            result = bootstrap()
        elif sys.argv[1:] == ['--refresh']:
            result = refresh()
        elif sys.argv[1:] == ['--diagnose']:
            result = diagnose()
        else:
            sys.exit(2)
        print(json.dumps(result, ensure_ascii=False))
    except Exception:
        sys.exit(1)
