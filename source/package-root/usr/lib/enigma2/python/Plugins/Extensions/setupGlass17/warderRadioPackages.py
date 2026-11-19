"""Verified local country bouquets and isolated Warder Radio Live picon ZIPs.

No network or Enigma imports at module import time. Never change user/TV/SAT
picons; only touch the dedicated PATHS/picon/radio directory after ownership
and archive integrity checks. This is a candidate, not a production installer.
"""
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import stat
import tempfile
import time
from uuid import UUID
from zipfile import ZipFile, BadZipFile

from . import warderRadioLive as live

COUNTRY = re.compile(r'^[A-Z]{2}$')
PNG_NAME = re.compile(r'^4097_0_2_(?:[0-9A-F]{1,8}_){6}[0-9A-F]{1,8}\.png$')
SHA = re.compile(r'^[0-9a-f]{64}$')
OWNER_FILE = '.warder-radio-country.json'
MAX_STATIONS = 12000
MAX_MANIFEST = 64 * 1024
MAX_OWNER_MANIFEST = 4 * 1024 * 1024
MAX_BOUQUET = 12 * 1024 * 1024
MAX_CATALOGUE = 24 * 1024 * 1024
MAX_ZIP = 1024 * 1024 * 1024
MAX_PNG = 512 * 1024
MAX_EXPANDED = 1024 * 1024 * 1024


def _file(root, relative, max_size):
    """Read only regular files below a trusted non-symlink package root."""
    root = Path(root)
    if root.is_symlink() or not root.is_dir():
        raise ValueError('Unsafe radio country package root')
    path = root
    for component in relative.split('/'):
        if component in ('', '.', '..'):
            raise ValueError('Unsafe package path')
        path = path / component
        if path.is_symlink():
            raise ValueError('Symlink in package path')
    if not path.is_file() or path.stat().st_size > max_size:
        raise ValueError('Missing or oversized country package')
    return path.read_bytes()


def _json(data):
    try:
        value = json.loads(data.decode('utf-8'))
    except (ValueError, UnicodeError):
        raise ValueError('Invalid country package JSON')
    if not isinstance(value, dict):
        raise ValueError('Invalid country package JSON structure')
    return value


def _verified_member(root, manifest, relative, max_size):
    files = manifest.get('files')
    entry = files.get(relative) if isinstance(files, dict) else None
    if (not isinstance(entry, dict) or
            not isinstance(entry.get('sha256'), str) or
            not SHA.fullmatch(entry['sha256']) or
            type(entry.get('bytes')) is not int or
            not 0 < entry['bytes'] <= max_size):
        raise ValueError('Invalid country manifest member')
    raw = _file(root, relative, max_size)
    if len(raw) != entry['bytes'] or hashlib.sha256(raw).hexdigest() != entry['sha256']:
        raise ValueError('Country asset SHA-256 mismatch')
    return raw


def _verified_large_file(root, manifest, relative, maximum):
    """Stream SHA for country ZIP without loading the full archive into RAM."""
    entry = manifest.get('files', {}).get(relative)
    if (not isinstance(entry, dict) or
            type(entry.get('bytes')) is not int or
            not 0 < entry['bytes'] <= maximum or
            not isinstance(entry.get('sha256'), str) or
            not SHA.fullmatch(entry['sha256'])):
        raise ValueError('Invalid country ZIP manifest')
    parent = Path(root)
    if parent.is_symlink() or not parent.is_dir():
        raise ValueError('Unsafe package root')
    for part in relative.split('/'):
        if part in ('', '.', '..'):
            raise ValueError('Unsafe ZIP path')
        parent = parent / part
        if parent.is_symlink():
            raise ValueError('Symlink in package path')
    if not parent.is_file() or parent.stat().st_size != entry['bytes']:
        raise ValueError('Invalid country ZIP size')
    digest = hashlib.sha256()
    with parent.open('rb') as handle:
        for chunk in iter(lambda: handle.read(256 * 1024), b''):
            digest.update(chunk)
    if digest.hexdigest() != entry['sha256']:
        raise ValueError('Country asset SHA-256 mismatch')
    return parent


