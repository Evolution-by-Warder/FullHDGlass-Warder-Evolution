#!/usr/bin/env python3
"""Reuse approved CANAL bytes using a reviewed service/market map; never render."""
from pathlib import Path
from collections import Counter,defaultdict
from zipfile import ZipFile,ZIP_DEFLATED,ZipInfo
import json,hashlib,io,urllib.request,concurrent.futures,copy,argparse
sha=lambda b:hashlib.sha256(b).hexdigest()
def ident(r):return tuple(r.split('_')[3:7])
def ref(n):
 p=Path(n).stem.split('_')
 if len(p)!=10:return None
 try:return '_'.join(f'{int(x,16):X}' for x in p)
 except ValueError:return None

def run(root,inputs,cache,write):
 data=root/'assets/warder/downloads/picons/channels'; mf=data/'manifest.json'
 before=json.loads(mf.read_text()); plan=json.loads((inputs/'reuse-map.json').read_text())
 assert sha(mf.read_bytes())==plan['manifest_sha256'],'Live catalogue changed; rebase and re-audit required'
 doc=copy.deepcopy(before);meta={x['filename']:x for x in before['parts']}
 candidates=plan['candidates'];byid={}
 for c in candidates:
  key=ident(c['reference']);assert key not in byid,('Ambiguous current service',key);byid[key]=c
 canonical_packages=[p for p in before['packages'] if p['selector_id'] in ('CANALPLUS_SK','CANALPLUS_CZ')]
 targets=[p for p in before['packages'] if p['selector_id'] in plan['target_selectors']]
 urls={u for p in canonical_packages+targets for u in p['parts']};cache.mkdir(parents=True,exist_ok=True)
 def download(u):
  name=u.rsplit('/',1)[-1];p=cache/name;s=meta[name]
  if p.exists() and p.stat().st_size==s['bytes'] and sha(p.read_bytes())==s['sha256']:return
  for attempt in range(4):
   try:
    with urllib.request.urlopen(u.replace('/main/','/'+plan['catalogue_commit']+'/'),timeout=120) as r:b=r.read()
    assert len(b)==s['bytes'] and sha(b)==s['sha256'],name;p.write_bytes(b);return
   except Exception:
    if attempt==3:raise
 with concurrent.futures.ThreadPoolExecutor(max_workers=12) as pool:
  for i,_ in enumerate(pool.map(download,sorted(urls)),1):
   if i%50==0:print('DOWNLOAD',i,len(urls),flush=True)
 def archive(p):
  raw=b''.join((cache/u.rsplit('/',1)[-1]).read_bytes() for u in p['parts'])
  assert len(raw)==p['bytes'] and sha(raw)==p['sha256'],p['filename']
  z=ZipFile(io.BytesIO(raw));assert z.testzip() is None;assert len(z.namelist())==len(set(z.namelist()));return z
 canonical={};source_meta={}
 for p in canonical_packages:
  v=(p['resolution'],p['family']);bucket=canonical.setdefault(v,{})
  with archive(p) as z:
   for n in z.namelist():
    r=ref(n)
    if not r or not n.endswith('.png'):continue
    b=z.read(n)
    if r in bucket:assert bucket[r]==b,('CANAL market source conflict',v,r)
    bucket[r]=b;source_meta[(v,r)]={'package':p['filename'],'member':n,'sha256':sha(b)}
 for c in candidates:
  assert all(c['source_reference'] in canonical[v] for v in canonical),'Incomplete canonical variants'
 changes=[];newparts=[];changedkeys=set();stats=Counter();unrelated=0
 for number,p in enumerate(targets,1):
  v=(p['resolution'],p['family']);samepos=[c for c in candidates if c['position']==p['warder_key']]
  replacements={};additions={};evidence={};oldhashes={}
  with archive(p) as z:
   members={ref(n):n for n in z.namelist() if n.endswith('.png') and ref(n)}
   assert len(members)==sum(n.endswith('.png') and bool(ref(n)) for n in z.namelist()),'Duplicate normalized references'
   assert len(members)==p['png_count'],p['filename']
   for r,n in members.items():
    c=byid.get(ident(r))
    if c is None:continue
    # Full-position sets only reconcile their own position; provider sets use
    # existing membership as independent evidence for provider inclusion.
    if '/' not in p['warder_key'] and c['position']!=p['warder_key']:continue
    b=canonical[v][c['source_reference']];old=z.read(n)
    if old!=b:replacements[n]=b;oldhashes[n]=sha(old);evidence[n]=c
    if c['reference'] not in members:additions[c['reference']+'.png']=b;evidence[c['reference']+'.png']=c
   for c in samepos:
    if c['reference'] not in members:additions[c['reference']+'.png']=canonical[v][c['source_reference']];evidence[c['reference']+'.png']=c
   if not replacements and not additions:
    print('UNCHANGED',p['selector_id'],*v,flush=True);continue
   # All original entry bytes and ZIP metadata remain unchanged unless listed.
   output=io.BytesIO()
   with ZipFile(output,'w') as out:
    out.comment=z.comment
    for info in z.infolist():out.writestr(copy.copy(info),replacements.get(info.filename,z.read(info.filename)))
    for n,b in sorted(additions.items()):
     info=ZipInfo(n,(2026,11,5,0,0,0));info.compress_type=ZIP_DEFLATED;info.external_attr=0o100644<<16;out.writestr(info,b,compresslevel=9)
   raw=output.getvalue()
   with ZipFile(io.BytesIO(raw)) as out:
    assert out.testzip() is None
    assert set(out.namelist())==set(z.namelist())|set(additions)
    for n in z.namelist():
     expected=replacements.get(n,z.read(n));assert out.read(n)==expected,n
     if n not in replacements:unrelated+=1
    for n,b in additions.items():assert out.read(n)==b
    for n in replacements.keys()|additions.keys():
     c=evidence[n];assert sha(out.read(n))==sha(canonical[v][c['source_reference']])
   digest=sha(raw);name='warder-'+p['selector_id'].lower()+'-'+p['resolution']+'-'+p['family'].removeprefix('channel-')+'-'+digest[:16]+'.zip'
   oldname=p['filename'];prefix=p['parts'][0].rsplit('/',1)[0]+'/';urls=[]
   for i,start in enumerate(range(0,len(raw),4*1024*1024)):
    part=name+'.part%02d'%i;b=raw[start:start+4*1024*1024];urls.append(prefix+part);newparts.append({'filename':part,'bytes':len(b),'sha256':sha(b)})
    if write:(data/part).write_bytes(b)
   package=next(q for q in doc['packages'] if q['filename']==oldname)
   package.update(filename=name,sha256=digest,bytes=len(raw),parts=urls,png_count=len(members)+len(additions))
   if 'included_references' in package:package['included_references']=sorted(set(members)|{ref(n) for n in additions})
   package['canal_reuse_20261105']={'source_archive_sha256':{q['selector_id']:q['sha256'] for q in canonical_packages if (q['resolution'],q['family'])==v},'replaced':len(replacements),'added':len(additions),'method':'BYTE_EXACT_COPY_NO_RENDER','mapping':'reports/canal-reuse-20261105/reuse-map.json'}
   rows=[]
   for n,b in sorted({**replacements,**additions}.items()):
    c=evidence[n];rows.append({'member':n,'reference':ref(n),'source_reference':c['source_reference'],'station':c['name'],'position':c['position'],'provider':c['provider'],'identity_evidence':c['identity_evidence'],'before_sha256':oldhashes.get(n),'sha256':sha(b),'operation':'REPLACE' if n in replacements else 'ADD'})
   changes.append({'selector':p['selector_id'],'resolution':v[0],'family':v[1],'before_archive_sha256':p['sha256'],'archive_sha256':digest,'archive_filename':name,'replaced':len(replacements),'added':len(additions),'changes':rows})
   stats['replaced']+=len(replacements);stats['added']+=len(additions);changedkeys.add((p['selector_id'],*v))
   print('REUSED',number,len(targets),p['selector_id'],*v,len(replacements),len(additions),flush=True)
  if write:
   # Release memory and checkpoint immutable parts in Actions before the final
   # catalogue commit. No live ref is modified by these staging commits.
   checkpoint=plan.get('checkpoint_script')
   if checkpoint:
    import subprocess
    subprocess.run(['python3',checkpoint],check=True)
   if plan.get('purge_processed_cache'):
    for u in p['parts']:(cache/u.rsplit('/',1)[-1]).unlink(missing_ok=True)
 doc['canal_reuse_20261105']={'method':'BYTE_EXACT_COPY_NO_RENDER','canonical_catalogue_commit':plan['catalogue_commit'],'canonical_source_repository':'Evolution-by-Warder/PiconHub-Warder-Evolution','canonical_source_ref':'b498c30b11f47f28bbc7a068d5bd671395ca4e8c','master_sync_ref':'ea20b2328333763f0c06c18411c8c5dbe58d2a74','service_settings_sha256':'64d8d143422945679d491d139bca95667ab0a14809ccb4e50adb09f1d55a061c','verification_report':'reports/canal-reuse-20261105/verification.json','replaced_pngs':stats['replaced'],'added_pngs':stats['added'],'held_candidate_services':plan['held_candidate_services']}
 oldcanon=[p for p in before['packages'] if p['selector_id'] in ('CANALPLUS_SK','CANALPLUS_CZ')]
 assert oldcanon==[p for p in doc['packages'] if p['selector_id'] in ('CANALPLUS_SK','CANALPLUS_CZ')]
 for p,q in zip(before['packages'],doc['packages']):
  if (p['selector_id'],p['resolution'],p['family']) not in changedkeys:assert p==q
 # Historical archive files stay immutable; receiver metadata lists only live parts.
 referenced={u.rsplit('/',1)[-1] for p in doc['packages'] for u in p['parts']}
 doc['parts']=sorted([p for p in doc['parts']+newparts if p['filename'] in referenced],key=lambda x:x['filename']);assert len({p['filename'] for p in doc['parts']})==len(doc['parts'])
 report={'canonical_packages_unchanged':len(oldcanon),'rendered_images':0,'changed_packages':len(changes),'changed_selectors':sorted({x['selector'] for x in changes}),'replaced_pngs':stats['replaced'],'added_pngs':stats['added'],'unrelated_original_entries_preserved':unrelated,'held_candidate_services':plan['held_candidate_services'],'changes':changes}
 expected_report=plan.get('expected_verification_sha256')
 if expected_report:assert sha((json.dumps(report,ensure_ascii=False,indent=2)+'\n').encode())==expected_report,'Verification differs from independently tested local run'
 dest=inputs/'verification.json';dest.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
 if write:
  mf.write_text(json.dumps(doc,ensure_ascii=False,sort_keys=True,indent=2)+'\n')
  sums=data/'SHA256SUMS';values={l.split()[-1]:l.split()[0] for l in sums.read_text().splitlines() if l.strip()};values.update({p['filename']:p['sha256'] for p in newparts});values['manifest.json']=sha(mf.read_bytes());sums.write_text(''.join(h+'  '+n+'\n' for n,h in sorted(values.items())))
 print('COMPLETE',json.dumps({k:v for k,v in report.items() if k!='changes'}),flush=True)
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--root',type=Path,required=True);ap.add_argument('--inputs',type=Path,required=True);ap.add_argument('--cache',type=Path,required=True);ap.add_argument('--write',action='store_true');a=ap.parse_args();run(a.root,a.inputs,a.cache,a.write)
