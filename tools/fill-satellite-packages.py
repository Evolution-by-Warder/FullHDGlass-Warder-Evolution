#!/usr/bin/env python3
"""Append existing approved PNGs; never replace an existing package member."""
import ast
import copy
import gzip
import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path
import shutil
import stat
import struct
import subprocess
import tempfile
from concurrent.futures import ThreadPoolExecutor
from urllib.request import urlopen
import zipfile

ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'tools/data/satellite-additive-fill-plan.json.gz'
DELIVERY=ROOT/'assets/warder/downloads/picons/channels'
PKG=ROOT/'source/package-root/usr/lib/enigma2/python/Plugins/Extensions/setupGlass17'
STYLES=('transparent','white','black')

def sha(data):return hashlib.sha256(data).hexdigest()

def fetch(package,ref):
    chunks=[]
    for url in package.get('parts') or [package['url']]:
        tail=url.split('/assets/',1)[1]
        immutable='https://raw.githubusercontent.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/'+ref+'/assets/'+tail
        for attempt in range(3):
            try:
                with urlopen(immutable,timeout=90) as response:chunk=response.read()
                break
            except Exception:
                if attempt==2:raise
        chunks.append(chunk)
    data=b''.join(chunks)
    assert len(data)==package['bytes'] and sha(data)==package['sha256']
    return data

