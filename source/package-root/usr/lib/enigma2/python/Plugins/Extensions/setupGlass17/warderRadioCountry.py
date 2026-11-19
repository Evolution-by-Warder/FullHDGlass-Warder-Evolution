"""Warder Radio Live: one persistent active country, chosen from Radio Browser.

This module never changes personal bouquets, image-owned ChannelSelection.py,
or standalone Radio plugin settings. Network work runs only in subprocesses.
"""
import fcntl
import hashlib
import json
import os
from pathlib import Path
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
MAX_PAGES_PER_JOB = 3
MAX_STATIONS = 4000
DAY = 86400
RETRY = 15 * 60
STEP = 10
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


def _owner_valid(directory, original, state):
    if original is None:
        return True
    if not original.startswith(live.HEADER):
        return False
    checksum = hashlib.sha256(original).hexdigest()
    current = state.get('sha256')
    old = live._read_json(Path(directory) / live.STATE_FILE, {})
    old_sha = old.get('bouquet_sha256') if isinstance(old, dict) else None
    return checksum in (current, old_sha)


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
                      'pending_started': int(time.time()), 'last_attempt': 0})
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
        if not _owner_valid(directory, before, state):
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
            return {'changed': False, 'skipped': 'radio-browser-unavailable'}
        if more:
            if len(collected) >= MAX_STATIONS:
                return {'changed': False, 'skipped': 'too-many-stations'}
            staging_data = {'country': country, 'rows': collected, 'offset': offset}
            encoded = live._json_bytes(staging_data)
            if len(encoded) > 4 * 1024 * 1024:
                return {'changed': False, 'skipped': 'country-too-large'}
            live._write(staging, encoded)
            return {'changed': False, 'incomplete': True, 'country': country,
                    'downloaded': len(collected)}
        if not collected:
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
        if not mapping.exists() or mapping.read_bytes() != payload:
            live._write(mapping, payload)
        changed = raw != before
        if changed:
            live._write(target, raw)
        state.update({'active': country, 'sha256': hashlib.sha256(raw).hexdigest(),
                      'last_success': now, 'last_attempt': now})
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
        try:
            controller = live._controller
            if controller is not None:
                controller.request_refresh()
        except (AttributeError, OSError):
            pass
        session.open(MessageBox, ui_text("Loading radio stations for the selected country."),
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
            result = {'active': active_country(), 'choice': _choice(DIRECTORY)}
        else:
            sys.exit(2)
        print(json.dumps(result, ensure_ascii=False))
    except Exception:
        sys.exit(1)
