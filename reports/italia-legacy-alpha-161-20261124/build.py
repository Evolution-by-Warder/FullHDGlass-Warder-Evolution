import json,io,zipfile,hashlib,collections
from pathlib import Path
import numpy as np
from PIL import Image
from scipy.ndimage import label,distance_transform_edt,binary_dilation
P=Path(__file__).parent;plan=json.loads((P/'plan.json').read_text());A=Path('assets/warder/downloads/picons/providers');C=Path('assets/warder/downloads.json');cat=json.loads(C.read_text());assets=cat.get('assets',cat)
def sha(b):return hashlib.sha256(b).hexdigest()
keys={'transparent':'piconProv-220','white':'piconProv-w','black':'piconProv-b'}
raw={s:(A/s/'piconProv.zip').read_bytes() for s in keys}
for s in raw:
 assert sha(raw[s])==plan['baseline'][s]['sha256']==assets[keys[s]]['sha256']
zs={s:zipfile.ZipFile(io.BytesIO(b)) for s,b in raw.items()}
for s,z in zs.items():assert z.testzip() is None and len(z.namelist())==plan['baseline'][s]['count'] and len(set(z.namelist()))==len(z.namelist())
def read(z,n):return np.asarray(Image.open(io.BytesIO(z.read(n))).convert('RGBA')).copy()
y,x=np.indices((132,220));edge=(x<7)|(x>212)|(y<7)|(y>124);points=[(0,0),(0,110),(131,110),(10,10),(10,209),(121,10),(121,209),(66,2),(66,217)]
def key(a):return tuple(int(v) for p in points for v in a[p])
models={}
for s in ('white','black'):
 groups=collections.defaultdict(list)
 for n in zs[s].namelist():
  a=read(zs[s],n)
  if a.shape!=(132,220,4):continue
  groups[key(a)].append(n)
 models[s]=[]
 for k,ns in sorted(groups.items(),key=lambda v:-len(v[1]))[:16]:
  if len(ns)<8:continue
  sample=[ns[i] for i in np.linspace(0,len(ns)-1,min(len(ns),160),dtype=int)]
  arr=np.sort(np.stack([read(zs[s],n) for n in sample]).view(np.uint32).squeeze(-1),axis=0)
  last=arr[0].copy();cur=np.ones(arr.shape[1:],np.int16);best=cur.copy();value=last.copy()
  for i in range(1,len(arr)):
   same=arr[i]==last;cur=np.where(same,cur+1,1);take=cur>best;value=np.where(take,arr[i],value);best=np.maximum(best,cur);last=arr[i]
  bg=value.view(np.uint8).reshape((132,220,4));models[s].append((bg,best/len(arr),len(ns)))
def extract_one(a,s):
 rgb=a[:,:,:3].astype(float)
 def score(t):
  d=np.max(np.abs(a.astype(float)-t[0].astype(float)),2)[edge];return np.median(d)+np.percentile(d,75)*.4
 bg,conf,N=min(models[s],key=score);b=bg[:,:,:3].astype(float);d=rgb-b;mag=np.max(np.abs(d),2);fit=score((bg,conf,N))
 tol=np.where(conf>.6,4,np.where(conf>.3,8,14));tol=np.maximum(tol,min(18,float(np.percentile(mag[edge],75))+3));mask=(mag>=tol)&(a[:,:,3]>20)
 mask[:3]=False;mask[-3:]=False;mask[:,:3]=False;mask[:,-3:]=False
 lab,_=label(mask);sizes=np.bincount(lab.ravel());keep=sizes>=3;keep[0]=False;mask=keep[lab]
 min_alpha=np.max(np.where(d>=0,d/np.maximum(255-b,1),-d/np.maximum(b,1)),axis=2);min_alpha=np.clip(min_alpha,0,1)
 hi=rgb.max(2);lo=rgb.min(2);neutral=(hi-lo<40)&(hi>65)&mask
 if s=='black':
  white_alpha=np.clip(np.sum(d*(255-b),2)/np.maximum(np.sum((255-b)**2,2),1),0,1);alpha=np.where(neutral,white_alpha,min_alpha)
 else:alpha=min_alpha
 return bg,mask,alpha,fit,neutral,conf
def extract(n):
 a=read(zs['black'],'piconProv/'+n);w=read(zs['white'],'piconProv/'+n);bg,mb,alpha,fit,neutral,conf=extract_one(a,'black');wg,mw,wa,wfit,_,wc=extract_one(w,'white')
 support=binary_dilation(mw,iterations=2);mask=mb&(support|(conf>.75));lab,_=label(mask);sz=np.bincount(lab.ravel());keep=sz>=3;keep[0]=False;mask=keep[lab]
 rgb=a[:,:,:3].astype(float);b=bg[:,:,:3].astype(float);d=rgb-b;dist=distance_transform_edt(mask);alpha=np.where(neutral,alpha,np.maximum(alpha,np.where(dist>=1.5,1,np.where(dist>=1,.85,0))));alpha=np.where(mask,np.clip(alpha,0,1),0);fg=np.clip(b+d/np.maximum(alpha[...,None],1e-6),0,255);fg[neutral&mask]=255
 rgba=np.round(np.dstack((fg,alpha*255))).astype(np.uint8);rgba[rgba[:,:,3]==0,:3]=0;im=Image.fromarray(rgba)
 assert fit==0 and wfit==0 and (mask&support).sum()/max(mask.sum(),1)>.99
 return im
h=hashlib.sha256();adds={}
for n in sorted(plan['names']):
 path='piconProv/'+n;assert path not in zs['transparent'].namelist() and all(path in zs[s].namelist() for s in ('white','black'))
 im=extract(n);assert im.size==(220,132) and im.getchannel('A').getextrema()[0]==0 and im.getchannel('A').getbbox()
 h.update(n.encode()+b'\0'+im.tobytes());buf=io.BytesIO();im.save(buf,'PNG',optimize=True);adds[path]=buf.getvalue()
assert len(adds)==29 and h.hexdigest()==plan['pixel_digest'],(len(adds),h.hexdigest())
old=set(zs['transparent'].namelist());assert not {n.casefold() for n in old}&{n.casefold() for n in adds}
out=io.BytesIO(raw['transparent'])
with zipfile.ZipFile(out,'a',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
 for n,b in sorted(adds.items()):z.writestr(zipfile.ZipInfo(n,(1980,1,1,0,0,0)),b,compress_type=zipfile.ZIP_DEFLATED,compresslevel=9)
after=out.getvalue()
with zipfile.ZipFile(io.BytesIO(after)) as z:
 assert z.testzip() is None and set(z.namelist())==old|set(adds) and all(z.read(n)==zs['transparent'].read(n) for n in old) and all(z.read(n)==b for n,b in adds.items())
assert len(after)<32*1024*1024
(A/'transparent'/'piconProv.zip').write_bytes(after);assets[keys['transparent']].update(sha256=sha(after),size=len(after),png_count=len(old)+len(adds));C.write_text(json.dumps(cat,ensure_ascii=False,indent=2)+'\n')
report={'added':len(adds),'count':len(old)+len(adds),'preserved':len(old),'sha256':sha(after),'size':len(after),'pixel_digest':h.hexdigest(),'names':plan['names'],'unchanged_white_black':True}
(P/'build.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(json.dumps(report,ensure_ascii=False))
