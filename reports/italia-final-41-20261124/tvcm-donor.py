import json,hashlib,urllib.request,io,zipfile,re,concurrent.futures
from pathlib import Path
from PIL import Image
P=Path('production');out=Path('remaining-donors');out.mkdir(exist_ok=True)
base='https://raw.githubusercontent.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/0449f449bd0ebcb8086dde953943e3f79c4f0473/'
def sha(b):return hashlib.sha256(b).hexdigest()
def get(u):
 with urllib.request.urlopen(u,timeout=60) as r:return r.read()
m=json.loads((P/'assets/warder/downloads/picons/channels/manifest.json').read_text())
meta={x['filename']:x for x in m['parts']}
recipe=json.loads((P/'reports/dtt-italia-20261123/recipe.json').read_text())
# Known exact service identities; no automatic provider alias assignment.
wanted={'tvcm':(0x1771,0x60e1,0x217c),'teleradiopace1':(0xfa3,0x40e1,0x217c),'teleradiopace2':(0xfae,0x40e1,0x217c)}
def parse(n):
 a=n.rsplit('/',1)[-1].removesuffix('.png').split('_')
 if len(a)!=10:return None
 try:return tuple(int(x,16) for x in a[3:6])
 except ValueError:return None
pkgs=[p for p in m['packages'] if p.get('resolution')=='220x132' and p.get('selector_id') =='90E']
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

(out/'result.json').write_text(json.dumps({'matches':results,'errors':errors},indent=2))
print(json.dumps({'matches':results,'errors':errors}),flush=True)
assert results and not errors
