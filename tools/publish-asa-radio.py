#!/usr/bin/env python3
"""Append authenticated ASA DE picons to the shared full-23.5E catalog."""
import argparse, importlib.util, json, os, re, struct, time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('shared',Path(__file__).with_name('append-dab-satellite-picons.py'))
shared=importlib.util.module_from_spec(spec);spec.loader.exec_module(shared)
sha=shared.sha;DIRECTORY=shared.DIRECTORY;LIVE_ROOT=shared.LIVE_ROOT;REPO=shared.REPO

def commit(api,parent,entries,message):
    old=api.api('GET','/git/commits/'+parent)
    tree=api.api('POST','/git/trees',{'base_tree':old['tree']['sha'],'tree':entries})
    return api.api('POST','/git/commits',{'parents':[parent],'tree':tree['sha'],'message':message})['sha']
def advance(api,parent,revision):
    if api.api('GET','/git/ref/heads/main')['object']['sha']!=parent:raise ValueError('Main advanced; rerun against the new manifest')
    api.api('PATCH','/git/refs/heads/main',{'sha':revision,'force':False})
def entry(api,path,value):
    raw=value.encode() if isinstance(value,str) else (json.dumps(value,ensure_ascii=False,indent=2)+'\n').encode()
    return {'path':path,'mode':'100644','type':'blob','sha':api.blob(raw)}

