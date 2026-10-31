#!/usr/bin/env python3
"""Explicit rollback of this candidate's own files; never called on startup."""
import argparse
import hashlib
import json
from pathlib import Path

SPINNER = Path('/usr/share/enigma2/hd_glass17/spinner')
MARKER = '.warder-spinner-candidate.json'


def disable(folder=SPINNER):
    folder = Path(folder)
    marker = folder / MARKER
    if folder.is_symlink() or not folder.is_dir() or marker.is_symlink() or not marker.is_file():
        raise ValueError('No owned spinner candidate found; nothing changed')
    if marker.stat().st_size > 16384:
        raise ValueError('Invalid candidate ownership record')
    record = json.loads(marker.read_text())
    if record.get('product') != 'FullHDGlass-spinner-candidate':
        raise ValueError('Unrecognized spinner ownership; nothing changed')
    entries = record.get('frames', [])
    if [x.get('name') for x in entries] != ['wait%d.png' % i for i in range(1, 19)]:
        raise ValueError('Incomplete candidate inventory; nothing changed')
    verified = []
    for entry in entries:
        path = folder / entry['name']
        if path.is_symlink() or not path.is_file() or path.stat().st_size > 131072:
            raise ValueError('Candidate was modified; nothing changed')
        if hashlib.sha256(path.read_bytes()).hexdigest() != entry['sha256']:
            raise ValueError('Candidate was modified; nothing changed')
        verified.append(path)
    # All files are validated before changing any of them.
    for path in verified:
        path.unlink()
    marker.unlink()
    if not any(folder.iterdir()):
        folder.rmdir()
    return len(verified)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--disable', action='store_true', required=True)
    parser.parse_args()
    print('Removed %d owned spinner frames. Restart the GUI to reload the image spinner.' % disable())
