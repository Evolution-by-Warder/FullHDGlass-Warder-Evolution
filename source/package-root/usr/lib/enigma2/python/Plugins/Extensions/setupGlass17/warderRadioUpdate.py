"""Silently install and refresh the managed Warder radio bouquet off the GUI."""
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
from urllib.request import Request, urlopen

BASE = 'https://raw.githubusercontent.com/Evolution-by-Warder/PiconHub-Warder-Evolution/'
CATALOG = 'picons/IPTV-SK-CZ/'
REPORT_URL = BASE + 'main/' + CATALOG + 'catalog/world-radio-update.json'
BOUQUET_PATH = CATALOG + 'bouquets/userbouquet.warder.radio'
FILENAME = 'userbouquet.warder.radio'
STATE_NAME = 'warder-radio-update.json'
WEEK = 7 * 24 * 60 * 60
RETRY = 6 * 60 * 60
LIMIT = 4 * 1024 * 1024
HEADER = b'#NAME Warder Radio Streams\n'
INDEX_NAME = 'bouquets.radio'
INDEX_ENTRY = ('#SERVICE 1:7:2:0:0:0:0:0:0:0:FROM BOUQUET "' + FILENAME + '" ORDER BY bouquet\n').encode()
_controller = None


def read_state(directory):
    try:
        value = json.loads((directory / STATE_NAME).read_text())
        return value if isinstance(value, dict) else {}
    except (OSError, ValueError):
        return {}


def due(state, now):
    # A clock correction must not postpone checks indefinitely.
    success = float(state.get('last_success', 0))
    attempt = float(state.get('last_attempt', 0))
    return (not success or now < success or now - success >= WEEK) and (not attempt or now < attempt or now - attempt >= RETRY)


def fetch(url, maximum):
    request = Request(url, headers={'User-Agent': 'FullHDGlass-radio-update/1',
                                    'Cache-Control': 'no-cache'})
    with urlopen(request, timeout=15) as response:
        if response.geturl() != url:
            raise ValueError('Unexpected radio catalogue redirect')
        data = response.read(maximum + 1)
    if not data or len(data) > maximum:
        raise ValueError('Empty or oversized radio download')
    return data


def write_atomic(path, data):
    temp = None
    try:
        with tempfile.NamedTemporaryFile(dir=str(path.parent), delete=False) as handle:
            temp = Path(handle.name)
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        os.chmod(str(temp), 0o644)
        os.replace(str(temp), str(path))
        temp = None
    finally:
        if temp is not None:
            try:temp.unlink()
            except OSError:pass


def install_if_missing(path, data):
    """Publish a complete download without replacing a concurrently created file."""
    temp = None
    try:
        with tempfile.NamedTemporaryFile(dir=str(path.parent), delete=False) as handle:
            temp = Path(handle.name)
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        os.chmod(str(temp), 0o644)
        os.link(str(temp), str(path))
    finally:
        if temp is not None:
            temp.unlink()


def register_radio(directory):
    """Append only our reference; preserve the user's index bytes and ordering."""
    path = directory / INDEX_NAME
    flags = os.O_RDWR | os.O_CREAT | os.O_APPEND | os.O_NOFOLLOW
    with os.fdopen(os.open(str(path), flags, 0o644), 'a+b') as handle:
        handle.seek(0)
        before = handle.read()
        pattern = rb'^#SERVICE[^\r\n]*FROM BOUQUET "' + re.escape(FILENAME.encode()) + rb'"(?:[ \t]|\r?$)'
        if re.search(pattern, before, re.MULTILINE):
            return False
        addition = (b'#NAME Bouquets (Radio)\n' if not before else b'' if before.endswith(b'\n') else b'\n') + INDEX_ENTRY
        handle.write(addition)
        handle.flush()
        os.fsync(handle.fileno())
    return True


def validate(raw, report):
    if hashlib.sha256(raw).hexdigest() != report.get('bouquet_sha256'):
        raise ValueError('Radio bouquet checksum mismatch')
    if not raw.startswith(HEADER):
        raise ValueError('Unexpected radio bouquet header')
    lines = raw.decode('utf-8').splitlines()
    refs = set()
    groups = []
    for i in range(1, len(lines), 2):
        if i + 1 >= len(lines) or not lines[i].startswith('#SERVICE ') or not lines[i+1].startswith('#DESCRIPTION '):
            raise ValueError('Truncated radio bouquet')
        fields = lines[i][9:].split(':', 10)
        if len(fields) != 11 or not all(re.fullmatch('[0-9A-Fa-f]+', f) for f in fields[:10]):
            raise ValueError('Invalid radio service')
        if fields[1] == '64':
            groups.append(lines[i+1][13:])
            continue
        ref = ':'.join(fields[:10])
        if fields[0] not in ('4097','5001','5002','8193') or fields[1:3] != ['0','2'] or ref in refs:
            raise ValueError('Invalid or duplicated radio identity')
        if not fields[10].lower().startswith(('http%3a//','https%3a//')):
            raise ValueError('Invalid radio stream URL')
        refs.add(ref)
    if groups[:2] != ['Slovensko', 'Čechy'] or len(refs) != report.get('total_stations') or len(refs) < 3000:
        raise ValueError('Unexpected radio catalogue structure or count')


