#!/usr/bin/env python3
"""Prepare one attributed preview directory per unique supplied spinner.

Read PNGs only; never execute installers or copy archive paths onto a receiver.
Original submitted archives remain byte-identical in the source collection.
"""
import collections
import ctypes as ct
import ctypes.util
import hashlib
import html
import io
import json
from pathlib import Path
import re
import shutil
import subprocess
import unicodedata
import zipfile

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'assets/warder/downloads/ui/spinners/sources/community'
LIBRARY = ROOT / 'assets/warder/downloads/ui/spinners/preview-library'
OUTPUT = LIBRARY / 'community'
ARCHIVES = [
    ('techkings', 'spinners-with-setup-original.zip', 'spinners with setup.zip',
     '96c8b5131d0e10a45663cc24454afce946b39a47813575d9e1f9943bd6e0bbab'),
    ('openpli', 'spinner-pack-2-1-original.rar', 'Spinner Pack_2_1.rar',
     'bb4159ff9bd7fde37bfcfb12df747d1aa7631bc605b5fdac5285443f4faaa110'),
    ('football', 'spinner-football-soccer-original.zip', 'spinner_football_soccer.zip',
     '1cc8da9d04553bd51808e6cb22f3fb68a705b16829d500b6d48aae5e63e65e95'),
]
FRAME = re.compile(r'^wait(\d+)\.png$', re.I)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def rar_entries(path):
    lib = ct.CDLL(ctypes.util.find_library('archive'))
    signatures = [
        ('archive_read_new', ct.c_void_p, []),
        ('archive_read_support_filter_all', ct.c_int, [ct.c_void_p]),
        ('archive_read_support_format_all', ct.c_int, [ct.c_void_p]),
        ('archive_read_open_filename', ct.c_int, [ct.c_void_p, ct.c_char_p, ct.c_size_t]),
        ('archive_read_next_header', ct.c_int, [ct.c_void_p, ct.POINTER(ct.c_void_p)]),
        ('archive_entry_pathname', ct.c_char_p, [ct.c_void_p]),
        ('archive_entry_size', ct.c_longlong, [ct.c_void_p]),
        ('archive_read_data', ct.c_longlong, [ct.c_void_p, ct.c_void_p, ct.c_size_t]),
        ('archive_read_free', ct.c_int, [ct.c_void_p]),
        ('archive_error_string', ct.c_char_p, [ct.c_void_p]),
    ]
    for name, result, args in signatures:
        function = getattr(lib, name)
        function.restype, function.argtypes = result, args
    archive = lib.archive_read_new()
    lib.archive_read_support_filter_all(archive)
    lib.archive_read_support_format_all(archive)
    try:
        if lib.archive_read_open_filename(archive, str(path).encode(), 65536):
            raise ValueError('Cannot open submitted RAR')
        entry, buffer = ct.c_void_p(), ct.create_string_buffer(65536)
        while True:
            status = lib.archive_read_next_header(archive, ct.byref(entry))
            if status == 1:
                break
            if status != 0:
                raise ValueError(lib.archive_error_string(archive))
            name = lib.archive_entry_pathname(entry).decode('utf-8', 'replace').replace('\\', '/')
            if not FRAME.fullmatch(name.rsplit('/', 1)[-1]):
                continue
            size = lib.archive_entry_size(entry)
            if not 0 < size < 16 * 1024 * 1024:
                raise ValueError('Unexpected PNG member size')
            chunks = []
            while True:
                count = lib.archive_read_data(archive, buffer, len(buffer))
                if count == 0:
                    break
                if count < 0:
                    raise ValueError(lib.archive_error_string(archive))
                chunks.append(buffer.raw[:count])
            raw = b''.join(chunks)
            if len(raw) != size:
                raise ValueError('Truncated RAR member')
            yield name, raw
    finally:
        lib.archive_read_free(archive)


def read_pngs(path):
    if path.suffix == '.rar':
        yield from rar_entries(path)
    else:
        with zipfile.ZipFile(path) as archive:
            if archive.testzip() is not None:
                raise ValueError('ZIP checksum failure')
            for member in archive.infolist():
                if FRAME.fullmatch(member.filename.rsplit('/', 1)[-1]):
                    yield member.filename, archive.read(member)


def natural(text):
    return [int(part) if part.isdigit() else part.lower() for part in re.split(r'(\d+)', text)]


def slug(text):
    ascii_text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode()
    return re.sub('[^a-z0-9]+', '-', ascii_text.lower()).strip('-')


def preview(folder, count):
    subprocess.run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-f', 'lavfi', '-i',
        'color=c=0x071321:s=104x104:r=10', '-framerate', '10', '-i', str(folder/'frames/wait%d.png'),
        '-filter_complex', '[0:v][1:v]overlay=shortest=1:format=auto,split[a][b];[a]palettegen=stats_mode=full[p];[b][p]paletteuse=dither=sierra2_4a',
        '-t', str(count/10), '-loop', '0', '-y', str(folder/'preview.gif')], check=True)


