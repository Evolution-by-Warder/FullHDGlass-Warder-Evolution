import concurrent.futures,hashlib,io,json,urllib.request,zipfile
from pathlib import Path
from PIL import Image
P=Path(__file__).parent
BASE='https://raw.githubusercontent.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/main/assets/warder/downloads/picons/channels/'
EXPECTED='6d0e7268cc3b2cdb30b705a2f89b5ba6310dc4ffa81a84103a007a714016c9ed'
def sha(x):return hashlib.sha256(x).hexdigest()
def get(url):
 with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'WarderEvolution/1.0'}),timeout=90) as r:return r.read()
raw=get(BASE+'manifest.json');assert sha(raw)==EXPECTED
d=json.loads(raw);parts={p['filename']:p for p in d['parts']}
assert len(d['packages'])==507 and len(parts)==2224
sums=get(BASE+'SHA256SUMS').decode()
assert sums==EXPECTED+'  manifest.json\n'+''.join(x['sha256']+'  '+x['filename']+'\n' for x in d['parts'])
delta=(P/'Warder_Azzurra_9E_verified_36.zip').read_bytes();assert sha(delta)=='54fb58787a37863468be59aedc0d0492fb74d7077f17e3ba9c4bc2359fce0b52'
with zipfile.ZipFile(io.BytesIO(delta)) as z:
 assert z.testzip() is None
 rows=json.loads(z.read('manifest.json'))['rows'];assert len(rows)==36
 approved={x['path']:z.read(x['path']) for x in rows}
def check(p):
 chunks=[]
 for u in p['parts']:
  n=u.rsplit('/',1)[-1];assert u==BASE+n
  b=get(u);assert len(b)==parts[n]['bytes'] and sha(b)==parts[n]['sha256'],n;chunks.append(b)
 data=b''.join(chunks);assert len(data)==p['bytes'] and sha(data)==p['sha256']
 s=p['resolution'];t=p['family'][8:]
 matches=[x for x in rows if x['resolution']==s and x['style']==t];assert len(matches)==4
 with zipfile.ZipFile(io.BytesIO(data)) as z:
  assert z.testzip() is None and len(z.namelist())==p['png_count']==len(set(z.namelist()))
  for x in matches:
   b=z.read(x['ref']);assert b==approved[x['path']] and sha(b)==x['sha256']
   with Image.open(io.BytesIO(b)) as im:assert im.size==tuple(map(int,s.split('x')));im.verify()
 return {'archive':p['filename'],'parts':len(chunks),'png_count':p['png_count'],'verified_replacements':4}
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:
 result=list(ex.map(check,[p for p in d['packages'] if p['selector_id']=='90E']))
assert len(result)==9 and sum(p['parts'] for p in result)==61
assert sha(get(BASE+'manifest.json'))==EXPECTED
report={'manifest_sha256':EXPECTED,'archives':result,'verified_png':36,'verified_parts':61,'status':'PASS'}
Path('live-audit.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report))
