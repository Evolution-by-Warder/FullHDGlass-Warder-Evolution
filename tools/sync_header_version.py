#!/usr/bin/env python3
"""Synchronize generated header labels with the packaged runtime version."""
import argparse
from pathlib import Path
import re

PLUGIN = Path('usr/lib/enigma2/python/Plugins/Extensions/setupGlass17')
FILES = ('plugin.py', 'warderDialogSkins.py')
LABEL = re.compile(r'(<eLabel\b(?=[^>]*\bposition="1680,70")[^>]*\btext=")([^"<>]*)(")')
VERSION = re.compile(r'\d+\.\d+\.\d+(?:-test\d+)?')


def sync_headers(payload, check=False):
    folder = Path(payload) / PLUGIN
    version = (folder / 'version').read_text().strip()
    if not VERSION.fullmatch(version):
        raise ValueError('Invalid packaged runtime version')
    counts = {}
    staged = []
    for name in FILES:
        path = folder / name
        original = path.read_text()
        labels = list(LABEL.finditer(original))
        if not labels or any(not VERSION.fullmatch(m[2]) for m in labels):
            raise ValueError('Missing or invalid version header in ' + name)
        if check and any(m[2] != version for m in labels):
            raise ValueError('Header version differs from runtime version in ' + name)
        updated = LABEL.sub(lambda m: m[1] + version + m[3], original)
        staged.append((path, original, updated))
        counts[name] = len(labels)
    if not check:
        for path, original, updated in staged:
            if updated != original:
                path.write_text(updated)
    return {'version': version, 'headers': counts}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    print(sync_headers(Path(__file__).resolve().parents[1] / 'source/package-root', args.check))


if __name__ == '__main__':
    main()
