#!/usr/bin/env python3
"""Replace only the approved TA3 220x132 black PNG in the full 23.5E archive."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import copy
import hashlib
import importlib.util
import io
import json
import os
import struct
import urllib.request
import zipfile

ROOT=Path(__file__).resolve().parents[1]
DIRECTORY=ROOT/'assets/warder/downloads/picons/channels'
REFERENCE='1_0_1_1328_CA2_3_EB0000_0_0_0.png'
SOURCE_REF='09e6e6ed78f3dbd18daeefe3fb88108e14f4e9d7'
SOURCE_ROOT='https://raw.githubusercontent.com/Evolution-by-Warder/PiconHub-Warder-Evolution/'+SOURCE_REF+'/'
APPROVED_SHA='6654300f844e34b151a855bd5fe3e2636b6170134f1b25d9f361a94e49bdcf10'
OLD_PNG_SHA='73cb4d642b0338904aa68ca50b587ff5faa1f33d23b9d56d57afc57f1df35326'
OLD_ARCHIVE_SHA='8f3be7598749dbe7e4fda3bb3ab823dc7910dac35adb8d6a855063bbacf4fbb9'
sha=lambda data:hashlib.sha256(data).hexdigest()


def get(url):
    with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Warder-approved-TA3','Cache-Control':'no-cache'}),timeout=90) as response:
        return response.read()


def archive_bytes(package,metadata):
    cache=Path(os.environ.get('TA3_PACKAGE_CACHE','/tmp/warder-ta3-parts'))
    cache.mkdir(exist_ok=True,parents=True)
    def part(url):
        path=cache/url.rsplit('/',1)[-1];record=metadata[path.name]
        data=path.read_bytes() if path.is_file() else get(url)
        assert len(data)==record['bytes'] and sha(data)==record['sha256'],path.name
        if not path.exists():path.write_bytes(data)
        return data
    with ThreadPoolExecutor(max_workers=6) as pool:data=b''.join(pool.map(part,package['parts']))
    assert len(data)==package['bytes'] and sha(data)==package['sha256']
    return data


def package_png(data):
    with zipfile.ZipFile(io.BytesIO(data)) as archive:
        names=archive.namelist();assert len(names)==len(set(names))
        assert names.count(REFERENCE)==1
        return archive.read(REFERENCE)


def main():
    manifest=DIRECTORY/'manifest.json';original=json.loads(manifest.read_text());doc=copy.deepcopy(original)
    selected={p['selector_id']:p for p in doc['packages'] if p['selector_id'] in ('235E','CANALPLUS_SK','CANALPLUS_CZ') and p['resolution']=='220x132' and p['family']=='channel-black'}
    assert set(selected)=={'235E','CANALPLUS_SK','CANALPLUS_CZ'}
    approved=get(SOURCE_ROOT+'picons/23.5e/canal-plus-sk/black/'+REFERENCE)
    assert sha(approved)==APPROVED_SHA
    assert approved.startswith(b'\x89PNG\r\n\x1a\n') and struct.unpack('>II',approved[16:24])==(220,132)
    assert get(SOURCE_ROOT+'picons/23.5e/canal-plus-cz/black/'+REFERENCE)==approved
    metadata={p['filename']:p for p in doc['parts']}
    for selector in ('CANALPLUS_SK','CANALPLUS_CZ'):
        assert package_png(archive_bytes(selected[selector],metadata))==approved,selector
    package=selected['235E'];assert package['sha256']==OLD_ARCHIVE_SHA
    packed=archive_bytes(package,metadata);assert sha(package_png(packed))==OLD_PNG_SHA
    output=io.BytesIO()
    with zipfile.ZipFile(io.BytesIO(packed)) as archive:
        old_files={info.filename:archive.read(info) for info in archive.infolist()}
        with zipfile.ZipFile(output,'w') as result:
            result.comment=archive.comment
            for info in archive.infolist():result.writestr(info,approved if info.filename==REFERENCE else old_files[info.filename])
    new=output.getvalue()
    with zipfile.ZipFile(io.BytesIO(new)) as archive:
        assert set(archive.namelist())==set(old_files)
        assert archive.read(REFERENCE)==approved
        assert all(archive.read(name)==data for name,data in old_files.items() if name!=REFERENCE)
    digest=sha(new);filename='warder-235e-220x132-black-'+digest[:16]+'.zip'
    prefix=package['parts'][0].rsplit('/',1)[0]+'/'
    records=[];urls=[]
    for number,start in enumerate(range(0,len(new),4*1024*1024)):
        name=filename+'.part%02d'%number;data=new[start:start+4*1024*1024]
        (DIRECTORY/name).write_bytes(data)
        records.append({'filename':name,'bytes':len(data),'sha256':sha(data)});urls.append(prefix+name)
    old_names={url.rsplit('/',1)[-1] for url in package['parts']}
    package.update(filename=filename,bytes=len(new),sha256=digest,parts=urls)
    package['owner_approved_ta3_20261101']={'source_repository':'Evolution-by-Warder/PiconHub-Warder-Evolution','source_ref':SOURCE_REF,'reference':REFERENCE,'png_sha256':APPROVED_SHA}
    doc['parts']=[p for p in doc['parts'] if p['filename'] not in old_names]+records
    before_others=[p for p in original['packages'] if (p['selector_id'],p['family'],p['resolution'])!=('235E','channel-black','220x132')]
    after_others=[p for p in doc['packages'] if (p['selector_id'],p['family'],p['resolution'])!=('235E','channel-black','220x132')]
    assert before_others==after_others
    module_path=ROOT/'source/package-root/usr/lib/enigma2/python/Plugins/Extensions/setupGlass17/warderPiconSync.py'
    spec=importlib.util.spec_from_file_location('ta3_publication_sync',module_path);sync=importlib.util.module_from_spec(spec);spec.loader.exec_module(sync)
    assert sync.validate_publication_manifest(doc,'production')==[]
    manifest.write_text(json.dumps(doc,sort_keys=True,indent=2)+'\n')
    sums=DIRECTORY/'SHA256SUMS';checksums={line.split()[-1]:line.split()[0] for line in sums.read_text().splitlines() if line.strip()}
    checksums.update({p['filename']:p['sha256'] for p in records});checksums['manifest.json']=sha(manifest.read_bytes())
    sums.write_text(''.join(digest+'  '+name+'\n' for name,digest in sorted(checksums.items())))
    report={'reference':REFERENCE,'style':'black','resolution':'220x132','source_ref':SOURCE_REF,'source_png_sha256':APPROVED_SHA,'old_png_sha256':OLD_PNG_SHA,'old_archive_sha256':OLD_ARCHIVE_SHA,'archive_sha256':digest,'archive_filename':filename,'archive_bytes':len(new),'png_count':len(old_files),'pngs_replaced':1,'unrelated_pngs_verified_unchanged':len(old_files)-1,'other_packages_verified_unchanged':len(before_others),'all_three_ta3_pngs_identical':True,'ipk_changed':False,'old_immutable_archives_preserved':True}
    destination=ROOT/'reports/ta3-canal-235e-20261101.json';destination.parent.mkdir(exist_ok=True);destination.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))


if __name__=='__main__':main()
