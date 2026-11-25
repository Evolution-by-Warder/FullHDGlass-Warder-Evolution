import json,hashlib,urllib.request,io,zipfile,re,concurrent.futures
from pathlib import Path
from PIL import Image
P=Path('production');out=Path('remaining-donors');out.mkdir(exist_ok=True)
base='https://raw.githubusercontent.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/884e555486e32764129ba442ba7ec50f4b6336bb/'
def sha(b):return hashlib.sha256(b).hexdigest()
def get(u):
 with urllib.request.urlopen(u,timeout=60) as r:return r.read()
m=json.loads((P/'assets/warder/downloads/picons/channels/manifest.json').read_text())
meta={x['filename']:x for x in m['parts']}
recipe=json.loads((P/'reports/dtt-italia-20261123/recipe.json').read_text())
# Known exact service identities; no automatic provider alias assignment.
wanted={'radio-mater':(0x7d1,0x20e1,0x217c),'amici':(0x1c2e,0x384,0x110),'telepace-trento':(0xaf3,0x28e1,0x217c),'italia7':(0x1392,0x50e1,0x217c)}
def parse(n):
 a=n.rsplit('/',1)[-1].removesuffix('.png').split('_')
 if len(a)!=10:return None
 try:return tuple(int(x,16) for x in a[3:6])
 except ValueError:return None
pkgs=[p for p in m['packages'] if p.get('resolution')=='220x132' and p.get('selector_id') in ('90E','DTT_ITALIA')]
print('packages',[(p['selector_id'],p['family'],p['png_count']) for p in pkgs],flush=True)
def inspect(p):
 found=[];chunks=[]
 for u in p['parts']:
  n=u.rsplit('/',1)[-1];d=get(base+'assets/warder/downloads/picons/channels/'+n)
  assert len(d)==meta[n]['bytes'] and sha(d)==meta[n]['sha256'],n;chunks.append(d)
 raw=b''.join(chunks);assert sha(raw)==p['sha256']
 with zipfile.ZipFile(io.BytesIO(raw)) as z:
  for n in z.namelist():
   tup=parse(n)
   for k,t in wanted.items():
    if tup!=t:continue
    b=z.read(n);im=Image.open(io.BytesIO(b));assert im.size==(220,132)
    name=p['selector_id']+'_'+p['family']+'_'+n.rsplit('/',1)[-1]
    (out/name).write_bytes(b);found.append({'identity':k,'name':name,'service':n,'sha256':sha(b),'archive':p['sha256']})
 return found
results=[];errors=[]
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:
 for p,fu in [(p,ex.submit(inspect,p)) for p in pkgs]:
  try:results.extend(fu.result())
  except Exception as e:errors.append({'selector':p['selector_id'],'family':p['family'],'error':repr(e)})
# Direct provider data for all pending names, with exact same-style duplicates.
a=json.loads((P/'assets/warder/downloads.json').read_text())['assets']
pending=['1 CENT','AN','BBC WORLD','DGB3','DORIA','FREE TV','GTSS','MULTIPROGRAM','NT','RADIO MATER DAB%2A','RETECAPRI TRTN','SERVICE N','SESTARETE & RETE 8','SHARAVOZ','TELERADIOPACE','TV SYSTEM','TVCM']
aliases={}
for s,key in [('transparent','piconProv-220'),('white','piconProv-w'),('black','piconProv-b')]:
 items={}
 for q in [a[key]]+(a['piconProv-w-v2']['extensions'] if s=='white' else []):
  d=get(q['url']);assert sha(d)==q['sha256']
  with zipfile.ZipFile(io.BytesIO(d)) as z:
   assert len(z.namelist())==q['png_count'] and z.testzip() is None
   items.update({n:z.read(n) for n in z.namelist()})
 aliases[s]={}
 for t in pending:
  n='piconProv/'+t+'.png'
  if n in items:
   aliases[s][t]=[k for k,b in items.items() if k!=n and b==items[n]]
   (out/(s+'_'+t+'.png')).write_bytes(items[n])
(out/'result.json').write_text(json.dumps({'matches':results,'errors':errors,'aliases':aliases},ensure_ascii=False,indent=2))
print(json.dumps({'matches':results,'errors':errors},ensure_ascii=False),flush=True)
