#!/usr/bin/env python3
"""Integrate approved exact references additively; publish the catalogue last."""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import argparse, copy, hashlib, importlib.util, io, json, os, subprocess, tempfile, zipfile
from PIL import Image

ROOT=Path(__file__).resolve().parents[1]
DELIVERY=ROOT/'assets/warder/downloads/picons/channels'
PROVENANCE='plugin/artwork/provenance/warder-unchanged622-20261104'
REPORT=ROOT/'reports/unchanged622-publication-20261104.json'
BRANCH='release/unchanged622-20261104'
PART_ROOT='https://raw.githubusercontent.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/main/assets/warder/downloads/picons/channels/'
SPEC=importlib.util.spec_from_file_location('approved_publisher',ROOT/'tools/publish-warder-approved11-20261104.py')
HELPER=importlib.util.module_from_spec(SPEC);SPEC.loader.exec_module(HELPER)
sha=HELPER.sha

def approved_inputs(source):
    base=source/PROVENANCE
    plan=json.loads((base/'publication-plan.json').read_text())
    assert plan['status']=='OWNER_AUTHORIZED_INTEGRATION'
    assert plan['eligible_references']==796 and len(plan['mappings'])==796 and len(plan['excluded'])==13
    assert plan['styles']==['white','black']
    assert not HELPER.PROVIDERS.intersection(m['selector_id'] for m in plan['mappings'])
    routes={m['position']:m['selector_id'] for m in plan['mappings']}
    assert routes['0.8w']=='08W' and routes['16.0e']=='160E' and routes['23.5e']=='235E'
    blocked={m['reference'] for m in plan['excluded']}
    assert not blocked.intersection(m['reference'] for m in plan['mappings'])
    assert len({m['reference'] for m in plan['mappings']})==796
    packed=b''.join((base/'assets'/('approved-pngs.zip.part%02d'%i)).read_bytes() for i in range(plan['archive_parts']))
    assert sha(packed)==plan['approved_archive_sha256']
    artwork={}
    records=sum([json.loads(p.read_text()) for p in sorted(base.glob('artwork-*.json'))],[])
    assert len(records)==622
    with zipfile.ZipFile(io.BytesIO(packed)) as archive:
        assert len(archive.namelist())==1244 and len(set(archive.namelist()))==1244
        for record in records:
            assert record['visual_status']=='OWNER_APPROVED_UNCHANGED'
            for style,value in record['outputs'].items():
                assert style in plan['styles']
                raw=archive.read(value['archive_member'])
                assert sha(raw)==value['sha256']
                with Image.open(io.BytesIO(raw)) as image: assert image.size==(220,132)
                artwork[record['source_pixel_key'],style]=raw
    assert len(artwork)==1244
    for mapping in plan['mappings']:
        assert mapping['status'] in ('VERIFIED_EXACT_NOVEMBER_ASSIGNMENT','VERIFIED_EXISTING_EXACT_REFERENCE_ARTWORK','VERIFIED_TECHNICAL_OR_GENERIC_REFERENCE')
        assert (mapping['source_pixel_key'],'white') in artwork
    return plan,artwork

