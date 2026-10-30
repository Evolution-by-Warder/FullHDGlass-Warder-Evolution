#!/usr/bin/env python3
"""Publish owner-authorized audited picon candidates without modifying receiver code or IPKs."""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import argparse
import ast
import copy
import hashlib
import importlib.util
import io
import json
import os
import re
import shutil
import stat
import tempfile
import urllib.request
import zipfile

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
DELIVERY = ROOT / 'assets/warder/downloads/picons/channels'
MANIFEST_URL = 'https://raw.githubusercontent.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/main/assets/warder/downloads/picons/channels/manifest.json'
PART_ROOT = MANIFEST_URL.rsplit('/', 1)[0]+'/'
PROVENANCE = 'plugin/artwork/provenance/picons-assimilated-20261030'
PROVIDERS = {'ANTIKSAT','DIGI_TELLY','FREESAT','SKYLINK','CANALPLUS_SK','CANALPLUS_CZ'}
PART_LIMIT = 16*1024*1024


def sha(data):
    return hashlib.sha256(data).hexdigest()


def fetch(url):
    for attempt in range(3):
        try:
            request=urllib.request.Request(url,headers={'User-Agent':'Warder-audited-picon-candidates/20261030'})
            with urllib.request.urlopen(request,timeout=90) as response:
                return response.read()
        except Exception:
            if attempt == 2:
                raise


def identity(filename):
    name=Path(filename).name
    if not re.fullmatch(r'[0-9a-fA-F]+(?:_[0-9a-fA-F]+){9}\.png',name):
        return None
    fields=name[:-4].split('_')
    return tuple(int(fields[n],16) for n in (3,4,5))+(int(fields[6],16)>>16,)


def resized(data,resolution):
    if resolution == '220x132':
        return data
    assert resolution in ('50x30','400x240')
    with Image.open(io.BytesIO(data)) as original:
        image=original.convert('RGBA').convert('RGBa').resize(tuple(map(int,resolution.split('x'))),Image.Resampling.LANCZOS).convert('RGBA')
        output=io.BytesIO()
        image.save(output,format='PNG')
        return output.getvalue()