def main():
    OUTPUT.mkdir(parents=True, exist_ok=True)
    catalog, duplicates, seen, source_records = [], [], {}, []
    group_count, input_frames = 0, 0
    for source_id, filename, original_name, checksum in ARCHIVES:
        archive_path = SOURCE / filename
        assert sha(archive_path.read_bytes()) == checksum
        groups = collections.defaultdict(list)
        for name, raw in read_pngs(archive_path):
            parent, _, base = name.rpartition('/')
            groups[parent].append((int(FRAME.fullmatch(base)[1]), raw, name))
        source_records.append({'id':source_id, 'filename':filename, 'original_filename':original_name,
                               'sha256':checksum, 'groups':len(groups), 'bytes':archive_path.stat().st_size})
        for parent, members in sorted(groups.items(), key=lambda item:natural(item[0])):
            group_count += 1
            members.sort()
            input_frames += len(members)
            if not 1 <= len(members) <= 64 or len({index for index,_,_ in members}) != len(members):
                raise ValueError('Invalid source sequence: '+parent)
            images = []
            for _, raw, name in members:
                with Image.open(io.BytesIO(raw)) as image:
                    image.load()
                    if image.width > 2048 or image.height > 2048:
                        raise ValueError('Unexpected source dimensions: '+name)
                    images.append(image.convert('RGBA'))
            width, height = max(image.width for image in images), max(image.height for image in images)
            # Do not invent extra detail in small originals. Use one fixed
            # aspect-preserving transform for the complete source sequence.
            scale = min(96/width, 96/height, 1.0)
            target = max(1, round(width*scale)), max(1, round(height*scale))
            native_images = []
            for image in images:
                canvas = Image.new('RGBA', (width,height), (0,0,0,0))
                canvas.paste(image,(0,0))
                fitted = canvas.convert('RGBa').resize(target, Image.Resampling.LANCZOS).convert('RGBA')
                native = Image.new('RGBA',(104,104),(0,0,0,0))
                native.paste(fitted,((104-target[0])//2,(104-target[1])//2))
                native_images.append(native)
            identity = tuple(sha(image.convert('RGBa').tobytes()) for image in native_images)
            label = parent.rsplit('/',1)[-1] if parent else 'Football Soccer'
            origin = {'source':source_id,'archive_folder':parent,'name':label,
                      'source_indices':[index for index,_,_ in members]}
            if identity in seen:
                canonical = seen[identity]
                canonical['origins'].append(origin)
                duplicates.append(dict(origin,canonical=canonical['folder']))
                continue
            number = len(catalog)+1
            folder_name = '%03d-%s-%s' % (number,source_id,slug(label))
            folder = OUTPUT / folder_name
            (folder/'frames').mkdir(parents=True, exist_ok=True)
            frames = []
            for index, image in enumerate(native_images,1):
                name = 'wait%d.png' % index
                image.save(folder/'frames'/name,format='PNG',optimize=True,compress_level=9)
                frames.append({'name':name,'sha256':sha((folder/'frames'/name).read_bytes())})
            author = 'ekremtt — podľa označenia v zdrojovej kolekcii' if 'by ekremtt' in parent.lower() else 'Autor v archíve neuvedený'
            row = {'id':folder_name,'folder':folder_name,'title':label,'author':author,
                   'license':'not-specified-in-submitted-archive','origins':[origin],
                   'size':[104,104],'source_canvas':[width,height],'inner_size':list(target),
                   'frame_count':len(frames),'interval_ms':100,'frames':frames,
                   'source_has_opaque_frames':any(image.getchannel('A').getextrema()[0]==255 for image in images),
                   'motion':len(set(identity))>1,'state':'preview-only-not-installed'}
            catalog.append(row)
            seen[identity] = row
            preview(folder,len(frames))
            (folder/'AUTOR.txt').write_text(label+'\n'+author+'\nZdroj: '+original_name+'\nPôvodné farby a poradie snímok sú zachované.\nPriehľadné snímky 104 × 104 px; originál je uložený bez úprav.\nLicencia v pôvodnom archíve nebola uvedená.\nZatiaľ iba ukážka, nie súčasť IPK.\n')
            (folder/'index.html').write_text('<!doctype html><html lang="sk"><meta charset="utf-8"><title>'+html.escape(label)+'</title><style>body{background:#071321;color:#eee;font:18px system-ui;text-align:center;margin:3rem}img{width:104px;height:104px}a{color:#3ccfff}</style><h1>'+html.escape(label)+'</h1><img src="preview.gif" alt="Pohyblivá ukážka"><p>'+html.escape(author)+'</p><p>104 × 104 px</p><p><a href="../../index.html">Späť na zoznam</a></p></html>')
            print('Prepared '+folder_name,flush=True)
    for row in catalog:
        (OUTPUT/row['folder']/'metadata.json').write_text(json.dumps(row,ensure_ascii=False,indent=2)+'\n')
    result = {'schema':1,'sources':source_records,'source_groups':group_count,'input_frames':input_frames,
              'unique_spinners':len(catalog),'duplicate_sequences':len(duplicates),'duplicates':duplicates,
              'native_frames':sum(row['frame_count'] for row in catalog),'entries':catalog,
              'new_ipk':False,'receiver_test':False}
    (OUTPUT/'catalog.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    (SOURCE/'manifest.json').write_text(json.dumps({'schema':1,'archives':source_records},indent=2)+'\n')
    build_combined(catalog)
    for row in catalog:
        folder = OUTPUT/row['folder']
        assert len(list((folder/'frames').glob('*.png'))) == row['frame_count']
        for entry in row['frames']:
            assert sha((folder/'frames'/entry['name']).read_bytes()) == entry['sha256']
            with Image.open(folder/'frames'/entry['name']) as image:
                assert image.mode=='RGBA' and image.size==(104,104)
                assert image.getchannel('A').getextrema()[0]==0
    report = {key:result[key] for key in ('source_groups','input_frames','unique_spinners','duplicate_sequences','native_frames','new_ipk')}
    (OUTPUT/'verification.json').write_text(json.dumps(report,indent=2)+'\n')
    # Build the final ZIP after all verification files have been written.
    bundle = LIBRARY/'warder-spinnery-na-vyber.zip'
    with zipfile.ZipFile(bundle,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as archive:
        for path in sorted(LIBRARY.rglob('*')):
            if path.is_file() and path.suffix!='.zip':
                archive.write(path,path.relative_to(LIBRARY))
    report.update(bundle_bytes=bundle.stat().st_size,bundle_sha256=sha(bundle.read_bytes()))
    print(json.dumps(report),flush=True)


def build_combined(community):
    spin = json.loads((LIBRARY/'spinkit/catalog.json').read_text())['entries']
    all_rows = [dict(row,preview_path='spinkit/'+row['folder']+'/preview.gif',directory='spinkit/'+row['folder']) for row in spin]
    all_rows += [dict(row,preview_path='community/'+row['folder']+'/preview.gif',directory='community/'+row['folder']) for row in community]
    minimal = [{key:row[key] for key in ('title','author','preview_path','directory')} for row in all_rows]
    data = json.dumps(minimal,ensure_ascii=False).replace('</','<\\/')
    (LIBRARY/'catalog.json').write_text(json.dumps({'schema':1,'spinners':len(all_rows),'entries':all_rows},ensure_ascii=False,indent=2)+'\n')
    (LIBRARY/'index.html').write_text('''<!doctype html><html lang="sk"><meta charset="utf-8"><title>Warder — spinnery na výber</title>
<style>body{margin:0;background:#071321;color:#eee;font:18px system-ui;text-align:center}main{max-width:700px;margin:3rem auto;padding:1rem}select{max-width:100%;padding:.7rem;background:#132a40;color:#eee;border:1px solid #3ccfff}button{padding:.7rem;margin:.4rem;background:#132a40;color:#3ccfff;border:1px solid #3ccfff;cursor:pointer}.stage{height:180px;display:grid;place-items:center}img{width:104px;height:104px}a{color:#3ccfff}small{color:#bccbd5}</style>
<main><h1>Spinnery na výber</h1><p>Každý spinner má vlastný adresár. Prezeraj si ich po jednom.</p><select id="pick" aria-label="Vybrať spinner"></select><div class="stage"><img id="preview" alt="Pohyblivá ukážka"></div><h2 id="name"></h2><p id="author"></p><p><button id="prev">← Predchádzajúci</button><button id="next">Ďalší →</button></p><p><a id="folder">Otvoriť samostatnú ukážku</a></p><small>104 × 104 px · zatiaľ iba ukážky, bez nového IPK</small></main>
<script>const rows=DATA;const pick=document.getElementById('pick');rows.forEach((row,i)=>pick.add(new Option((i+1)+'. '+row.title,i)));function show(i){i=(i+rows.length)%rows.length;pick.value=i;const row=rows[i];document.getElementById('preview').src=row.preview_path;document.getElementById('name').textContent=(i+1)+' / '+rows.length+' — '+row.title;document.getElementById('author').textContent=row.author;document.getElementById('folder').href=row.directory+'/index.html';location.hash=String(i+1)}pick.onchange=()=>show(Number(pick.value));document.getElementById('prev').onclick=()=>show(Number(pick.value)-1);document.getElementById('next').onclick=()=>show(Number(pick.value)+1);show(Math.max(0,(parseInt(location.hash.slice(1))||1)-1));</script></html>'''.replace('DATA',data))
    (LIBRARY/'README.md').write_text('# Warder — spinnery na výber\n\nRozbaľte celý archív a otvorte index.html. Ukazuje vždy jednu animáciu; prechádzať môžete tlačidlami Predchádzajúci/Ďalší alebo výberom názvu.\n\nKaždý spinner má vlastný pomenovaný adresár s preview.gif, snímkami vo frames/, vlastnou ukážkou index.html a údajmi o autorovi a zdroji. SpinKit obsahuje úplnú licenciu MIT. Neuvedené autorstvo ani licencie komunitných archívov nie sú domýšľané.\n\nDuplicity sú evidované v community/catalog.json a pôvodné archívy zostávajú zachované bez úprav. Zatiaľ iba ukážky, bez nového IPK.\n')


if __name__ == '__main__':
    main()
