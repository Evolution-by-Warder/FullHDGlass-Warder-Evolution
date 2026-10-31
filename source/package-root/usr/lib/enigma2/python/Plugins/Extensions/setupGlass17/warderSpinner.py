"""Select native, pre-rendered skin spinners at save/install time only.

No renderer, background worker, playback timer or diagnostic files are added.
The image/system/user spinner paths are never changed. Enigma2 loads the
selected private skin frames on the next GUI start.
"""
import hashlib
import json
import os
from pathlib import Path
import re
import tempfile

SKIN_ROOT = Path('/usr/share/enigma2/hd_glass17')
CATALOG = Path(__file__).with_name('warder-spinners.json')
SETTING = 'config.plugins.setupGlass17.par230'
DOWNLOAD_ROOT = Path('/var/lib/fullhdglass17/spinner-themes')


def validate_theme(theme):
    frames = theme['frames']
    if not 1 <= len(frames) <= 64:
        raise ValueError('Unsupported frame count')
    if [item['name'] for item in frames] != ['wait%d.png' % n for n in range(1, len(frames) + 1)]:
        raise ValueError('Spinner frames must be sequential PNG files')
    if any(not re.fullmatch('[0-9a-f]{64}', item['sha256']) for item in frames + theme.get('legacy_frames', [])):
        raise ValueError('Invalid spinner hash')
    width, height = theme['size']
    if not (0 < width <= 128 and 0 < height <= 128 and width * height * 4 < 48000):
        raise ValueError('Spinner exceeds reviewed surface bounds')


def downloaded(root=DOWNLOAD_ROOT):
    root = Path(root)
    if root.is_symlink():
        raise ValueError('Linked spinner storage')
    if not root.exists():
        return {}
    result = {}
    for folder in list(root.iterdir())[:8]:
        if not re.fullmatch(r'dl-[0-9a-f]{16}', folder.name):
            continue
        path = folder/'manifest.json'
        if folder.is_symlink() or path.is_symlink() or not path.is_file() or path.stat().st_size > 20000:
            raise ValueError('Invalid downloaded spinner storage')
        data = json.loads(path.read_text())
        if data.get('product') != 'FullHDGlass-spinner' or data.get('id') != folder.name:
            raise ValueError('Unknown downloaded spinner')
        validate_theme(data['theme'])
        result[folder.name] = data
    return result


def catalog(path=CATALOG, download_root=DOWNLOAD_ROOT):
    value = json.loads(Path(path).read_text())
    if value.get('schema') != 1 or value.get('default') != 'dove':
        raise ValueError('Unsupported spinner catalog')
    themes = value['themes']
    if not themes or value['default'] not in themes or any(not re.fullmatch('[a-z][a-z0-9-]{0,31}', key) for key in themes):
        raise ValueError('Invalid spinner theme identifiers')
    for theme in themes.values():
        validate_theme(theme)
    sources = {}
    try:
        stored = downloaded(download_root)
    except (OSError, ValueError, KeyError, TypeError):
        stored = {}  # Optional data must never prevent the settings from opening.
    for theme_id, data in stored.items():
        themes[theme_id] = data['theme']
        sources[theme_id] = str(Path(download_root)/theme_id)
    value['downloaded_sources'] = sources
    return value


def choices(translate, catalog_path=CATALOG):
    return [(key, translate(theme['title'])) for key, theme in catalog(catalog_path)['themes'].items()]


def _read_frame(path):
    if path.is_symlink() or not path.is_file():
        raise ValueError('Spinner frame is not a regular file')
    raw = path.read_bytes()
    return raw, hashlib.sha256(raw).hexdigest()


def _known_files(folder, themes):
    """Accept only positively identified package frames, including an upgrade mix.

    opkg can overlay eighteen default frames onto a twenty-frame selection;
    the two remaining frames must be recognized before they can be removed.
    An unknown/user file or link refuses the complete operation.
    """
    if folder.is_symlink() or not folder.is_dir():
        raise ValueError('Spinner directory is not a regular directory')
    allowed = {}
    for theme in themes.values():
        for entry in theme['frames'] + theme.get('legacy_frames', []):
            allowed.setdefault(entry['name'], set()).add(entry['sha256'])
    entries = list(folder.iterdir())
    for path in entries:
        if path.name not in allowed or _read_frame(path)[1] not in allowed[path.name]:
            raise ValueError('A custom spinner file must be preserved')
    return entries