def patch_archive(data,package,mappings,artwork):
    """Append missing references; retain every installed archive PNG byte."""
    style=package['family'].removeprefix('channel-')
    resolution=package['resolution']
    with zipfile.ZipFile(io.BytesIO(data)) as source:
        names=source.namelist()
        assert len(names)==len(set(names))
        assert all('/' not in n and '\\' not in n and n.lower().endswith('.png') for n in names)
        changes={}
        for mapping in mappings:
            if package['selector_id']!=mapping['selector_id']:continue
            aliases=sorted(n for n in names if identity(n)==tuple(mapping['identity']))
            approved=source.read(aliases[0]) if aliases else resized(artwork[(mapping['slug'],style)],resolution)
            for reference in mapping.get('references',[mapping['reference']]):
                assert identity(reference)==tuple(mapping['identity'])
                if reference not in names:changes[reference]=approved
        if not changes:return None
        preserved={n:sha(source.read(n)) for n in names}
        output=io.BytesIO()
        with zipfile.ZipFile(output,'w',zipfile.ZIP_DEFLATED,6) as target:
            for name in sorted(set(names)|set(changes)):
                info=zipfile.ZipInfo(name,(2026,10,30,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o100644<<16
                target.writestr(info,changes[name] if name in changes else source.read(name))
    packed=output.getvalue()
    with zipfile.ZipFile(io.BytesIO(packed)) as verify:
        assert verify.testzip() is None
        assert all(sha(verify.read(n))==digest for n,digest in preserved.items())
        assert all(verify.read(n)==b for n,b in changes.items())
    return packed,{'replaced':[],'added':sorted(changes),'unrelated_preserved':len(preserved),'changed_names':sorted(changes)}


def receiver_installer():
    pkg=ROOT/'source/package-root/usr/lib/enigma2/python/Plugins/Extensions/setupGlass17'
    spec=importlib.util.spec_from_file_location('receiver_sync',pkg/'warderPiconSync.py')
    sync=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(sync)
    tree=ast.parse((pkg/'plugin.py').read_bytes())
    nodes=[node for node in ast.walk(tree) if isinstance(node,ast.FunctionDef) and node.name=='_warderInstallChannelArchive']
    assert len(nodes)==1
    scope=dict(warderPiconSync=sync,os=os,shutil=shutil,stat=stat,tempfile=tempfile,zipfile=zipfile)
    exec(compile(ast.Module(body=nodes,type_ignores=[]),'actual-receiver-installer','exec'),scope)
    return sync,scope['_warderInstallChannelArchive']


def publish(source_root,source_ref):
    base=source_root/PROVENANCE
    plan=json.loads((base/'publication-plan.json').read_text())
    assert plan['status']=='OWNER_AUTHORIZED_INTEGRATION'
    assert plan['graphic_count']==63 and plan['artwork_count']==189 and len(plan['mappings'])==70
    assert all(m['quality'] in ('PASS','EXACT_EXISTING_WARDER_ARTWORK') for m in plan['mappings'])
    assert len(plan['excluded'])==9 and not ({m['reference'] for m in plan['mappings']} & {m['reference'] for m in plan['excluded']})
    artwork={}
    for item in plan['artwork']:
        for style,value in item['outputs'].items():
            data=(source_root/value['path']).read_bytes()
            assert sha(data)==value['sha256']
            with Image.open(io.BytesIO(data)) as image:
                assert image.size==(220,132)
                assert image.mode in ('RGBA','P')
            artwork[(item['slug'],style)]=data
    assert len(artwork)==189
    assert len({tuple(m['identity']) for m in plan['mappings']})==len(plan['mappings'])
    assert all(identity(m['reference'])==tuple(m['identity']) for m in plan['mappings'])
    path=DELIVERY/'manifest.json'
    previous_manifest_sha256=sha(path.read_bytes())
    assert previous_manifest_sha256==plan['base_manifest_sha256']
    document=json.loads(path.read_text())
    before=copy.deepcopy(document)
    part_meta={p['filename']:p for p in document['parts']}
    selectors={m['selector_id'] for m in plan['mappings']}
    candidates=[p for p in document['packages'] if p['selector_id'] in selectors]
    records=[]
    new_parts={}
    results={}
    sync,install=receiver_installer()

    def process(package):
        chunks=[]
        for url in package.get('parts',[package.get('url')]):
            assert url.startswith(PART_ROOT)
            data=fetch(url)
            if package.get('parts'):
                expected=part_meta[url.rsplit('/',1)[-1]]
                assert len(data)==expected['bytes'] and sha(data)==expected['sha256'],url
            chunks.append(data)
        data=b''.join(chunks)
        assert len(data)==package['bytes'] and sha(data)==package['sha256'],package['filename']
        result=patch_archive(data,package,plan['mappings'],artwork)
        if result is None:
            print('UNCHANGED',package['selector_id'],package['resolution'],package['family'],flush=True)
            return None
        packed,evidence=result
        digest=sha(packed)
        style=package['family'].removeprefix('channel-')
        filename=f'warder-{package["selector_id"].lower()}-{package["resolution"]}-{style}-{digest[:16]}.zip'
        parts=[]
        metadata=[]
        for number,start in enumerate(range(0,len(packed),PART_LIMIT)):
            name=filename+f'.part{number:02d}'
            chunk=packed[start:start+PART_LIMIT]
            destination=DELIVERY/name
            if destination.exists():
                assert destination.read_bytes()==chunk,'Immutable part collision'
            else:
                destination.write_bytes(chunk)
            parts.append(PART_ROOT+name)
            metadata.append({'filename':name,'bytes':len(chunk),'sha256':sha(chunk)})
        # Run the installed receiver's actual selective installer against every
        # changed full ZIP, including all sizes/styles. Unrelated user PNG stays.
        with tempfile.TemporaryDirectory() as temporary:
            folder=Path(temporary)
            archive=folder/'input.zip'
            archive.write_bytes(packed)
            destination=folder/'picon'
            destination.mkdir()
            sentinel=destination/'unrelated-user.png'
            sentinel.write_bytes(b'preserve-user-file')
            installed,available=install(None,str(archive),str(destination),wanted=set(evidence['changed_names']))
            assert installed==set(evidence['changed_names']) and installed<=available
            assert sentinel.read_bytes()==b'preserve-user-file'
            with zipfile.ZipFile(archive) as verify:
                assert all((destination/name).read_bytes()==verify.read(name) for name in installed)
        item=copy.deepcopy(package)
        item.update(filename=filename,bytes=len(packed),sha256=digest,parts=parts,png_count=len(available),source_repository='Evolution-by-Warder/PiconHub-Warder-Evolution',source_ref=source_ref)
        item.pop('url',None)
        if 'included_references' in item:
            item['included_references']=sorted(Path(n).stem for n in available)
        item['picons_assimilated_20261030']={'source_ref':source_ref,'replaced':len(evidence['replaced']),'added':len(evidence['added']),'unrelated_preserved':evidence['unrelated_preserved']}
        record=dict(selector_id=package['selector_id'],resolution=package['resolution'],style=style,filename=filename,sha256=digest,bytes=len(packed),**evidence)
        print('VERIFIED',package['selector_id'],package['resolution'],style,len(evidence['replaced']),'replaced',len(evidence['added']),'added',flush=True)
        return (package['selector_id'],package['resolution'],package['family']),item,metadata,record

    with ThreadPoolExecutor(max_workers=6) as executor:
        for result in executor.map(process,candidates):
            if result:
                key,item,metadata,record=result
                results[key]=item
                new_parts.update({m['filename']:m for m in metadata})
                records.append(record)
    assert 0<len(results)<=len(candidates)
    for i,package in enumerate(document['packages']):
        key=(package['selector_id'],package['resolution'],package['family'])
        if key in results:
            document['packages'][i]=results[key]
        else:
            assert package==before['packages'][i]
    all_parts={**part_meta,**new_parts}
    needed={url.rsplit('/',1)[-1] for p in document['packages'] for url in p.get('parts',[])}
    document['parts']=[all_parts[name] for name in sorted(needed)]
    document['picons_assimilated_20261030']={'source_ref':source_ref,'graphic_count':63,'approved_png_count':189,'new_upstream_logos':13,'reused_warder_logos':50,'service_mappings':len(plan['mappings']),'package_count':len(results),'unrelated_png_bytes_preserved':True,'ipk_changed':False}
    assert not sync.validate_publication_manifest(document,MANIFEST_URL)
    planner_checks=0
    for (selector,resolution,family),package in results.items():
        binding=sync.task_binding_for_package_selector(selector)
        if not binding:
            assert selector in PROVIDERS
            continue
        prefs=sync.set_task_position_bindings(sync.default_preferences(),[binding])
        prefs.update(resolution=resolution,style=family.removeprefix('channel-'),update_mode=sync.UPDATE_MODE_REPLACE_ALL)
        queue=sync.build_runtime_queue(prefs,publication={'persistent':True,'manifest_url':MANIFEST_URL})
        jobs=sync.build_download_jobs(document,sync.plan_runtime_packages(document,queue,MANIFEST_URL),MANIFEST_URL)
        assert jobs['state']=='ready' and len(jobs['jobs'])==1
        assert jobs['jobs'][0]['sha256']==package['sha256']
        planner_checks+=1
    path.write_text(json.dumps(document,sort_keys=True,indent=2)+'\n')
    sums=DELIVERY/'SHA256SUMS'
    lines={line.split()[-1]:line.split()[0] for line in sums.read_text().splitlines() if line.strip()}
    lines.update({name:meta['sha256'] for name,meta in new_parts.items()})
    lines['manifest.json']=sha(path.read_bytes())
    sums.write_text(''.join(digest+'  '+name+'\n' for name,digest in sorted(lines.items())))
    report={'status':'VERIFIED_PUBLICATION_CANDIDATE','source_ref':source_ref,'previous_manifest_sha256':previous_manifest_sha256,'manifest_sha256':sha(path.read_bytes()),'graphic_count':63,'approved_png_count':189,'new_upstream_logos':13,'reused_warder_logos':50,'service_mappings':plan['mappings'],'service_source':plan['service_source'],'source_archive':plan['source_archive'],'scanned_packages':len(candidates),'total_catalog_packages':len(before['packages']),'changed_packages':len(results),'receiver_selective_installer_checks':len(results),'receiver_planner_checks':planner_checks,'unrelated_png_bytes_preserved':True,'old_archives_retained':True,'ipk_changed':False,'excluded':plan['excluded'],'scope_exclusions':'Unlisted candidates, test/data services, all existing PNG replacements, Trezor and IPKs','packages':records,'new_parts':list(new_parts.values())}
    target=ROOT/'reports/picons-assimilated-publication-20261030.json'
    target.parent.mkdir(exist_ok=True)
    target.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print('DONE',len(results),'packages,',planner_checks,'receiver plans,',len(results),'actual installer checks',flush=True)


def verify_public(ref):
    report=json.loads((ROOT/'reports/picons-assimilated-publication-20261030.json').read_text())
    root=PART_ROOT.replace('/main/','/'+ref+'/')
    def verify(item):
        data=fetch(root+item['filename'])
        assert len(data)==item['bytes'] and sha(data)==item['sha256'],item['filename']
        return item['filename']
    with ThreadPoolExecutor(max_workers=6) as executor:
        verified=list(executor.map(verify,report['new_parts']))
    report['public_verification']={'ref':ref,'verified_parts':len(verified),'all_sizes_and_sha256_match':True}
    (ROOT/'reports/picons-assimilated-publication-20261030.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print('PUBLIC PARTS VERIFIED',len(verified),flush=True)


def reuse_candidate(source_ref):
    """Resume evidence writeback without rebuilding immutable verified ZIPs."""
    report=json.loads((ROOT/'reports/picons-assimilated-publication-20261030.json').read_text())
    document=json.loads((DELIVERY/'manifest.json').read_text())
    assert report['source_ref']==source_ref
    assert report['manifest_sha256']==sha((DELIVERY/'manifest.json').read_bytes())
    assert report['receiver_selective_installer_checks']==report['changed_packages']
    assert report['receiver_planner_checks']==report['changed_packages']
    assert report['graphic_count']==63 and report['approved_png_count']==189
    entries={(p['selector_id'],p['resolution'],p['family']):p for p in document['packages']}
    for package in report['packages']:
        found=entries[(package['selector_id'],package['resolution'],'channel-'+package['style'])]
        assert found['sha256']==package['sha256'] and found['bytes']==package['bytes']
    metadata={part['filename']:part for part in document['parts']}
    assert all(metadata[part['filename']]==part for part in report['new_parts'])
    print('REUSING VERIFIED CANDIDATE',report['changed_packages'],'archives; public bytes will be verified again',flush=True)


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--source-root',type=Path)
    parser.add_argument('--source-ref')
    parser.add_argument('--verify-public')
    parser.add_argument('--reuse-candidate',action='store_true')
    args=parser.parse_args()
    if args.verify_public:
        verify_public(args.verify_public)
    elif args.reuse_candidate:
        reuse_candidate(args.source_ref)
    else:
        assert args.source_root and args.source_ref
        publish(args.source_root,args.source_ref)
