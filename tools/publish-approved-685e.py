#!/usr/bin/env python3
"""Append approved SRP artwork to 68.5E packages; preserve every old PNG."""
import copy,hashlib,io,json,os,struct,urllib.request,zipfile
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
ROOT=Path.cwd();D=ROOT/'assets/warder/downloads/picons/channels';SOURCE_REF=os.environ['APPROVED_PICON_REF'];SOURCE='https://raw.githubusercontent.com/Evolution-by-Warder/PiconHub-Warder-Evolution/'+SOURCE_REF+'/migration/gioppygio/68.5e-approved-20261022/'
sha=lambda b:hashlib.sha256(b).hexdigest()
def download(url):
 req=urllib.request.Request(url,headers={'User-Agent':'Warder-approved-picon-publication'})
 with urllib.request.urlopen(req,timeout=120) as response:return response.read()
def archive_pngs(p):
 urls=p.get('parts') or [p['url']];data=b''.join(download(x if isinstance(x,str) else x['url']) for x in urls)
 assert len(data)==p['bytes'] and sha(data)==p['sha256']
 with zipfile.ZipFile(io.BytesIO(data)) as z:
  names=z.namelist();assert len(names)==len(set(names));assert all('/' not in n and n.lower().endswith('.png') for n in names)
  return {n:z.read(n) for n in names}
def pack(files):
 o=io.BytesIO()
 with zipfile.ZipFile(o,'w',zipfile.ZIP_DEFLATED,9) as z:
  for name,b in sorted(files.items()):
   i=zipfile.ZipInfo(name,(2026,10,22,0,0,0));i.compress_type=zipfile.ZIP_DEFLATED;i.create_system=3;i.external_attr=0o100644<<16;z.writestr(i,b)
 return o.getvalue()
plan=json.loads(download(SOURCE+'approval.json'));assert len(plan['artwork_files'])==552 and len(plan['mappings'])==66
manifests={suffix:json.loads((D/suffix/'manifest.json').read_text()) for suffix in ['','test-candidate']};main=manifests[''];existing={(p['resolution'],p['family'].removeprefix('channel-')):p for p in main['packages'] if p['selector_id']=='685E'}
rows=[];updates={};payloads={};approved_cache={}
def get_art(k):
 size,style,name=k;rel=f'{size}/{style}/{name}.png';b=download(SOURCE+'artwork/'+rel);assert sha(b)==plan['artwork_files'][rel];assert b[:8]==b'\x89PNG\r\n\x1a\n' and struct.unpack('>II',b[16:24])==tuple(map(int,size.split('x')));return k,b
for size in ['220x132','400x240']:
 for style in ['transparent','white','black']:
  key=(size,style);old=existing.get(key);baseline=archive_pngs(old) if old else {};files=dict(baseline)
  needed=[(size,style,m['artwork']) for m in plan['mappings'] if m['reference'] not in files]
  needed=sorted(set(needed))
  with ThreadPoolExecutor(max_workers=8) as ex:
   for k,b in ex.map(get_art,needed):approved_cache[k]=b
  for m in plan['mappings']:
   if m['reference'] not in files:files[m['reference']]=approved_cache[(size,style,m['artwork'])]
  assert all(files[n]==b for n,b in baseline.items());assert all(m['reference'] in files for m in plan['mappings'])
  for name,b in files.items():assert b[:8]==b'\x89PNG\r\n\x1a\n' and struct.unpack('>II',b[16:24])==tuple(map(int,size.split('x')))
  added=len(files)-len(baseline);row={'resolution':size,'style':style,'existing_pngs_preserved':len(baseline),'added_pngs':added,'png_count':len(files),'all_original_png_bytes_unchanged':True};rows.append(row)
  if old and not added:continue
  data=pack(files)
  with zipfile.ZipFile(io.BytesIO(data)) as z:assert {n:z.read(n) for n in z.namelist()}==files
  filename=f'warder-685e-{size}-{style}-{sha(data)[:16]}.zip';chunks=[data[i:i+4*1024*1024] for i in range(0,len(data),4*1024*1024)];partnames=[filename+'.part%02d'%i for i in range(len(chunks))]
  for n,b in zip(partnames,chunks):payloads[n]=b
  item=copy.deepcopy(old or existing[(size,'white')]);item.update(filename=filename,bytes=len(data),sha256=sha(data),png_count=len(files),selector_id='685E',family='channel-'+style,resolution=size,warder_key='68.5e',source_repository='Evolution-by-Warder/PiconHub-Warder-Evolution',source_ref=SOURCE_REF)
  item.pop('url',None);item.pop('included_references',None);item['approved_gioppygio_append']={'source_ref':SOURCE_REF,'added':added,'preserved':len(baseline),'mapped_artworks':64,'mapped_references':66}
  updates[key]=(item,partnames)
