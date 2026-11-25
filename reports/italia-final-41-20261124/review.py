# Read-only production preflight; do not regenerate approved graphics.
import hashlib, io, json, urllib.request, zipfile, concurrent.futures
from pathlib import Path
from PIL import Image
P=Path(__file__).parent
out=P/'review-output';out.mkdir(exist_ok=True)
BASE='a568467cc3fc05dae0c3c00bca9c3a6c56e0dd64'
root='https://raw.githubusercontent.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/'+BASE+'/assets/warder/downloads/picons/channels/'
def sha(b):return hashlib.sha256(b).hexdigest()
def get(u,limit=32*1024*1024):
 req=urllib.request.Request(u,headers={'User-Agent':'WarderEvolution/1.0'})
 with urllib.request.urlopen(req,timeout=90) as r:b=r.read(limit+1)
 assert len(b)<=limit,u
 return b
templates={}
for style,expected,pixel in [('white','c6ae4a808a65ffc8e6458336fccbfe4216de1e832ec0a9abf800907f2f783589','68e9f6e532ec60ba81157ca63e8445cbac8986aeaa1c7111891bca46bffdb732'),('black','61e69f7fc46e340453bf74ccd7af6ac9d8eba9f8e232884659e1ea99f6abf3fe','0ac6fb363683cb4cb1493e39a841c2a6d158cd0a643fcf423c282f77a637f8b2')]:
 b=(P/(style+'-sablona.png')).read_bytes()
 assert sha(b)==expected
 im=Image.open(io.BytesIO(b)).convert('RGBA')
 assert im.size==(220,132)
 templates[style]={'file_sha256':sha(b),'pixel_sha256':sha(im.tobytes()),'local_reconstruction_matches':sha(im.tobytes())==pixel}
refs={'1_0_19_1392_50E1_217C_EEEE0000_0_0_0.png','1_0_16_1392_50E1_217C_EEEE0000_0_0_0.png',*('1_0_1_'+str(i)+'_A002_217C_EEEE0000_0_0_0.png' for i in (1,2,4,5))}
m=get(root+'manifest.json');d=json.loads(m);meta={p['filename']:p for p in d['parts']}
packages=[p for p in d['packages'] if p['selector_id']=='DTT_ITALIA']
assert len(packages)==9
def inspect(p):
 dim=tuple(map(int,p['resolution'].split('x')))
 chunks=[]
 for u in p['parts']:
  n=u.rsplit('/',1)[-1];b=get(root+n)
  assert sha(b)==meta[n]['sha256'] and len(b)==meta[n]['bytes'],n
  chunks.append(b)
 raw=b''.join(chunks);assert len(raw)==p['bytes'] and sha(raw)==p['sha256']
 with zipfile.ZipFile(io.BytesIO(raw)) as z:
  assert z.testzip() is None and len(z.namelist())==len(set(z.namelist()))==p['png_count']
  names={n.casefold():n for n in z.namelist()}
  assert len(names)==len(z.namelist())
  coll={n:sha(z.read(names[n.casefold()])) for n in sorted(refs) if n.casefold() in names}
  for n in z.namelist():
   if n.endswith('.png'):
    im=Image.open(io.BytesIO(z.read(n)));assert im.size==dim,(n,im.size,dim);im.verify()
 return {'resolution':p['resolution'],'family':p['family'],'sha256':p['sha256'],'count':p['png_count'],'parts':len(chunks),'bytes':len(raw),'collisions':coll,'missing':sorted(refs-set(coll))}
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex: rows=list(ex.map(inspect,packages))
report={'baseline':BASE,'manifest_sha256':sha(m),'manifest_git_sha':hashlib.sha1(b'blob '+str(len(m)).encode()+b'\0'+m).hexdigest(),'templates':templates,'approved_delta_sha256':'5fb0217df0d7e73c931092e858faa2f37c73aeb01632ece28f3c99e805822846','packages':rows,'untouched_other_packages':len(d['packages'])-9,'new_entries_if_no_other_changes':sum(len(p['missing']) for p in rows),'publication':'NOT_PUBLISHED; exact approved delta must be imported before build'}
(out/'dtt-publication-preflight.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report))
assert all(t['local_reconstruction_matches'] for t in templates.values()),'Reconstructed MASTER background differs; block publication'
