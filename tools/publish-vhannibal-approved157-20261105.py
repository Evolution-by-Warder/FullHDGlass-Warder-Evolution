#!/usr/bin/env python3
"""Install exact approved Warder artwork; copy CANAL and unrelated bytes intact."""
from pathlib import Path
from zipfile import ZipFile,ZipInfo,ZIP_DEFLATED
from collections import Counter
import argparse,copy,hashlib,io,json,urllib.request,concurrent.futures,sys,importlib.util
from PIL import Image
sha=lambda b:hashlib.sha256(b).hexdigest()
blobsha=lambda b:hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
def ref(n):
 p=Path(n).stem.split('_')
 if len(p)!=10:return None
 try:return '_'.join(f'{int(x,16):X}' for x in p)
 except ValueError:return None
def ident(r):return tuple(r.split('_')[3:7])
def fetch(url):
 for i in range(4):
  try:
   with urllib.request.urlopen(url,timeout=120) as r:return r.read()
  except Exception:
   if i==3:raise

def run(root,inputs,caches,write=True):
 plan=json.loads((inputs/'publication-plan.json').read_text());data=root/'assets/warder/downloads/picons/channels';mf=data/'manifest.json';rawmf=mf.read_bytes();assert sha(rawmf)==plan['base_manifest_sha256'];before=json.loads(rawmf);doc=copy.deepcopy(before);parts={p['filename']:p for p in doc['parts']}
 arts={a['slug']:a for a in plan['artwork']};rows=plan['mappings'];byid={ident(r['reference']):r for r in rows};assert len(byid)==len(rows)==175
 assets=inputs/'assets';assets.mkdir(exist_ok=True)
 def asset_get(item):
  file,o=item;p=assets/file
  if p.exists():assert sha(p.read_bytes())==o['sha256'];return
  b=fetch('https://raw.githubusercontent.com/Evolution-by-Warder/PiconHub-Warder-Evolution/'+plan['source_ref']+'/'+o['source_path']);assert sha(b)==o['sha256'];p.write_bytes(b)
 with concurrent.futures.ThreadPoolExecutor(max_workers=12) as pool:list(pool.map(asset_get,[(o['file'],o) for a in arts.values() for o in a['outputs'].values()]))
 # Each approved graphic/size/background is materialized once and reused.
 rendered={}
 for a in arts.values():
  for style,o in a['outputs'].items():
   b=(assets/o['file']).read_bytes();assert sha(b)==o['sha256']
   with Image.open(io.BytesIO(b)) as im:
    assert im.size==(220,132) and im.mode in ('RGBA','P')
    for res in ('220x132','50x30','400x240'):
     if res=='220x132':v=b
     else:
      image=im.convert('RGBA').convert('RGBa').resize(tuple(map(int,res.split('x'))),Image.Resampling.LANCZOS).convert('RGBA');out=io.BytesIO();image.save(out,format='PNG');v=out.getvalue()
     expected=o.get('derived_sha256',{}).get(res)
     if expected:assert sha(v)==expected,('Size derivative mismatch',a['slug'],style,res)
     rendered[(a['slug'],style,res)]=v
 meta={p['filename']:p for p in before['parts']};selectors={'08W','130E','192E','ANTIKSAT','DIGI_TELLY','FREESAT','SKYLINK'};packages=[p for p in before['packages'] if p['selector_id'] in selectors];urls={u for p in packages for u in p['parts']};cache=caches[0];cache.mkdir(parents=True,exist_ok=True)
 def get(u):
  name=u.rsplit('/',1)[-1];spec=meta[name]
  for folder in caches:
   path=folder/name
   if path.exists() and path.stat().st_size==spec['bytes'] and sha(path.read_bytes())==spec['sha256']:return
  b=fetch(u.replace('/main/','/'+plan['catalogue_commit']+'/'));assert len(b)==spec['bytes'] and sha(b)==spec['sha256'];(cache/name).write_bytes(b)
 with concurrent.futures.ThreadPoolExecutor(max_workers=12) as pool:
  for i,_ in enumerate(pool.map(get,sorted(urls)),1):
   if i%40==0:print('FETCH',i,len(urls),flush=True)
 def part(u):
  n=u.rsplit('/',1)[-1]
  for c in caches:
   p=c/n
   if p.exists() and sha(p.read_bytes())==meta[n]['sha256']:return p.read_bytes()
  raise FileNotFoundError(n)
 report=[];newmeta=[];gitproof={};guardplan=[];reused_bytes=0;changedkeys=set()
 for number,p in enumerate(packages,1):
  style=p['family'].removeprefix('channel-');res=p['resolution'];original_parts=[part(u) for u in p['parts']];raw=b''.join(original_parts);assert sha(raw)==p['sha256'] and len(raw)==p['bytes']
  with ZipFile(io.BytesIO(raw)) as z:
   assert z.testzip() is None;assert len(z.namelist())==len(set(z.namelist()));members={ref(n):n for n in z.namelist() if n.endswith('.png') and ref(n)};assert len(members)==p['png_count'];changes={};proofrows={};oldhashes={}
   for r,n in members.items():
    row=byid.get(ident(r))
    if not row:continue
    if '/' not in p['warder_key'] and p['warder_key']!=row['position']:continue
    b=rendered[(row['slug'],style,res)]
    if z.read(n)!=b:changes[n]=b;oldhashes[n]=sha(z.read(n));proofrows[n]=row
   for row in rows:
    own=p['selector_id'] in ('08W','130E','192E') and p['warder_key']==row['position'];provider=p['selector_id']=='DIGI_TELLY' and any(b.endswith('dbe78.tv') for b in row['bouquets'])
    n=row['reference']+'.png'
    if (own or provider) and row['reference'] not in members:changes[n]=rendered[(row['slug'],style,res)];proofrows[n]=row
   if not changes:print('UNCHANGED',p['selector_id'],res,style,flush=True);continue
   # Keep original compressed local records. Replace central-directory entries
   # and append only approved payloads, avoiding recompression of old graphics.
   output=io.BytesIO(raw)
   with ZipFile(output,'a') as out:
    out.filelist=[copy.copy(info) for info in out.filelist if info.filename not in changes];out.NameToInfo={info.filename:info for info in out.filelist}
    for n,b in sorted(changes.items()):
     info=ZipInfo(n,(2026,11,5,0,0,0));info.compress_type=ZIP_DEFLATED;info.external_attr=0o100644<<16;out.writestr(info,b,compresslevel=9)
   packed=output.getvalue()
   with ZipFile(io.BytesIO(packed)) as verify:
    assert verify.testzip() is None;assert len(verify.namelist())==len(set(verify.namelist()));assert set(verify.namelist())==set(z.namelist())|set(changes)
    for n in z.namelist():assert verify.read(n)==changes.get(n,z.read(n)),n
    for n,b in changes.items():assert verify.read(n)==b
   digest=sha(packed);filename='warder-'+p['selector_id'].lower()+'-'+res+'-'+style+'-'+digest[:16]+'.zip';prefix=p['parts'][0].rsplit('/',1)[0]+'/';chunks=[];offset=0
   for old in original_parts:
    if offset+len(old)>z.start_dir:break
    assert packed[offset:offset+len(old)]==old;chunks.append(old);offset+=len(old);reused_bytes+=len(old)
   chunks.extend(packed[start:start+4*1024*1024] for start in range(offset,len(packed),4*1024*1024));urls=[]
   for i,b in enumerate(chunks):
    name=filename+'.part%02d'%i;urls.append(prefix+name);newmeta.append({'filename':name,'bytes':len(b),'sha256':sha(b)});gitproof[name]=blobsha(b)
    if write:(data/name).write_bytes(b)
   q=next(q for q in doc['packages'] if q['filename']==p['filename']);q.update(filename=filename,sha256=digest,bytes=len(packed),parts=urls,png_count=len(members)+sum(ref(n) not in members for n in changes))
   if 'included_references' in q:q['included_references']=sorted(set(members)|{ref(n) for n in changes})
   q['vhannibal_approved157_20261105']={'source_ref':plan['source_ref'],'approved_graphics_used':len(set(r['slug'] for r in proofrows.values())),'replaced':len(oldhashes),'added':len(changes)-len(oldhashes),'approval':'OWNER_APPROVED_EXACT_220X132_PNGS_WITH_STANDARD_SIZE_DERIVATIVES'}
   records=[]
   for n,b in sorted(changes.items()):
    row=proofrows[n];record={'member':n,'reference':ref(n),'station':row['name'],'slug':row['slug'],'before_sha256':oldhashes.get(n),'sha256':sha(b),'operation':'REPLACE' if n in oldhashes else 'ADD'};records.append(record);guardplan.append({'path':'packages/'+p['selector_id']+'/'+n,'reference':ref(n),'position':row['position'],'station_names':[row['name']],'selector_id':p['selector_id']})
   report.append({'selector':p['selector_id'],'resolution':res,'family':p['family'],'before_archive_sha256':p['sha256'],'archive_sha256':digest,'replaced':len(oldhashes),'added':len(changes)-len(oldhashes),'unrelated_preserved':len(z.namelist())-len(oldhashes),'changes':records});changedkeys.add((p['selector_id'],res,p['family']));print('PATCHED',number,len(packages),p['selector_id'],res,style,len(oldhashes),len(changes)-len(oldhashes),flush=True)
  if plan.get('checkpoint_script'):
   import subprocess
   subprocess.run(['python3',plan['checkpoint_script']],check=True)
 # Preflight uses the pinned canonical-protection evidence, including full NS.
 guardroot=inputs/'guard';spec=importlib.util.spec_from_file_location('guard',guardroot/'guard.py');guard=importlib.util.module_from_spec(spec);spec.loader.exec_module(guard);decisions=guard.validate_plan(guardplan);assert all(r['allowed'] for r in decisions),[r for r in decisions if not r['allowed']][:3]
 for a,b in zip(before['packages'],doc['packages']):
  if (a['selector_id'],a['resolution'],a['family']) not in changedkeys:assert a==b
 assert [p for p in before['packages'] if p['selector_id'] in ('CANALPLUS_SK','CANALPLUS_CZ')]==[p for p in doc['packages'] if p['selector_id'] in ('CANALPLUS_SK','CANALPLUS_CZ')]
 referenced={u.rsplit('/',1)[-1] for p in doc['packages'] for u in p['parts']};doc['parts']=sorted([x for x in before['parts']+newmeta if x['filename'] in referenced],key=lambda x:x['filename']);assert len(set(x['filename'] for x in doc['parts']))==len(doc['parts'])
 summary={'approved_graphics_accounted_for':157,'graphics_previously_satisfied_by_canal':11,'graphics_published_from_approved_pngs':138,'graphics_reused_from_existing_master':8,'exact_current_references':175,'changed_packages':len(report),'replaced_png_entries':sum(r['replaced'] for r in report),'added_png_entries':sum(r['added'] for r in report),'unrelated_archive_entries_preserved':sum(r['unrelated_preserved'] for r in report),'original_archive_prefix_bytes_reused':reused_bytes,'canonical_source_packages_preserved':18,'held_new_references':0,'master_source_ref':plan['source_ref'],'changes':report}
 doc['vhannibal_approved157_20261105']={k:v for k,v in summary.items() if k!='changes'}
 if plan.get('expected_verification_sha256'):assert sha((json.dumps(summary,ensure_ascii=False,indent=2)+'\n').encode())==plan['expected_verification_sha256'],'Verification differs from locally tested archives'
 (inputs/'verification.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n');(inputs/'part-git-shas.json').write_text(json.dumps(gitproof,sort_keys=True,indent=2)+'\n')
 if write:
  final_bytes=(json.dumps(doc,ensure_ascii=False,sort_keys=True,indent=2)+'\n').encode()
  if plan.get('expected_manifest_sha256'):assert sha(final_bytes)==plan['expected_manifest_sha256'],'Manifest differs from locally verified catalogue'
  mf.write_bytes(final_bytes);sums=data/'SHA256SUMS';values={l.split()[-1]:l.split()[0] for l in sums.read_text().splitlines() if l.strip()};values.update({x['filename']:x['sha256'] for x in newmeta});values['manifest.json']=sha(mf.read_bytes());sums.write_text(''.join(h+'  '+n+'\n' for n,h in sorted(values.items())))
 print('COMPLETE',json.dumps({k:v for k,v in summary.items() if k!='changes'}),flush=True)
if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('--root',type=Path,required=True);a.add_argument('--inputs',type=Path,required=True);a.add_argument('--cache',type=Path,action='append',required=True);v=a.parse_args();run(v.root,v.inputs,v.cache)
