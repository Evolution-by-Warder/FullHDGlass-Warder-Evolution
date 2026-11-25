import io,hashlib,json,urllib.request,zipfile,concurrent.futures
from pathlib import Path
from PIL import Image
BASE='d28cf4c62a9deb7af08dfa5ebc435a9d650da497'
RAW='https://raw.githubusercontent.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/'+BASE+'/assets/warder/downloads/picons/channels/'
P=Path('cgtn-donor-audit');P.mkdir(exist_ok=True)
def sha(b):return hashlib.sha256(b).hexdigest()
def get(n):
 with urllib.request.urlopen(urllib.request.Request(RAW+n,headers={'User-Agent':'WarderEvolution/1.0'}),timeout=90) as r:return r.read()
raw=get('manifest.json');assert sha(raw)=='6d0e7268cc3b2cdb30b705a2f89b5ba6310dc4ffa81a84103a007a714016c9ed'
d=json.loads(raw);meta={p['filename']:p for p in d['parts']}
targets={'130E':{'1_0_1_36C_3C28_13E_820000_0_0_0.png','1_0_1_36D_3C28_13E_820000_0_0_0.png'},'90E':{'1_0_1_26D_1900_9C_5A0000_0_0_0.png','1_0_1_26E_1900_9C_5A0000_0_0_0.png'}}
def audit(p):
 b=[]
 for u in p['parts']:
  n=u.rsplit('/',1)[-1];x=get(n);assert len(x)==meta[n]['bytes'] and sha(x)==meta[n]['sha256'];b.append(x)
 data=b''.join(b);assert len(data)==p['bytes'] and sha(data)==p['sha256']
 result=[]
 with zipfile.ZipFile(io.BytesIO(data)) as z:
  assert z.testzip() is None and len(z.namelist())==p['png_count']==len(set(z.namelist()))
  for n in sorted(targets[p['selector_id']]):
   if n not in z.namelist():continue
   raw=z.read(n)
   with Image.open(io.BytesIO(raw)) as im:assert im.format=='PNG' and im.size==tuple(map(int,p['resolution'].split('x')));im.load()
   dst=P/p['selector_id']/p['resolution']/p['family']/n;dst.parent.mkdir(parents=True,exist_ok=True);dst.write_bytes(raw)
   result.append({'ref':n,'sha256':sha(raw),'path':str(dst.relative_to(P))})
 return {'selector':p['selector_id'],'resolution':p['resolution'],'family':p['family'],'archive_sha256':p['sha256'],'donors':result}
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:
 r=list(ex.map(audit,[p for p in d['packages'] if p['selector_id'] in targets]))
assert len(r)==18
(P/'report.json').write_text(json.dumps(r,indent=2)+'\n')
print(json.dumps({'archives':len(r),'donors':sum(len(p['donors']) for p in r)}))
