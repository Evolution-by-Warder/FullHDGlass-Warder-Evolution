#!/usr/bin/env python3
"""Finish separate, attributed native PNG folders and looped GIF previews."""
import hashlib
import html
import json
from pathlib import Path
import shutil
import subprocess
import zipfile

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'assets/warder/downloads/ui/spinners/sources/spinkit'
OUTPUT = ROOT / 'assets/warder/downloads/ui/spinners/preview-library/spinkit'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    catalog = json.loads((OUTPUT / 'catalog.json').read_text())
    assert len(catalog['entries']) == 12
    license_text = (SOURCE / 'LICENSE').read_text()
    assert 'Tobias Ahlin' in license_text and 'Permission is hereby granted' in license_text
    links = []
    for number, row in enumerate(catalog['entries'], 1):
        folder = OUTPUT / row['folder']
        native = folder / 'frames'
        native.mkdir(exist_ok=True)
        frames = []
        for index in range(1, row['frame_count'] + 1):
            name = 'wait%d.png' % index
            with Image.open(folder / 'rendered' / name) as source:
                assert source.size == (416, 416)
                image = source.convert('RGBA').convert('RGBa').resize((104, 104), Image.Resampling.LANCZOS).convert('RGBA')
            image.save(native / name, format='PNG', optimize=True, compress_level=9)
            frames.append({'name': name, 'sha256': sha(native / name)})
        row['frames'] = frames
        row['decoded_32bit_surface_bytes'] = 104 * 104 * 4
        row['source_css_sha256'] = sha(SOURCE / 'spinkit.css')
        (folder / 'metadata.json').write_text(json.dumps(row, ensure_ascii=False, indent=2) + '\n')
        shutil.copyfile(SOURCE / 'LICENSE', folder / 'LICENSE.txt')
        (folder / 'AUTOR.txt').write_text('SpinKit — ' + row['name'] + '\nAutor: Tobias Ahlin\nLicencia: MIT; úplné znenie je v LICENSE.txt.\nZdroj: ' + row['source_url'] + '\nPripravené pre FullHDGlass: modrá #3CCFFF, priehľadné snímky 104 × 104 px.\nTáto ukážka zatiaľ nie je súčasťou inštalačného balíka.\n')
        duration = row['frame_count'] / 10
        subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-f','lavfi','-i',
            'color=c=0x071321:s=104x104:r=10','-framerate','10','-i',str(native/'wait%d.png'),
            '-filter_complex','[0:v][1:v]overlay=shortest=1:format=auto,split[a][b];[a]palettegen=stats_mode=full[p];[b][p]paletteuse=dither=sierra2_4a',
            '-t',str(duration),'-loop','0','-y',str(folder/'preview.gif')],check=True)
        (folder / 'index.html').write_text('<!doctype html><html lang="sk"><meta charset="utf-8"><title>'+html.escape(row['title'])+'</title><style>body{background:#071321;color:#eee;font:18px system-ui;text-align:center;margin:3rem}img{width:104px;height:104px}a{color:#3ccfff}</style><h1>'+str(number)+'. '+html.escape(row['title'])+'</h1><img src="preview.gif" alt="Pohyblivá ukážka"><p>SpinKit — '+html.escape(row['name'])+'</p><p>Autor: Tobias Ahlin · 104 × 104 px</p><p><a href="../index.html">Späť na zoznam</a></p></html>')
        links.append('<li><a href="'+row['folder']+'/index.html">'+html.escape(row['title'])+' — '+row['name']+'</a></li>')
        shutil.rmtree(folder / 'rendered')
    (OUTPUT / 'catalog.json').write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + '\n')
    (OUTPUT / 'index.html').write_text('<!doctype html><html lang="sk"><meta charset="utf-8"><title>Spinnery po jednom</title><style>body{background:#071321;color:#eee;font:18px system-ui;max-width:650px;margin:3rem auto;line-height:1.8}a{color:#3ccfff}</style><h1>Spinnery na výber</h1><p>Každý odkaz otvorí jednu samostatnú pohyblivú ukážku.</p><ol>'+''.join(links)+'</ol><p>Autor SpinKit: Tobias Ahlin · MIT. Zatiaľ iba ukážky.</p></html>')
    (OUTPUT / 'README.md').write_text('# Samostatné ukážky spinnerov\n\nOtvorte index.html alebo ktorýkoľvek pomenovaný adresár. Každý obsahuje vlastnú animáciu preview.gif, priehľadné snímky vo frames/, údaje o autorovi a licenciu.\n\nAutor SpinKit: Tobias Ahlin, licencia MIT. Pripravené iba na prezeranie a schválenie; bez nového IPK.\n')
    # Each native sequence is distinct and intact; blank initial pulse frames
    # are intentional, but a whole static/empty sequence must never pass.
    totals = {'spinners': 12, 'frames': 0, 'source_css_sha256': sha(SOURCE/'spinkit.css'), 'new_ipk': False}
    seen = set()
    for row in catalog['entries']:
        paths = list((OUTPUT/row['folder']/'frames').glob('*.png'))
        assert len(paths) == row['frame_count'] <= 64
        pixels = []
        for entry in row['frames']:
            path = OUTPUT/row['folder']/'frames'/entry['name']
            assert sha(path) == entry['sha256']
            with Image.open(path) as image:
                assert image.mode == 'RGBA' and image.size == (104,104)
                assert image.getchannel('A').getextrema()[0] == 0
                pixels.append(hashlib.sha256(image.tobytes()).hexdigest())
        assert len(set(pixels)) > 1, row['id']
        identity = tuple(pixels)
        assert identity not in seen, 'Duplicate native spinner'
        seen.add(identity)
        totals['frames'] += len(paths)
    (OUTPUT / 'verification.json').write_text(json.dumps(totals,indent=2)+'\n')
    bundle = OUTPUT.parent/'spinkit-samostatne-ukazky.zip'
    with zipfile.ZipFile(bundle,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as archive:
        for path in sorted(OUTPUT.rglob('*')):
            if path.is_file():
                archive.write(path, path.relative_to(OUTPUT))
    print(json.dumps(dict(totals,bundle_bytes=bundle.stat().st_size,bundle_sha256=sha(bundle))))


if __name__ == '__main__':
    main()
