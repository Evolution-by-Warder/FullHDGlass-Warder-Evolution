#!/usr/bin/env python3
"""Build native spinner assets; Pillow is used only on the build machine."""
import hashlib
import io
import importlib.util
import json
from pathlib import Path
import zipfile

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SKIN = ROOT / 'source/package-root/usr/share/enigma2/hd_glass17'
PLUGIN = ROOT / 'source/package-root/usr/lib/enigma2/python/Plugins/Extensions/setupGlass17'
SOURCES = ROOT / 'design/spinner-choice/sources.json'
spec = importlib.util.spec_from_file_location('spinner_png_optimizer', ROOT/'tools/optimize-png.py')
optimizer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(optimizer)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def build():
    definitions = json.loads(SOURCES.read_text())
    catalog = {'schema': 1, 'default': definitions['default'], 'themes': {}}
    for definition in definitions['themes']:
        theme, title, author = (definition[key] for key in ('id', 'title', 'author'))
        count, size, source = definition['frames'], tuple(definition['size']), definition['source']
        if size[0] * size[1] * 4 >= 48000 or not 1 <= count <= 64:
            raise ValueError('Spinner exceeds reviewed native bounds')
        folder = SKIN / 'spinner-themes' / theme
        folder.mkdir(parents=True, exist_ok=True)
        entries = []
        archive = None
        if source['type'] == 'zip':
            original = (ROOT / source['path']).read_bytes()
            if sha(original) != source['sha256']:
                raise ValueError('The submitted archive has changed')
            archive = zipfile.ZipFile(io.BytesIO(original))
        elif source['type'] == 'directory':
            pinned = json.loads((ROOT / source['manifest']).read_text())
            approved = {Path(entry['path']).name: entry['sha256'] for entry in pinned['assets']}
        elif source['type'] == 'prepared':
            pinned = json.loads((ROOT/source['manifest']).read_text())
            approved = {entry['name']:entry['sha256'] for entry in pinned['frames']}
            if sha((ROOT/source['original_archive']).read_bytes()) != source['original_sha256']:
                raise ValueError('Original spinner archive changed')
        else:
            raise ValueError('Unsupported spinner source type')
        try:
            for index in range(1, count + 1):
                name = 'wait%d.png' % index
                raw = archive.read(source['prefix'] + name) if archive else (ROOT / source['path'] / name).read_bytes()
                if not archive and sha(raw) != approved[name]:
                    raise ValueError('Approved source frame has changed')
                with Image.open(io.BytesIO(raw)) as image:
                    if image.mode != 'RGBA' or image.size != tuple(source.get('size', size)):
                        raise ValueError('Unexpected submitted spinner format')
                    if image.size != size:
                        # Full-frame premultiplied alpha keeps original artwork
                        # proportions, frame order, transparency and antialiasing.
                        image = image.convert('RGBa').resize(size, Image.Resampling.LANCZOS).convert('RGBA')
                        output = io.BytesIO()
                        image.save(output, format='PNG', compress_level=9)
                        raw = output.getvalue()
                if source['type'] == 'prepared':
                    raw = optimizer.optimize(raw)
                (folder / name).write_bytes(raw)
                entries.append({'name': name, 'sha256': sha(raw)})
        finally:
            if archive:
                archive.close()
        catalog['themes'][theme] = {'title': title, 'author': author, 'size': list(size), 'frames': entries}
        if source['type'] == 'zip':
            catalog['themes'][theme]['source_sha256'] = source['sha256']
        if source['type'] == 'prepared':
            catalog['themes'][theme]['source_sha256'] = source['original_sha256']
        if definition.get('legacy_frames'):
            catalog['themes'][theme]['legacy_frames'] = definition['legacy_frames']
    (PLUGIN / 'warder-spinners.json').write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + '\n')
    assets = [{'path': 'usr/share/enigma2/hd_glass17/spinner-themes/' + key + '/' + entry['name'],
               'sha256': entry['sha256']} for key, theme in catalog['themes'].items() for entry in theme['frames']]
    record = {'schema': 1, 'assets': assets,
              'catalog_sha256': sha((PLUGIN / 'warder-spinners.json').read_bytes()),
              'physical_receiver_test': False}
    (ROOT / 'design/spinner-choice/assets.json').write_text(json.dumps(record, indent=2) + '\n')
    print('Prepared %d native spinner themes from the source registry' % len(catalog['themes']))


if __name__ == '__main__':
    build()
