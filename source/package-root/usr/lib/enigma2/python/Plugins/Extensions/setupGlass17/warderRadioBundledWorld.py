"""Built-in immutable world bouquet index: no extra folder or user action.

One signed 224-country, 48,219-station Radio Browser snapshot is shipped with
FullHDGlass. Validate SHA-256 before staging exclusively to external PATHS.
Logo PNGs are never included in flash; active-country images download only to
PATHS/picon/radio/CC/. No GUI-thread Internet/FS operations.
"""
from pathlib import Path
import hashlib
from . import warderRadioWorld as world

WORLD_SHA = '771953b41ceab46f8852f5e3219338cb1369d7f653ed7d329ad551e481f88d68'
SOURCE = Path('/usr/share/enigma2/hd_glass17/radio-world/radio-countries-bouquets.zip')

def sync_world(paths_root, require_external=True, source_archive=SOURCE):
    root=Path(paths_root)
    if not world._safe_directory(root):
        return {'changed':False,'skipped':'unsafe-storage'}
    if require_external and root.stat().st_dev == Path('/').stat().st_dev:
        return {'changed':False,'skipped':'unsafe-internal-flash'}
    archive=Path(source_archive)
    if archive.is_symlink() or not archive.is_file() or archive.stat().st_size>world.MAX_ARCHIVE:
        return {'changed':False,'skipped':'missing-bundled-world'}
    sha=hashlib.sha256()
    with archive.open('rb') as f:
        for chunk in iter(lambda:f.read(256*1024),b''):sha.update(chunk)
    if sha.hexdigest()!=WORLD_SHA:
        raise ValueError('Bundled 224-country radio-world SHA mismatch')
    return world.install_world(archive,WORLD_SHA,root,
        require_external=require_external,expected_countries=224)
