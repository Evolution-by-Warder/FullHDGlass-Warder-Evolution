from pathlib import Path
import zipfile,io,hashlib,json,urllib.request,struct
from PIL import Image,ImageFilter
import numpy as np
from scipy.ndimage import label
P=Path(__file__).parent;plan=json.loads((P/'plan.json').read_text());C=Path('assets/warder/downloads/picons/channels');C.mkdir(parents=True,exist_ok=True)
R='https://raw.githubusercontent.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/b49196d5ff83d924bc5049f0e904c5ae594acf26/assets/warder/downloads/picons/channels/'
S='https://raw.githubusercontent.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/main/assets/warder/downloads/picons/channels/'
T='https://raw.githubusercontent.com/Evolution-by-Warder/PiconHub-Warder-Evolution/27df64cf3884d1190c9016a0fcdac2866c5b5f7e/plugin/artwork/templates/picons/'
def get(u):
 with urllib.request.urlopen(u,timeout=90) as r:return r.read()
def sha(b):return hashlib.sha256(b).hexdigest()
def gitsha(b):return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
def dump(o):return (json.dumps(o,ensure_ascii=False,indent=2,sort_keys=True)+'\n').encode()
raw=(P/'sources.zip').read_bytes();assert sha(raw)==plan['source_zip_sha256'];src=zipfile.ZipFile(io.BytesIO(raw));assert src.testzip() is None
M={}
for s,h in [('white','c6ae4a808a65ffc8e6458336fccbfe4216de1e832ec0a9abf800907f2f783589'),('black','61e69f7fc46e340453bf74ccd7af6ac9d8eba9f8e232884659e1ea99f6abf3fe')]:
 b=get(T+s+'-sablona.png');assert sha(b)==h;M[s]=Image.open(io.BytesIO(b)).convert('RGBA')
light_on_white={'TVA TELENORMANNA','TELERENT 7GOLD','6 SESTARETE TV','NOTIX TV','ANTENNA SICILIA','TELECOLOR','TGS','TRM','TELE GELA'}
def source(n):
 a=np.array(Image.open(io.BytesIO(src.read(n))).convert('RGBA'));h,w=a.shape[:2];labels,count=label(a[:,:,3]>0)
 for i in range(1,count+1):
  yy,xx=np.where(labels==i)
  if len(xx)<=30 and len(xx)>0 and xx.min()>=w-9 and yy.min()>=h-9:a[labels==i]=0
 return Image.fromarray(a)
def fg_for(im,s,name):
 a=np.array(im);rgb=a[:,:,:3].astype(float);lo=rgb.min(2);hi=rgb.max(2);chroma=hi-lo
 if s=='white' and name in light_on_white:
  strength=np.clip((lo-145)/90,0,1)*np.clip((45-chroma)/30,0,1)
  if name=='TELERENT 7GOLD':strength[:,int(im.width*.62):]=0
  rgb=rgb*(1-strength[:,:,None])+np.array([27,31,37])*strength[:,:,None]
  a[:,:,:3]=rgb.round().astype(np.uint8);return Image.fromarray(a)
 if (s=='black' and name in {'TELESTAR','Video Mediterraneo','TRM'}) or (s=='white' and name in {'SICILIAUNO','TVM','TELECOLOR'}):
  edge=im.getchannel('A').filter(ImageFilter.MaxFilter(3)).point(lambda v:round(v*.37));layer=Image.new('RGBA',im.size,(215,224,235,0) if s=='black' else (35,39,42,0));layer.putalpha(edge);return Image.alpha_composite(layer,im)
 return im
