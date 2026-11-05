#!/usr/bin/env python3
"""Finish an interrupted staging run from independently verified local archives."""
from pathlib import Path
from zipfile import ZipFile,ZipInfo,ZIP_DEFLATED
from collections import defaultdict
import json,hashlib,io,copy,urllib.request,subprocess,concurrent.futures
ROOT=Path('.');INPUT=ROOT/'reports/canal-reuse-20261105';DATA=ROOT/'assets/warder/downloads/picons/channels';CACHE=Path('/tmp/canal-recovery');CACHE.mkdir(exist_ok=True)
sha=lambda b:hashlib.sha256(b).hexdigest()
blobsha=lambda b:hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
import gzip
for name in ('candidate-manifest.json','verification.json'):
 (INPUT/name).write_bytes(gzip.decompress((INPUT/(name+'.gz')).read_bytes()))
plan=json.loads((INPUT/'reuse-map.json').read_text());before=json.loads((DATA/'manifest.json').read_text());after=json.loads((INPUT/'candidate-manifest.json').read_text());report=json.loads((INPUT/'verification.json').read_text());proof=json.loads((INPUT/'part-git-shas.json').read_text())
assert sha((DATA/'manifest.json').read_bytes())==plan['manifest_sha256']
assert sha((INPUT/'verification.json').read_bytes())==plan['expected_verification_sha256']
assert all(p==q for p,q in zip(before['packages'],after['packages']) if p['selector_id'] in ('CANALPLUS_SK','CANALPLUS_CZ'))
changed={(x['selector'],x['resolution'],x['family']):x for x in report['changes']}
key=lambda p:(p['selector_id'],p['resolution'],p['family'])
for p,q in zip(before['packages'],after['packages']):
 if key(p) not in changed:assert p==q
 else:assert q['sha256']==changed[key(p)]['archive_sha256'] and p['sha256']==changed[key(p)]['before_archive_sha256']
meta={p['filename']:p for p in before['parts']};newmeta={p['filename']:p for p in after['parts']}
result=subprocess.check_output(['git','ls-tree','-r','HEAD','--',str(DATA)]).decode();tracked={}
for line in result.splitlines():
 info,path=line.split('\t',1);tracked[Path(path).name]=info.split()[2]
missing=set()
for n,h in proof.items():
 if n in tracked:assert tracked[n]==h,('Published part blob differs',n)
 else:missing.add(n)
print('Verified staged immutable parts',len(proof)-len(missing),'missing',len(missing),flush=True)
def download(u):
 n=u.rsplit('/',1)[-1];p=CACHE/n;spec=meta[n]
 for attempt in range(4):
  try:
   if p.exists():b=p.read_bytes()
   else:
    with urllib.request.urlopen(u.replace('/main/','/'+plan['catalogue_commit']+'/'),timeout=120) as r:b=r.read()
   assert len(b)==spec['bytes'] and sha(b)==spec['sha256'];p.write_bytes(b);return
  except Exception:
   p.unlink(missing_ok=True)
   if attempt==3:raise
packages={key(p):p for p in before['packages']};newpackages={key(p):p for p in after['packages']}
needed=[k for k,c in changed.items() if any(u.rsplit('/',1)[-1] in missing for u in newpackages[k]['parts'])]
canonical=[p for p in before['packages'] if p['selector_id'] in ('CANALPLUS_SK','CANALPLUS_CZ')]
urls={u for p in canonical+[packages[k] for k in needed] for u in p['parts']}
with concurrent.futures.ThreadPoolExecutor(max_workers=12) as pool:list(pool.map(download,sorted(urls)))
def archive(p):
 b=b''.join((CACHE/u.rsplit('/',1)[-1]).read_bytes() for u in p['parts']);assert len(b)==p['bytes'] and sha(b)==p['sha256'];z=ZipFile(io.BytesIO(b));assert z.testzip() is None;return z
source={}
for p in canonical:
 v=(p['resolution'],p['family']);bucket=source.setdefault(v,{})
 with archive(p) as z:
  for n in z.namelist():
   if not n.endswith('.png'):continue
   r=Path(n).stem;b=z.read(n)
   if r in bucket:assert bucket[r]==b
   bucket[r]=b
for k in needed:
 p=packages[k];q=newpackages[k];c=changed[k];repl={};adds={}
 for row in c['changes']:
  b=source[(p['resolution'],p['family'])][row['source_reference']];assert sha(b)==row['sha256'];(repl if row['operation']=='REPLACE' else adds)[row['member']]=b
 with archive(p) as z:
  output=io.BytesIO()
  with ZipFile(output,'w') as out:
   out.comment=z.comment
   for info in z.infolist():out.writestr(copy.copy(info),repl.get(info.filename,z.read(info.filename)))
   for n,b in sorted(adds.items()):
    info=ZipInfo(n,(2026,11,5,0,0,0));info.compress_type=ZIP_DEFLATED;info.external_attr=0o100644<<16;out.writestr(info,b,compresslevel=9)
  raw=output.getvalue();assert len(raw)==q['bytes'] and sha(raw)==q['sha256'],('Regenerated archive differs',k)
  with ZipFile(io.BytesIO(raw)) as out:
   assert out.testzip() is None
   for n in z.namelist():assert out.read(n)==repl.get(n,z.read(n))
   for n,b in adds.items():assert out.read(n)==b
 offset=0
 for u in q['parts']:
  n=u.rsplit('/',1)[-1];spec=newmeta[n];b=raw[offset:offset+spec['bytes']];offset+=len(b);assert sha(b)==spec['sha256'] and blobsha(b)==proof[n]
  if n in missing:(DATA/n).write_bytes(b);missing.remove(n)
 assert offset==len(raw)
 print('Recovered',k,flush=True)
assert not missing,missing
import importlib.util
path=ROOT/'source/package-root/usr/lib/enigma2/python/Plugins/Extensions/setupGlass17/warderPiconSync.py';spec=importlib.util.spec_from_file_location('sync',path);sync=importlib.util.module_from_spec(spec);spec.loader.exec_module(sync);errors=sync.validate_publication_manifest(after,'production');assert not errors,errors
(DATA/'manifest.json').write_bytes((INPUT/'candidate-manifest.json').read_bytes())
sums=DATA/'SHA256SUMS';values={l.split()[-1]:l.split()[0] for l in sums.read_text().splitlines() if l.strip()};values.update({n:p['sha256'] for n,p in newmeta.items()});values['manifest.json']=sha((DATA/'manifest.json').read_bytes());sums.write_text(''.join(h+'  '+n+'\n' for n,h in sorted(values.items())))
print('COMPLETE: all canonical, unrelated, archive and receiver checks passed',flush=True)