def main():
    plan=json.loads(gzip.decompress(DATA.read_bytes()))
    assert plan['policy']=='add-missing-only-preserve-every-existing-png-byte'
    protected=[PKG/'version',PKG/'plugin.py',PKG/'warderPiconSync.py',ROOT/'source/control/control',ROOT/'update.json',ROOT/'update-test.json']
    before={str(p):sha(p.read_bytes()) for p in protected}
    assert (PKG/'version').read_text().strip()=='1.0.13'
    source=ROOT/'.approved-picons'
    paths=sorted({r['path'] for p in plan['positions'] for r in p['source']})
    subprocess.run(['git','sparse-checkout','set','--no-cone','--stdin'],input='\n'.join('/'+p for p in paths)+'\n',cwd=source,text=True,check=True)
    spec=importlib.util.spec_from_file_location('sync',PKG/'warderPiconSync.py');sync=importlib.util.module_from_spec(spec);spec.loader.exec_module(sync)
    method=next(n for n in ast.walk(ast.parse((PKG/'plugin.py').read_bytes())) if isinstance(n,ast.FunctionDef) and n.name=='_warderInstallChannelArchive')
    scope=dict(warderPiconSync=sync,os=os,shutil=shutil,stat=stat,tempfile=tempfile,zipfile=zipfile)
    exec(compile(ast.Module(body=[method],type_ignores=[]),'native-installer','exec'),scope);installer=scope['_warderInstallChannelArchive']
    docs={s:json.loads((DELIVERY/s/'manifest.json').read_text()) for s in ('','test-candidate')}
    originals=copy.deepcopy(docs)
    # Only the existing generic 0.8W triad is promoted; provider choices remain separate.
    for p in docs['test-candidate']['packages']:
        if p['selector_id']=='08W' and not any(q['selector_id']=='08W' and q['family']==p['family'] for q in docs['']['packages']):docs['']['packages'].append(copy.deepcopy(p))
    packages_by_key={(suffix,p['selector_id'],p['family']):p for suffix,doc in docs.items() for p in doc['packages']}
    work=[]
    pending=[]
    source_rejected=[]
    for position in plan['positions']:
        for style in STYLES:
            key=('test-candidate',position['selector'],'channel-'+style)
            package=packages_by_key.get(key) or packages_by_key.get(('',position['selector'],'channel-'+style))
            if package is None:
                pending.append(dict(position=position['position'],style=style,reason='no-existing-approved-package',trezor=position.get('trezor')))
                continue
            additions={}
            for row in position['source']:
                if row['style']!=style:continue
                data=(source/row['path']).read_bytes()
                assert hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()==row['blob']
                if data[:8]!=b'\x89PNG\r\n\x1a\n' or len(data)<24 or struct.unpack('>II',data[16:24])!=(220,132):
                    source_rejected.append(dict(path=row['path'],reason='not-valid-220x132-PNG-header'));continue
                assert row['name'] not in additions or additions[row['name']]==data
                additions[row['name']]=data
            if additions or position['selector']=='08W':work.append((position,style,package,additions))
    # Immutable archives can be shared by both catalogues and downloaded once.
    bases={p['sha256']:p for _,_,p,_ in work}
    with ThreadPoolExecutor(max_workers=5) as pool:
        downloads=dict(zip(bases,pool.map(lambda p:fetch(p,plan['base_ref']),bases.values())))
    report=[]
    for position,style,base,proposed in work:
        old=zipfile.ZipFile(io.BytesIO(downloads[base['sha256']]))
        old_files={n:old.read(n) for n in old.namelist()}
        additions={n:b for n,b in proposed.items() if n not in old_files}
        assert len(additions)==len(proposed), 'plan attempted to replace existing PNG'
        if not additions and position['selector']!='08W':continue
        output=io.BytesIO()
        with zipfile.ZipFile(output,'w') as archive:
            archive.comment=old.comment
            for entry in old.infolist():archive.writestr(copy.copy(entry),old_files[entry.filename])
            for name,data in sorted(additions.items()):
                entry=zipfile.ZipInfo(name,(2026,10,22,0,0,0));entry.compress_type=zipfile.ZIP_DEFLATED;entry.create_system=3;entry.external_attr=0o100644<<16
                archive.writestr(entry,data)
        data=output.getvalue();new=zipfile.ZipFile(io.BytesIO(data))
        assert set(new.namelist())==old_files.keys()|additions.keys()
        assert all(new.read(n)==png for n,png in old_files.items()),'existing PNG overwritten'
        assert all(new.read(n)==png for n,png in additions.items())
        assert new.testzip() is None
        with tempfile.TemporaryDirectory() as temp:
            archive_path=Path(temp)/'package.zip';dest=Path(temp)/'picon';dest.mkdir();archive_path.write_bytes(data)
            if old_files:
                keep=next(iter(old_files));(dest/keep).write_bytes(old_files[keep])
            installed,available=installer(None,str(archive_path),str(dest),set(additions))
            assert installed==additions.keys() and available==set(new.namelist())
            if old_files:assert (dest/keep).read_bytes()==old_files[keep]
        filename='warder-'+position['selector'].lower()+'-channel-'+style+'-'+sha(data)[:16]+'.zip'
        for suffix,doc in docs.items():
            package=next((p for p in doc['packages'] if p['selector_id']==position['selector'] and p['family']=='channel-'+style),None)
            if package is None:continue
            # Both current catalogues must start from the same immutable package.
            assert package['sha256']==base['sha256']
            directory=DELIVERY/suffix;branch='main' if not suffix else 'warder-modernization-work'
            root='https://raw.githubusercontent.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/'+branch+'/'+directory.relative_to(ROOT).as_posix()+'/'
            old_names={u.rsplit('/',1)[-1] for u in package.get('parts',[])}
            urls=[];records=[]
            for number,start in enumerate(range(0,len(data),18*1024*1024)):
                name=filename+'.part%02d'%number;part=data[start:start+18*1024*1024];(directory/name).write_bytes(part)
                urls.append(root+name);records.append(dict(filename=name,bytes=len(part),sha256=sha(part)))
            doc['parts']=[p for p in doc['parts'] if p['filename'] not in old_names]+records
            package.pop('url',None)
            package.update(filename=filename,parts=urls,bytes=len(data),sha256=sha(data),source_ref=plan['source_ref'],png_count=len(new.namelist()),included_references=sorted(n[:-4] for n in new.namelist()))
            package['additive_completion']=dict(base_sha256=base['sha256'],added_pngs=len(additions),existing_pngs_preserved=len(old_files))
            sums=directory/'SHA256SUMS';checks={line.split()[-1]:line.split()[0] for line in sums.read_text().splitlines()}
            checks.update({r['filename']:r['sha256'] for r in records});sums.write_text('\n'.join(f'{digest}  {name}' for name,digest in sorted(checks.items()))+'\n')
            report.append(dict(catalog=suffix or 'production',position=position['position'],selector=position['selector'],style=style,old_pngs=len(old_files),added_pngs=len(additions),png_count=len(new.namelist()),added_names=sorted(additions),sha256=sha(data),existing_pngs_unchanged=True,native_install_verified=True))
        print('ADDED',position['position'],style,len(additions),'PRESERVED',len(old_files),flush=True)
    changed={(r['selector'],'channel-'+r['style']) for r in report}
    for suffix,doc in docs.items():
        for original in originals[suffix]['packages']:
            key=(original['selector_id'],original['family'])
            if key not in changed:assert original==next(p for p in doc['packages'] if (p['selector_id'],p['family'])==key)
        assert not sync.validate_publication_manifest(doc,'production' if not suffix else 'test-candidate')
        doc['additive_satellite_completion']=dict(source_ref=plan['source_ref'],policy=plan['policy'])
        (DELIVERY/suffix/'manifest.json').write_text(json.dumps(doc,indent=2,sort_keys=True)+'\n')
    for tool in ('test-live-picon-catalog.py','verify-radio-release.py'):subprocess.run(['python3',str(ROOT/'tools'/tool)],cwd=ROOT,check=True)
    assert before=={str(p):sha(p.read_bytes()) for p in protected}
    result=dict(policy=plan['policy'],base_ref=plan['base_ref'],source_ref=plan['source_ref'],ipk_unchanged='1.0.13',packages=report,pending_packages=pending,rejected_source_pngs=source_rejected,unresolved_conflicts=[dict(position=p['position'],entries=p['conflicts']) for p in plan['positions'] if p['conflicts']],protected_files=before)
    out=ROOT/'reports/satellite-additive-fill-20261022.json';out.parent.mkdir(exist_ok=True);out.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    assert report and all(r['existing_pngs_unchanged'] for r in report)
    print('PASS: added missing existing PNGs only; every old PNG byte preserved; unchanged IPK and approved graphics',flush=True)

if __name__=='__main__':main()
