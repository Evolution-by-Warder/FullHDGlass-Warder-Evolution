from pathlib import Path
from zipfile import ZipFile,ZipInfo,ZIP_DEFLATED
from concurrent.futures import ThreadPoolExecutor
from collections import defaultdict
import json,hashlib,io,copy,urllib.request,importlib.util,sys,os
from PIL import Image
sha=lambda b:hashlib.sha256(b).hexdigest()
blob=lambda b:hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
def run(B,root):
 cfg=json.load(open(B/'config.json'));rows=json.load(open(B/'resolved-plans.json'));assets=json.load(open(B/'asset-index.json'));data=root/'assets/warder/downloads/picons/channels';data.mkdir(parents=True,exist_ok=True);original=(B/'before-manifest.json').read_bytes();mf=data/'manifest.json'
 if mf.exists():assert mf.read_bytes()==original
 m=json.loads(original);doc=copy.deepcopy(m);meta={x['filename']:x for x in m['parts']};cache=B/'cache';cache.mkdir(exist_ok=True);folders=[Path(p)for p in cfg.get('local_caches',[])]+[cache];url='https://raw.githubusercontent.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/'+cfg['live_base']+'/assets/warder/downloads/picons/channels/';paths={}
 def get(n):
  spec=meta[n]
  for d in folders:
   p=d/n
   if p.exists() and p.stat().st_size==spec['bytes'] and sha(p.read_bytes())==spec['sha256']:paths[n]=p;return
  for attempt in range(4):
   try:v=urllib.request.urlopen(url+n,timeout=90).read();assert len(v)==spec['bytes'] and sha(v)==spec['sha256'];p=cache/n;p.write_bytes(v);paths[n]=p;return
   except Exception:
    if attempt==3:raise
 positions={r['selector'] for r in rows};providers={'ANTIKSAT','DIGI_TELLY','FREESAT','SKYLINK'};packages=[p for p in m['packages'] if p['selector_id'] in positions|providers];names={u.rsplit('/',1)[-1]for p in packages for u in p['parts']}
 with ThreadPoolExecutor(max_workers=10)as pool:
  for i,_ in enumerate(pool.map(get,sorted(names)),1):
   if i%100==0:print('INPUT_PARTS',i,len(names),flush=True)
 def arc(p):
  v=b''.join(paths[u.rsplit('/',1)[-1]].read_bytes()for u in p['parts']);assert sha(v)==p['sha256'];z=ZipFile(io.BytesIO(v));assert z.testzip()is None;assert len(z.namelist())==len(set(z.namelist()));return v,z
 updates=[];newparts=[];proof={};plan=[];coverage=defaultdict(set)
 for p in packages:
  raw,z=arc(p)
  with z:
   members={Path(n).stem:n for n in z.namelist()if n.lower().endswith('.png')};selected=[r for r in rows if (p['selector_id']==r['selector'] or (p['selector_id']in providers and r['reference']in members))];changes={};details=[]
   for r in selected:
    ref=r['reference'];n=members.get(ref,ref+'.png');asset=assets[r['asset_key']][p['resolution']+'|'+p['family']];v=(B/'assets'/asset['file']).read_bytes();assert sha(v)==asset['sha256'];before=z.read(n)if ref in members else None
    if before==v:
     coverage[ref].add((p['selector_id'],p['resolution'],p['family']));continue
    changes[n]=v;details.append({'reference':ref,'name':r['name'],'asset':r['asset_key'],'member':n,'before_sha256':sha(before)if before is not None else None,'sha256':sha(v)});coverage[ref].add((p['selector_id'],p['resolution'],p['family']));plan.append({'path':'packages/'+p['selector_id']+'/'+n,'selector_id':p['selector_id'],'reference':ref,'position':r['position'],'station_names':[r['name']],'content_sha256':sha(v),'resolution':p['resolution'],'family':p['family']})
   if not changes:continue
   output=io.BytesIO(raw)
   with ZipFile(output,'a')as out:
    out.filelist=[copy.copy(i)for i in out.filelist if i.filename not in changes];out.NameToInfo={i.filename:i for i in out.filelist};out.start_dir=len(raw)
    for n,v in sorted(changes.items()):
     info=ZipInfo(n,(2026,11,5,0,0,0));info.compress_type=ZIP_DEFLATED;info.external_attr=0o100644<<16;out.writestr(info,v,compresslevel=9)
   packed=output.getvalue()
   with ZipFile(io.BytesIO(packed))as test:
    assert test.testzip()is None and len(test.namelist())==len(set(test.namelist()));assert set(test.namelist())==set(z.namelist())|set(changes)
    for n in z.namelist():assert test.read(n)==changes.get(n,z.read(n))
    for n,v in changes.items():assert test.read(n)==v
   digest=sha(packed);filename='warder-'+p['selector_id'].lower()+'-'+p['resolution']+'-'+p['family'].removeprefix('channel-')+'-'+digest[:16]+'.zip';chunks=[];off=0
   for u in p['parts']:
    v=paths[u.rsplit('/',1)[-1]].read_bytes();assert packed[off:off+len(v)]==v;chunks.append((v,True));off+=len(v)
   chunks.extend((packed[i:i+4*1024*1024],False)for i in range(off,len(packed),4*1024*1024));urls=[]
   for i,(v,reuse)in enumerate(chunks):
    n=filename+'.part%02d'%i;urls.append(p['parts'][0].rsplit('/',1)[0]+'/'+n);newparts.append({'filename':n,'bytes':len(v),'sha256':sha(v)});proof[n]=blob(v)
    if not reuse:(data/n).write_bytes(v)
   q=next(x for x in doc['packages']if x['filename']==p['filename']);q.update(filename=filename,parts=urls,bytes=len(packed),sha256=digest,png_count=len(members)+sum(d['before_sha256']is None for d in details));q['identity_resolutions_20261105']={'case_refs':[d['reference']for d in details],'report':'reports/vhannibal-six-resolutions-20261105/resolutions.json'}
   if 'included_references'in q:q['included_references']=sorted(set(members)|{d['reference']for d in details})
   updates.append({'selector':p['selector_id'],'resolution':p['resolution'],'family':p['family'],'archive_sha256':digest,'before_archive_sha256':p['sha256'],'added':sum(d['before_sha256']is None for d in details),'replaced':sum(d['before_sha256']is not None for d in details),'unrelated_preserved':len(z.namelist())-sum(d['before_sha256']is not None for d in details),'changes':details});print('VERIFIED_PACKAGE',p['selector_id'],p['resolution'],p['family'],len(details),flush=True)
 for r in rows:assert {(r['selector'],size,f)for size in ('50x30','220x132','400x240')for f in ('channel-transparent','channel-white','channel-black')}<=coverage[r['reference']]
 gdir=B/'guard';s=importlib.util.spec_from_file_location('guard',gdir/'guard.py');g=importlib.util.module_from_spec(s);s.loader.exec_module(g);decisions=g.validate_plan(plan);assert all(x['allowed']for x in decisions),[x for x in decisions if not x['allowed']]
 assert [p for p in doc['packages']if p['selector_id']in ('CANALPLUS_SK','CANALPLUS_CZ')]==[p for p in m['packages']if p['selector_id']in ('CANALPLUS_SK','CANALPLUS_CZ')]
 used={u.rsplit('/',1)[-1]for p in doc['packages']for u in p['parts']};doc['parts']=sorted([x for x in m['parts']+newparts if x['filename']in used],key=lambda x:x['filename']);assert len({x['filename']for x in doc['parts']})==len(doc['parts'])
 summary={'status':'FIVE_NAMED_STATIONS_RESOLVED_ONE_DATA_SERVICE_EXCLUDED','new_current_references':5,'existing_same_programme_reference_corrected':1,'accepted_current_references':12508,'terminal_reference_exceptions':193,'named_cases_closed':6,'packages_changed':len(updates),'added_png_entries':sum(x['added']for x in updates),'corrected_png_entries':sum(x['replaced']for x in updates),'canonical_canal_packages_preserved':18,'changes':updates,'full_position_reference_coverage':{r:len(v)for r,v in coverage.items()}}
 doc['vhannibal_identity_resolutions_20261105']={k:v for k,v in summary.items()if k not in ('changes','full_position_reference_coverage')};raw=(json.dumps(doc,ensure_ascii=False,sort_keys=True,indent=2)+'\n').encode()
 if cfg.get('expected_manifest_sha256'):assert sha(raw)==cfg['expected_manifest_sha256']
 mf.write_bytes(raw);values={l.split()[-1]:l.split()[0]for l in (B/'before-SHA256SUMS').read_text().splitlines()if l.strip()};values.update({x['filename']:x['sha256']for x in newparts});values['manifest.json']=sha(raw);(data/'SHA256SUMS').write_text(''.join(h+'  '+n+'\n'for n,h in sorted(values.items())))
 (B/'live-verification.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n');(B/'part-git-shas.json').write_text(json.dumps(proof,indent=2)+'\n');print('IDENTITY_LIVE_COMPLETE',json.dumps({k:v for k,v in summary.items()if k not in ('changes','full_position_reference_coverage')}),sha(raw),flush=True)
if __name__=='__main__':run(Path(sys.argv[1]),Path(sys.argv[2]))
