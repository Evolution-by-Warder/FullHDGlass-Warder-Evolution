import hashlib,io,json,sys,zipfile,urllib.request,re
from pathlib import Path
from PIL import Image
P=Path(sys.argv[1]);R=Path(sys.argv[2]);work=Path(__file__).parent;out=P/'reports/italia-7g-telepace-20261125';out.mkdir(parents=True,exist_ok=True)
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
hashes={'transparent':'f8bfd80d9656ccc43d834d61b54758d0a34ef42f4a0e16b54189f9327166c990','white':'33c652c0b00221a39c8a1344b13021d15dd6833275c149ef4ef0f240615a82b2','black':'fb9a1db76e9270845579ad13aba2d9f525fdef8d1ea7d6d40a009be16fcfdd92'}
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
from PIL import ImageDraw, ImageFilter
import numpy as np
from scipy.ndimage import label
sources=[
 ('SESTARETE & RETE 8','https://www.litaliaindigitale.it/wp-content/uploads/2024/01/7-GOLD-2024.png','https://www.agcom.it/sites/default/files/documenti/audizioni_parlamentari/Lista%20SIG%202026_0.pdf'),
 ('TELERADIOPACE','https://www.litaliaindigitale.it/wp-content/uploads/2023/06/TELERADIOPACE1-HD-n.png','https://www.diocesichiavari.it/enti/teleradiopace/')
]
records=[];held=[]
def get(u):
 req=urllib.request.Request(u,headers={'User-Agent':'WarderEvolution/1.0 (public picon source review)'})
 with urllib.request.urlopen(req,timeout=40) as r:
  b=r.read(3000001);assert len(b)<=3000000;return b
for name,url,evidence in sources:
 try:
  b=get(url);im=Image.open(io.BytesIO(b)).convert('RGBA');im.load()
  # Accept source transparency or remove only uniform near-white connected outside matte.
  a=np.array(im)
  if a[:,:,3].min()==255:
   bg=(a[:,:,:3].min(axis=2)>=248)
   lab,count=label(bg);edge=set(lab[0,:])|set(lab[-1,:])|set(lab[:,0])|set(lab[:,-1]);edge.discard(0)
   exterior=np.isin(lab,list(edge));assert exterior.sum()>a.shape[0]*a.shape[1]*.1
   a[exterior,3]=0
  assert a[:,:,3].min()==0 and a[:,:,3].max()==255
  im=Image.fromarray(a);im=im.crop(im.getchannel('A').getbbox())
  factor=min(194/im.width,108/im.height)
  im=im.resize((max(1,round(im.width*factor)),max(1,round(im.height*factor))),Image.Resampling.LANCZOS)
  fg=Image.new('RGBA',(220,132));fg.alpha_composite(im,((220-im.width)//2,(132-im.height)//2))
  (out/(name+'-source.png')).write_bytes(b)
  for s in keys:
   if s=='transparent':dst=fg.copy()
   else:
    template=(work/(s+'-sablona.png')).read_bytes()
    assert sha(template)=={'white':'c6ae4a808a65ffc8e6458336fccbfe4216de1e832ec0a9abf800907f2f783589','black':'61e69f7fc46e340453bf74ccd7af6ac9d8eba9f8e232884659e1ea99f6abf3fe'}[s]
    # Preserve colors; thin neutral edge only if required to retain pale text on white.
    layer=fg.copy()
    if s=='white' and name=='TELERADIOPACE':
     edge=fg.getchannel('A').filter(ImageFilter.MaxFilter(3)).point(lambda v:round(v*.55))
     outline=Image.new('RGBA',fg.size,(40,44,48,0));outline.putalpha(edge);layer=Image.alpha_composite(outline,fg)
    dst=Image.alpha_composite(Image.open(io.BytesIO(template)).convert('RGBA'),layer)
   buf=io.BytesIO();dst.save(buf,'PNG',optimize=True);d=buf.getvalue();valid(d);assert n(name) not in allstyle[s];deltas[s][n(name)]=d
   (out/(s+'-'+name+'.png')).write_bytes(d)
  records.append({'name':name,'source_url':url,'source_sha256':sha(b),'identity_evidence':evidence,'source_dimensions':list(Image.open(io.BytesIO(b)).size)})
 except Exception as e:
  for s in keys:deltas[s].pop(n(name),None)
  held.append({'name':name,'error':repr(e)})
assert records
report={'base':'8afd39c48c16366290a3af4da796fbad111721ba','new_png':sum(map(len,deltas.values())),'complete_provider_names':len(records),'records':records,'held':held,'archives':[]}
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
(out/'README.md').write_text('Current 7G identity confirmed by AGCOM 2026 list page 6. Teleradiopace Chiavari logo per June 2023 monitoring and official diocese identity. All original PNG retained, four white extensions, no IPK or DTT change. Visual review required before merge.\n')
print(json.dumps(report))
