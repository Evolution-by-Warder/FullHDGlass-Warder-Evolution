"""Fetch the explicitly supplied archive transfer and verify it before extraction."""
import hashlib,json,shutil,stat,zipfile
from pathlib import Path
from urllib.request import urlopen
R=Path(__file__).resolve().parents[1]
descriptor=R/'.transfer/source-artifact.json';doc=json.loads(descriptor.read_text());transfers=doc['artifacts']
dest=R/'.original-sets';dest.mkdir(exist_ok=True)
for doc in transfers:
 url=doc['url'];print('::add-mask::'+url,flush=True)
 archive=R/'.original-sets.zip';digest=hashlib.sha256()
 with urlopen(url,timeout=180) as response,archive.open('wb') as out:
  while True:
   chunk=response.read(1024*1024)
   if not chunk:break
   digest.update(chunk);out.write(chunk)
 assert digest.hexdigest()==doc['sha256'],'source artifact checksum mismatch'
 with zipfile.ZipFile(archive) as z:
  for entry in z.infolist():
   path=Path(entry.filename)
   assert not path.is_absolute() and '..' not in path.parts and not stat.S_ISLNK(entry.external_attr>>16)
   target=dest/path
   if entry.is_dir():target.mkdir(parents=True,exist_ok=True);continue
   assert not target.exists(), 'overlapping source transport entries'
   target.parent.mkdir(parents=True,exist_ok=True)
   with z.open(entry) as src,target.open('wb') as out:shutil.copyfileobj(src,out)
 archive.unlink()
assert (dest/'index.json').is_file(), 'source index missing'
descriptor.unlink()
print('PASS: original archive transfer verified and extracted',flush=True)