def _remove_known(folder, themes):
    for path in _known_files(folder, themes):
        path.unlink()
    folder.rmdir()


def apply(theme_id, skin_root=SKIN_ROOT, catalog_path=CATALOG, download_root=DOWNLOAD_ROOT):
    """Validate first, swap a complete private set, roll back failed swaps."""
    data = catalog(catalog_path, download_root)
    themes = data['themes']
    if theme_id not in themes:
        raise ValueError('Unknown spinner selection')
    root = Path(skin_root)
    if root.is_symlink() or not root.is_dir():
        raise ValueError('Skin directory is not a regular directory')
    source = Path(data['downloaded_sources'].get(theme_id, root / 'spinner-themes' / theme_id))
    library = root / 'spinner-themes'
    if library.is_symlink() or source.is_symlink() or not source.is_dir():
        raise ValueError('Spinner source directory is not a regular directory')
    frames = []
    for entry in themes[theme_id]['frames']:
        raw, digest = _read_frame(source / entry['name'])
        if digest != entry['sha256']:
            raise ValueError('Spinner source verification failed')
        frames.append((entry['name'], raw, digest))
    active = root / 'spinner'
    previous = root / '.warder-spinner-previous'
    # Recover an interruption between the two directory renames.
    if previous.exists() or previous.is_symlink():
        _known_files(previous, themes)
        if not active.exists() and not active.is_symlink():
            os.rename(previous, active)
        else:
            _known_files(active, themes)
            _remove_known(previous, themes)
    if active.exists() or active.is_symlink():
        current = _known_files(active, themes)
        if {path.name for path in current} == {name for name, _, _ in frames} and all(
                _read_frame(active / name)[1] == digest for name, _, digest in frames):
            return False
    staging = Path(tempfile.mkdtemp(prefix='.warder-spinner-stage-', dir=str(root)))
    # mkdtemp is private while preparing; installed PNGs must remain readable.
    staging.chmod(0o755)
    try:
        for name, raw, digest in frames:
            path = staging / name
            with path.open('xb') as output:
                output.write(raw)
                output.flush()
                os.fsync(output.fileno())
            path.chmod(0o644)
            if _read_frame(path)[1] != digest:
                raise OSError('Spinner copy verification failed')
        moved = active.exists()
        if moved:
            os.rename(active, previous)
        try:
            os.rename(staging, active)
        except OSError:
            if moved:
                os.rename(previous, active)
            raise
        if moved:
            _remove_known(previous, themes)
        return True
    finally:
        # Remove only our staging files, even after a partial write failure.
        if staging.exists() and not staging.is_symlink():
            for path in staging.iterdir():
                if path.name in {name for name, _, _ in frames} and path.is_file() and not path.is_symlink():
                    path.unlink()
            staging.rmdir()


def saved_theme(settings, catalog_path=CATALOG):
    value = 'dove'
    path = Path(settings)
    if path.is_file():
        for line in path.read_text(errors='replace').splitlines():
            key, separator, selected = line.partition('=')
            if separator and key == SETTING:
                value = selected.strip()
    data = catalog(catalog_path)
    return value if value in data['themes'] else data['default']


if __name__ == '__main__':
    import sys
    try:
        if sys.argv[1:] == ['--prepare-removal']:
            # Return to the package-owned eighteen files before opkg removes
            # them, so a longer selected set cannot leave an unowned tail.
            apply('dove')
        elif not sys.argv[1:]:
            apply(saved_theme('/etc/enigma2/settings'))
        else:
            sys.exit(2)
    except (OSError, ValueError, KeyError, TypeError):
        # Optional appearance must never break installation or erase user data.
        sys.exit(1)
