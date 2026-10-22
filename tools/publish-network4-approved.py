#!/usr/bin/env python3
"""Publish the exact user-approved Network4 batch without changing unrelated PNG bytes."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import copy,hashlib,importlib.util,io,json,os,urllib.request,zipfile,threading
from PIL import Image
R=Path.cwd();D=R/'assets/warder/downloads/picons/channels';REF=os.environ['APPROVED_PICON_REF'];PREFIX='migration/network4-approved-20261022';ROOT=f'https://raw.githubusercontent.com/Evolution-by-Warder/PiconHub-Warder-Evolution/{REF}/'
sha=lambda b:hashlib.sha256(b).hexdigest()
def get(u):
 for a in range(3):
  try:
   with urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'Warder-approved-Network4'}),timeout=120) as r:return r.read()
  except Exception:
   if a==2:raise
plan=json.loads(get(ROOT+PREFIX+'/approval.json'));assert plan['status']=='approved' and len(plan['mappings'])==22
art={}
for m in plan['mappings']:
 for style,v in m['artwork'].items():
  path=v.get('path',v.get('existing_path'));b=art.get(path)
  if b is None:
   b=get(ROOT+path)
   if 'sha256' in v:assert sha(b)==v['sha256']
   if 'git_blob_sha' in v:assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==v['git_blob_sha']
   im=Image.open(io.BytesIO(b));assert im.size==(220,132) and im.mode=='RGBA';art[path]=b

def identity(name):
 p=Path(name).name.removesuffix('.png').split('_')
 try:return tuple(int(x,16) for x in p[3:6])+(int(p[6],16)>>16,)
 except:return None

def rendered(m,style,size):
 v=m['artwork'][style];b=art[v.get('path',v.get('existing_path'))]
 if size=='220x132':return b
 im=Image.open(io.BytesIO(b)).convert('RGBA').convert('RGBa').resize(tuple(map(int,size.split('x'))),Image.Resampling.LANCZOS).convert('RGBA');out=io.BytesIO();im.save(out,format='PNG');return out.getvalue()
def satellite(m):return ('08W' if m['position_tenths']==-8 else str(abs(m['position_tenths']))+('E' if m['position_tenths']>0 else 'W'))
docs={s:json.loads((D/s/'manifest.json').read_text()) for s in ['','test-candidate']};before=copy.deepcopy(docs)
def process(p):
 style=p['family'].removeprefix('channel-');size=p['resolution'];sel=p['selector_id'];key=(sel,size,p['family']);assert style in ['transparent','white','black']
 data=b''.join(get(u) for u in p.get('parts',[p.get('url')]));assert len(data)==p['bytes'] and sha(data)==p['sha256'];src=zipfile.ZipFile(io.BytesIO(data));names=src.namelist();assert len(names)==len(set(names));replacements={}
 byid={identity(m['reference']):m for m in plan['mappings'] if style in m['artwork']}
 for n in names:
  m=byid.get(identity(n))
  if m and not(size=='220x132' and m.get('preserve_existing_220')):replacements[n]=rendered(m,style,size)
 for m in byid.values():
  found=any(identity(n)==identity(m['reference']) for n in names)
  if (sel==satellite(m) or found) and m['reference'] not in names:replacements[m['reference']]=rendered(m,style,size)
 replaced=[n for n,b in replacements.items() if n in names and b!=src.read(n)];added=[n for n in replacements if n not in names]
 if not replaced and not added:return None
 packed_io=io.BytesIO();preserved={n:sha(src.read(n)) for n in names if n not in replacements}
 with zipfile.ZipFile(packed_io,'w',zipfile.ZIP_DEFLATED,6) as dst:
  for n in sorted(set(names)|set(replacements)):
   b=replacements[n] if n in replacements else src.read(n);zi=zipfile.ZipInfo(n,(2026,10,22,0,0,0));zi.compress_type=zipfile.ZIP_DEFLATED;zi.external_attr=0o100644<<16;dst.writestr(zi,b)
 packed=packed_io.getvalue()
 with zipfile.ZipFile(io.BytesIO(packed)) as z:
  assert all(sha(z.read(n))==h for n,h in preserved.items());assert all(z.read(n)==b for n,b in replacements.items())
 digest=sha(packed);filename=f'warder-{sel.lower()}-{size}-{style}-{digest[:16]}.zip';parts=[];meta=[]
 for i,start in enumerate(range(0,len(packed),16*1024*1024)):
  n=filename+f'.part{i:02d}';b=packed[start:start+16*1024*1024];parts.append(n);meta.append({'filename':n,'bytes':len(b),'sha256':sha(b)})
  for suffix in docs:(D/suffix/n).write_bytes(b)
 item=copy.deepcopy(p);item.update(filename=filename,bytes=len(packed),sha256=digest,png_count=len(set(names)|set(replacements)),source_repository='Evolution-by-Warder/PiconHub-Warder-Evolution',source_ref=REF);item.pop('url',None)
 if 'included_references' in item:item['included_references']=sorted(Path(n).name.removesuffix('.png') for n in set(names)|set(replacements))
 item['approved_network4_refresh']={'source_ref':REF,'replaced':len(replaced),'added':len(added),'unrelated_preserved':len(preserved)}
 report={'selector_id':sel,'resolution':size,'style':style,'replaced':replaced,'added':added,'unchanged_unrelated_pngs':len(preserved),'sha256':digest,'bytes':len(packed)}
 print('UPDATED',key,len(replaced),'replaced',len(added),'added',flush=True);return key,item,parts,meta,report
updates={};metadata={};reports=[];verified=0
with ThreadPoolExecutor(8) as ex:
 for result in ex.map(process,docs['']['packages']):
  verified+=1
  if result:
   key,item,parts,meta,report=result;updates[key]=(item,parts);metadata.update({x['filename']:x for x in meta});reports.append(report)
  if verified%20==0:print('AUDITED',verified,'archives',flush=True)
assert verified==len(docs['']['packages']) and len(updates)>20
for suffix,doc in docs.items():
 branch='main' if not suffix else 'warder-modernization-work';root=f'https://raw.githubusercontent.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/{branch}/'+str((D/suffix).relative_to(R))+'/'
 for i,p in enumerate(doc['packages']):
  key=(p['selector_id'],p['resolution'],p['family'])
  if key in updates:
   item,parts=updates[key];item=copy.deepcopy(item);item['parts']=[root+n for n in parts];doc['packages'][i]=item
  else:assert p==before[suffix]['packages'][i]
 meta={x['filename']:x for x in doc['parts']};meta.update(metadata);needed={u.rsplit('/',1)[-1] for p in doc['packages'] for u in p.get('parts',[])};assert needed<=set(meta);doc['parts']=[meta[n] for n in sorted(needed)]
 doc['approved_network4_refresh_20261022']={'source_ref':REF,'artwork_count':26,'service_mappings':22,'package_count':len(updates),'correct_cz_sk_220_preserved':True,'unrelated_artwork_unchanged':True}
 (D/suffix/'manifest.json').write_text(json.dumps(doc,indent=2,sort_keys=True)+'\n');sums=D/suffix/'SHA256SUMS';lines={x.split()[-1]:x.split()[0] for x in sums.read_text().splitlines() if x.strip()};lines.update({n:v['sha256'] for n,v in metadata.items()});lines['manifest.json']=sha((D/suffix/'manifest.json').read_bytes());sums.write_text(''.join(h+'  '+n+'\n' for n,h in sorted(lines.items())))
spec=importlib.util.spec_from_file_location('receiver_sync',R/'source/package-root/usr/lib/enigma2/python/Plugins/Extensions/setupGlass17/warderPiconSync.py');sync=importlib.util.module_from_spec(spec);spec.loader.exec_module(sync);checks=0
for suffix,doc in docs.items():
 branch='main' if not suffix else 'warder-modernization-work';root=f'https://raw.githubusercontent.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/{branch}/'+str((D/suffix).relative_to(R))+'/'
 url=root+'manifest.json';sync.PUBLICATION_SOURCES['approved-network4']={'manifest_url':url,'package_root':root};assert not sync.validate_publication_manifest(doc,url)
 for sel,size,family in updates:
  if not any((p['selector_id'],p['resolution'],p['family'])==(sel,size,family) for p in doc['packages']):continue
  binding=sync.task_binding_for_package_selector(sel)
  if not binding:
   assert sel=='SKYLINK',sel
   continue # Retired legacy bundle remains updated, but has no menu binding.
  prefs=sync.set_task_position_bindings(sync.default_preferences(),[binding]);prefs.update(resolution=size,style=family.removeprefix('channel-'),update_mode=sync.UPDATE_MODE_INCREMENTAL);queue=sync.build_runtime_queue(prefs,publication={'persistent':True,'manifest_url':url});jobs=sync.build_download_jobs(doc,sync.plan_runtime_packages(doc,queue,url),url);assert jobs['state']=='ready' and len(jobs['jobs'])==1,(sel,size,family,jobs);checks+=1
report={'source_ref':REF,'approved_png_count':26,'archive_count_verified':verified,'packages':reports,'package_count':len(updates),'unrelated_artwork_unchanged':True,'correct_cz_sk_220_preserved':True,'receiver_planner_checks':checks,'ipk_changed':False}
(R/'reports').mkdir(exist_ok=True);(R/'reports/network4-publication-20261022.json').write_text(json.dumps(report,indent=2)+'\n');print('DONE',len(updates),'packages',checks,'receiver plans',flush=True)

# Approved batch: user confirmed all 26 review PNGs before publication.
