"""Publish hash-verified terrestrial data; leave all application releases unchanged."""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from urllib.request import Request,urlopen
import hashlib,io,json,re,stat,subprocess,zipfile
from PIL import Image
REPO='Evolution-by-Warder/FullHDGlass-Warder-Evolution'
BRANCH='data/dvb-t-skcz-refresh'
EXPECTED='0b631a089599a89ba9f956ccbc5bb673a7f700fb'
ROOT=Path('assets/warder/downloads/picons')
AUDIT=ROOT/'dvb-t-skcz'
CHANNELS=ROOT/'channels'
MANIFEST=CHANNELS/'manifest.json'
def sha(b):return hashlib.sha256(b).hexdigest()
def git(*args):return subprocess.check_output(['git',*args],text=True).strip()
def head(branch):return git('ls-remote','origin','refs/heads/'+branch).split()[0]
def fetch(task):
 url,entry=task;assert url.startswith('https://raw.githubusercontent.com/'+REPO+'/')
 with urlopen(Request(url,headers={'User-Agent':'Warder-DTT-publication'}),timeout=90) as response:b=response.read(entry['bytes']+1)
 assert len(b)==entry['bytes'] and sha(b)==entry['sha256'],url
 return b

def main():
 assert head('main')==EXPECTED,'Production advanced; refresh lease before publishing'
 manifest=json.loads(MANIFEST.read_text());original_manifest=json.loads(MANIFEST.read_text());base={p['family'].removeprefix('channel-'):p for p in manifest['packages'] if p.get('selector_id')=='DVB-T-SK-CZ'}
 assert set(base)=={'transparent','white','black'}
 parts={p['filename']:p for p in manifest['parts']};index=json.loads((AUDIT/'catalog/delta-index.json').read_text());delta={s:{} for s in base}
 payload=json.loads((AUDIT/'catalog/delta-payload.json').read_text());raw=b''
 for part in payload['parts']:
  b=(AUDIT/part['filename']).read_bytes();assert len(b)==part['bytes'] and sha(b)==part['sha256'];raw+=b
 assert len(raw)==payload['bytes'] and sha(raw)==payload['sha256']
 removals=json.loads((AUDIT/'catalog/removals.json').read_text())
 with zipfile.ZipFile(io.BytesIO(raw)) as z:
  assert set(z.namelist())==set(index) and len(z.namelist())==len(index) and z.testzip() is None
  for name in z.namelist():
   style,filename=name.split('/');assert style in base and re.fullmatch(r'1_0_[0-9A-F]+_([0-9A-F]+_){6}[0-9A-F]+\.png',filename)
   b=z.read(name);assert sha(b)==index[name];im=Image.open(io.BytesIO(b));assert im.size==(220,132);im.verify();delta[style][filename]=b
 assert all(set(x)==set(delta['transparent']) for x in delta.values())
 tasks=[(url,parts[url.rsplit('/',1)[1]]) for p in base.values() for url in p['parts']]
 with ThreadPoolExecutor(max_workers=10) as pool:downloaded=list(pool.map(fetch,tasks))
 downloaded={u:b for (u,_),b in zip(tasks,downloaded)};newentries={};proof={};allrecords={};generated=[]
 old_common=None;new_common=None
 for style,entry in base.items():
  raw=b''.join(downloaded[u] for u in entry['parts']);assert len(raw)==entry['bytes'] and sha(raw)==entry['sha256']
  with zipfile.ZipFile(io.BytesIO(raw)) as z:
   assert z.testzip() is None and len(z.namelist())==len(set(z.namelist()))==2674
   files={n:z.read(n) for n in z.namelist()}
  oldnames=set(files)
  if old_common is None:old_common=oldnames
  assert old_common==oldnames
  oldhashes={n:sha(b) for n,b in files.items()};assert set(removals)<=oldnames and not set(removals)&set(delta[style])
  for n in removals:del files[n]
  files.update(delta[style]);assert oldnames-set(removals)<=set(files)
  if new_common is None:new_common=set(files)
  assert set(files)==new_common and len(files)==2531
  for n,b in files.items():
   assert Path(n).name==n
   with Image.open(io.BytesIO(b)) as im:assert im.size==(220,132);im.verify()
   if n not in delta[style]:assert sha(b)==oldhashes[n]
   allrecords.setdefault(n,{})[style]=sha(b)
  output=io.BytesIO()
  with zipfile.ZipFile(output,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
   for n,b in sorted(files.items()):
    info=zipfile.ZipInfo(n,(1980,1,1,0,0,0));info.external_attr=(stat.S_IFREG|0o644)<<16;info.compress_type=zipfile.ZIP_DEFLATED;z.writestr(info,b,compress_type=zipfile.ZIP_DEFLATED,compresslevel=9)
  raw=output.getvalue();digest=sha(raw);name=f'warder-dvb-t-sk-cz-220x132-{style}-{digest[:16]}.zip';pp=[]
  for i,offset in enumerate(range(0,len(raw),4*1024*1024)):
   b=raw[offset:offset+4*1024*1024];filename=name+f'.part{i:02d}';(CHANNELS/filename).write_bytes(b);part=dict(filename=filename,bytes=len(b),sha256=sha(b));pp.append(part);generated.append(part)
  newentries[style]=dict(filename=name,bytes=len(raw),sha256=digest,png_count=len(files),part_filenames=[p['filename'] for p in pp])
  proof[style]=dict(old_png_count=len(oldnames),new_png_count=len(files),added_files=len(set(files)-oldnames),removed_files=len(removals),changed_existing_files=sum(n in oldnames and sha(b)!=oldhashes[n] for n,b in delta[style].items()),unselected_original_png_bytes_preserved=True,all_pngs_decoded=True)
 for part in payload['parts']:(AUDIT/part['filename']).unlink()
 (AUDIT/'catalog/variants.json').write_text(json.dumps(dict(schema=1,records=allrecords),indent=2)+'\n')
 (AUDIT/'catalog/install-inventory.json').write_text(json.dumps(proof,indent=2)+'\n')
 git('config','user.name','Warder data publication');git('config','user.email','warder-release@users.noreply.github.com');git('add','--sparse',str(ROOT));git('commit','-m','Build three verified DVB-T SK/CZ picon archives with audited receiver mappings')
 revision=git('rev-parse','HEAD');git('push','origin','HEAD:refs/heads/'+BRANCH)
 public=[('https://raw.githubusercontent.com/'+REPO+'/'+revision+'/'+str(CHANNELS/p['filename']),p) for p in generated]
 with ThreadPoolExecutor(max_workers=10) as pool:list(pool.map(fetch,public))
 for style,p in base.items():
  p.update({k:v for k,v in newentries[style].items() if k!='part_filenames'})
  p['parts']=['https://raw.githubusercontent.com/'+REPO+'/main/'+str(CHANNELS/n) for n in newentries[style]['part_filenames']]
  p['source_repository']=REPO;p['source_ref']=revision
  p['original_source'].update(images_changed=True,revision='2026.10.28-dtt-audit',historical_original_png_count=2674,audit_url='https://raw.githubusercontent.com/'+REPO+'/'+revision+'/'+str(AUDIT/'catalog/station-list.json'))
  p['original_source'].pop('unique_images',None)
 referenced={u.rsplit('/',1)[-1] for p in manifest['packages'] for u in p['parts']}
 manifest['parts']=[p for p in manifest['parts'] if p['filename'] in referenced]+generated
 # Only the three shared DTT package records may change. Other programmes and releases remain byte-for-byte equivalent.
 assert [p for p in manifest['packages'] if p.get('selector_id')!='DVB-T-SK-CZ']==[p for p in original_manifest['packages'] if p.get('selector_id')!='DVB-T-SK-CZ']
 assert {p['filename'] for p in manifest['parts']}==referenced
 assert len({p['filename'] for p in manifest['parts']})==len(manifest['parts'])
 assert all(u.startswith('https://raw.githubusercontent.com/'+REPO+'/main/'+str(CHANNELS)+'/') for p in base.values() for u in p['parts'])
 MANIFEST.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
 publication=dict(status='verified-and-active',payload_commit=revision,packages=newentries,verification=proof,public_parts_verified=len(generated),other_package_records_unchanged=True,application_versions_unchanged=True)
 (AUDIT/'catalog/publication.json').write_text(json.dumps(publication,indent=2)+'\n')
 git('add','--sparse',str(ROOT));git('commit','-m','Activate audited terrestrial picons in the shared skin and PiconHub catalogue');git('push','origin','HEAD:refs/heads/'+BRANCH)
 assert head('main')==EXPECTED,'Production advanced before activation'
 git('fetch','--no-tags','--filter=blob:none','--deepen=16','origin',BRANCH,'main:refs/remotes/origin/main');git('push','origin','HEAD:refs/heads/main')
 print(json.dumps(publication,indent=2))
if __name__=='__main__':main()
