import hashlib,io,json,sys,zipfile,urllib.request,re
from pathlib import Path
from PIL import Image
P=Path(sys.argv[1]);R=Path(sys.argv[2]);work=Path(__file__).parent;out=P/'reports/italia-radio-mater-20261125';out.mkdir(parents=True,exist_ok=True)
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
hashes={'transparent':'04bfd97db1c4b9f7653204cae07ea66e7f7092acce825433a6fccc9c90c3aa75','white':'33c652c0b00221a39c8a1344b13021d15dd6833275c149ef4ef0f240615a82b2','black':'083d97f79096b14a039290d3031d4edb1e4d9f0e9e8fea940bc6d4f529a06f45'}
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
# The DAB label is a recovered alpha mask from the owner-supplied source, not invented lettering.
import base64,zlib
alpha=Image.frombytes('L',(59,25),zlib.decompress(base64.b64decode((work/'mater-dab-alpha.b64').read_text())))
src=(R/'90E_channel-transparent_1_0_16_7D1_20E1_217C_5A0000_0_0_0.png').read_bytes()
assert sha(src)=='e4f38fdb1a9e2c671e5ea5d19cbd38de0cf4830b5e892476a8e83ace04182b37'
(out/'radio-mater-approved-donor.png').write_bytes(src)
logo=Image.open(io.BytesIO(src)).convert('RGBA');logo.paste((0,0,0,0),(200,118,220,132));logo=logo.crop(logo.getbbox());logo.thumbnail((178,112),Image.Resampling.LANCZOS)
canvas=Image.new('RGBA',(220,132));canvas.alpha_composite(logo,(12,(132-logo.height)//2))
t=Image.new('RGBA',alpha.size,(0,148,235));t.putalpha(alpha);canvas.alpha_composite(t,(220-t.width-8,8))
for s in keys:
 if s=='transparent':dst=canvas.copy()
 else:
  template=(work/(s+'-sablona.png')).read_bytes()
  assert sha(template)=={'white':'c6ae4a808a65ffc8e6458336fccbfe4216de1e832ec0a9abf800907f2f783589','black':'61e69f7fc46e340453bf74ccd7af6ac9d8eba9f8e232884659e1ea99f6abf3fe'}[s]
  dst=Image.alpha_composite(Image.open(io.BytesIO(template)).convert('RGBA'),canvas)
 b=io.BytesIO();dst.save(b,'PNG',optimize=True);d=b.getvalue();valid(d)
 assert n('RADIO MATER DAB%2A') not in allstyle[s];deltas[s][n('RADIO MATER DAB%2A')]=d
 (out/(s+'-RADIO-MATER-DAB.png')).write_bytes(d)
report={'base':'884e555486e32764129ba442ba7ec50f4b6336bb','new_png':3,'complete_provider_names':1,'identity_source':'https://it.kingofsat.info/radio-9.0E','official_source':'https://www.radiomater.org/P/Content?name=Frequenze','donor_run':45563401111,'donor_reference':'1_0_16_7D1_20E1_217C_5A0000_0_0_0.png','donor_sha256':sha(src),'dab_mask_sha256':sha(alpha.tobytes()),'archives':[]}
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
(out/'README.md').write_text('Radio Mater DAB* verified current 9E provider SID 2001, TSID 8417, NID 8572. Approved clean Radio Mater artwork from existing exact multiplex/service donor; original DAB lettering recovered from supplied provider raster, with all 3 variants visually reviewed before merge. No other PNG changed. DGB3 historical Mooz 4K service removed October 2021: https://www.satindex.de/sender-updates/2021-10/ . Keep prior black historical PNG; no new variants for retired label without new evidence. No DTT or IPK changes.\n')
print(json.dumps(report))
