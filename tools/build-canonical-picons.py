#!/usr/bin/env python3
"""Build original-named complete picon packages from the current approved sets."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import hashlib
import io
import json
from pathlib import Path
import stat
import urllib.request
import zipfile
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
RAW='https://raw.githubusercontent.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/main/'


def fetch(asset,cache):
    target=cache/(asset['sha256']+'.zip')
    def valid(raw):return len(raw)==asset['size'] and hashlib.sha256(raw).hexdigest()==asset['sha256']
    if target.exists() and valid(target.read_bytes()):return target
    chunks=[]
    for url in asset.get('parts') or [asset['url']]:
        if not url.startswith(('https://raw.githubusercontent.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/','https://raw.githubusercontent.com/Evolution-by-Warder/PiconHub-Warder-Evolution/')):raise ValueError('Untrusted picon input')
        with urllib.request.urlopen(url,timeout=60) as response:chunks.append(response.read(asset['size']+1))
    raw=b''.join(chunks)
    if not valid(raw):raise ValueError('Picon input checksum mismatch: '+asset['id'])
    target.write_bytes(raw);return target


def merge(layers,kind):
    files={};resized=0
    for asset,path in layers:
        with zipfile.ZipFile(path) as source:
            if source.testzip() is not None:raise ValueError('Invalid ZIP CRC')
            for member in source.infolist():
                if member.is_dir():continue
                parts=member.filename.split('/')
                if len(parts)!=2 or parts[0]!=asset['root'] or not parts[1].lower().endswith('.png') or '\\' in parts[1] or stat.S_ISLNK(member.external_attr>>16):raise ValueError('Unsafe picon ZIP member')
                raw=source.read(member)
                with Image.open(io.BytesIO(raw)) as image:
                    if image.size!=(220,132):
                        image=image.convert('RGBA').resize((220,132),Image.Resampling.LANCZOS)
                        output=io.BytesIO();image.save(output,format='PNG',compress_level=9);raw=output.getvalue();resized+=1
                files[parts[1].casefold()]=(parts[1],raw)
    # Existing approved Canal+ SK/CZ correction retired the ambiguous Skylink logo.
    if kind=='provider':files.pop('skylink.png',None)
    return sorted(files.values()),resized


def package(path,root,files):
    path.parent.mkdir(parents=True,exist_ok=True)
    with zipfile.ZipFile(path,'w') as archive:
        for name,raw in files:
            member=zipfile.ZipInfo(root+'/'+name,(1980,1,1,0,0,0));member.compress_type=zipfile.ZIP_STORED;member.external_attr=(stat.S_IFREG|0o644)<<16
            archive.writestr(member,raw)
    raw=path.read_bytes()
    if len(raw)>32*1024*1024:raise ValueError('Picon ZIP exceeds receiver size limit')
    return len(raw),hashlib.sha256(raw).hexdigest()


def build(inputs,output,cache):
    output.mkdir(parents=True,exist_ok=True);cache.mkdir(parents=True,exist_ok=True)
    unique={a['sha256']:a for v in inputs['variants'].values() for a in v['layers']}
    with ThreadPoolExecutor(max_workers=4) as pool:prepared=dict(zip(unique,pool.map(lambda a:fetch(a,cache),unique.values())))
    result={'schema':1,'resolution':[220,132],'variants':{},'remove_paths':[
        'assets/warder/downloads/picons/providers/220x132/piconProv_220x132.zip',
        'assets/warder/downloads/picons/satellites/220x132/piconSat_220x132.zip',
        'assets/warder/downloads/picons/providers/transparent-legacy/provider-transparent-canalplus.zip',
        'assets/warder/downloads/picons/providers/white/parts/piconProv-white.zip.chunk00.part',
        'assets/warder/downloads/picons/providers/white/parts/piconProv-white.zip.chunk01.part']}
    for key,spec in inputs['variants'].items():
        files,resized=merge([(a,prepared[a['sha256']]) for a in spec['layers']],key.split('/')[0])
        size,digest=package(output/spec['path'],spec['root'],files)
        result['variants'][key]={'filename':spec['root']+'.zip','root':spec['root'],'png_count':len(files),'size':size,'sha256':digest,'url':RAW+spec['path'],'publication_source_id':'fullhd-production','path':spec['path'],'resolution':[220,132],'delivery':'canonical-220x132-v1','legacy_images_normalized':resized}
        print(key,len(files),'PNGs',size,'bytes',digest,flush=True)
    (output/'catalogue.json').write_text(json.dumps(result,indent=2)+'\n');return result


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--inputs',type=Path,default=ROOT/'design/picon-package-inputs.json');p.add_argument('--output',type=Path,default=Path('/tmp/warder-canonical-picons'));p.add_argument('--cache',type=Path,default=Path('/tmp/warder-picon-inputs'));a=p.parse_args();build(json.loads(a.inputs.read_text()),a.output,a.cache)