def run(source_ref,publish=False):
    if not re.fullmatch('[0-9a-f]{40}',source_ref):raise ValueError('Immutable source required')
    api=shared.GitHub(os.environ.get('GITHUB_TOKEN') if publish else None)
    if publish and not api.token:raise ValueError('Workflow token required')
    head=api.api('GET','/git/ref/heads/main')['object']['sha']
    root='https://raw.githubusercontent.com/'+REPO+'/'+head+'/'
    original=shared.public(root+DIRECTORY+'manifest.json');doc=json.loads(original)
    prefix='https://raw.githubusercontent.com/'+shared.PICON_REPO+'/'+source_ref+'/'
    plan_raw=shared.public(prefix+'picons/DAB/asa/approval.json');plan=json.loads(plan_raw)
    expected={'4115_0_2_1019_C98_3_EB0000_1019_10C4_10BC.png','4115_0_2_1019_5_85_C00000_1019_10C4_10BC.png'}
    if plan.get('status')!='owner-authorized' or set(plan['references'])!=expected:raise ValueError('ASA authorization mismatch')
    if plan['source_sha256']!='3c4d930cb58e2b56f04a41c00dbed6dacc83a8ba6707dd42878b3602c2c3e0f8':raise ValueError('Unexpected official logo')
    art={}
    for size,styles in plan['artwork'].items():
        if size not in ('50x30','220x132','400x240') or set(styles)!={'transparent','white','black'}:raise ValueError('Unsupported variant')
        for style,item in styles.items():
            if item['path']!='picons/DAB/asa/artwork/'+size+'/'+style+'/asa-de.png':raise ValueError('Unexpected source path')
            b=shared.public(prefix+item['path'])
            if len(b)!=item['bytes'] or sha(b)!=item['sha256'] or b[:8]!=b'\x89PNG\r\n\x1a\n' or struct.unpack('>II',b[16:24])!=tuple(map(int,size.split('x'))):raise ValueError('ASA PNG integrity failure')
            art[size,style]=b
    selectors={'235E'}
    if plan.get('satellite_selectors')!=['235E']:raise ValueError('ASA is authorized only for standalone DAB and full 23.5E')
    packages=[p for p in doc['packages'] if p['selector_id'] in selectors]
    if {p['selector_id'] for p in packages}!=selectors:raise ValueError('Missing satellite/provider group')
    metadata={p['filename']:p for p in doc['parts']};new_meta={};entries=[];reports=[];updates=[];removed=set()
    for p in packages:
        sel=p['selector_id'];size=p['resolution'];style=p['family'].removeprefix('channel-')
        image=art[size,style];orbital=235
        additions={n:image for n in expected if shared.position(n)==orbital}
        if len(additions)!=1:raise ValueError('Incorrect orbital reference')
        def download(url):
            if not url.startswith(LIVE_ROOT) or '/' in url[len(LIVE_ROOT):]:raise ValueError('Untrusted native URL')
            name=url.rsplit('/',1)[-1];b=shared.public(root+DIRECTORY+name);m=metadata[name]
            if len(b)!=m['bytes'] or sha(b)!=m['sha256']:raise ValueError('Native part checksum failed')
            return b
        with ThreadPoolExecutor(max_workers=4) as pool:raw=b''.join(pool.map(download,p['parts']))
        if len(raw)!=p['bytes'] or sha(raw)!=p['sha256']:raise ValueError('Native archive checksum failed')
        data,added,preserved=shared.append_archive(raw,additions)
        report={'selector':sel,'resolution':size,'style':style,'added':added,'preserved':preserved,'before_sha256':p['sha256']}
        if not added:
            print('PRESENT',sel,size,style,flush=True);reports.append(report);continue
        digest=sha(data);filename='warder-'+sel.lower().replace('_','-')+'-'+size+'-'+style+'-'+digest[:16]+'.zip';urls=[]
        for index,offset in enumerate(range(0,len(data),16*1024*1024)):
            part=data[offset:offset+16*1024*1024];name=filename+'.part%02d'%index
            new_meta[name]={'filename':name,'bytes':len(part),'sha256':sha(part)}
            entries.append({'path':DIRECTORY+name,'mode':'100644','type':'blob','sha':api.blob(part) if publish else shared.git_sha(part)})
            urls.append(LIVE_ROOT+name)
        removed.update(url.rsplit('/',1)[-1] for url in p['parts'])
        p.update(filename=filename,bytes=len(data),sha256=digest,parts=urls,png_count=p['png_count']+added,approved_asa_de={'source_commit':source_ref,'approval_sha256':sha(plan_raw),'added':added,'preserved':preserved})
        report.update(sha256=digest,bytes=len(data));reports.append(report);updates.append(p)
        print('APPENDED',sel,size,style,'preserved',preserved,flush=True)
    if not updates:print('All applicable ASA references are already present.');return
    doc['parts']=sorted([p for p in doc['parts'] if p['filename'] not in removed]+list(new_meta.values()),key=lambda p:p['filename'])
    doc['approved_asa_de_20261027']={'repository':shared.PICON_REPO,'ref':source_ref,'approval_sha256':sha(plan_raw),'packages':len(updates),'unrelated_pngs_preserved':True}
    spec=importlib.util.spec_from_file_location('sync',ROOT/'source/package-root/usr/lib/enigma2/python/Plugins/Extensions/setupGlass17/warderPiconSync.py')
    sync=importlib.util.module_from_spec(spec);spec.loader.exec_module(sync)
    if sync.validate_publication_manifest(doc):raise ValueError('Receiver rejects manifest')
    checks=0
    for p in updates:
        binding=sync.task_binding_for_package_selector(p['selector_id'])
        if not binding:
            if p['selector_id']!='SKYLINK':raise ValueError('Missing receiver binding')
            continue
        prefs=sync.set_task_position_bindings(sync.default_preferences(),[binding]);prefs.update(resolution=p['resolution'],style=p['family'].removeprefix('channel-'),update_mode=sync.UPDATE_MODE_INCREMENTAL)
        queue=sync.build_runtime_queue(prefs,publication=sync.runtime_publication());jobs=sync.build_download_jobs(doc,sync.plan_runtime_packages(doc,queue))
        if jobs['state']!='ready' or len(jobs['jobs'])!=1:raise ValueError('Receiver planning failure')
        checks+=1
    report={'schema':1,'source_commit':source_ref,'baseline_skin_commit':head,'packages':reports,'receiver_plan_checks':checks,'ipk_changed':False,'unrelated_pngs_preserved':True}
    if not publish:Path('/tmp/asa-radio-report.json').write_text(json.dumps(report,indent=2)+'\n');return
    staged=commit(api,head,entries+[entry(api,'assets/warder/asa-radio-staging.json',report)],'Stage official ASA DE in every applicable satellite and Canal+ package');advance(api,head,staged)
    def verify(item):
        name,meta=item
        for attempt in range(5):
            try:
                b=shared.public('https://raw.githubusercontent.com/'+REPO+'/'+staged+'/'+DIRECTORY+name)
                if len(b)!=meta['bytes'] or sha(b)!=meta['sha256']:raise ValueError('Public part checksum failed')
                return
            except Exception:
                if attempt==4:raise
                time.sleep(2)
    with ThreadPoolExecutor(max_workers=4) as pool:list(pool.map(verify,new_meta.items()))
    report.update(public_parts_verified=len(new_meta),public_part_sha256_verified=True)
    sums=''.join(p['sha256']+'  '+p['filename']+'\n' for p in sorted(doc['packages'],key=lambda p:p['filename']))
    live=commit(api,staged,[entry(api,DIRECTORY+'manifest.json',doc),entry(api,DIRECTORY+'SHA256SUMS',sums),entry(api,'assets/warder/asa-radio-publication.json',report)],'Activate verified ASA DE for the shared PiconHub and FullHDGlass catalog');advance(api,staged,live)
    print('LIVE ASA DE:',live,len(updates),'packages;',checks,'receiver plans;',len(new_meta),'public parts verified',flush=True)
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--source',required=True);p.add_argument('--publish',action='store_true');a=p.parse_args();run(a.source,a.publish)
