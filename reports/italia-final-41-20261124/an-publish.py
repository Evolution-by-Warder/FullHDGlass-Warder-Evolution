import hashlib,io,json,sys,zipfile,urllib.request,re
from pathlib import Path
from PIL import Image
P=Path(sys.argv[1]);R=Path(sys.argv[2]);work=Path(__file__).parent;out=P/'reports/italia-an-20261125';out.mkdir(parents=True,exist_ok=True)
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
hashes={'transparent':'d24985eb4bfda876bb96f3a63c16b73642593b09d320103c73991861fff0dd19','white':'33c652c0b00221a39c8a1344b13021d15dd6833275c149ef4ef0f240615a82b2','black':'6ba557c2b4a4a96defc9b4bbe4787c5367f854e24ce3ac7f93d86c3019fe1ba8'}
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
url='https://upload.wikimedia.org/wikipedia/commons/c/cc/Antenna_3_Toscana_-_logo.png'
req=urllib.request.Request(url,headers={'User-Agent':'WarderEvolution/1.0 (public logo review; https://warder-evolution.eu)'})
with urllib.request.urlopen(req,timeout=40) as response:src=response.read(1000001)
assert len(src)==55012 and hashlib.sha1(src).hexdigest()=='d63912f81bdde834b641f1e14a8051cc805575b9'
im=Image.open(io.BytesIO(src)).convert('RGBA');assert im.size==(483,518) and im.getchannel('A').getextrema()==(0,255)
im=im.crop(im.getchannel('A').getbbox());im.thumbnail((194,108),Image.Resampling.LANCZOS)
fg=Image.new('RGBA',(220,132));fg.alpha_composite(im,((220-im.width)//2,(132-im.height)//2))
(out/'AN-source.png').write_bytes(src)
for s in keys:
 if s=='transparent':dst=fg.copy()
 else:
  template=(work/(s+'-sablona.png')).read_bytes()
  assert sha(template)=={'white':'c6ae4a808a65ffc8e6458336fccbfe4216de1e832ec0a9abf800907f2f783589','black':'61e69f7fc46e340453bf74ccd7af6ac9d8eba9f8e232884659e1ea99f6abf3fe'}[s]
  dst=Image.alpha_composite(Image.open(io.BytesIO(template)).convert('RGBA'),fg)
 buf=io.BytesIO();dst.save(buf,'PNG',optimize=True);d=buf.getvalue();valid(d);assert n('AN') not in allstyle[s];deltas[s][n('AN')]=d
 (out/(s+'-AN.png')).write_bytes(d)
report={'base':'8e65c33210beeec19178a17cce1040c99f03d515','new_png':3,'complete_provider_names':1,'identity':'Antenna 3 Radio Televisione Toscana','provider':'An','provider_evidence':'https://www.digital-forum.it/threads/segnali-tv-in-toscana-riassegnazioni-tv-nazionali-e-locali-2022.212576/page-48','official_station':'https://www.antenna3.tv/','source':url,'source_sha256':sha(src),'source_sha1':hashlib.sha1(src).hexdigest(),'archives':[]}
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
(out/'README.md').write_text('AN provider: Antenna 3 Radio Televisione Toscana, actual DVB measurement explicitly lists Provider: An, current broadcaster confirmed by official website. Exact green/pink artwork matches supplied original, 483x518 transparent source pinned by SHA1. Uses original MASTER V9 templates pinned by SHA256; no previous PNG changed, no DTT/IPK changes. Review before merge.\n')
print(json.dumps(report))