def refresh(directory=Path('/etc/enigma2'), now=None):
    """No Enigma imports: all file/network work happens outside the GUI thread."""
    target = directory / FILENAME
    index = directory / INDEX_NAME
    if target.is_symlink() or (target.exists() and not target.is_file()) or index.is_symlink() or (index.exists() and not index.is_file()):
        return {'changed': False, 'skipped': 'unsafe-path'}
    # Exact managed filename and header prevent touching arbitrary user bouquets.
    before = target.read_bytes() if target.exists() else None
    if before is not None and not before.startswith(HEADER):
        return {'changed': False, 'skipped': 'unmanaged'}
    lock_flags = os.O_WRONLY | os.O_CREAT | os.O_NOFOLLOW
    with os.fdopen(os.open(str(directory / (STATE_NAME + '.lock')), lock_flags, 0o644), 'a') as lock:
        try:fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:return {'changed': False, 'skipped': 'busy'}
        now = time.time() if now is None else now
        # Wait until the system clock is set (avoid writing bogus weekly dates).
        if now < 1700000000:
            return {'changed': False, 'skipped': 'clock'}
        state = read_state(directory)
        registered = register_radio(directory) if before is not None else False
        if not due(state, now):
            return {'changed': True} if registered else {'changed': False, 'skipped': 'not-due'}
        state['last_attempt'] = now
        write_atomic(directory / STATE_NAME, json.dumps(state).encode())
        report = json.loads(fetch(REPORT_URL, 16384).decode('utf-8'))
        expected = report.get('bouquet_sha256', '')
        if not re.fullmatch('[0-9a-f]{64}', expected):
            raise ValueError('Invalid radio catalogue checksum')
        changed = before is None or hashlib.sha256(before).hexdigest() != expected
        if changed:
            # Resolve main once. Both files are then read at the same commit to
            # avoid mixing a manifest with a concurrently refreshed bouquet.
            metadata_url = 'https://api.github.com/repos/Evolution-by-Warder/PiconHub-Warder-Evolution/commits?path='+BOUQUET_PATH+'&per_page=1'
            metadata = json.loads(fetch(metadata_url, 65536).decode('utf-8'))
            revision = metadata[0]['sha']
            if not re.fullmatch('[0-9a-f]{40}', revision):
                raise ValueError('Invalid radio source revision')
            report = json.loads(fetch(BASE+revision+'/'+CATALOG+'catalog/world-radio-update.json', 16384).decode('utf-8'))
            raw = fetch(BASE+revision+'/'+BOUQUET_PATH, LIMIT)
            validate(raw, report)
            # Respect concurrent user/import edits made while downloads ran.
            if target.is_symlink() or (before is not None and target.read_bytes() != before):
                raise ValueError('Radio bouquet changed during download')
            changed = raw != before
            if changed:
                if before is None:
                    install_if_missing(target, raw)
                else:
                    write_atomic(directory / (FILENAME + '.bak'), before)
                    write_atomic(target, raw)
        registered = register_radio(directory) or registered
        state.update(last_success=now, sha256=report['bouquet_sha256'])
        write_atomic(directory / STATE_NAME, json.dumps(state).encode())
        return {'changed': changed or registered}


class Controller:
    def __init__(self, event_loop=None, reload_bouquets=None):
        from .warderHelpPreview import _NativeLoop
        self.loop = event_loop or _NativeLoop()
        self.reload = reload_bouquets or self._reload
        self.worker = None
        self.pending = self.loop.callLater(60, self.check)
        self.timeout = None
        self.closed = False
        # postinst may already have installed the data while Enigma was running.
        self.initial_reload = True

    @staticmethod
    def _reload():
        from enigma import eDVBDB
        # Reload service-list data only. Never stop/zap the playing service.
        eDVBDB.getInstance().reloadBouquets()

    def check(self):
        self.pending = None
        if self.closed:return
        from .warderHelpPreview import _Worker
        self.worker = _Worker(self.finished)
        try:
            path = os.path.abspath(__file__)
            self.loop.spawnProcess(self.worker, '/usr/bin/python3', ['/usr/bin/python3', path, '--refresh'], env=dict(os.environ))
            self.timeout = self.loop.callLater(90, self.timed_out)
        except Exception:
            self.finished(None)

    def finished(self, result):
        self.worker = None
        if self.timeout is not None and self.timeout.active():self.timeout.cancel()
        self.timeout = None
        if self.closed:return
        ready = isinstance(result, dict) and ('changed' in result) and result.get('skipped') in (None, 'not-due')
        if ready and (result.get('changed') or self.initial_reload):
            try:
                self.reload()
                self.initial_reload = False
            except Exception:pass
        self.pending = self.loop.callLater(3600, self.check)

    def timed_out(self):
        self.timeout = None
        if self.worker is not None:
            try:self.worker.transport.kill()
            except Exception:pass
        # Native appClosed callback will schedule the next silent check.

    def close(self):
        self.closed = True
        for call in (self.pending, self.timeout):
            if call is not None and call.active():call.cancel()
        if self.worker is not None:
            try:self.worker.transport.kill()
            except Exception:pass


def start(reason=0):
    global _controller
    if reason == 0 and _controller is None:
        _controller = Controller()
    elif reason != 0 and _controller is not None:
        _controller.close()
        _controller = None


if __name__ == '__main__':
    if sys.argv[1:] != ['--refresh']:sys.exit(2)
    try:
        signal.alarm(90)
        os.nice(10)
        print(json.dumps(refresh()))
    except Exception:
        # No popup, stdout traceback, or receiver restart on network failure.
        sys.exit(1)
