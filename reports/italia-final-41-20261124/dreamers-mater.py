import hashlib,io,json,sys,zipfile,urllib.request,re
from pathlib import Path
from PIL import Image
P=Path(sys.argv[1]);R=Path(sys.argv[2]);work=Path(__file__).parent;out=P/'reports/italia-dreamers-mater-20261125';out.mkdir(parents=True,exist_ok=True)
A=P/'assets/warder/downloads/picons/providers';C=P/'assets/warder/downloads.json';catalog=json.loads(C.read_text());assets=catalog['assets']
def sha(b):return hashlib.sha256(b).hexdigest()
def verify(path,a):
 b=path.read_bytes();assert len(b)==a['size'] and sha(b)==a['sha256'];z=zipfile.ZipFile(io.BytesIO(b));assert z.testzip() is None and len(z.namelist())==a['png_count'];return b,z
def pack(values,base=None):
 b=io.BytesIO(base or b'')
 with zipfile.ZipFile(b,'a' if base else 'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
  for n,d in sorted(values.items()):z.writestr(zipfile.ZipInfo(n,(1980,1,1,0,0,0)),d,compress_type=zipfile.ZIP_DEFLATED,compresslevel=9)
 return b.getvalue()
def valid(b):
 im=Image.open(io.BytesIO(b));im.load();assert im.size==(220,132) and im.mode=='RGBA'
def n(s):return 'piconProv/'+s+'.png'
keys={'transparent':'piconProv-220','white':'piconProv-w','black':'piconProv-b'}
hashes={'transparent':'fec84946799e57b286b4db4b5d541a51fe74816965e9bcca241907fcf8985495','white':'33c652c0b00221a39c8a1344b13021d15dd6833275c149ef4ef0f240615a82b2','black':'a759cc100c0f1237d90377420c382ac01db6a1c3eabcd7b744571c87e982b6b1'}
baseline={};allstyle={};deltas={s:{} for s in keys}
for s,key in keys.items():
 a=assets[key];assert a['sha256']==hashes[s];path=A/s/'piconProv.zip';raw,z=verify(path,a)
 values={k:z.read(k) for k in z.namelist()};baseline[s]=(raw,z,path)
 if s=='white':
  v=assets[key+'-v2'];assert v['base_sha256']==hashes[s] and len(v['extensions'])==4
  for i,e in enumerate(v['extensions'],1):
   b,ez=verify(A/s/f'extension-{i:02d}'/'piconProv.zip',e);assert not set(ez.namelist())&set(values);values.update({k:ez.read(k) for k in ez.namelist()})
  assert len(values)==v['png_count'] and sum(map(len,values.values()))==v['unpacked_size']
 allstyle[s]=values
# Clean recovery of the exact horizontal official JPEG, keeping internal lettering and colored components.
import numpy as np
from scipy.ndimage import binary_fill_holes,binary_dilation
src=(R/'next-logo-review/ASSOCIAZIONE_DREAMER_1.jpg').read_bytes()
assert sha(src)=='fdbcf237d500a581cce6895952ca69fb3970032a5ee105f38a05702150c64adc'
(out/'digital-dreamers-official.jpg').write_bytes(src)
im=Image.open(io.BytesIO(src)).convert('RGB');a=np.array(im).astype(float)
strength=255-a.mean(axis=2);body=binary_fill_holes(strength>50);core=binary_fill_holes(strength>210)
fringe=binary_dilation(body,iterations=2)&~core
alpha=np.where(core,255,np.where(fringe,np.clip(strength,0,255),0));alpha[body&~fringe]=255
alpha[body&(a.max(axis=2)-a.min(axis=2)>30)]=255
fg=np.zeros((a.shape[0],a.shape[1],4),dtype=np.uint8)
fg[:,:,:3]=np.where((alpha<254)[:,:,None],np.clip((a-255*(1-alpha[:,:,None]/255))/np.maximum(alpha[:,:,None]/255,1e-5),0,255),a).astype('uint8')
fg[:,:,3]=alpha.round().astype('uint8');im=Image.fromarray(fg);im=im.crop(im.getbbox());im.thumbnail((194,108),Image.Resampling.LANCZOS)
logo=Image.new('RGBA',(220,132));logo.alpha_composite(im,((220-im.width)//2,(132-im.height)//2))
for s in keys:
 if s=='transparent':dst=logo
 else:
  t=(work/(s+'-sablona.png')).read_bytes()
  assert sha(t)=={'white':'c6ae4a808a65ffc8e6458336fccbfe4216de1e832ec0a9abf800907f2f783589','black':'61e69f7fc46e340453bf74ccd7af6ac9d8eba9f8e232884659e1ea99f6abf3fe'}[s]
  dst=Image.alpha_composite(Image.open(io.BytesIO(t)).convert('RGBA'),logo)
 buf=io.BytesIO();dst.save(buf,'PNG',optimize=True);d=buf.getvalue();valid(d)
 (out/(s+'-DIGITAL-DREAMERS.png')).write_bytes(d)
 for name in ['ASSOCIAZIONE DREAMER','ASSOCIAZIONE_DREAMER']:
  if n(name) in allstyle[s]:
   assert name=='ASSOCIAZIONE_DREAMER' and s=='black'
   (out/'black-existing-alias.png').write_bytes(allstyle[s][n(name)])
  else:deltas[s][n(name)]=d
assert sum(map(len,deltas.values()))==5
# Radio Mater exact station name and service reference, retrieve verified production archive parts.
mater_ref='1_0_1_7D1_20E1_217C_5A0000_0_0_0.png'
mater={}
try:
 m=json.loads((P/'assets/warder/downloads/picons/channels/manifest.json').read_text())
 recipe=json.loads((P/'reports/dtt-italia-20261123/recipe.json').read_text())
 assert recipe['selectors']['90E'][mater_ref[:-4]]['name']=='RADIO MATER DAB*'
 meta={p['filename']:p for p in m['parts']}
 def get(u):
  with urllib.request.urlopen(u,timeout=60) as r:return r.read()
 for p in m['packages']:
  if p['selector_id']!='90E' or p['resolution']!='220x132':continue
  s=p['family'].split('-')[-1];assert s in keys
  chunks=[]
  for u in p['parts']:
   nn=u.rsplit('/',1)[-1];b=get('https://raw.githubusercontent.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/deb96b7808b5abbca87b02897e4537938219e5d8/assets/warder/downloads/picons/channels/'+nn)
   assert len(b)==meta[nn]['bytes'] and sha(b)==meta[nn]['sha256'];chunks.append(b)
  b=b''.join(chunks);assert sha(b)==p['sha256']
  with zipfile.ZipFile(io.BytesIO(b)) as z:
   matches=[x for x in z.namelist() if x.rsplit('/',1)[-1]==mater_ref];assert len(matches)==1
   d=z.read(matches[0]);valid(d);assert n('RADIO MATER DAB%2A') not in allstyle[s]
   mater[s]=d;(out/(s+'-RADIO-MATER-DAB.png')).write_bytes(d)
 assert set(mater)==set(keys)
 for s,d in mater.items():deltas[s][n('RADIO MATER DAB%2A')]=d
 mater_status={'status':'BUILT_REVIEW_REQUIRED','ref':mater_ref,'source':'https://www.radiomater.org/P/Content?id=ef14a3c4-c9a8-4aec-9a7d-f9e2d0a896bf','donor_sha256':{s:sha(d) for s,d in mater.items()}}
except Exception as e:
 for s in keys:deltas[s].pop(n('RADIO MATER DAB%2A'),None)
 mater_status={'status':'HOLD','error':str(e)}
report={'base':'deb96b7808b5abbca87b02897e4537938219e5d8','new_png':sum(map(len,deltas.values())),'complete_provider_names':2+(mater_status['status']=='BUILT_REVIEW_REQUIRED'),'dreamers_source':'https://www.associazionedigitaldreamers.it/wp-content/uploads/2019/09/logoDD_colore_esteso-1.jpg','dreamers_source_sha256':sha(src),'mater':mater_status,'archives':[]}
for s,key in keys.items():
 d=deltas[s];old=allstyle[s];assert not {k.casefold() for k in d}&{k.casefold() for k in old}
 a=assets[key];raw,z,path=baseline[s]
 if s=='white':
  v=assets[key+'-v2'];assert len(v['extensions'])==4
  e=v['extensions'][-1];np=A/s/'extension-04'/'piconProv.zip'
  old_ext,ez=verify(np,e);b=pack(d,old_ext)
  assert len(b)<=32*1024*1024
  with zipfile.ZipFile(io.BytesIO(b)) as nz:
   assert nz.testzip() is None and set(nz.namelist())==set(ez.namelist())|set(d)
   assert all(nz.read(k)==ez.read(k) for k in ez.namelist()) and all(nz.read(k)==v for k,v in d.items())
  np.write_bytes(b);e.update(png_count=e['png_count']+len(d),size=len(b),sha256=sha(b));v['png_count']+=len(d);v['unpacked_size']+=sum(map(len,d.values()))
  assert path.read_bytes()==raw
  report['archives'].append(dict(style=s,count=v['png_count'],extension04_sha256=sha(b),extension04_bytes=len(b),all_existing_png_bytes_unchanged=True))
 else:
  b=pack(d,raw);assert len(b)<=32*1024*1024
  with zipfile.ZipFile(io.BytesIO(b)) as nz:
   assert nz.testzip() is None and set(nz.namelist())==set(old)|set(d)
   assert all(nz.read(k)==v for k,v in old.items()) and all(nz.read(k)==v for k,v in d.items())
  path.write_bytes(b);a.update(size=len(b),sha256=sha(b),png_count=len(old)+len(d))
  report['archives'].append(dict(style=s,count=a['png_count'],sha256=sha(b),bytes=len(b),all_existing_png_bytes_unchanged=True))
C.write_text(json.dumps(catalog,ensure_ascii=False,indent=2)+'\n')
(out/'build.json').write_text(json.dumps(report,indent=2)+'\n')
(out/'README.md').write_text('Owner-approved continuation. Digital Dreamers official horizontal logo, white-matte extraction preserving internal lettering; two aliases. Radio Mater DAB exact 9E donor if available; visual review required. Existing PNGs preserved, 4 white extensions retained; no DTT/IPK change.\n')
print(json.dumps(report))
