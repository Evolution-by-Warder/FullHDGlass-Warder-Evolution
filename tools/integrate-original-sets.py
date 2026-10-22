#!/usr/bin/env python3
"""Wire supplied original position sets; append only to every existing PNG set."""
import ast,copy,hashlib,importlib.util,io,json,os,re,shutil,stat,struct,subprocess,tempfile,zipfile
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from urllib.request import urlopen
from read_7z import png_files
R=Path(__file__).resolve().parents[1];P=R/'source/package-root/usr/lib/enigma2/python/Plugins/Extensions/setupGlass17';D=R/'assets/warder/downloads/picons/channels';S=R/'.original-sets';BASE='39460b6a644365e0267bf37d410b11c5049ef774'
STYLES=('transparent','white','black');SIZES=('50x30','220x132','400x240');PROVIDERS={'antiksat':'ANTIKSAT','skylink':('CANALPLUS_SK','CANALPLUS_CZ'),'freesat':'FREESAT','digiczsk':'DIGI_TELLY'}
def sha(data):return hashlib.sha256(data).hexdigest()
def logical(name):
 p=name[:-4].split('_');return tuple(int(x,16) for x in p[3:7])
def fetch(package):
 chunks=[]
 for u in package.get('parts') or [package['url']]:
  tail=u.split('/assets/',1)[1];url='https://raw.githubusercontent.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/'+BASE+'/assets/'+tail
  for attempt in range(3):
   try:
    with urlopen(url,timeout=120) as response:b=response.read()
    break
   except Exception:
    if attempt==2:raise
  chunks.append(b)
 data=b''.join(chunks);assert len(data)==package['bytes'] and sha(data)==package['sha256'];return data

