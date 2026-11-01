#!/usr/bin/env python3
"""Audit exact native-position PNG overlaps in full 23.5E and both Canal+ sets."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import hashlib,importlib.util,io,json,os,struct,urllib.request,zipfile
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'assets/warder/downloads/picons/channels'
CACHE=Path(os.environ.get('CANAL_ARCHIVE_CACHE','/tmp/warder-canal-archives'))
CACHE.mkdir(exist_ok=True,parents=True)
PART_CACHES=[Path(p) for p in os.environ.get('CANAL_PART_CACHES','/tmp/warder-canal-parts').split(':')]
PART_CACHES[0].mkdir(exist_ok=True,parents=True)
sha=lambda b:hashlib.sha256(b).hexdigest()

def load_sync():
 spec=importlib.util.spec_from_file_location('canal_overlap_sync',ROOT/'source/package-root/usr/lib/enigma2/python/Plugins/Extensions/setupGlass17/warderPiconSync.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m

def fetch(url):
 for attempt in range(3):
  try:
   with urllib.request.urlopen(urllib.request.Request(url,headers={'Cache-Control':'no-cache','User-Agent':'Warder-Canal-overlap-audit'}),timeout=90) as r:return r.read()
  except Exception:
   if attempt==2:raise

def read_archive(package,metadata):
 archive=CACHE/package['filename']
 if archive.is_file():
  data=archive.read_bytes();assert len(data)==package['bytes'] and sha(data)==package['sha256'];return data
 def part(url):
  name=url.rsplit('/',1)[-1];record=metadata[name];path=next((d/name for d in PART_CACHES if (d/name).is_file()),None)
  data=path.read_bytes() if path else fetch(url)
  assert len(data)==record['bytes'] and sha(data)==record['sha256'],name
  if path is None:(PART_CACHES[0]/name).write_bytes(data)
  return data
 with ThreadPoolExecutor(max_workers=5) as pool:data=b''.join(pool.map(part,package['parts']))
 assert len(data)==package['bytes'] and sha(data)==package['sha256']
 archive.write_bytes(data);return data

def native_images(package,data,sync):
 result={};invalid=[];ignored=0
 with zipfile.ZipFile(io.BytesIO(data)) as z:
  assert len(z.namelist())==len(set(z.namelist())),package['filename']
  for info in z.infolist():
   if info.is_dir() or not info.filename.lower().endswith('.png'):continue
   stem=sync.normalize_service_reference(Path(info.filename).stem)
   if not stem or sync.service_orbital_position(stem)!='23.5e':ignored+=1;continue
   name=stem+'.png';png=z.read(info)
   if name in result:assert result[name]==png,(package['selector_id'],name,'internal conflict')
   result[name]=png
   try:
    with Image.open(io.BytesIO(png)) as im:
     im.load()
     if im.size!=tuple(map(int,package['resolution'].split('x'))) or not im.convert('RGBA').getchannel('A').getbbox():invalid.append(name)
   except Exception:invalid.append(name)
 return result,sorted(set(invalid)),ignored

def audit(document):
 sync=load_sync();assert sync.validate_publication_manifest(document,'production')==[]
 metadata={p['filename']:p for p in document['parts']}
 packages=[p for p in document['packages'] if p['selector_id'] in ('235E','CANALPLUS_SK','CANALPLUS_CZ')]
 def read(p):
  data=read_archive(p,metadata);images,invalid,ignored=native_images(p,data,sync)
  print('AUDITED',p['selector_id'],p['family'],p['resolution'],len(images),'native',flush=True)
  return (p['resolution'],p['family'],p['selector_id']),{'package':p,'images':images,'invalid':invalid,'foreign_ignored':ignored}
 with ThreadPoolExecutor(max_workers=3) as pool:loaded=dict(pool.map(read,packages))
 reports=[]
 for size,family in sorted({(k[0],k[1]) for k in loaded}):
  group={sid:loaded[(size,family,sid)] for sid in ('235E','CANALPLUS_SK','CANALPLUS_CZ')}
  sk=group['CANALPLUS_SK']['images'];cz=group['CANALPLUS_CZ']['images'];full=group['235E']['images']
  conflicts=sorted(n for n in sk.keys()&cz.keys() if sk[n]!=cz[n]);canonical=dict(sk);canonical.update(cz)
  replacements=sorted(n for n in canonical.keys()&full.keys() if canonical[n]!=full[n])
  reports.append({'resolution':size,'family':family,'provider_conflicts':conflicts,'invalid_native_images':{sid:v['invalid'] for sid,v in group.items() if v['invalid']},'replacements':replacements,'missing_from_full':sorted(canonical.keys()-full.keys()),'native_provider_union':len(canonical),'full_native_pngs':len(full),'packages':{sid:v['package']['sha256'] for sid,v in group.items()}})
 return loaded,reports

def main():
 document=json.loads((DATA/'manifest.json').read_text());loaded,reports=audit(document)
 path=ROOT/'reports/canal-overlap-audit-20261101.json';path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps({'groups':reports,'total_replacements':sum(len(r['replacements']) for r in reports)},indent=2)+'\n')
 print(json.dumps({'total_replacements':sum(len(r['replacements']) for r in reports),'groups':[{'resolution':r['resolution'],'family':r['family'],'replacements':len(r['replacements']),'conflicts':len(r['provider_conflicts']),'invalid':r['invalid_native_images'],'missing':len(r['missing_from_full'])} for r in reports]},indent=2),flush=True)

if __name__=='__main__':main()