def patch_archive(data,package,mappings,artwork):
    style=package['family'].removeprefix('channel-')
    assert style in ('white','black')
    with zipfile.ZipFile(io.BytesIO(data)) as old:
        names=old.namelist()
        assert len(names)==len(set(names)) and all('/' not in n and '\\' not in n and n.endswith('.png') for n in names)
        relevant=[m for m in mappings if m['selector_id']==package['selector_id']]
        retained=[m['reference'] for m in relevant if m['reference'] in names]
        changes={m['reference']:HELPER.resized(artwork[m['source_pixel_key'],style],package['resolution']) for m in relevant if m['reference'] not in names}
        existing={n:sha(old.read(n)) for n in names}
        evidence={'added':sorted(changes),'retained_existing_exact_references':sorted(retained),'preserved_pngs':len(names),'preserved_png_hashes_sha256':sha(json.dumps(existing,sort_keys=True).encode())}
        if not changes: return None,evidence
        output=io.BytesIO()
        with zipfile.ZipFile(output,'w',zipfile.ZIP_DEFLATED,6) as target:
            for name in sorted(set(names)|set(changes)):
                info=zipfile.ZipInfo(name,(2026,11,4,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o100644<<16
                target.writestr(info,changes[name] if name in changes else old.read(name))
        packed=output.getvalue()
        with zipfile.ZipFile(io.BytesIO(packed)) as check:
            assert check.testzip() is None
            assert all(sha(check.read(n))==digest for n,digest in existing.items())
            assert all(check.read(n)==raw for n,raw in changes.items())
            assert all(m['reference'] in check.namelist() for m in relevant)
    return packed,evidence

def empty_zip():
    output=io.BytesIO()
    with zipfile.ZipFile(output,'w'):pass
    return output.getvalue()

def verify_planners(document,records,source_root):
    receiver,_=HELPER.receiver_installer()
    spec=importlib.util.spec_from_file_location('piconhub_sync',source_root/'plugin/src/Plugins/Extensions/WarderPiconHub/warder_skin_sync.py')
    piconhub=importlib.util.module_from_spec(spec);spec.loader.exec_module(piconhub)
    checks={}
    for label,sync in [('receiver',receiver),('piconhub',piconhub)]:
        assert not sync.validate_publication_manifest(document,HELPER.MANIFEST_URL)
        count=0;direct=[]
        for item in records:
            binding=sync.task_binding_for_package_selector(item['selector_id'])
            if binding is None:
                assert item['selector_id'] in ('345W','500E')
                direct.append(item['selector_id']);continue
            prefs=sync.set_task_position_bindings(sync.default_preferences(),[binding])
            prefs.update(resolution=item['resolution'],style=item['style'],update_mode=sync.UPDATE_MODE_REPLACE_ALL)
            queue=sync.build_runtime_queue(prefs,publication={'persistent':True,'manifest_url':HELPER.MANIFEST_URL})
            jobs=sync.build_download_jobs(document,sync.plan_runtime_packages(document,queue,HELPER.MANIFEST_URL),HELPER.MANIFEST_URL)
            assert jobs['state']=='ready' and len(jobs['jobs'])==1
            assert jobs['jobs'][0]['sha256']==item['sha256']
            count+=1
        checks[label+'_planner_checks']=count
        checks[label+'_new_selectors_requiring_client_update']=sorted(set(direct))
    return checks

def publish(source_root,source_ref,repair_routing=False):
    plan,artwork=approved_inputs(source_root)
    manifest=DELIVERY/'manifest.json'
    document=json.loads(manifest.read_text())
    reused_records=[];reused_parts={};routing_repair=None
    if repair_routing:
        old_report=json.loads(REPORT.read_text())
        assert sha(manifest.read_bytes())==old_report['manifest_sha256']
        baseline_raw=(ROOT/'reports/unchanged622-base-manifest-20261104.json').read_bytes()
        assert sha(baseline_raw)==plan['base_manifest_sha256']
        baseline=json.loads(baseline_raw)
        base_pkgs={(p['selector_id'],p['family'],p['resolution']):p for p in baseline['packages']}
        wrong={'ANTIKSAT','DIGI_TELLY','CANALPLUS_CZ'}
        corrected={'08W','160E','235E'}
        for i,p in enumerate(document['packages']):
            key=p['selector_id'],p['family'],p['resolution']
            if p['selector_id'] in wrong:document['packages'][i]=copy.deepcopy(base_pkgs[key])
        reused_records=[r for r in old_report['packages'] if r['selector_id'] not in wrong]
        assert len(reused_records)==162
        reused_names={url.rsplit('/',1)[-1] for p in document['packages'] if p['selector_id'] not in HELPER.PROVIDERS for url in p.get('parts',[])}
        reused_parts={p['filename']:p for p in old_report['new_parts'] if p['filename'] in reused_names}
        previous=plan['base_manifest_sha256']
        parts={p['filename']:p for p in baseline['parts']}
        parts.update({p['filename']:p for p in document['parts']})
        candidates=[p for p in document['packages'] if p['selector_id'] in corrected and p['family'] in ('channel-white','channel-black')]
        assert len(candidates)==18
        routing_repair={'restored_provider_packages':sorted(wrong),'correct_satellite_selectors':sorted(corrected),'reused_verified_package_builds':162,'superseded_manifest_sha256':old_report['manifest_sha256']}
    else:
        assert sha(manifest.read_bytes())==plan['base_manifest_sha256'],'Production catalogue changed: rebase and compare before publication'
        previous=sha(manifest.read_bytes())
        baseline=copy.deepcopy(document)
        parts={x['filename']:x for x in document['parts']}
        selectors={m['selector_id'] for m in plan['mappings']}
        candidates=[p for p in document['packages'] if p['selector_id'] in selectors and p['family'] in ('channel-white','channel-black')]
        for selector,position in plan['new_satellite_selectors'].items():
            assert not any(p['selector_id']==selector for p in document['packages'])
            for resolution in plan['sizes']:
                for style in plan['styles']:
                    candidates.append({'selector_id':selector,'warder_key':position,'family':'channel-'+style,'resolution':resolution,'new_standalone_satellite_package':True})
    before=copy.deepcopy(document)
    sync,install=HELPER.receiver_installer()
    def process(package):
        original=b''
        if package.get('new_standalone_satellite_package'):
            data=empty_zip()
        else:
            chunks=[]
            for url in package.get('parts',[package.get('url')]):
                assert url.startswith(PART_ROOT)
                raw=HELPER.fetch(url)
                if package.get('parts'):
                    meta=parts[url.rsplit('/',1)[-1]]
                    assert len(raw)==meta['bytes'] and sha(raw)==meta['sha256']
                chunks.append(raw)
            data=b''.join(chunks)
            assert len(data)==package['bytes'] and sha(data)==package['sha256']
        packed,evidence=patch_archive(data,package,plan['mappings'],artwork)
        base={'selector_id':package['selector_id'],'resolution':package['resolution'],'style':package['family'].removeprefix('channel-'),**evidence}
        if packed is None:
            print('UNCHANGED',base['selector_id'],base['resolution'],base['style'],len(base['retained_existing_exact_references']),flush=True)
            return None,[],dict(base,filename=package['filename'],sha256=package['sha256'],bytes=package['bytes'],changed=False)
        digest=sha(packed);filename='warder-%s-%s-%s-%s.zip'%(base['selector_id'].lower().replace('_',''),base['resolution'],base['style'],digest[:16])
        metadata=[];urls=[]
        for i,start in enumerate(range(0,len(packed),HELPER.PART_LIMIT)):
            name=filename+'.part%02d'%i;raw=packed[start:start+HELPER.PART_LIMIT]
            path=DELIVERY/name
            if path.exists(): assert path.read_bytes()==raw
            else:path.write_bytes(raw)
            metadata.append({'filename':name,'bytes':len(raw),'sha256':sha(raw)});urls.append(PART_ROOT+name)
        with tempfile.TemporaryDirectory() as temp:
            folder=Path(temp);archive=folder/'input.zip';archive.write_bytes(packed);dest=folder/'picons';dest.mkdir()
            sentinel=dest/'unrelated-user.png';sentinel.write_bytes(b'preserve-user-file')
            installed,available=install(None,str(archive),str(dest),wanted=set(evidence['added']))
            assert installed==set(evidence['added']) and sentinel.read_bytes()==b'preserve-user-file'
            with zipfile.ZipFile(archive) as check: assert all((dest/n).read_bytes()==check.read(n) for n in installed)
        item=copy.deepcopy(package);item.update(filename=filename,parts=urls,bytes=len(packed),sha256=digest,png_count=len(available),source_repository='Evolution-by-Warder/PiconHub-Warder-Evolution',source_ref=source_ref)
        item.pop('url',None)
        if 'included_references' in item:item['included_references']=sorted(Path(n).stem for n in available)
        item['unchanged622_20261104']={'added':len(evidence['added']),'all_existing_png_bytes_preserved':True,'source_ref':source_ref}
        print('VERIFIED',base['selector_id'],base['resolution'],base['style'],len(evidence['added']),'added;',len(evidence['retained_existing_exact_references']),'already present',flush=True)
        return item,metadata,dict(base,filename=filename,sha256=digest,bytes=len(packed),changed=True)
    results={};new_parts=dict(reused_parts);records=list(reused_records)
    with ThreadPoolExecutor(max_workers=4) as pool:
        for item,metadata,record in pool.map(process,candidates):
            records.append(record)
            if item:results[item['selector_id'],item['family'],item['resolution']]=item
            new_parts.update({p['filename']:p for p in metadata})
    expected={(m['selector_id'],m['reference'],style,resolution) for m in plan['mappings'] for style in plan['styles'] for resolution in plan['sizes']}
    actual={(r['selector_id'],name,r['style'],r['resolution']) for r in records for name in r['added']+r['retained_existing_exact_references']}
    assert actual==expected and len(actual)==4776
    old_keys={(p['selector_id'],p['family'],p['resolution']) for p in document['packages']}
    for i,p in enumerate(document['packages']):
        key=p['selector_id'],p['family'],p['resolution']
        if key in results: document['packages'][i]=results[key]
        else: assert p==before['packages'][i]
    document['packages'].extend(value for key,value in sorted(results.items()) if key not in old_keys)
    base_provider={(p['selector_id'],p['family'],p['resolution']):p for p in baseline['packages'] if p['selector_id'] in HELPER.PROVIDERS}
    actual_provider={(p['selector_id'],p['family'],p['resolution']):p for p in document['packages'] if p['selector_id'] in HELPER.PROVIDERS}
    assert actual_provider==base_provider,'Provider packages must stay byte-for-byte bound to the original production archives'
    assert [p for p in document['packages'] if p['family']=='channel-transparent']==[p for p in baseline['packages'] if p['family']=='channel-transparent']
    metadata={**parts,**new_parts};needed={u.rsplit('/',1)[-1] for p in document['packages'] for u in p.get('parts',[])}
    document['parts']=[metadata[name] for name in sorted(needed)]
    checks=verify_planners(document,records,source_root)
    document['unchanged622_20261104']={'source_ref':source_ref,'approved_graphic_groups':622,'eligible_exact_references':796,'blocked_references':13,'existing_png_bytes_preserved':True,'transparent_packages_preserved':True,'client_update_needed_for_new_selectors':['345W','500E']}
    manifest.write_text(json.dumps(document,sort_keys=True,indent=2)+'\n')
    sums=DELIVERY/'SHA256SUMS';lines={line.split()[-1]:line.split()[0] for line in sums.read_text().splitlines() if line.strip()}
    lines.update({n:p['sha256'] for n,p in new_parts.items()});lines['manifest.json']=sha(manifest.read_bytes())
    sums.write_text(''.join(digest+'  '+name+'\n' for name,digest in sorted(lines.items())))
    report={'status':'VERIFIED_PUBLICATION_CANDIDATE','date':'2026-11-04','source_ref':source_ref,'previous_manifest_sha256':previous,'manifest_sha256':sha(manifest.read_bytes()),'approved_png_hashes_checked':1244,'eligible_references':796,'verified_programme_mappings':661,'technical_references':135,'blocked_references':plan['excluded'],'changed_packages':sum(r['changed'] for r in records),'scanned_packages':len(records),'new_satellite_packages':12,'reference_style_size_checks':len(actual),'receiver_selective_installer_checks':sum(r['changed'] for r in records),'added_png_entries':sum(len(r['added']) for r in records),'retained_existing_png_entries':sum(len(r['retained_existing_exact_references']) for r in records),'all_existing_png_bytes_preserved':True,'all_transparent_packages_preserved':True,'frozen_master_unchanged':True,'ipk_changed':False,'packages':records,'new_parts':list(new_parts.values()),**checks}
    if routing_repair:report['routing_correction']=routing_repair
    report['all_provider_packages_preserved']=True
    REPORT.parent.mkdir(exist_ok=True);REPORT.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print('COMPLETE',sum(r['changed'] for r in records),'changed packages;',len(actual),'exact reference/style/size decisions;',len(new_parts),'parts',flush=True)

def git(*args,capture=False):
    return subprocess.run(['git',*args],cwd=ROOT,check=True,text=True,stdout=subprocess.PIPE if capture else None).stdout

def bounded_push(branch):
    assert branch==BRANCH
    head=git('rev-parse','HEAD',capture=True).strip()
    for attempt in range(3):
        try:
            result=subprocess.run(['git','push','origin','HEAD:'+branch],cwd=ROOT,timeout=300)
            if result.returncode==0:return
        except subprocess.TimeoutExpired:
            print('Transfer exceeded five minutes; checking remote state before retry',flush=True)
        remote=git('ls-remote','origin','refs/heads/'+branch,capture=True).split()
        if remote and remote[0]==head:return
    raise RuntimeError('Bounded archive transfer failed; retain the last complete production catalogue')


def push_changes():
    report=json.loads(REPORT.read_text());assert report['status']=='VERIFIED_PUBLICATION_CANDIDATE'
    assert report['reference_style_size_checks']==4776
    spec=importlib.util.spec_from_file_location('bounded_push',ROOT/'tools/push-warder-approved11-20261104.py')
    mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
    # PNG ZIP parts are already compressed. Disable expensive binary delta
    # searches and avoid large chunked HTTP requests on a resumed publication.
    for key,value in [('pack.window','0'),('pack.depth','0'),('pack.compression','0'),('core.compression','0'),('http.postBuffer','157286400'),('http.version','HTTP/1.1'),('http.lowSpeedLimit','1024'),('http.lowSpeedTime','120')]:
        git('config',key,value)
    mod.push=bounded_push
    groups=mod.batches(report['new_parts'],128*1024*1024)
    for i,group in enumerate(groups,1):
        paths=[]
        for part in group:
            name='assets/warder/downloads/picons/channels/'+part['filename']
            if (ROOT/name).is_file():paths.append(name)
            else:assert git('ls-files','--error-unmatch','--',name,capture=True).strip()==name
        if paths:mod.commit_files(paths,'Stage approved unchanged picon archive parts %d of %d'%(i,len(groups)),BRANCH)
        print('TRANSFER BATCH',i,'/',len(groups),'complete',flush=True)
    mod.commit_files(['assets/warder/downloads/picons/channels/manifest.json','assets/warder/downloads/picons/channels/SHA256SUMS',str(REPORT.relative_to(ROOT))], 'Activate complete additive unchanged-picon catalogue after all archive parts',BRANCH)

def verify_public(ref):
    report=json.loads(REPORT.read_text());root=PART_ROOT.replace('/main/','/'+ref+'/')
    with ThreadPoolExecutor(max_workers=6) as pool:
        def check(item):
            raw=HELPER.fetch(root+item['filename']);assert len(raw)==item['bytes'] and sha(raw)==item['sha256'];return item['filename']
        verified=list(pool.map(check,report['new_parts']))
    raw=HELPER.fetch(root+'manifest.json');assert sha(raw)==report['manifest_sha256']
    report['public_verification']={'ref':ref,'verified_parts':len(verified),'all_sizes_and_sha256_match':True,'manifest_matches':True}
    REPORT.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print('PUBLIC VERIFIED',len(verified),'parts and manifest',flush=True)

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--source-root',type=Path);parser.add_argument('--source-ref');parser.add_argument('--push',action='store_true');parser.add_argument('--verify-public');parser.add_argument('--repair-routing',action='store_true')
    args=parser.parse_args()
    if args.push:push_changes()
    elif args.verify_public:verify_public(args.verify_public)
    else:publish(args.source_root,args.source_ref,args.repair_routing)
