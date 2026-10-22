#!/usr/bin/env python3
"""Publish the approved 15 PNG bytes as three new 45W 400x240 packages."""
import copy,hashlib,io,importlib.util,json,os,struct,urllib.request,zipfile
from pathlib import Path
R=Path.cwd();D=R/'assets/warder/downloads/picons/channels';REF=os.environ['APPROVED_45W_REF'];SOURCE='https://raw.githubusercontent.com/Evolution-by-Warder/PiconHub-Warder-Evolution/'+REF+'/migration/45w-400x240-review-20261022/'
sha=lambda b:hashlib.sha256(b).hexdigest()
def get(url):
 with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Warder-approved-45W-publication'}),timeout=90) as r:return r.read()
proof=json.loads(get(SOURCE+'review.json'));assert proof['status']=='approved' and len(proof['files'])==15
approved={p['path']:p['sha256'] for p in proof['files']};payloads={};new={};rows=[]
for style in ['transparent','white','black']:
 data=get(SOURCE+'warder-45w-400x240-'+style+'-review.zip');digest=sha(data);name='warder-450w-400x240-'+style+'-'+digest[:16]+'.zip';part=name+'.part00'
 with zipfile.ZipFile(io.BytesIO(data)) as z:
  names=z.namelist();assert len(names)==5 and len(set(names))==5
  for n in names:
   assert '/' not in n and n.endswith('.png');b=z.read(n);assert sha(b)==approved['400x240/'+style+'/'+n]
   assert b[:8]==b'\x89PNG\r\n\x1a\n' and struct.unpack('>II',b[16:24])==(400,240)
 payloads[part]=data;new[style]={'filename':name,'part':part,'bytes':len(data),'sha256':digest,'png_count':5};rows.append(dict(style=style,**new[style]))
S=R/'source/package-root/usr/lib/enigma2/python/Plugins/Extensions/setupGlass17/warderPiconSync.py';spec=importlib.util.spec_from_file_location('actual_receiver_planner',S);sync=importlib.util.module_from_spec(spec);spec.loader.exec_module(sync)
for suffix in ['','test-candidate']:
 path=D/suffix/'manifest.json';doc=json.loads(path.read_text());before=copy.deepcopy(doc['packages']);assert not any(p['selector_id']=='450W' and p['resolution']=='400x240' for p in before)
 branch='main' if not suffix else 'warder-modernization-work';root='https://raw.githubusercontent.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/'+branch+'/'+str((D/suffix).relative_to(R))+'/'
 for style,meta in new.items():
  template=next(p for p in before if p['selector_id']=='450W' and p['resolution']=='220x132' and p['family']=='channel-'+style);p=copy.deepcopy(template)
  p.update(filename=meta['filename'],bytes=meta['bytes'],sha256=meta['sha256'],png_count=5,resolution='400x240',parts=[root+meta['part']],kind='satellite',orbital_position='45.0w',source_repository='Evolution-by-Warder/PiconHub-Warder-Evolution',source_ref=REF)
  p.pop('url',None);p['approved_resampling']={'source_resolution':'220x132','target_resolution':'400x240','method':'premultiplied-alpha LANCZOS','source_png_count':5,'approved_source_ref':REF};doc['packages'].append(p)
  (D/suffix/meta['part']).write_bytes(payloads[meta['part']])
 assert doc['packages'][:len(before)]==before
 parts={p['filename']:p for p in doc['parts']};parts.update({name:{'filename':name,'bytes':len(b),'sha256':sha(b)} for name,b in payloads.items()});doc['parts']=[parts[n] for n in sorted(parts)]
 doc['approved_45w_400x240_source']={'repository':'Evolution-by-Warder/PiconHub-Warder-Evolution','ref':REF,'png_count':15,'styles':['transparent','white','black'],'source_220x132_preserved':True}
 manifest_url=root+'manifest.json';sync.PUBLICATION_SOURCES['verify-45w']={'manifest_url':manifest_url,'package_root':root};errors=sync.validate_publication_manifest(doc,manifest_url);assert not errors,errors
 for size in ['220x132','400x240']:
  for style in ['transparent','white','black']:
   prefs=sync.set_task_position_bindings(sync.default_preferences(),[sync.task_binding_for_package_selector('450W')]);prefs.update(resolution=size,style=style,update_mode=sync.UPDATE_MODE_INCREMENTAL)
   queue=sync.build_runtime_queue(prefs,publication={'persistent':True,'manifest_url':manifest_url});plan=sync.plan_runtime_packages(doc,queue,manifest_url);assert plan['state']=='ready',plan
   jobs=sync.build_download_jobs(doc,plan,manifest_url);assert jobs['state']=='ready' and len(jobs['jobs'])==1,jobs
 path.write_text(json.dumps(doc,indent=2,sort_keys=True)+'\n');sums=D/suffix/'SHA256SUMS';lines={x.split()[-1]:x.split()[0] for x in sums.read_text().splitlines() if x.strip()};lines.update({n:sha(b) for n,b in payloads.items()});lines['manifest.json']=sha(path.read_bytes());sums.write_text(''.join(d+'  '+n+'\n' for n,d in sorted(lines.items())))
report={'source_ref':REF,'approved_pngs':15,'packages':rows,'existing_220x132_and_all_other_packages_unchanged':True,'receiver_download_plans_passed':12,'new_ipk_required':False,'current_ipk':'1.0.15'}
p=R/'reports/approved-45w-400x240-20261022.json';p.parent.mkdir(exist_ok=True);p.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
