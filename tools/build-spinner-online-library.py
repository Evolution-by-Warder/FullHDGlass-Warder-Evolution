#!/usr/bin/env python3
"""One deterministic archive and one static PNG per spinner, outside the IPK."""
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import zipfile

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
LIBRARY = ROOT/'assets/warder/downloads/ui/spinners/preview-library'
OUTPUT = ROOT/'assets/warder/downloads/ui/spinners/online'
PLUGIN = ROOT/'source/package-root/usr/lib/enigma2/python/Plugins/Extensions/setupGlass17'
SKIN = ROOT/'source/package-root/usr/share/enigma2/hd_glass17'
spec = importlib.util.spec_from_file_location('online_spinner_build_core', PLUGIN/'warderSpinnerOnline.py')
online = importlib.util.module_from_spec(spec)
spec.loader.exec_module(online)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def store(kind, key, suffix, raw):
    path = OUTPUT/kind/(key+'-'+sha(raw)[:12]+'.'+suffix)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(raw)
    return {'path':str(path.relative_to(OUTPUT)), 'bytes':len(raw), 'sha256':sha(raw)}


def pack(files):
    stream = io.BytesIO()
    with zipfile.ZipFile(stream, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for name, raw in sorted(files.items()):
            info = zipfile.ZipInfo(name, (2026,1,1,0,0,0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, raw)
    return stream.getvalue()


def main():
    source = json.loads((LIBRARY/'catalog.json').read_text())['entries']
    audit = {r['id']:r for r in json.loads((ROOT/'reports/spinner-quality-20261031/audit.json').read_text())['entries']}
    native = json.loads((PLUGIN/'warder-spinners.json').read_text())['themes']
    definitions = []
    for key, theme in native.items():
        folder = SKIN/'spinner-themes'/key
        definitions.append((key, theme, folder, 'wait1.png', None))
    for row in source:
        key = row['id'] if row['id'].startswith('spinkit-') else 'community-'+row['id'].split('-',1)[0]
        folder = LIBRARY/row['directory']
        theme = {k:row[k] for k in ('title','author','size','frames')}
        definitions.append((key, theme, folder/'frames', audit[row['id']]['representative_frame'], folder))
    rows = []
    for key, original, folder, sample, source_folder in definitions:
        theme = {k:original[k] for k in ('title','author','size','frames')}
        theme['preview_frame'] = sample
        files = {f['name']:(folder/f['name']).read_bytes() for f in theme['frames']}
        for frame in theme['frames']:
            if sha(files[frame['name']]) != frame['sha256']:
                raise ValueError('Source spinner frame mismatch')
        files['manifest.json'] = (json.dumps({'schema':1,'id':key,'theme':theme},ensure_ascii=False,sort_keys=True)+'\n').encode()
        files['AUTOR.txt'] = (theme['title']+'\n'+theme['author']+'\n').encode()
        if source_folder:
            if (source_folder/'AUTOR.txt').exists():
                files['AUTOR.txt'] = (source_folder/'AUTOR.txt').read_bytes()
            for license_name in ('LICENSE', 'LICENSE.txt'):
                if (source_folder/license_name).exists():
                    files['LICENSE.txt'] = (source_folder/license_name).read_bytes()
        output = io.BytesIO()
        with Image.open(folder/sample) as image:
            thumb = image.convert('RGBa')
            thumb.thumbnail((76,76), Image.Resampling.LANCZOS)
            frame = Image.new('RGBA',(80,80),(0,0,0,0))
            frame.paste(thumb.convert('RGBA'),((80-thumb.width)//2,(80-thumb.height)//2))
            frame.save(output,format='PNG',optimize=True,compress_level=9)
        raw = output.getvalue()
        online.png(raw,(80,80))
        item = {'id':key,'title':theme['title'],'author':theme['author'],
                'archive':store('archives',key,'zip',pack(files)),
                'thumbnail':store('thumbnails',key,'png',raw),
                'frames_sha256':online.frame_digest(theme['frames'])}
        online.archive_data(item, (OUTPUT/item['archive']['path']).read_bytes(), lambda value:None)
        rows.append(item)
    data = (json.dumps({'schema':1,'product':'FullHDGlass-spinners','entries':rows},ensure_ascii=False,separators=(',',':'))+'\n').encode()
    online.parse_catalog(data)
    (OUTPUT/'catalog.json').write_bytes(data)
    report = {'schema':1,'spinners':len(rows),'catalog_bytes':len(data),
              'archive_bytes':sum(r['archive']['bytes'] for r in rows),
              'thumbnail_bytes':sum(r['thumbnail']['bytes'] for r in rows),
              'separate_archives':True,'static_thumbnails':True,'receiver_pillow_dependency':False,
              'native_frames_in_main_ipk':'Only the two bundled defaults; online library is external'}
    (OUTPUT/'verification.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report))


if __name__ == '__main__':
    main()
