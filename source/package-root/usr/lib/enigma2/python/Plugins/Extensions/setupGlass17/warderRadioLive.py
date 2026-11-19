"""Optional live Radio Browser bouquets and demand-loaded Enigma2 radio picons.

The managed live bouquet is separate from the legacy Warder Radio Streams file.
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
from urllib.parse import quote

DIRECTORY = Path('/etc/enigma2')
FILE = 'userbouquet.warder.live.radio'
HEADER = b'#NAME Warder Radio Live\n'
INDEX_LINE = ('#SERVICE 1:7:2:0:0:0:0:0:0:0:FROM BOUQUET "' + FILE + '" ORDER BY bouquet\n').encode()
DATA_FILE = 'warder-radio-live-stations.json'
STATE_FILE = 'warder-radio-live-state.json'
ICON_STATE = 'warder-radio-live-picons.json'
DAY = 24 * 3600
RETRY = 6 * 3600
MAX_PAGES = 3
MAX_STATIONS = 600
MAX_ICONS = 2 * MAX_STATIONS + 24  # two native Enigma2 filename variants
MIN_FREE = 16 * 1024 * 1024
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
    if not isinstance(uuid, str) or not re.fullmatch(r'[0-9a-f-]{36}', uuid, re.I):
        raise ValueError('Missing Radio Browser UUID')
    digest = hashlib.sha256(uuid.lower().encode('ascii')).hexdigest().upper()
    fields = ('4097', '0', '2', digest[:4], digest[4:8], digest[8:12],
              digest[12:20], '0', '0', '0')
    return '_'.join(fields)


def _entry(row):
    uuid, url, name = row.get('stationuuid'), row.get('url'), row.get('name')
    if not isinstance(url, str) or not url.lower().startswith(('http://', 'https://')):
        raise ValueError('Invalid radio URL')
    if not isinstance(name, str) or not name.strip():
        raise ValueError('Invalid radio name')
    if len(url) > 4096 or any(ord(char) < 32 for char in url):
        raise ValueError('Invalid radio URL')
    name = ' '.join(name.split())[:140]
    if not name:
        raise ValueError('Empty radio name')
    stem = service_stem(uuid)
    return {'stem': stem, 'stationuuid': uuid.lower(), 'name': name,
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


def _register(directory):
    index = directory / 'bouquets.radio'
    if not _safe_file(index):
        raise OSError('Unsafe radio index')
    flags = os.O_RDWR | os.O_CREAT | os.O_APPEND | os.O_NOFOLLOW
    with os.fdopen(os.open(str(index), flags, 0o644), 'a+b') as output:
        output.seek(0)
        before = output.read()
        if re.search(rb'^#SERVICE[^\r\n]*FROM BOUQUET "' +
                     re.escape(FILE.encode()) + rb'"', before, re.MULTILINE):
            return False
        output.write((b'#NAME Bouquets (Radio)\n' if not before else
                      b'' if before.endswith(b'\n') else b'\n') + INDEX_LINE)
        output.flush()
        os.fsync(output.fileno())
    return True


def refresh(directory=DIRECTORY, now=None, browser=None):
    """Publish only after all online pages validate. Keep previous data offline."""
    directory = Path(directory)
    now = time.time() if now is None else now
    if now < 1700000000:
        return {'changed': False, 'skipped': 'clock'}
    target = directory / FILE
    index = directory / 'bouquets.radio'
    data = directory / DATA_FILE
    state_path = directory / STATE_FILE
    if not all(_safe_file(path) for path in (target, index, data, state_path)):
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
        if before is not None:
            expected = state.get('bouquet_sha256', '')
            if (not isinstance(expected, str) or
                    not re.fullmatch(r'[0-9a-f]{64}', expected) or
                    hashlib.sha256(before).hexdigest() != expected):
                return {'changed': False, 'skipped': 'owner-modified'}
        success, attempt = state.get('success', 0), state.get('attempt', 0)
        if before is not None and success and 0 <= now-success < DAY:
            changed = _register(directory)
            return {'changed': changed, 'skipped': 'not-due'}
        if attempt and 0 <= now-attempt < RETRY:
            changed = _register(directory) if before is not None else False
            return {'changed': changed, 'skipped': 'not-due'}
        state['attempt'] = now
        _write(state_path, _json_bytes(state))
        # Radio plugin is optional. It owns the online client and logo validation.
        if browser is None:
            RadioBrowser, _ = _plugin()
            browser = RadioBrowser('/etc/enigma2/warder-radio')
        plugin_dir = directory / 'warder-radio'
        groups, saved, seen = [], [], set()
        for country in _countries(plugin_dir):
            rows = []
            for page in range(MAX_PAGES):
                result = browser.page(country=country, offset=page * 60)
                if result.offline:
                    raise OSError('Radio Browser is offline; keep previous bouquet')
                for station in result.rows:
                    try:
                        item = _entry(station)
                    except (ValueError, AttributeError, TypeError):
                        continue
                    if item['stationuuid'] in seen:
                        continue
                    seen.add(item['stationuuid'])
                    rows.append(item)
                if not result.more or len(seen) >= MAX_STATIONS:
                    break
            if not rows:
                raise ValueError('Empty live country; keep previous bouquet')
            for item in rows:
                item['countrycode'] = country
            groups.append((country, rows))
            saved.extend(rows)
        raw = _bouquet(groups)
        if not saved or len(raw) > 4 * 1024 * 1024:
            raise ValueError('Invalid live radio bouquet')
        if target.exists() and target.read_bytes() != before:
            raise OSError('Concurrent bouquet edit')
        # Keep mapping and bouquet together: an old mapping is always harmless.
        mapping_bytes = _json_bytes({'schema': 1, 'stations': saved})
        if not data.exists() or data.read_bytes() != mapping_bytes:
            _write(data, mapping_bytes)
        changed = raw != before
        if changed:
            if before is not None:
                _write(directory / (FILE + '.bak'), before)
            _write(target, raw)
        registered = _register(directory)
        state['success'] = now
        state['bouquet_sha256'] = hashlib.sha256(raw).hexdigest()
        _write(state_path, _json_bytes(state))
        return {'changed': changed or registered, 'stations': len(saved)}


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
        if not directory.exists():
            directory.mkdir(mode=0o755)
        if not directory.is_dir() or not os.access(str(directory), os.W_OK):
            return None
        if os.statvfs(str(directory)).f_bavail * os.statvfs(str(directory)).f_frsize < MIN_FREE:
            return None
        return str(directory)
    except (AttributeError, ImportError, OSError, TypeError, ValueError):
        return None


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
    if controller is not None:
        controller.enqueue_icon(reference)


class Controller:
    def __init__(self, event_loop=None, reload_bouquets=None):
        from .warderHelpPreview import _NativeLoop
        self.loop = event_loop or _NativeLoop()
        self.reload = reload_bouquets or self._reload
        self.pending = self.loop.callLater(75, self.check)
        self.icon_timer = self.loop.callLater(25, self.check_icon)
        self.worker = None
        self.icon_worker = None
        self.timeout = None
        self.closed = False
        self.last_icon = None
        self.icon_queue = []
        self.known_icons = set()
        self.icon_requested = set()
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
        self.loop.spawnProcess(worker, '/usr/bin/python3', ['/usr/bin/python3', path] + args,
                               env=dict(os.environ))
        return worker

    def check(self):
        self.pending = None
        if self.closed or self.worker is not None:
            return
        try:
            self.worker = self._spawn('refresh', ['--refresh'], self.finished)
            self.timeout = self.loop.callLater(90, self.timed_out)
        except Exception:
            self.finished(None)

    def finished(self, result):
        self.worker = None
        if self.timeout is not None and self.timeout.active():
            self.timeout.cancel()
        self.timeout = None
        if self.closed:
            return
        if isinstance(result, dict) and result.get('changed'):
            try:
                self.reload()
            except Exception:
                pass
        self.pending = self.loop.callLater(3600, self.check)

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
        data = _read_json(mapping, {}) if mtime is not None else {}
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
            if seen[code] <= 12:
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
            if stem in self.icon_requested:
                return
            # Only the visible live-bouquet identities are accepted.
            if stem not in self.known_icons:
                return
            if stem in self.icon_queue:
                self.icon_queue.remove(stem)
            self.icon_queue.insert(0, stem)
            self.icon_queue = self.icon_queue[:48]
            self.icon_requested.add(stem)
            if self.icon_worker is None:
                if self.icon_timer is not None and self.icon_timer.active():
                    self.icon_timer.cancel()
                self.icon_timer = self.loop.callLater(0.3, self.check_icon)
        except (AttributeError, TypeError, ValueError):
            return

    def check_icon(self):
        self.icon_timer = None
        if self.closed:
            return
        try:
            if self.icon_worker is None:
                # Prefetch only a few visible-country stations, never the whole catalogue.
                self._load_icon_map()
                from NavigationInstance import instance
                ref = instance.getCurrentlyPlayingServiceReference() if instance else None
                fields = ref.toString().split(':') if ref else []
                stem = '_'.join(field.upper() for field in fields[:10])
                candidate = None
                if len(fields) >= 11 and stem.startswith('4097_0_2_') and stem != self.last_icon:
                    self.last_icon = stem
                    candidate = stem
                elif self.icon_queue:
                    candidate = self.icon_queue.pop(0)
                if candidate:
                    destination = _skin_picon_directory()
                    if destination:
                        self.icon_worker = self._spawn(
                            'icon', ['--icon', candidate, destination], self.icon_done)
        except Exception:
            pass
        self.icon_timer = self.loop.callLater(12, self.check_icon)

    def icon_done(self, result):
        self.icon_worker = None

    def close(self):
        self.closed = True
        for call in (self.pending, self.icon_timer, self.timeout):
            if call is not None and call.active():
                call.cancel()
        for worker in (self.worker, self.icon_worker):
            if worker is not None:
                try:
                    worker.transport.kill()
                except Exception:
                    pass


def start(reason=0):
    global _controller
    if reason == 0 and _controller is None:
        _controller = Controller()
    elif reason != 0 and _controller is not None:
        _controller.close()
        _controller = None


if __name__ == '__main__':
    try:
        signal.alarm(90)
        os.nice(10)
        if sys.argv[1:] == ['--refresh']:
            result = refresh()
        elif len(sys.argv) == 4 and sys.argv[1] == '--icon':
            destination = Path(sys.argv[3])
            # Prevent forged CLI paths from writing to receiver flash.
            if (not destination.is_dir() or destination.is_symlink() or
                    os.stat(str(destination)).st_dev == os.stat('/').st_dev):
                sys.exit(3)
            result = get_icon(sys.argv[2], destination=destination)
        else:
            sys.exit(2)
        print(json.dumps(result))
    except Exception:
        sys.exit(1)
