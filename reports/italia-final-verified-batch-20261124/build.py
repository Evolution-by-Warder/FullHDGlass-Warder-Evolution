import hashlib,io,json,zipfile,urllib.request
from pathlib import Path
from PIL import Image
import numpy as np
ROOT=Path(__file__).parent
def sha(b):return hashlib.sha256(b).hexdigest()
def get(u):
 with urllib.request.urlopen(u,timeout=60) as r:return r.read()
def image(b):
 im=Image.open(io.BytesIO(b)).convert('RGBA');assert im.size==(220,132);return im
def png(im):
 b=io.BytesIO();im.save(b,'PNG',compress_level=6);return b.getvalue()
planraw=(ROOT/'plan.json').read_bytes();assert sha(planraw)=='8618b8c22a3a929d3b9685133113613764d52d60b028735252087050d984939d';plan=json.loads(planraw)
assert plan['baseline']=='286291aaac56f78015c7d147bcafc4ade8604a6c' and len(plan['names'])==70 and plan['counts']=={'transparent':70,'white':41,'black':31}
source=(ROOT/'foregrounds.zip').read_bytes();assert sha(source)=='faa33529d0107883e4c086302d606a3e8cc63f8422d48250538d3e5a829c7e34'
masters={}
for s,h in [('white','c6ae4a808a65ffc8e6458336fccbfe4216de1e832ec0a9abf800907f2f783589'),('black','61e69f7fc46e340453bf74ccd7af6ac9d8eba9f8e232884659e1ea99f6abf3fe')]:
 b=get('https://raw.githubusercontent.com/Evolution-by-Warder/PiconHub-Warder-Evolution/64237bcea7519645c143a88ff201c7701a5630fc/plugin/artwork/templates/picons/'+s+'-sablona.png');assert sha(b)==h;masters[s]=image(b)
def render(t,s,whiteadapt,plate,name):
 if s=='transparent':return t.copy()
 a=np.array(t);rgb=a[:,:,:3].astype(float);lo=rgb.min(2);hi=rgb.max(2);ch=hi-lo
 if s=='white' and whiteadapt and not plate:
  strength=np.clip((lo-130)/90,0,1)*np.clip((50-ch)/35,0,1);rgb=rgb*(1-strength[:,:,None])+np.array([26,30,36])*strength[:,:,None]
 if s=='black' and name=='TELSTRA.png':
  blue=(rgb[:,:,2]>rgb[:,:,0]+15)&(hi<155)&(a[:,:,3]>0);rgb[blue]=np.clip(rgb[blue]*1.45+np.array([16,16,12]),0,255)
 a[:,:,:3]=np.round(rgb).astype(np.uint8);a[a[:,:,3]==0,:3]=0
 return Image.alpha_composite(masters[s],Image.fromarray(a))
delta={}
with zipfile.ZipFile(io.BytesIO(source)) as z:
 assert z.testzip() is None and len(z.namelist())==50
 for rec in plan['names']:
  n=rec['name'];raw=z.read(rec['foreground_sha']+'.png');assert sha(raw)==rec['foreground_sha'];t=image(raw)
  assert t.getchannel('A').getextrema()[0]==0 and t.getchannel('A').getbbox()
  assert '/' not in n and n.endswith('.png') and n not in {'FREE TV.png','RETECAPRI TRTN.png','TIVIBU.png','SKYLINK.png'}
  for s in rec['styles']:
   data=raw if s=='transparent' else png(render(t,s,rec['whiteadapt'],rec['plate'],n))
   assert sha(image(data).tobytes())==rec['variants'][s],(n,s)
   delta[s+'/piconProv/'+n]=data
h=hashlib.sha256()
for n,b in sorted(delta.items()):h.update(n.encode()+b'\0'+image(b).tobytes())
assert len(delta)==142 and h.hexdigest()==plan['pixel_digest']=='519877627b6ba40aad9bd70e7383313f1cb8f2b1d2cb7325d12115bf9ac4f8da'
catpath=Path('assets/warder/downloads.json');cat=json.loads(catpath.read_text());assets=cat.get('assets',cat);report=[]
for s,key,oldcount,oldsha,expected in [('transparent','piconProv-220',1297,'27a4ad5422accee9f245f5da4cc70761f177d0ff1d91c6dd821a38749d3880ab',70),('white','piconProv-w',1346,'8b33b141be669734e741e2b6e2765791e3cbb6ad43f8371d1acad715f314bfe2',41),('black','piconProv-b',1371,'70c26caa1c2402fa3fe24b74975bc1701248546aa225094636e02e07904a0107',31)]:
 path=Path('assets/warder/downloads/picons/providers')/s/'piconProv.zip';before=path.read_bytes();meta=assets[key]
 assert sha(before)==meta['sha256']==oldsha
 add={n.split('/',1)[1]:b for n,b in delta.items() if n.startswith(s+'/')};assert len(add)==expected
 with zipfile.ZipFile(io.BytesIO(before)) as a:
  old=set(a.namelist());assert len(old)==oldcount and a.testzip() is None
  assert not {n.casefold() for n in old}&{n.casefold() for n in add}
 buf=io.BytesIO(before)
 with zipfile.ZipFile(buf,'a',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
  for n,b in sorted(add.items()):z.writestr(zipfile.ZipInfo(n,(1980,1,1,0,0,0)),b,compress_type=zipfile.ZIP_DEFLATED,compresslevel=9)
 after=buf.getvalue()
 with zipfile.ZipFile(io.BytesIO(before)) as a,zipfile.ZipFile(io.BytesIO(after)) as z:
  assert z.testzip() is None and set(z.namelist())==old|set(add) and len(z.namelist())==len(old)+len(add)
  assert all(z.read(n)==a.read(n) for n in old)
  assert all(z.read(n)==b for n,b in add.items())
  assert {'piconProv/'+rec['name'] for rec in plan['names']}<=set(z.namelist())
 assert len(after)<32*1024*1024
 path.write_bytes(after);meta.update(sha256=sha(after),size=len(after),png_count=len(old)+len(add))
 report.append({'style':s,'added':len(add),'count':len(old)+len(add),'preserved':len(old),'sha256':sha(after),'bytes':len(after)})
catpath.write_text(json.dumps(cat,ensure_ascii=False,indent=2)+'\n')
(ROOT/'build.json').write_text(json.dumps({'pixel_sha256':h.hexdigest(),'archives':report,'names':[x['name'] for x in plan['names']]},ensure_ascii=False,indent=2)+'\n')
print(json.dumps(report))
