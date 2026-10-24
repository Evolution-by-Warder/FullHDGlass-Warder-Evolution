#!/usr/bin/env python3
"""Prepare the approved TEST258 previews at build time, never in the menu.

Pillow is a build-only dependency. The complete independent pixel comparison
in test-help-art.py must pass before this archive may be packaged.
"""
import argparse
import base64
import hashlib
import importlib.util
import io
from pathlib import Path
import zipfile
import zlib

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / 'source/package-root/usr/lib/enigma2/python/Plugins/Extensions/setupGlass17'
spec = importlib.util.spec_from_file_location('help_art_build', PLUGIN / 'warderHelpArt.py')
art = importlib.util.module_from_spec(spec)
spec.loader.exec_module(art)


def build(bundle, output):
    index = art._index()
    raw = Path(bundle).read_bytes()
    if hashlib.sha256(raw).hexdigest() != index['source_bundle_sha256']:
        raise ValueError('Help bundle SHA256 mismatch')
    lookup = [min(255, value + offset) for offset in art._BACKGROUND for value in range(256)]
    seen = set()
    with zipfile.ZipFile(io.BytesIO(raw)) as source, zipfile.ZipFile(output, 'w') as target:
        for name in sorted(source.namelist()):
            if not name.lower().endswith('.png'):
                continue
            original = source.read(name)
            digest = hashlib.sha256(original).hexdigest()
            if digest in seen:
                continue
            seen.add(digest)
            entry = index['images'][digest]
            image = Image.open(io.BytesIO(original)).convert('RGBA')
            bits = zlib.decompress(base64.b64decode(entry['mask']))
            mask = Image.frombytes('L', image.size, bytes(
                255 if bits[i >> 3] & (128 >> (i & 7)) else 0 for i in range(882 * 300)))
            navy = image.convert('RGB').point(lookup)
            result = Image.composite(image.convert('RGB'), navy, mask).convert('RGBA')
            result.putalpha(image.getchannel('A'))
            revision = hashlib.sha256((art._STYLE + ':' + entry['mask']).encode('ascii')).hexdigest()[:12]
            member = zipfile.ZipInfo(digest + '-' + revision + '.png', (1980, 1, 1, 0, 0, 0))
            member.compress_type = zipfile.ZIP_STORED
            target.writestr(member, art.encode_png(882, 300, result.tobytes()))
    if seen != set(index['images']):
        raise ValueError('Incomplete prepared help artwork')
    print('Prepared', len(seen), 'unique previews for all 252 original filenames')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--bundle', required=True)
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    build(args.bundle, args.output)