def main():
 subprocess.run(['python3',str(R/'tools/patch-original-set-runtime.py')],cwd=R,check=True)
 spec=importlib.util.spec_from_file_location('sync',P/'warderPiconSync.py');sync=importlib.util.module_from_spec(spec);spec.loader.exec_module(sync)
 method=next(n for n in ast.walk(ast.parse((P/'plugin.py').read_bytes())) if isinstance(n,ast.FunctionDef) and n.name=='_warderInstallChannelArchive')
 scope=dict(warderPiconSync=sync,os=os,shutil=shutil,stat=stat,tempfile=tempfile,zipfile=zipfile)
 exec(compile(ast.Module(body=[method],type_ignores=[]),'native-installer','exec'),scope);installer=scope['_warderInstallChannelArchive']
 index=json.loads((S/'index.json').read_text());assert index['source_ref']=='1be99df112e0c22038e98841160d4dd763d5ad70'
 docs={suffix:json.loads((D/suffix/'manifest.json').read_text()) for suffix in ('','test-candidate')};before_docs=copy.deepcopy(docs)
 original_packages={(p['selector_id'],p['family'],p['resolution']):copy.deepcopy(p) for p in docs['']['packages']}
 needed={p['sha256']:p for p in original_packages.values() if p['resolution']=='220x132'}
 with ThreadPoolExecutor(max_workers=5) as pool:downloaded=dict(zip(needed,pool.map(fetch,needed.values())))
 baseline_paths={};cache=R/'.baseline-archives';cache.mkdir(exist_ok=True)
 for digest,data in downloaded.items():
  path=cache/(digest+'.zip');path.write_bytes(data);baseline_paths[digest]=path
 downloaded.clear()
 def read_baseline(key):
  pkg=original_packages.get(key)
  if not pkg or pkg['sha256'] not in baseline_paths:return None
  with zipfile.ZipFile(baseline_paths[pkg['sha256']]) as z:return {n:z.read(n) for n in z.namelist()}
 source={};rejected=[]
 for row in index['records']:
  path=S/row['path'];assert sha(path.read_bytes())==row['sha256'] and path.stat().st_size==row['bytes']
  source[(row['position'],row['style'],row['resolution'])]=row
 def read_source(key):
  row=source.get(key)
  if row is None:return None
  files={};size=tuple(map(int,row['resolution'].split('x')))
  for name,png in png_files(S/row['path']):
   if not sync.safe_archive_member(name) or png[:8]!=b'\x89PNG\r\n\x1a\n' or len(png)<24 or struct.unpack('>II',png[16:24])!=size:
    rejected.append(dict(archive=row['path'],filename=name,reason='wrong-dimensions-or-invalid-reference'));continue
   assert name not in files or files[name]==png,'conflicting duplicate in supplied archive'
   files[name]=png
  assert files,('empty valid source archive',row['path'])
  return files
 legacy_baselines={}
 for row in index['baselines']:
  path=S/row['path'];assert sha(path.read_bytes())==row['sha256']
  files=dict(png_files(path));assert all(struct.unpack('>II',b[16:24])==tuple(map(int,row['resolution'].split('x'))) for b in files.values())
  legacy_baselines[(row['position'],row['style'],row['resolution'])]=files
 positions=sorted({key[0] for key in source if re.fullmatch(r'\d+\.\d+[ew]',key[0])})
 report=[];coverage=[];published={};protected=[]
 for pos in positions:
  selector=sync.selector_id_for_position(pos)
  assert selector and sync.canonical_position_for_selector(selector)==pos,(pos,selector)
  for size in SIZES:
   for style in STYLES:
    incoming=read_source((pos,style,size))
    if incoming is None:continue
    key=(selector,'channel-'+style,size);old_pkg=original_packages.get(key);old=read_baseline(key) or legacy_baselines.get((pos,style,size),{})
    exclusions={e['filename'] for e in (old_pkg or {}).get('ambiguous_exclusions',[])}
    additions={n:b for n,b in incoming.items() if n not in old and n not in exclusions}
    files=dict(old);files.update(additions)
    assert all(files[n]==b for n,b in old.items()),'existing position PNG changed'
    published[key]=publish(docs,key,files,pos,old_pkg,old,additions)
    report.append(dict(position=pos,selector=selector,size=size,style=style,old_png_count=len(old),added_png_count=len(additions),png_count=len(files),preserved_png_count=len(old),all_existing_pngs_unchanged=True,excluded_existing_conflicts=sorted(exclusions),sha256=published[key]['sha256']))
    if pos in ['16.0e','23.5e']:
     protected.append(dict(position=pos,size=size,style=style,existing_png_count=len(old),preserved=True,aggregate_before=sha(b''.join(n.encode()+b'\0'+hashlib.sha256(b).digest() for n,b in sorted(old.items()))),aggregate_after=sha(b''.join(n.encode()+b'\0'+hashlib.sha256(files[n]).digest() for n in sorted(old)))))
    print('PUBLISH',pos,size,style,'old',len(old),'added',len(additions),'total',len(files),flush=True)
    # Validate real installer for all supported source combinations.
    with tempfile.TemporaryDirectory() as temp:
     archive=Path(temp)/'package.zip';dest=Path(temp)/'picon';dest.mkdir();archive.write_bytes(published[key]['payload'])
     keep=next(iter(old)) if old else None
     if keep:(dest/keep).write_bytes(old[keep])
     installed,available=installer(None,str(archive),str(dest),set(additions))
     assert installed==additions.keys() and available==files.keys()
     if keep:assert (dest/keep).read_bytes()==old[keep]
     assert all((dest/n).read_bytes()==b for n,b in additions.items())
    published[key].pop('payload',None)
 for provider,selectors in PROVIDERS.items():
  for selector in ([selectors] if isinstance(selectors,str) else selectors):
   pos=sync.canonical_position_for_selector(selector)
   for style in STYLES:
    old_key=(selector,'channel-'+style,'220x132');approved=read_baseline(old_key)
    if not approved:continue
    # Existing 220x132 provider and country FastScan packages remain byte-identical.
    for size in ['50x30','400x240']:
     pool=read_source((provider,style,size)) or read_source((pos,style,size))
     if not pool:continue
     by_logical={}
     for n,b in sorted(pool.items()):by_logical.setdefault(logical(n),b)
     files={};scaled=[]
     from PIL import Image
     for name,png220 in approved.items():
      png=pool.get(name) or by_logical.get(logical(name))
      if png is None:
       # Reuse the already approved artwork for a missing new FastScan reference.
       im=Image.open(io.BytesIO(png220));im=im.resize(tuple(map(int,size.split('x'))),Image.Resampling.LANCZOS);stream=io.BytesIO();im.save(stream,format='PNG');png=stream.getvalue();scaled.append(name)
      files[name]=png
     key=(selector,'channel-'+style,size)
     published[key]=publish(docs,key,files,pos,None,{},files,provider=True)
     published[key].pop('payload',None)
     report.append(dict(position=pos,selector=selector,size=size,style=style,png_count=len(files),country_reference_membership_preserved=True,scaled_approved_references=scaled,sha256=published[key]['sha256']))
 # Production and test catalogues expose the same newly integrated immutable payloads.
 for suffix,doc in docs.items():
  for old in before_docs[suffix]['packages']:
   key=(old['selector_id'],old['family'],old['resolution'])
   if key not in published:assert old==next(p for p in doc['packages'] if (p['selector_id'],p['family'],p['resolution'])==key)
  assert not sync.validate_publication_manifest(doc,'production' if not suffix else 'test-candidate')
  raw=json.dumps(doc,indent=2,sort_keys=True)+'\n';assert len(raw.encode())<4*1024*1024
  doc['original_supplied_sizes']=dict(source_ref=index['source_ref'],policy='append-only; existing PNG wins',protected_positions=['16.0e','23.5e'],sizes=list(SIZES))
  (D/suffix/'manifest.json').write_text(json.dumps(doc,indent=2,sort_keys=True)+'\n')
 assert protected and all(p['preserved'] and p['aggregate_before']==p['aggregate_after'] for p in protected)
 assert all(p['existing_png_count']>0 for p in protected if p['size']=='220x132')
 # Confirm the download planner binds every offered job to its exact position/size/style.
 for pos in positions:
  selector=sync.selector_id_for_position(pos)
  for size in SIZES:
   for style in STYLES:
    prefs=sync.set_task_position_bindings(sync.default_preferences('/tmp/picon'),[sync.task_binding_for_package_selector(selector)])
    prefs.update(resolution=size,style=style,update_mode=sync.UPDATE_MODE_INCREMENTAL,prepared=True)
    queue=sync.build_runtime_queue(prefs,publication=sync.runtime_publication());planned=sync.plan_runtime_packages(docs[''],queue)
    exists=(selector,'channel-'+style,size) in published
    assert (planned['state']=='ready')==exists,(pos,size,style,planned)
    if exists:assert len(planned['packages'])==1 and planned['packages'][0]['resolution']==size and planned['packages'][0]['family']=='channel-'+style
 allowed={(p['selector_id'],p['resolution'],p['family']) for p in docs['']['packages']}
 for selector in ['ANTIKSAT','CANALPLUS_SK','CANALPLUS_CZ']:
  assert all((selector,size,'channel-'+style) in allowed for size in SIZES for style in STYLES)
 result=dict(source_ref=index['source_ref'],base_ref=BASE,packages=report,protected_positions=protected,rejected_source_pngs=rejected,source_position_count=len(positions),missing_source_combinations=[dict(position=pos,size=size,style=style) for pos in positions for size in SIZES for style in STYLES if (pos,style,size) not in source],no_original_pngs_modified=True,menu_positions_without_supplied_archives=['12.5w','11.0w','3.1e','74.9e','85.0e','85.1e'],existing_native_only_position='45.0w')
 out=R/'reports/original-sets-integration-20261022.json';out.parent.mkdir(exist_ok=True);out.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
 subprocess.run(['python3',str(R/'tools/test-original-set-routing.py')],cwd=R,check=True)
 subprocess.run(['python3',str(R/'tools/test-runtime-safety.py')],cwd=R,check=True)
 subprocess.run(['python3',str(R/'tools/test-live-picon-catalog.py')],cwd=R,check=True)
 subprocess.run(['python3',str(R/'tools/build-release-ipk.py')],cwd=R,check=True)
 ipk=R/'packages/enigma2-skin-fullhdglass17-warder-evolution_1.0.14_all.ipk';digest=sha(ipk.read_bytes())
 for name in ['update.json','update-test.json']:
  path=R/name;doc=json.loads(path.read_text());doc.update(version='1.0.14',sha256=digest,package_url='https://raw.githubusercontent.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/main/packages/'+ipk.name,changelog='Povodne baliky satelitnych piconov 50x30, 220x132 a 400x240 vo vsetkych dostupnych farbach. Zachovane aktualne PNG 16.0E a 23.5E, doplnene iba chybajuce. Zive katalogy bez dalsich IPK pri aktualizacii piconov.');path.write_text(json.dumps(doc,ensure_ascii=False,indent=2)+'\n')
 subprocess.run(['python3',str(R/'tools/verify-radio-release.py')],cwd=R,check=True)
 readme=R/'README.md';text=readme.read_text().replace('Latest approved release: 1.0.13','Latest approved release: 1.0.14').replace('evolution_1.0.13_all.ipk','evolution_1.0.14_all.ipk');readme.write_text(text+'\nRelease 1.0.14 connects the supplied original 50x30, 220x132 and 400x240 position sets through the live catalogue. Existing PNGs take precedence, especially at 16.0E and 23.5E.\n')
 print('PASS: original size sets integrated; existing protected PNGs byte-identical; all routing tests and IPK 1.0.14 verified',flush=True)

