import concurrent.futures,hashlib,io,json,urllib.request,zipfile
from pathlib import Path
from PIL import Image
P=Path(__file__).parent
BASE='https://raw.githubusercontent.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/main/assets/warder/downloads/picons/channels/'
EXPECTED='f19668010148a473a79b7414fac41f2d060faa06c76b20d7cfedbf6054c25460'
def sha(x):return hashlib.sha256(x).hexdigest()
def get(url):
 with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'WarderEvolution/1.0'}),timeout=90) as r:return r.read()
raw=get(BASE+'manifest.json');assert sha(raw)==EXPECTED
d=json.loads(raw);parts={p['filename']:p for p in d['parts']}
assert len(d['packages'])==507 and len(parts)==2233
sums=get(BASE+'SHA256SUMS').decode()
assert sums==EXPECTED+'  manifest.json\n'+''.join(x['sha256']+'  '+x['filename']+'\n' for x in d['parts'])
delta=(P/'Warder_Azzurra_9E_verified_36.zip').read_bytes();assert sha(delta)=='54fb58787a37863468be59aedc0d0492fb74d7077f17e3ba9c4bc2359fce0b52'
with zipfile.ZipFile(io.BytesIO(delta)) as z:
 assert z.testzip() is None
 rows=json.loads(z.read('manifest.json'))['rows'];assert len(rows)==36
 approved={x['path']:z.read(x['path']) for x in rows}
delta2=(P/'Warder_Azzurra_CGTN_Russian_verified_9.zip').read_bytes();assert sha(delta2)=='bd3b40b980e34042c55d256e5d92c0c8d211a81f1eae77e06b2edff7ce777bcf'
with zipfile.ZipFile(io.BytesIO(delta2)) as z:
 assert z.testzip() is None
 newrows=json.loads(z.read('manifest.json'))['rows'];assert len(newrows)==9
 assert {x['ref'] for x in newrows}=={'1_0_1_26D_1900_9C_5A0000_0_0_0.png'}
 approved.update({x['path']:z.read(x['path']) for x in newrows})
 rows+=newrows
assert len(approved)==45 and len(rows)==45
oldbase='https://raw.githubusercontent.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/3dd2c9b4c234d26cfad22a9854e45ca9e07c3b64/assets/warder/downloads/picons/channels/'
oldraw=get(oldbase+'manifest.json');assert sha(oldraw)=='6d0e7268cc3b2cdb30b705a2f89b5ba6310dc4ffa81a84103a007a714016c9ed'
old=json.loads(oldraw);oldparts={x['filename']:x for x in old['parts']}
assert [p for p in d['packages'] if p['selector_id']!='90E']==[p for p in old['packages'] if p['selector_id']!='90E']
def check(p):
 chunks=[]
 for u in p['parts']:
  n=u.rsplit('/',1)[-1];assert u==BASE+n
  b=get(u);assert len(b)==parts[n]['bytes'] and sha(b)==parts[n]['sha256'],n;chunks.append(b)
 data=b''.join(chunks);assert len(data)==p['bytes'] and sha(data)==p['sha256']
 s=p['resolution'];t=p['family'][8:]
 matches=[x for x in rows if x['resolution']==s and x['style']==t];assert len(matches)==5
 with zipfile.ZipFile(io.BytesIO(data)) as z:
  assert z.testzip() is None and len(z.namelist())==p['png_count']==len(set(z.namelist()))
  for x in matches:
   b=z.read(x['ref']);assert b==approved[x['path']] and sha(b)==x['sha256']
   with Image.open(io.BytesIO(b)) as im:assert im.size==tuple(map(int,s.split('x')));im.verify()
  oldp=next(q for q in old['packages'] if q['selector_id']=='90E' and q['resolution']==s and q['family']==p['family'])
  oldchunks=[]
  for u in oldp['parts']:
   n=u.rsplit('/',1)[-1];b=get(oldbase+n);assert len(b)==oldparts[n]['bytes'] and sha(b)==oldparts[n]['sha256'];oldchunks.append(b)
  olddata=b''.join(oldchunks);assert sha(olddata)==oldp['sha256']
  with zipfile.ZipFile(io.BytesIO(olddata)) as oz:
   assert oz.testzip() is None and oz.namelist()==z.namelist()
   ref='1_0_1_26D_1900_9C_5A0000_0_0_0.png'
   assert all(oz.read(n)==z.read(n) for n in z.namelist() if n!=ref)
   assert sha(oz.read(ref))==next(x['old_sha256'] for x in newrows if x['resolution']==s and x['style']==t)
 return {'archive':p['filename'],'parts':len(chunks),'png_count':p['png_count'],'verified_replacements':5,'preserved':p['png_count']-1}
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:
 result=list(ex.map(check,[p for p in d['packages'] if p['selector_id']=='90E']))
assert len(result)==9 and sum(p['parts'] for p in result)==70
assert sha(get(BASE+'manifest.json'))==EXPECTED
report={'manifest_sha256':EXPECTED,'archives':result,'verified_png':45,'verified_parts':70,'preserved_png':sum(p['preserved'] for p in result),'unrelated_packages':498,'status':'PASS'}
Path('live-audit.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report))
