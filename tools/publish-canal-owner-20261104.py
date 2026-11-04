#!/usr/bin/env python3
"""Publish exact owner-approved Canal+ artwork; keep catalogue activation last."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import argparse,ast,copy,hashlib,importlib.util,io,json,os,shutil,stat,subprocess,sys,tempfile,time,types,urllib.request,zipfile
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'assets/warder/downloads/picons/channels'
REPORT=ROOT/'reports/canal-owner-publication-20261104.json'
SOURCE_REF='b498c30b11f47f28bbc7a068d5bd671395ca4e8c'
SOURCE=ROOT/'.approved-source'
ART=SOURCE/'plugin/artwork/provenance/canal-owner-20261104'
BRANCH='release/canal-owner-20261104'
REPO='Evolution-by-Warder/FullHDGlass-Warder-Evolution'
PREFIX='assets/warder/downloads/picons/channels/'
RAW='https://raw.githubusercontent.com/'+REPO+'/main/'+PREFIX
sha=lambda b:hashlib.sha256(b).hexdigest()

def git(*args):
 return subprocess.check_output(['git',*args],cwd=ROOT,text=True).strip()

def load(name,path):
 s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m

def fetch(url,head=False):
 for attempt in range(3):
  try:
   q=urllib.request.Request(url,headers={'User-Agent':'Warder-Canal-owner-approved/20261104','Cache-Control':'no-cache'},method='HEAD' if head else 'GET')
   with urllib.request.urlopen(q,timeout=90) as r:
    assert r.status==200
    return dict(r.headers) if head else r.read()
  except Exception:
   if attempt==2:raise
   time.sleep(1+attempt)

def runtimes():
 pkg=ROOT/'source/package-root/usr/lib/enigma2/python/Plugins/Extensions/setupGlass17'
 sync=load('canal_skin_sync',pkg/'warderPiconSync.py')
 node=next(n for n in ast.walk(ast.parse((pkg/'plugin.py').read_bytes())) if isinstance(n,ast.FunctionDef) and n.name=='_warderInstallChannelArchive')
 scope=dict(warderPiconSync=sync,os=os,shutil=shutil,stat=stat,tempfile=tempfile,zipfile=zipfile)
 exec(compile(ast.Module(body=[node],type_ignores=[]),'actual-FullHDGlass-installer','exec'),scope)
 ns='canal_actual_piconhub';module=types.ModuleType(ns);module.__path__=[str(SOURCE/'plugin/src/Plugins/Extensions/WarderPiconHub')];sys.modules[ns]=module
 engine=__import__(ns+'.warder_engine',fromlist=['PiconRunner'])
 return sync,scope['_warderInstallChannelArchive'],engine

def approved():
 owner=json.loads((ART/'owner-approval.json').read_text());plan=json.loads((ART/'publication-plan.json').read_text());review=json.loads((ART/'review-manifest.json').read_text())
 assert owner['status']=='OWNER_APPROVED_EXACT_OUTPUTS' and owner['instruction']=='laska beriem'
 assert plan['owner_approval_sha256']==sha((ART/'owner-approval.json').read_bytes())
 assert plan['status']=='OWNER_AUTHORIZED_PRODUCTION_PUBLICATION' and len(plan['references'])==11 and plan['expected_package_count']==45
 assert len({r['reference'] for r in plan['references']})==11
 assert not ({r['reference'] for r in plan['references']} & {r['reference'] for r in plan['excluded']})
 assert sha((ART/'Warder-Canal-kontrola.png').read_bytes())==owner['approved_preview_sha256']
 art={}
 for style,h in owner['templates'].items():assert sha((SOURCE/'plugin/artwork/templates/picons'/(style+'-sablona.png')).read_bytes())==h
 for row in review['artwork']:
  for key,meta in row['outputs'].items():
   raw=(ART/meta['path']).read_bytes();assert sha(raw)==meta['sha256']==owner['outputs'][row['slug']][key]
   with Image.open(io.BytesIO(raw)) as im:im.load();assert im.size==tuple(map(int,key.split('/')[0].split('x'))) and im.mode=='RGBA'
   size,style=key.split('/');art[row['slug'],size,style]=raw
 assert len(art)==36
 for r in plan['references']:
  assert r['reference'].split('_')[6]==r['namespace']
  assert set(r['target_selectors'])<=set(plan['target_selectors'])
 return owner,plan,art

def build():
 owner,plan,art=approved();raw=(DATA/'manifest.json').read_bytes();doc=json.loads(raw);before=copy.deepcopy(doc)
 meta={p['filename']:p for p in doc['parts']};candidates=[p for p in doc['packages'] if p['selector_id'] in plan['target_selectors']]
 assert len(candidates)==45
 sync,install,engine=runtimes();cache=ROOT/'.canal-cache';cache.mkdir(exist_ok=True);records=[];newparts={};changed={}
 def part(url):
  name=url.rsplit('/',1)[-1];assert url.startswith(RAW);expected=meta[name];p=cache/name
  data=p.read_bytes() if p.exists() else fetch(url)
  assert len(data)==expected['bytes'] and sha(data)==expected['sha256'],name
  if not p.exists():p.write_bytes(data)
  return data
 def process(package):
  original=b''.join(part(url) for url in package['parts']);assert sha(original)==package['sha256'] and len(original)==package['bytes']
  style=package['family'].removeprefix('channel-');size=package['resolution']
  selected={r['reference']:art[r['slug'],size,style] for r in plan['references'] if package['selector_id'] in r['target_selectors']}
  with zipfile.ZipFile(io.BytesIO(original)) as source:
   names=source.namelist();assert len(names)==len(set(names))==package['png_count'];assert all('/' not in n and '\\' not in n and n.endswith('.png') for n in names)
   modified={n:b for n,b in selected.items() if n not in names or source.read(n)!=b};assert modified
   preserved={n:sha(source.read(n)) for n in names if n not in modified};out=io.BytesIO()
   with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED,6) as target:
    for n in sorted(set(names)|set(modified)):
     info=zipfile.ZipInfo(n,(2026,11,4,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o100644<<16
     target.writestr(info,modified[n] if n in modified else source.read(n))
  packed=out.getvalue();digest=sha(packed);filename=f'warder-{package["selector_id"].lower()}-{size}-{style}-{digest[:16]}.zip';parts=[];metadata=[]
  with zipfile.ZipFile(io.BytesIO(packed)) as z:
   assert z.testzip() is None and set(z.namelist())==set(names)|set(modified)
   assert all(sha(z.read(n))==h for n,h in preserved.items())
   assert all(z.read(n)==b for n,b in selected.items())
   total=len(z.namelist())
  for i,start in enumerate(range(0,len(packed),16*1024*1024)):
   name=filename+f'.part{i:02d}';chunk=packed[start:start+16*1024*1024];p=DATA/name
   if p.exists():assert p.read_bytes()==chunk
   else:p.write_bytes(chunk)
   parts.append(RAW+name);metadata.append(dict(filename=name,bytes=len(chunk),sha256=sha(chunk)))
  with tempfile.TemporaryDirectory() as tmp:
   t=Path(tmp);archive=t/'in.zip';archive.write_bytes(packed);dest=t/'picon';dest.mkdir();sentinel=dest/'unrelated-user.png';sentinel.write_bytes(b'preserve')
   installed,available=install(None,str(archive),str(dest),wanted=set(selected))
   assert installed==set(selected) and len(available)==total and sentinel.read_bytes()==b'preserve'
   assert all((dest/n).read_bytes()==b for n,b in selected.items())
  item=copy.deepcopy(package);item.update(filename=filename,parts=parts,sha256=digest,bytes=len(packed),png_count=total,source_repository='Evolution-by-Warder/PiconHub-Warder-Evolution',source_ref=SOURCE_REF);item.pop('url',None)
  if 'included_references' in item:item['included_references']=sorted(n[:-4] for n in set(names)|set(modified))
  item['canal_owner_20261104']={'source_ref':SOURCE_REF,'owner_approval_sha256':plan['owner_approval_sha256'],'changed':len(modified),'unrelated_preserved':len(preserved)}
  rec=dict(selector_id=package['selector_id'],resolution=size,style=style,filename=filename,sha256=digest,bytes=len(packed),old_sha256=package['sha256'],replaced=sorted(n for n in modified if n in names),added=sorted(n for n in modified if n not in names),unrelated_pngs_preserved=len(preserved),approved_pngs={n:sha(b) for n,b in selected.items()})
  print('BUILT AND SKIN INSTALLED',package['selector_id'],size,style,len(modified),'changes',flush=True)
  return (package['selector_id'],size,package['family']),item,metadata,rec
 with ThreadPoolExecutor(max_workers=4) as pool:
  for key,item,metas,record in pool.map(process,candidates):changed[key]=item;newparts.update({p['filename']:p for p in metas});records.append(record)
 for i,p in enumerate(doc['packages']):
  key=p['selector_id'],p['resolution'],p['family']
  if key in changed:doc['packages'][i]=changed[key]
  else:assert p==before['packages'][i]
 required={u.rsplit('/',1)[-1] for p in doc['packages'] for u in p.get('parts',[])};allparts={**meta,**newparts};doc['parts']=[allparts[n] for n in sorted(required)]
 doc['canal_owner_20261104']={'source_ref':SOURCE_REF,'owner_approval_sha256':plan['owner_approval_sha256'],'graphic_count':4,'approved_outputs':36,'reference_count':11,'changed_packages':45,'unrelated_png_bytes_preserved':True,'ipk_changed':False}
 for mod in [sync,engine.sync]:assert not mod.validate_publication_manifest(doc,mod.RUNTIME_MANIFEST_URL)
 body=json.dumps(doc,sort_keys=True,indent=2)+'\n';by_url={RAW+n:DATA/n for n in newparts}
 def opener(url):
  if url==engine.sync.RUNTIME_MANIFEST_URL:return io.BytesIO(body.encode())
  assert url in by_url,url
  return by_url[url].open('rb')
 for rec in records:
  key=rec['selector_id'],rec['resolution'],'channel-'+rec['style'];p=changed[key]
  for mod in [sync,engine.sync]:
   binding=mod.task_binding_for_package_selector(p['selector_id']);assert binding
   prefs=mod.set_task_position_bindings(mod.default_preferences(),[binding]);prefs.update(resolution=p['resolution'],style=rec['style'],update_mode=mod.UPDATE_MODE_REPLACE_ALL)
   queue=mod.build_runtime_queue(prefs,publication={'persistent':True,'manifest_url':mod.RUNTIME_MANIFEST_URL});jobs=mod.build_download_jobs(doc,mod.plan_runtime_packages(doc,queue,mod.RUNTIME_MANIFEST_URL),mod.RUNTIME_MANIFEST_URL)
   assert jobs['state']=='ready' and len(jobs['jobs'])==1 and jobs['jobs'][0]['sha256']==p['sha256']
  with tempfile.TemporaryDirectory() as tmp:
   t=Path(tmp);dest=t/'picon';dest.mkdir();foreign=dest/'1_0_1_FFFD_FFFE_3_2080000_0_0_0.png';foreign.write_bytes(b'foreign-position-user-file')
   for name in rec['approved_pngs']:(dest/name).write_bytes(b'old-user-picon')
   prefs=engine.sync.set_task_position_bindings(engine.sync.default_preferences(),[engine.sync.task_binding_for_package_selector(p['selector_id'])]);prefs.update(resolution=p['resolution'],style=rec['style'],destination=str(dest),update_mode=engine.sync.UPDATE_MODE_INCREMENTAL)
   runner=engine.PiconRunner(opener=opener,enigma2_dir=str(t/'enigma2'),lock_path=str(t/'lock'));result=runner.run([prefs])
   assert all(sha((dest/n).read_bytes())==h for n,h in rec['approved_pngs'].items());assert foreign.read_bytes()==b'foreign-position-user-file'
   if p['selector_id']=='CANALPLUS_SK' and p['resolution']=='220x132' and rec['style']=='black':assert runner.run([prefs])=={'added':0,'changed':0,'removed':0}
  rec['piconhub_actual_engine_install']=True
  print('HUB INSTALLED',rec['selector_id'],rec['resolution'],rec['style'],result,flush=True)
 (DATA/'manifest.json').write_text(body)
 sums={l.split()[-1]:l.split()[0] for l in (DATA/'SHA256SUMS').read_text().splitlines() if l.strip()};sums.update({n:p['sha256'] for n,p in newparts.items()});sums['manifest.json']=sha(body.encode());(DATA/'SHA256SUMS').write_text(''.join(h+'  '+n+'\n' for n,h in sorted(sums.items())))
 report=dict(status='VERIFIED_PUBLICATION_CANDIDATE',source_ref=SOURCE_REF,owner_approval_sha256=plan['owner_approval_sha256'],previous_manifest_sha256=sha(raw),manifest_sha256=sha(body.encode()),changed_packages=45,approved_output_count=36,reference_count=11,skin_actual_installer_checks=45,piconhub_actual_engine_checks=45,skin_planner_checks=45,piconhub_planner_checks=45,all_unrelated_png_bytes_preserved=True,old_archives_retained=True,ipk_changed=False,packages=records,new_parts=list(newparts.values()),excluded=plan['excluded'])
 REPORT.parent.mkdir(exist_ok=True);REPORT.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print('BUILD VERIFIED',len(newparts),'parts',flush=True)

def commit(paths,message):
 subprocess.run(['git','add','--sparse','--',*paths],cwd=ROOT,check=True)
 assert set(git('diff','--cached','--name-only').splitlines())<=set(paths)
 subprocess.run(['git','diff','--cached','--check'],cwd=ROOT,check=True)
 subprocess.run(['git','commit','-m',message],cwd=ROOT,check=True)
 expected=git('rev-parse','HEAD')
 for attempt in range(3):
  r=subprocess.run(['git','push','origin','HEAD:'+BRANCH],cwd=ROOT)
  if r.returncode==0:return
  remote=git('ls-remote','origin','refs/heads/'+BRANCH).split()
  if remote and remote[0]==expected:return
 raise RuntimeError('Publication branch push failed')

def stage():
 report=json.loads(REPORT.read_text());assert report['status']=='VERIFIED_PUBLICATION_CANDIDATE'
 group=[];size=0
 for p in sorted(report['new_parts'],key=lambda p:p['filename']):
  if group and size+p['bytes']>160*1024*1024:commit(group,'Stage verified Canal+ immutable archive parts');group=[];size=0
  name=PREFIX+p['filename'];assert sha((ROOT/name).read_bytes())==p['sha256'];group.append(name);size+=p['bytes']
 if group:commit(group,'Stage verified Canal+ immutable archive parts')
 commit([PREFIX+'manifest.json',PREFIX+'SHA256SUMS',str(REPORT.relative_to(ROOT))],'Publish complete verified Canal+ candidate catalogue after archives')

def readback(ref):
 report=json.loads(REPORT.read_text());root=RAW.replace('/main/','/'+ref+'/')
 def check(p):
  chunks=[]
  for url in json.loads((DATA/'manifest.json').read_text())['packages']:
   if url['filename']==p['filename']:package=url;break
  for url in package['parts']:
   n=url.rsplit('/',1)[-1];m=next(x for x in report['new_parts'] if x['filename']==n);b=fetch(root+n);assert sha(b)==m['sha256'] and len(b)==m['bytes'];chunks.append(b)
  raw=b''.join(chunks);assert sha(raw)==p['sha256'] and len(raw)==p['bytes']
  with zipfile.ZipFile(io.BytesIO(raw)) as z:
   for name,h in p['approved_pngs'].items():assert sha(z.read(name))==h
  print('PUBLIC VERIFIED',p['selector_id'],p['resolution'],p['style'],flush=True)
 with ThreadPoolExecutor(max_workers=4) as pool:list(pool.map(check,report['packages']))
 assert sha(fetch(root+'manifest.json'))==report['manifest_sha256']
 report['status']='PUBLIC_CANDIDATE_VERIFIED';report['public_verification']={'verified_archive_commit':ref,'verified_parts':len(report['new_parts']),'all_part_and_archive_sha256_match':True,'all_approved_png_sha256_match':True,'manifest_matches':True}
 REPORT.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');commit([str(REPORT.relative_to(ROOT))],'Record complete public Canal+ archive and PNG verification')

def verify_live():
 report=json.loads(REPORT.read_text());proof=report['public_verification'];assert report['status']=='PUBLIC_CANDIDATE_VERIFIED' and proof['all_part_and_archive_sha256_match'] and proof['all_approved_png_sha256_match']
 ref=proof['verified_archive_commit'];subprocess.run(['git','fetch','--depth=1','--filter=blob:none','origin',ref],cwd=ROOT,check=True)
 def tree(ref):
  raw=subprocess.check_output(['git','ls-tree','-rz',ref,'--',PREFIX],cwd=ROOT);return {p.decode():meta.split()[2].decode() for i in raw.split(b'\0') if i for meta,p in [i.split(b'\t',1)]}
 candidate=tree(ref);live=tree(os.environ['GITHUB_SHA'])
 def check(p):
  assert candidate[PREFIX+p['filename']]==live[PREFIX+p['filename']]
  headers=fetch(RAW+p['filename'],head=True);length=next(v for k,v in headers.items() if k.lower()=='content-length');assert int(length)==p['bytes']
 with ThreadPoolExecutor(max_workers=6) as pool:list(pool.map(check,report['new_parts']))
 assert sha(fetch(RAW+'manifest.json'))==report['manifest_sha256']
 report['production_verification']={'status':'PRODUCTION_MAIN_VERIFIED','main_commit':os.environ['GITHUB_SHA'],'matching_verified_git_blobs':len(report['new_parts']),'public_main_urls_and_sizes_verified':True,'live_manifest_sha256_matches':True};REPORT.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print('LIVE VERIFIED',len(report['new_parts']),'parts /',report['changed_packages'],'packages',flush=True)

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--build',action='store_true');p.add_argument('--stage',action='store_true');p.add_argument('--readback');p.add_argument('--verify-live',action='store_true');a=p.parse_args()
 if a.build:build()
 elif a.stage:stage()
 elif a.readback:readback(a.readback)
 elif a.verify_live:verify_live()
 else:p.error('mode required')