def publish(docs,key,files,pos,old_pkg,old,additions,provider=False):
 selector,family,size=key;style=family.removeprefix('channel-')
 if old_pkg and not additions:
  return dict(sha256=old_pkg['sha256'],payload=zip_payload(files))
 data=zip_payload(files);digest=sha(data);filename='warder-'+selector.lower()+'-'+size+'-'+style+'-'+digest[:16]+'.zip'
 for suffix,doc in docs.items():
  directory=D/suffix;branch='main' if not suffix else 'warder-modernization-work';root='https://raw.githubusercontent.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/'+branch+'/'+directory.relative_to(R).as_posix()+'/'
  pkg=next((p for p in doc['packages'] if (p['selector_id'],p['family'],p['resolution'])==key),None)
  if pkg is None:pkg=dict(selector_id=selector,family=family,resolution=size,kind='provider' if provider else 'satellite',orbital_position=pos,warder_key=pos);doc['packages'].append(pkg)
  old_names={u.rsplit('/',1)[-1] for u in pkg.get('parts',[])};records=[];urls=[]
  for n,start in enumerate(range(0,len(data),18*1024*1024)):
   name=filename+'.part%02d'%n;part=data[start:start+18*1024*1024];(directory/name).write_bytes(part);urls.append(root+name);records.append(dict(filename=name,bytes=len(part),sha256=sha(part)))
  doc['parts']=[p for p in doc['parts'] if p['filename'] not in old_names]+records
  pkg.pop('url',None);pkg.update(filename=filename,parts=urls,bytes=len(data),sha256=digest,png_count=len(files),source_repository='Evolution-by-Warder/Trezor',source_ref='1be99df112e0c22038e98841160d4dd763d5ad70')
  if provider:pkg['included_references']=sorted(n[:-4] for n in files)
  else:pkg.pop('included_references',None)
  pkg['append_only_integration']=dict(preserved=len(old),added=len(additions))
  checks=directory/'SHA256SUMS';sums={l.split()[-1]:l.split()[0] for l in checks.read_text().splitlines()};sums.update({p['filename']:p['sha256'] for p in records});checks.write_text('\n'.join(f'{h}  {n}' for n,h in sorted(sums.items()))+'\n')
 return dict(sha256=digest,payload=data)

def zip_payload(files):
 output=io.BytesIO()
 with zipfile.ZipFile(output,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
  for name,png in sorted(files.items()):
   entry=zipfile.ZipInfo(name,(2026,10,22,0,0,0));entry.compress_type=zipfile.ZIP_DEFLATED;entry.create_system=3;entry.external_attr=0o100644<<16;z.writestr(entry,png)
 data=output.getvalue();z=zipfile.ZipFile(io.BytesIO(data));assert z.testzip() is None and all(z.read(n)==p for n,p in files.items());return data

if __name__=='__main__':main()