def verified_country(root, code):
    """Validate a COMPLETE Radio Browser snapshot and exact Enigma2 references."""
    if not isinstance(code, str) or not COUNTRY.fullmatch(code):
        raise ValueError('Invalid country code')
    manifest = _json(_file(root, 'manifests/' + code + '.json', MAX_MANIFEST))
    if (manifest.get('country') != code or
            manifest.get('catalogue_complete') is not True or
            type(manifest.get('stations')) is not int or
            not 0 < manifest['stations'] <= MAX_STATIONS):
        raise ValueError('Incomplete or invalid country catalogue')
    data = _json(_verified_member(root, manifest, 'catalog/' + code + '.json', MAX_CATALOGUE))
    if (data.get('country') != code or data.get('catalogue_complete') is not True or
            not isinstance(data.get('stations'), list) or
            len(data['stations']) != manifest['stations']):
        raise ValueError('Invalid station-to-country mapping')
    name = data.get('name')
    if not isinstance(name, str) or not name or '\r' in name or '\n' in name:
        raise ValueError('Invalid country display name')
    used = set()
    for row in data['stations']:
        if not isinstance(row, dict) or row.get('countrycode') != code:
            raise ValueError('Untrusted station country')
        uuid = row.get('stationuuid')
        try:
            canonical = str(UUID(uuid))
        except (ValueError, AttributeError, TypeError):
            raise ValueError('Invalid Radio Browser UUID')
        if (uuid != canonical or row.get('stem') != live.service_stem(uuid) or
                uuid in used):
            raise ValueError('Duplicate or invalid station service ID')
        used.add(uuid)
        # Recheck the source URL, station name and identity using the skin's
        # own validator; do not trust JSON alone.
        actual = live._entry(row)
        if actual['stem'] != row['stem'] or actual['name'] != row['name']:
            raise ValueError('Unsafe station row')
    raw = _verified_member(root, manifest, 'bouquets/' + code + '.radio', MAX_BOUQUET)
    expected = live._bouquet([(name, data['stations'])])
    if raw != expected:
        raise ValueError('Country bouquet differs from signed service mapping')
    payload = live._json_bytes({'schema': 1, 'stations': data['stations']})
    if len(payload) > MAX_CATALOGUE:
        raise ValueError('Oversized local mapping')
    return raw, payload, manifest


def activate_local(root, code, directory):
    """Switch a cached country without Radio Browser or network requests."""
    raw, payload, _ = verified_country(root, code)
    directory = Path(directory)
    if directory.is_symlink() or not directory.is_dir():
        return {'changed': False, 'skipped': 'unsafe-path'}
    from . import warderRadioCountry as country
    target = directory / live.FILE
    state_file = directory / country.CHOICE_FILE
    mapping = directory / live.DATA_FILE
    staging = directory / country.PAGE_FILE
    if not all(live._safe_file(p) for p in (target, state_file, mapping, staging)):
        return {'changed': False, 'skipped': 'unsafe-path'}
    with country._lock(directory) as lock:
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            return {'changed': False, 'skipped': 'busy'}
        before = target.read_bytes() if target.exists() else None
        state = country._choice(directory)
        if not country._owner_valid(directory, before, state):
            return {'changed': False, 'skipped': 'owner-modified'}
        changed = before != raw
        if not mapping.exists() or mapping.read_bytes() != payload:
            live._write(mapping, payload)
        if changed:
            live._write(target, raw)
        now = time.time()
        state.update({'schema': country.VERSION, 'active': code,
                      'sha256': hashlib.sha256(raw).hexdigest(),
                      'last_success': now, 'last_attempt': now,
                      'last_error': None, 'downloaded': len(_json(payload)['stations']),
                      'partial': False})
        state.pop('pending', None)
        state.pop('pending_started', None)
        country._save_choice(directory, state)
        live._write(staging, b'{}')
        registered = live._register(directory)
        return {'changed': changed or registered, 'country': code,
                'stations': state['downloaded'], 'local': True}


