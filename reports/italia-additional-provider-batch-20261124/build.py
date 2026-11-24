import json,hashlib,io,zipfile,urllib.request,struct
from pathlib import Path
from PIL import Image
import numpy as np
ROOT=Path(__file__).parent;plan=json.loads((ROOT/'plan.json').read_text())
def sha(b):return hashlib.sha256(b).hexdigest()
def image(b):return Image.open(io.BytesIO(b)).convert('RGBA')
def get(url):
 with urllib.request.urlopen(url,timeout=40) as r:return r.read()
m=get('https://raw.githubusercontent.com/Evolution-by-Warder/PiconHub-Warder-Evolution/05f7e6e92f55c1476b1310287e9918f0968bf7ff/plugin/artwork/templates/picons/black-sablona.png')
assert sha(m)=='61e69f7fc46e340453bf74ccd7af6ac9d8eba9f8e232884659e1ea99f6abf3fe';master=image(m)
delta={}
with zipfile.ZipFile('vector-review/Warder_Vector_Provider_REVIEW.zip') as src:
 assert src.testzip() is None
 records={x['name']:x for x in json.loads(src.read('register.json')) if 'variants' in x}
 for n in plan['names']:
  r=records[n];t=src.read(r['variants']['transparent']['path']);assert sha(t)==r['variants']['transparent']['sha256']
  for s,v in r['variants'].items():
   raw=src.read(v['path']);assert sha(raw)==v['sha256']
   if s=='black' and n in {'TELESAT.png','PROMO TVCINE HD.png'}:
    a=np.array(image(t))
    if n=='TELESAT.png':
     mask=(a[:,:,3]>0)&(a[:,:,2].astype(int)>a[:,:,0].astype(int)+15);a[mask,:3]=(148,154,255)
    else:a[a[:,:,3]>0,:3]=(240,240,240)
    im=Image.alpha_composite(master,Image.fromarray(a));b=io.BytesIO();im.save(b,format='PNG',optimize=True);raw=b.getvalue()
   delta[s+'/piconProv/'+n]=raw
h=hashlib.sha256()
for n,b in sorted(delta.items()):h.update(n.encode()+b'\0'+image(b).tobytes())
assert len(delta)==18 and h.hexdigest()==plan['pixel_digest'],(len(delta),h.hexdigest())
catpath=Path('assets/warder/downloads.json');cat=json.loads(catpath.read_text());assets=cat.get('assets',cat);report=[]
for s,key,count in [('transparent','piconProv-220',6),('white','piconProv-w',6),('black','piconProv-b',6)]:
 path=Path('assets/warder/downloads/picons/providers')/s/'piconProv.zip';before=path.read_bytes();meta=assets[key];assert sha(before)==meta['sha256']==plan['base'][s]['sha256']
 add={n.split('/',1)[1]:b for n,b in delta.items() if n.startswith(s+'/')}
 with zipfile.ZipFile(io.BytesIO(before)) as z:
  old=set(z.namelist());assert z.testzip() is None and len(old)==plan['base'][s]['count']
  assert len(add)==count;assert not {n.casefold() for n in old}&{n.casefold() for n in add}
  assert all(image(b).size==(220,132) for b in add.values())
 buf=io.BytesIO(before)
 with zipfile.ZipFile(buf,'a',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
  for n,b in sorted(add.items()):z.writestr(zipfile.ZipInfo(n,(1980,1,1,0,0,0)),b,compress_type=zipfile.ZIP_DEFLATED)
 after=buf.getvalue()
 with zipfile.ZipFile(io.BytesIO(before)) as a,zipfile.ZipFile(io.BytesIO(after)) as z:
  assert z.testzip() is None and set(z.namelist())==set(a.namelist())|set(add)
  assert all(z.read(n)==a.read(n) for n in a.namelist()) and all(z.read(n)==b for n,b in add.items())
  assert {'piconProv/'+n for n in plan['names']}<=set(z.namelist())
 assert len(after)<32*1024*1024
 path.write_bytes(after);meta.update(sha256=sha(after),size=len(after),png_count=len(old)+len(add));report.append({'style':s,'added':len(add),'count':meta['png_count'],'sha256':sha(after),'preserved':len(old),'names':list(add)})
catpath.write_text(json.dumps(cat,ensure_ascii=False,indent=2)+'\n');(ROOT/'build.json').write_text(json.dumps({'pixel_digest':h.hexdigest(),'archives':report},ensure_ascii=False,indent=2)+'\n');print(json.dumps(report))