def render(im,s,w,h,name):
 crop=im.crop(im.getchannel('A').getbbox());crop=fg_for(crop,s,name)
 crop.thumbnail((round(w*192/220),round(h*104/132)),Image.Resampling.LANCZOS)
 can=Image.new('RGBA',(w,h)) if s=='transparent' else M[s].resize((w,h),Image.Resampling.LANCZOS)
 can.alpha_composite(crop,((w-crop.width)//2,(h-crop.height)//2));return can
def png(im):
 b=io.BytesIO();im.save(b,'PNG',optimize=True);return b.getvalue()
delta={};names={}
for n in src.namelist():
 keys=[k for k in plan['refs'] if n.startswith(k+'_')];assert len(keys)==1;name=plan['refs'][keys[0]];names[n]=name
 im=source(n)
 for w,h in [(50,30),(220,132),(400,240)]:
  for s in ('transparent','white','black'):
   path=f'variants/{w}x{h}/{s}/{n}';delta[path]=png(render(im,s,w,h,name))
assert len(names)==19 and len(delta)==171
h=hashlib.sha256()
for p,b in sorted(delta.items()):h.update(p.encode()+b'\0'+Image.open(io.BytesIO(b)).convert('RGBA').tobytes())
assert h.hexdigest()==plan['pixel_digest'],h.hexdigest()
manifest=get(R+'manifest.json');assert sha(manifest)==plan['baseline_manifest_sha256']
doc=json.loads(manifest);meta={p['filename']:p for p in doc['parts']};oldmeta=dict(meta);old_packages=[p.copy() for p in doc['packages'] if p['selector_id']!='DTT_ITALIA'];report=[]
for p in doc['packages']:
 if p['selector_id']!='DTT_ITALIA':continue
 res=p['resolution'];style=p['family'][8:];dim=tuple(map(int,res.split('x')))
 partnames=[u.rsplit('/',1)[-1] for u in p['parts']]
 chunks=[]
 for n in partnames:
  b=get(R+n);assert len(b)==meta[n]['bytes'] and sha(b)==meta[n]['sha256'];chunks.append(b)
 before=b''.join(chunks);assert sha(before)==p['sha256'] and len(before)==p['bytes']
 additions={n:delta[f'variants/{res}/{style}/{n}'] for n in names}
 with zipfile.ZipFile(io.BytesIO(before)) as z:
  old=set(z.namelist());assert len(old)==len(z.namelist())==323 and z.testzip() is None
  assert not {n.casefold() for n in old}&{n.casefold() for n in additions}
 buf=io.BytesIO(before)
 with zipfile.ZipFile(buf,'a',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
  for n,b in sorted(additions.items()):
   assert Image.open(io.BytesIO(b)).size==dim;z.writestr(zipfile.ZipInfo(n,(1980,1,1,0,0,0)),b,compress_type=zipfile.ZIP_DEFLATED)
 after=buf.getvalue()
 with zipfile.ZipFile(io.BytesIO(before)) as a,zipfile.ZipFile(io.BytesIO(after)) as z:
  assert z.testzip() is None and set(z.namelist())==old|set(additions) and len(z.namelist())==342
  assert all(z.read(n)==a.read(n) for n in old) and all(z.read(n)==b for n,b in additions.items())
 digest=sha(after);name='warder-dtt-italia-'+res+'-'+style+'-'+digest[:16]+'.zip';pos=0;urls=[]
 for i,oldchunk in enumerate(chunks):
  n=name+'.part%02d'%i;b=after[pos:] if i==len(chunks)-1 else after[pos:pos+len(oldchunk)];pos+=len(b);assert 0<len(b)<=20*1024*1024
  (C/n).write_bytes(b);meta[n]={'filename':n,'bytes':len(b),'sha256':sha(b)};urls.append(S+n)
 assert pos==len(after) and b''.join((C/u.rsplit('/',1)[-1]).read_bytes() for u in urls)==after
 for n in partnames:meta.pop(n)
 p.update(filename=name,sha256=digest,bytes=len(after),png_count=342,parts=urls)
 report.append({'resolution':res,'style':style,'filename':name,'sha256':digest,'count':342,'added':19,'parts':len(urls),'preserved':323})
assert len(report)==9 and len(meta)==len(oldmeta)==2224
assert old_packages==[p for p in doc['packages'] if p['selector_id']!='DTT_ITALIA']
for p in old_packages:
 for u in p['parts']:assert meta[u.rsplit('/',1)[-1]]==oldmeta[u.rsplit('/',1)[-1]]
doc['parts']=sorted(meta.values(),key=lambda p:p['filename']);m=dump(doc);(C/'manifest.json').write_bytes(m)
sums=(sha(m)+'  manifest.json\n'+''.join(p['sha256']+'  '+p['filename']+'\n' for p in doc['parts'])).encode();(C/'SHA256SUMS').write_bytes(sums)
result={'dtt':report,'names':names,'pixel_digest':h.hexdigest(),'added':171,'manifest_sha256':sha(m),'manifest_git_sha':gitsha(m),'sums_git_sha':gitsha(sums),'unchanged_catalog_entries':len(old_packages)}
(P/'build.json').write_bytes(dump(result));print(json.dumps(result,ensure_ascii=False))