def _owned_dir(folder):
    """Only a byte-for-byte owned RADIO directory may be replaced or deleted."""
    if folder.is_symlink():
        return False
    if not folder.exists():
        return True
    if not folder.is_dir():
        return False
    marker = folder / OWNER_FILE
    if marker.is_symlink() or not marker.is_file() or marker.stat().st_size > MAX_OWNER_MANIFEST:
        return False
    state = _json(marker.read_bytes())
    files = state.get('files')
    if state.get('owner') != 'WarderRadioLive' or not isinstance(files, dict):
        return False
    if set(p.name for p in folder.iterdir()) != set(files) | {OWNER_FILE}:
        return False
    for name, digest in files.items():
        if not isinstance(name, str) or not PNG_NAME.fullmatch(name) or (
                not isinstance(digest, str) or not SHA.fullmatch(digest)):
            return False
        p = folder / name
        if p.is_symlink() or not p.is_file() or p.stat().st_size > MAX_PNG:
            return False
        if hashlib.sha256(p.read_bytes()).hexdigest() != digest:
            return False
    return True


def install_logos(root, code, picon_root, require_external=True):
    """Atomic radio-only logo ZIP exchange. Keep old files on every failure.

    picon_root is PATHS/picon (not the global picon collection on flash).
    The caller must run this in a background worker, not the GUI event loop.
    """
    _, _, manifest = verified_country(root, code)
    if manifest.get('logo_package_complete') is not True:
        return {'changed': False, 'skipped': 'incomplete-logo-package'}
    picon_root = Path(picon_root)
    if (picon_root.name != 'picon' or picon_root.is_symlink() or
            not picon_root.is_dir() or
            (require_external and picon_root.stat().st_dev == Path('/').stat().st_dev)):
        return {'changed': False, 'skipped': 'unsafe-storage'}
    packed = _verified_large_file(root, manifest, 'logos/' + code + '.zip', MAX_ZIP)
    folder = picon_root / 'radio'
    if not _owned_dir(folder):
        return {'changed': False, 'skipped': 'unowned-radio-folder'}
    stage = Path(tempfile.mkdtemp(prefix='.warder-radio-stage-', dir=str(picon_root)))
    old = None
    changed = False
    try:
        total = 0
        hashes = {}
        try:
            with ZipFile(str(packed)) as z:
                members = z.infolist()
                if len(members) > MAX_STATIONS:
                    raise ValueError('Too many radio logos')
                for info in members:
                    name = info.filename
                    if (not PNG_NAME.fullmatch(name) or name in hashes or
                            info.file_size > MAX_PNG or
                            stat.S_ISLNK(info.external_attr >> 16)):
                        raise ValueError('Unsafe logo ZIP member')
                    png = z.read(info)
                    total += len(png)
                    if total > MAX_EXPANDED or not png.startswith(b'\x89PNG\r\n\x1a\n'):
                        raise ValueError('Invalid or oversized logo data')
                    p = stage / name
                    p.write_bytes(png)
                    hashes[name] = hashlib.sha256(png).hexdigest()
        except BadZipFile:
            raise ValueError('Invalid original logo ZIP')
        if len(hashes) != manifest.get('logos_found'):
            raise ValueError('Logo count differs from signed manifest')
        (stage / OWNER_FILE).write_text(
            json.dumps({'owner': 'WarderRadioLive', 'country': code,
                        'files': hashes}, sort_keys=True), encoding='utf-8')
        if folder.exists():
            old = Path(tempfile.mkdtemp(prefix='.warder-radio-old-', dir=str(picon_root)))
            old.rmdir()
            os.replace(str(folder), str(old))
        try:
            os.replace(str(stage), str(folder))
            changed = True
        except OSError:
            if old is not None and old.exists() and not folder.exists():
                os.replace(str(old), str(folder))
                old = None
            raise
        if old is not None:
            shutil.rmtree(str(old))
            old = None
        return {'changed': changed, 'country': code, 'logos': len(hashes)}
    finally:
        if stage.exists():
            shutil.rmtree(str(stage))
        # A failed rollback must never remove the surviving old radio folder.
