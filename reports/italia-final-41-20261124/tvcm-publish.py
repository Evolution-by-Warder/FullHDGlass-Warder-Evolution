import hashlib,io,json,sys,zipfile,urllib.request,re
from pathlib import Path
from PIL import Image
P=Path(sys.argv[1]);R=Path(sys.argv[2]);work=Path(__file__).parent;out=P/'reports/italia-tvcm-20261125';out.mkdir(parents=True,exist_ok=True)
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
hashes={'transparent':'b713864f13d519c427814b3666109a8f98ee0bdda29b84aa3b3256299573e34a','white':'33c652c0b00221a39c8a1344b13021d15dd6833275c149ef4ef0f240615a82b2','black':'87a33f09fd88db1fe26d3fa88dc28d17d5a7f173da290046f9c18f35bae4b1a0'}
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
ref='1_0_19_1771_60E1_217C_5A0000_0_0_0.png'
donors={'transparent':'d58b51be87e3d579218661de19934743254638eb70e01e45b5d2184ed9a3e7e3','white':'fc5fe9c0ec80176cb12013072f93a196f28e43473a164cb8bab9331b3963bc95','black':'c1527d85200737662eeb25287b0deaaa546eada49949eb5a66263ce46851d17f'}
for s in keys:
 b=(R/('90E_channel-'+s+'_'+ref)).read_bytes();assert sha(b)==donors[s];valid(b)
 assert n('TVCM') not in allstyle[s];deltas[s][n('TVCM')]=b;(out/(s+'-TVCM.png')).write_bytes(b)
report={'base':'0449f449bd0ebcb8086dde953943e3f79c4f0473','new_png':3,'complete_provider_names':1,'reference':ref,'source':'https://www.lyngsat.com/Eutelsat-9B-and-Ka-Sat-9A.html','identity_history':'https://www.litaliaindigitale.it/sites.google.com/site/litaliaindigitale/marcheindigitale/muxtvcentromarche/muxtvcentromarchearchivionewsdal2012al2015.html','donor_run':45565820791,'donors':donors,'archives':[]}
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
(out/'README.md').write_text('TVCM: TV Centro Marche, exact approved 9E donor in all three backgrounds. Current satellite SID 6001 TSID 24801 ONID 8572 independently verified; historical TVCM alias verified. Same woodpecker and HD brand as supplied original. All prior PNG bytes preserved, no IPK or DTT change.\n')
print(json.dumps(report))