for suffix,doc in manifests.items():
 branch='main' if not suffix else 'warder-modernization-work'
 other_before=[p for p in doc['packages'] if p['selector_id']!='685E'];pending=copy.deepcopy(updates);result=[]
 for p in doc['packages']:
  key=(p.get('resolution'),p.get('family','').removeprefix('channel-'))
  if p['selector_id']=='685E' and key in pending:item,names=pending.pop(key)
  else:result.append(p);continue
  item['parts']=['https://raw.githubusercontent.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/'+branch+'/'+str((D/suffix/n).relative_to(ROOT)) for n in names];result.append(item)
 for key,(item,names) in pending.items():
  item['parts']=['https://raw.githubusercontent.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/'+branch+'/'+str((D/suffix/n).relative_to(ROOT)) for n in names];result.append(item)
 doc['packages']=result
 referenced={u.rsplit('/',1)[-1] for p in result for u in p.get('parts',[])}
 metadata={p['filename']:p for p in doc['parts']}
 metadata.update({n:{'filename':n,'bytes':len(b),'sha256':sha(b)} for n,b in payloads.items()})
 assert referenced<=set(metadata)
 doc['parts']=[metadata[n] for n in sorted(referenced)]
 assert [p for p in result if p['selector_id']!='685E']==other_before
 doc['approved_gioppygio_685e_source']={'repository':'Evolution-by-Warder/PiconHub-Warder-Evolution','ref':SOURCE_REF,'approved_artworks':92,'mapped_artworks':64,'mapped_references':66,'unmapped_artwork':plan['unmapped_artwork'],'append_only':True}
 (D/suffix/'manifest.json').write_text(json.dumps(doc,indent=2,sort_keys=True)+'\n')
 for name,b in payloads.items():(D/suffix/name).write_bytes(b)
 sums=D/suffix/'SHA256SUMS';lines={line.split()[-1]:line.split()[0] for line in sums.read_text().splitlines() if line.strip()};lines.update({n:sha(b) for n,b in payloads.items()});lines['manifest.json']=sha((D/suffix/'manifest.json').read_bytes());sums.write_text(''.join(h+'  '+n+'\n' for n,h in sorted(lines.items())))
 # Check new package URLs resolve to precisely the staged bytes, including test-candidate.
 for p in doc['packages']:
  if p['selector_id']=='685E' and (p['resolution'],p['family'].removeprefix('channel-')) in updates:
   joined=b''.join((D/suffix/u.rsplit('/',1)[-1]).read_bytes() for u in p['parts']);assert sha(joined)==p['sha256'] and len(joined)==p['bytes']
# Run the installed receiver planner, rather than a separate imitation validator.
import importlib.util
sync_path=ROOT/'source/package-root/usr/lib/enigma2/python/Plugins/Extensions/setupGlass17/warderPiconSync.py'
spec=importlib.util.spec_from_file_location('warder_receiver_sync',sync_path);sync=importlib.util.module_from_spec(spec);spec.loader.exec_module(sync)
for suffix,doc in manifests.items():
 branch='main' if not suffix else 'warder-modernization-work';root='https://raw.githubusercontent.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/'+branch+'/'+str((D/suffix).relative_to(ROOT))+'/'
 manifest_url=root+'manifest.json';sync.PUBLICATION_SOURCES['ci-approved-685e']={'manifest_url':manifest_url,'package_root':root}
 errors=sync.validate_publication_manifest(doc,manifest_url);assert not errors,errors
 for size in ['220x132','400x240']:
  for style in ['transparent','white','black']:
   prefs=sync.set_task_position_bindings(sync.default_preferences(),[sync.task_binding_for_package_selector('685E')]);prefs.update(resolution=size,style=style,update_mode=sync.UPDATE_MODE_INCREMENTAL)
   queue=sync.build_runtime_queue(prefs,publication={'persistent':True,'manifest_url':manifest_url})
   planned=sync.plan_runtime_packages(doc,queue,manifest_url);assert planned['state']=='ready',planned
   jobs=sync.build_download_jobs(doc,planned,manifest_url);assert jobs['state']=='ready' and len(jobs['jobs'])==1,jobs
   assert jobs['jobs'][0]['selector_id']=='685E'
report={'source_ref':SOURCE_REF,'packages':rows,'all_other_packages_unchanged':True,'protected_positions_16e_and_235e_unchanged':True,'approved_artworks':92,'mapped_artworks':64,'mapped_references':66,'unmapped_artwork':plan['unmapped_artwork'],'receiver_planner_checks_passed':12,'new_ipk_required':False,'new_payload_parts':list(payloads)}
(ROOT/'reports').mkdir(exist_ok=True);(ROOT/'reports/gioppygio-685e-publication-20261022.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
