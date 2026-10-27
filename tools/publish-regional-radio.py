#!/usr/bin/env python3
"""Publish approved Fun/Melody/Regina assets without altering unrelated PNGs."""
import argparse,copy,importlib.util,io,json,os,re,struct,time,zipfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path,PurePosixPath
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('shared_publication',Path(__file__).with_name('append-dab-satellite-picons.py'));shared=importlib.util.module_from_spec(spec);spec.loader.exec_module(shared)
sha=shared.sha;DIRECTORY=shared.DIRECTORY;LIVE_ROOT=shared.LIVE_ROOT;REPO=shared.REPO
PREFIX='picons/radio-refresh-20261027/'
SIZES=('50x30','220x132','400x240');STYLES=('transparent','white','black')
def identity(name):
    p=PurePosixPath(name).name.removesuffix('.png').split('_')
    if len(p)!=10 or p[0]=='4115':return None
    try:return tuple(int(x,16) for x in p[3:6])+(int(p[6],16)>>16,)
    except ValueError:return None

def patch_archive(original,artwork,full_satellite=False):
    byid={identity(n):(n,b) for n,b in artwork.items()}
    if None in byid or len(byid)!=len(artwork) or any(PurePosixPath(n).name!=n or '\\' in n for n in artwork):raise ValueError('Invalid approved identity')
    with zipfile.ZipFile(io.BytesIO(original)) as src:
        names=src.namelist()
        if len(names)!=len(set(names)):raise ValueError('Duplicate member')
        if any(PurePosixPath(n).name!=n or '\\' in n or not n.endswith('.png') for n in names):raise ValueError('Unsafe member')
        before={n:sha(src.read(n)) for n in names};replacements={};found=set()
        for n in names:
            item=byid.get(identity(n))
            if item:replacements[n]=item[1];found.add(identity(n))
        for key,(n,b) in byid.items():
            if full_satellite or key in found:replacements.setdefault(n,b)
        changed=[n for n,b in replacements.items() if n in before and sha(b)!=before[n]];added=[n for n in replacements if n not in before]
        report={'replaced':sorted(changed),'added':sorted(added),'matched_unchanged':len(replacements)-len(changed)-len(added),'unrelated_pngs_preserved':len(set(names)-set(replacements)),'dab_pngs_preserved':sum(n.startswith('4115_') for n in names)}
        if not changed and not added:return original,report
        output=io.BytesIO()
        with zipfile.ZipFile(output,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as dst:
            dst.comment=src.comment
            for n in sorted(set(names)|set(replacements)):
                b=replacements[n] if n in replacements else src.read(n);info=zipfile.ZipInfo(n,(1980,1,1,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o100644<<16;dst.writestr(info,b)
    result=output.getvalue()
    with zipfile.ZipFile(io.BytesIO(result)) as dst:
        if len(dst.namelist())!=len(set(dst.namelist())):raise ValueError('Duplicate output')
        for n,h in before.items():
            if sha(dst.read(n))!=(sha(replacements[n]) if n in replacements else h):raise ValueError('Preservation failure: '+n)
        for n,b in replacements.items():
            if dst.read(n)!=b:raise ValueError('Incorrect replacement')
    return result,report

def commit(api,parent,entries,message):
    source=api.api('GET','/git/commits/'+parent);tree=api.api('POST','/git/trees',{'base_tree':source['tree']['sha'],'tree':entries})
    return api.api('POST','/git/commits',{'parents':[parent],'tree':tree['sha'],'message':message})['sha']
def advance(api,old,new):
    if api.api('GET','/git/ref/heads/main')['object']['sha']!=old:raise ValueError('Main advanced; rerun without overwriting changes')
    api.api('PATCH','/git/refs/heads/main',{'sha':new,'force':False})
def text_entry(api,path,value):
    data=(json.dumps(value,ensure_ascii=False,indent=2)+'\n').encode() if not isinstance(value,str) else value.encode()
    return {'path':path,'mode':'100644','type':'blob','sha':api.blob(data)}
def complete_scope(selector,complete_canal_radio=False):
    return selector=='235E' or (complete_canal_radio and selector in ('CANALPLUS_SK','CANALPLUS_CZ'))

def run(source_ref,publish=False,complete_canal_radio=False):
    if not re.fullmatch('[0-9a-f]{40}',source_ref):raise ValueError('Immutable source required')
    api=shared.GitHub(os.environ.get('GITHUB_TOKEN') if publish else None)
    if publish and not api.token:raise ValueError('Workflow token required')
    head=api.api('GET','/git/ref/heads/main')['object']['sha'];root='https://raw.githubusercontent.com/'+REPO+'/'+head+'/'
    original=shared.public(root+DIRECTORY+'manifest.json');doc=json.loads(original);before=copy.deepcopy(doc)
    source='https://raw.githubusercontent.com/'+shared.PICON_REPO+'/'+source_ref+'/'
    plan_raw=shared.public(source+PREFIX+'approval.json');plan=json.loads(plan_raw)
    if plan.get('status')!='owner-authorized' or len(plan['mappings'])!=9 or len(plan['artwork_files'])!=81:raise ValueError('Unexpected approved batch')
    if plan['master_sha256']!={'white':'c6ae4a808a65ffc8e6458336fccbfe4216de1e832ec0a9abf800907f2f783589','black':'61e69f7fc46e340453bf74ccd7af6ac9d8eba9f8e232884659e1ea99f6abf3fe'}:raise ValueError('Master mismatch')
    authorization=None
    if complete_canal_radio:
        authorization=json.loads((ROOT/'design/canal-radio-completion.json').read_text())
        if authorization.get('status')!='owner-authorized' or authorization['source_ref']!=source_ref or set(authorization['selectors'])!={'CANALPLUS_SK','CANALPLUS_CZ'} or set(authorization['references'])!={m['reference'] for m in plan['mappings']}:raise ValueError('Provider radio authorization does not match artwork')
    publication_name='canal-radio' if complete_canal_radio else 'regional-radio'
    def fetch_art(item):
        path,digest=item
        if not path.startswith('artwork/') or '..' in PurePosixPath(path).parts:raise ValueError('Unsafe artwork path')
        raw=shared.public(source+PREFIX+path)
        if sha(raw)!=digest or raw[:8]!=b'\x89PNG\r\n\x1a\n' or struct.unpack('>II',raw[16:24])!=tuple(map(int,path.split('/')[1].split('x'))):raise ValueError('Artwork verification failed')
        return path,raw
    with ThreadPoolExecutor(max_workers=6) as pool:art=dict(pool.map(fetch_art,plan['artwork_files'].items()))
    metadata={p['filename']:p for p in doc['parts']};new_meta={};entries=[];reports=[];updates={}
    selectors=('CANALPLUS_SK','CANALPLUS_CZ') if complete_canal_radio else ('235E','SKYLINK','CANALPLUS_SK','CANALPLUS_CZ')
    candidates=[p for p in doc['packages'] if p['selector_id'] in selectors and p['resolution'] in SIZES]
    if len(candidates)!=(18 if complete_canal_radio else 30):raise ValueError('Unexpected number of authorized archives')
    for package in candidates:
        style=package['family'].removeprefix('channel-');size=package['resolution']
        if style not in STYLES:raise ValueError('Unsupported style')
        def download(url):
            if not url.startswith(LIVE_ROOT) or '/' in url[len(LIVE_ROOT):]:raise ValueError('Untrusted part URL')
            name=url.rsplit('/',1)[-1];raw=shared.public(root+DIRECTORY+name);meta=metadata[name]
            if len(raw)!=meta['bytes'] or sha(raw)!=meta['sha256']:raise ValueError('Original part checksum failed')
            return raw
        with ThreadPoolExecutor(max_workers=4) as pool:raw=b''.join(pool.map(download,package['parts']))
        if len(raw)!=package['bytes'] or sha(raw)!=package['sha256']:raise ValueError('Original ZIP checksum failed')
        outputs={m['reference']:art[m['artwork'][size][style]['path'].removeprefix(PREFIX)] for m in plan['mappings']}
        result,report=patch_archive(raw,outputs,complete_scope(package['selector_id'],complete_canal_radio));report.update(selector=package['selector_id'],resolution=size,style=style,before_sha256=package['sha256'])
        if result==raw:print('UNCHANGED',package['selector_id'],size,style,flush=True);continue
        digest=sha(result);filename='warder-'+package['selector_id'].lower().replace('_','-')+'-'+size+'-'+style+'-'+digest[:16]+'.zip';parts=[];blobs=[]
        for i,offset in enumerate(range(0,len(result),16*1024*1024)):
            data=result[offset:offset+16*1024*1024];name=filename+'.part%02d'%i;new_meta[name]={'filename':name,'bytes':len(data),'sha256':sha(data)};parts.append(LIVE_ROOT+name);blobs.append((name,data))
        def upload(item):
            name,data=item;return {'path':DIRECTORY+name,'mode':'100644','type':'blob','sha':api.blob(data) if publish else shared.git_sha(data)}
        with ThreadPoolExecutor(max_workers=3) as pool:entries.extend(pool.map(upload,blobs))
        item=copy.deepcopy(package);item.update(filename=filename,sha256=digest,bytes=len(result),parts=parts,png_count=package['png_count']+len(report['added']),source_repository=shared.PICON_REPO,source_ref=source_ref)
        if 'included_references' in item:item['included_references']=sorted(set(item['included_references'])|{n.removesuffix('.png') for n in report['added']})
        item['approved_canal_radio_completion' if complete_canal_radio else 'approved_regional_radio']={'source_ref':source_ref,'replaced':len(report['replaced']),'added':len(report['added']),'unrelated_pngs_preserved':report['unrelated_pngs_preserved']}
        updates[(package['selector_id'],size,package['family'])]=item;report.update(sha256=digest,bytes=len(result));reports.append(report)
        print('VERIFIED',package['selector_id'],size,style,len(report['replaced']),'replaced',len(report['added']),'added',report['unrelated_pngs_preserved'],'unrelated preserved',flush=True)
    if not updates:print('All regional radio picons are current.');return
    for i,p in enumerate(doc['packages']):
        key=(p['selector_id'],p['resolution'],p['family'])
        if key in updates:doc['packages'][i]=updates[key]
        elif p!=before['packages'][i]:raise ValueError('Unrelated metadata changed')
    metadata.update(new_meta);needed={u.rsplit('/',1)[-1] for p in doc['packages'] for u in p.get('parts',[])};doc['parts']=[metadata[n] for n in sorted(needed)]
    doc['approved_canal_radio_completion_20261027' if complete_canal_radio else 'approved_regional_radio_20261027']={'repository':shared.PICON_REPO,'ref':source_ref,'approval_sha256':sha(plan_raw),'station_references':9,'artwork_files':81,'package_count':len(updates),'unrelated_pngs_preserved':True}
    spec=importlib.util.spec_from_file_location('receiver_sync',ROOT/'source/package-root/usr/lib/enigma2/python/Plugins/Extensions/setupGlass17/warderPiconSync.py');sync=importlib.util.module_from_spec(spec);spec.loader.exec_module(sync)
    if sync.validate_publication_manifest(doc):raise ValueError('Receiver rejects catalogue')
    checks=0
    for sel,size,family in updates:
        binding=sync.task_binding_for_package_selector(sel)
        if not binding:
            if sel!='SKYLINK':raise ValueError('Missing binding')
            continue
        prefs=sync.set_task_position_bindings(sync.default_preferences(),[binding]);prefs.update(resolution=size,style=family.removeprefix('channel-'),update_mode=sync.UPDATE_MODE_INCREMENTAL)
        queue=sync.build_runtime_queue(prefs,publication=sync.runtime_publication());jobs=sync.build_download_jobs(doc,sync.plan_runtime_packages(doc,queue))
        if jobs['state']!='ready' or len(jobs['jobs'])!=1:raise ValueError('Receiver planning failed')
        checks+=1
    report={'schema':1,'source_ref':source_ref,'base_skin_commit':head,'base_manifest_sha256':sha(original),'artwork_files':81,'packages':reports,'receiver_plan_checks':checks,'ipk_changed':False,'unrelated_pngs_preserved':True,'original_dab_preserved':True}
    if authorization:report['provider_radio_authorization']=authorization
    if not publish:Path('/tmp/'+publication_name+'-report.json').write_text(json.dumps(report,indent=2)+'\n');return
    staged=commit(api,head,entries+[text_entry(api,'assets/warder/'+publication_name+'-staging.json',report)],'Stage verified regional Fun, Melody and Regina radio picons');advance(api,head,staged)
    def verify_public(item):
        name,meta=item
        for attempt in range(5):
            try:
                raw=shared.public(LIVE_ROOT+name)
                if len(raw)!=meta['bytes'] or sha(raw)!=meta['sha256']:raise ValueError('Public part differs')
                return
            except Exception:
                if attempt==4:raise
                time.sleep(2)
    with ThreadPoolExecutor(max_workers=4) as pool:list(pool.map(verify_public,new_meta.items()))
    report.update(public_parts_verified=len(new_meta),public_part_sha256_verified=True)
    sums=''.join(p['sha256']+'  '+p['filename']+'\n' for p in sorted(doc['packages'],key=lambda p:p['filename']))
    activated=commit(api,staged,[text_entry(api,DIRECTORY+'manifest.json',doc),text_entry(api,DIRECTORY+'SHA256SUMS',sums),text_entry(api,'assets/warder/'+publication_name+'-publication.json',report)],'Activate approved regional radio picons for PiconHub and FullHDGlass');advance(api,staged,activated)
    work=api.api('GET','/git/ref/heads/warder-modernization-work')['object']['sha']
    if work in (head,os.environ.get('EXPECTED_WORK_HEAD')):api.api('PATCH','/git/refs/heads/warder-modernization-work',{'sha':activated,'force':False})
    print('LIVE REGIONAL RADIO:',activated,len(updates),'packages;',checks,'receiver plans;',len(new_meta),'public parts verified',flush=True)
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--source',required=True);p.add_argument('--publish',action='store_true');p.add_argument('--complete-canal-radio',action='store_true');a=p.parse_args();run(a.source,a.publish,a.complete_canal_radio)
