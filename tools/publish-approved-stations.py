#!/usr/bin/env python3
"""Publish exact approved PNGs and proportional sizes; preserve all other logos."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import copy,hashlib,importlib.util,io,json,os,urllib.request,zipfile
from PIL import Image
R=Path.cwd();D=R/'assets/warder/downloads/picons/channels';REF=os.environ['APPROVED_PICON_REF'];BASE=f'https://raw.githubusercontent.com/Evolution-by-Warder/PiconHub-Warder-Evolution/{REF}/migration/approved-new-stations-20261022/'
sha=lambda b:hashlib.sha256(b).hexdigest()
def get(u):
 for attempt in range(3):
  try:
   with urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'Warder-approved-station-publication'}),timeout=150) as r:return r.read()
  except Exception:
   if attempt==2:raise
plan=json.loads(get(BASE+'approval.json'));assert plan['status']=='approved' and len(plan['artwork_files'])==36
art={}
def fetch(kv):
 path,digest=kv;b=get(BASE+'artwork/'+path);assert sha(b)==digest;im=Image.open(io.BytesIO(b));assert im.size==(220,132) and im.mode=='RGBA';return path,b
with ThreadPoolExecutor(8) as ex:art.update(ex.map(fetch,plan['artwork_files'].items()))
def slug(name):return name.lower().replace('+','plus').replace(' ','-')
def rendered(station,style,size):
 b=art[f'220x132/{style}/{slug(station)}.png']
 if size=='220x132':return b
 im=Image.open(io.BytesIO(b)).convert('RGBA').convert('RGBa').resize(tuple(map(int,size.split('x'))),Image.Resampling.LANCZOS).convert('RGBA');out=io.BytesIO();im.save(out,format='PNG');return out.getvalue()
def identity(name):return tuple(name.split('_')[3:])
def selector(m):return str(abs(m['position_tenths']))+('E' if m['position_tenths']>0 else 'W')
mappings={}
for m in plan['mappings']:mappings.setdefault(selector(m),[]).append(m)
docs={s:json.loads((D/s/'manifest.json').read_text()) for s in ['','test-candidate']};before=copy.deepcopy(docs);updates={};payloads={};reports=[]
for p in docs['']['packages']:
 key=(p['selector_id'],p['resolution'],p['family'])
 if p['selector_id'] not in mappings or p['resolution'] not in ['50x30','220x132','400x240']:continue
 style=p['family'].removeprefix('channel-');assert style in ['transparent','white','black']
 data=b''.join(get(u) for u in p['parts']);assert len(data)==p['bytes'] and sha(data)==p['sha256']
 src=zipfile.ZipFile(io.BytesIO(data));names=src.namelist();assert len(names)==len(set(names)) and all('/' not in n and n.endswith('.png') for n in names)
 replacements={};by_id={identity(m['reference']):m for m in mappings[p['selector_id']]}
 for n in names:
  m=by_id.get(identity(n))
  if m:replacements[n]=rendered(m['station'],style,p['resolution'])
 for m in mappings[p['selector_id']]:replacements[m['reference']]=rendered(m['station'],style,p['resolution'])
 output=io.BytesIO();preserved={};replaced=[];added=[]
 with zipfile.ZipFile(output,'w',zipfile.ZIP_DEFLATED,6) as dst:
  for n in sorted(set(names)|set(replacements)):
   old=src.read(n) if n in names else None;b=replacements.get(n,old)
   if n not in replacements:preserved[n]=sha(b)
   elif old is None:added.append(n)
   elif b!=old:replaced.append(n)
   zi=zipfile.ZipInfo(n,(2026,10,22,0,0,0));zi.compress_type=zipfile.ZIP_DEFLATED;zi.external_attr=0o100644<<16;dst.writestr(zi,b)
 packed=output.getvalue()
 with zipfile.ZipFile(io.BytesIO(packed)) as z:
  assert all(sha(z.read(n))==h for n,h in preserved.items());assert all(z.read(n)==b for n,b in replacements.items())
 digest=sha(packed);filename=f'warder-{p["selector_id"].lower()}-{p["resolution"]}-{style}-{digest[:16]}.zip';parts=[]
 for i,start in enumerate(range(0,len(packed),16*1024*1024)):
  n=filename+f'.part{i:02d}';payloads[n]=packed[start:start+16*1024*1024];parts.append(n)
 item=copy.deepcopy(p);item.update(filename=filename,bytes=len(packed),sha256=digest,png_count=len(set(names)|set(replacements)),source_repository='Evolution-by-Warder/PiconHub-Warder-Evolution',source_ref=REF)
 item.pop('url',None);item.pop('included_references',None);item['approved_station_refresh']={'source_ref':REF,'replaced':len(replaced),'added':len(added),'unrelated_preserved':len(preserved)};updates[key]=(item,parts)
 reports.append({'selector_id':key[0],'resolution':key[1],'style':style,'replaced':replaced,'added':added,'unchanged_unrelated_pngs':len(preserved),'sha256':digest,'bytes':len(packed)})
 print('VERIFIED',key,'replaced',len(replaced),'added',len(added),'preserved',len(preserved),flush=True)
assert len(updates)>=18
for suffix,doc in docs.items():
 branch='main' if not suffix else 'warder-modernization-work';root=f'https://raw.githubusercontent.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/{branch}/'+str((D/suffix).relative_to(R))+'/'
 for i,p in enumerate(doc['packages']):
  key=(p['selector_id'],p['resolution'],p['family'])
  if key in updates:
   item,parts=updates[key];item=copy.deepcopy(item);item['parts']=[root+n for n in parts];doc['packages'][i]=item
  else:assert p==before[suffix]['packages'][i]
 meta={x['filename']:x for x in doc['parts']};meta.update({n:{'filename':n,'bytes':len(b),'sha256':sha(b)} for n,b in payloads.items()});needed={u.rsplit('/',1)[-1] for p in doc['packages'] for u in p.get('parts',[])};assert needed<=set(meta);doc['parts']=[meta[n] for n in sorted(needed)]
 doc['approved_station_refresh_20261022']={'source_ref':REF,'station_count':12,'package_count':len(updates),'approved_png_count':36,'unrelated_artwork_unchanged':True}
 for n,b in payloads.items():(D/suffix/n).write_bytes(b)
 (D/suffix/'manifest.json').write_text(json.dumps(doc,indent=2,sort_keys=True)+'\n')
 sums=D/suffix/'SHA256SUMS';lines={x.split()[-1]:x.split()[0] for x in sums.read_text().splitlines() if x.strip()};lines.update({n:sha(b) for n,b in payloads.items()});lines['manifest.json']=sha((D/suffix/'manifest.json').read_bytes());sums.write_text(''.join(h+'  '+n+'\n' for n,h in sorted(lines.items())))
spec=importlib.util.spec_from_file_location('receiver_sync',R/'source/package-root/usr/lib/enigma2/python/Plugins/Extensions/setupGlass17/warderPiconSync.py');sync=importlib.util.module_from_spec(spec);spec.loader.exec_module(sync)
checks=0
for suffix,doc in docs.items():
 branch='main' if not suffix else 'warder-modernization-work';root=f'https://raw.githubusercontent.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/{branch}/'+str((D/suffix).relative_to(R))+'/'
 url=root+'manifest.json';sync.PUBLICATION_SOURCES['approved-refresh']={'manifest_url':url,'package_root':root};assert not sync.validate_publication_manifest(doc,url)
 for sel,size,family in updates:
  prefs=sync.set_task_position_bindings(sync.default_preferences(),[sync.task_binding_for_package_selector(sel)]);prefs.update(resolution=size,style=family.removeprefix('channel-'),update_mode=sync.UPDATE_MODE_INCREMENTAL)
  queue=sync.build_runtime_queue(prefs,publication={'persistent':True,'manifest_url':url});jobs=sync.build_download_jobs(doc,sync.plan_runtime_packages(doc,queue,url),url);assert jobs['state']=='ready' and len(jobs['jobs'])==1;checks+=1
report={'source_ref':REF,'approved_station_count':12,'approved_png_count':36,'packages':reports,'package_count':len(updates),'unrelated_artwork_unchanged':True,'receiver_planner_checks':checks,'ipk_changed':False,'current_ipk':'1.0.15'}
(R/'reports').mkdir(exist_ok=True);(R/'reports/approved-stations-publication-20261022.json').write_text(json.dumps(report,indent=2)+'\n');print('DONE',len(updates),'packages',checks,'receiver plans',flush=True)
