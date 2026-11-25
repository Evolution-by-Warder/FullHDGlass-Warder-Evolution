import hashlib,io,json,sys,zipfile,urllib.request,re
from pathlib import Path
from PIL import Image
P=Path(sys.argv[1]);R=Path(sys.argv[2]);work=Path(__file__).parent;out=P/'reports/italia-doria-20261125';out.mkdir(parents=True,exist_ok=True)
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
hashes={'transparent':'0a9d0be0d5dbd641a991f58b444552c65cc2b972cad8a7ad3b69bbd305fe0e8b','white':'33c652c0b00221a39c8a1344b13021d15dd6833275c149ef4ef0f240615a82b2','black':'1a49db09ed584b96936b7bfb4d1942ce5bda2d095fe8aa423fcb7c69a1e762c0'}
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
ref='1_0_16_1C2E_384_110_5A0000_0_0_0.png'
donors={'transparent':'8a51042c2e8c7c79d524a5a6df19e1e9f196152757d267c2274111b0dfa5f1d2','white':'39471fa8bc19a2be5c67c64967f112b1fce8ab43e9fe95972a7dc173a439d0ae','black':'1f7fceeed3ec89253c42164f06e1f3b4ad157f685f408ef1048a1bf0c2ccd92e'}
for s in keys:
 b=(R/('90E_channel-'+s+'_'+ref)).read_bytes();assert sha(b)==donors[s];valid(b)
 assert n('DORIA') not in allstyle[s];deltas[s][n('DORIA')]=b;(out/(s+'-DORIA.png')).write_bytes(b)
report={'morpheus_lamedb_blob':'1604eb1f78ddf5ac6feee5739b7e9d54acc35fb3','observed_provider':'doria','observed_services':[{'sid':6805,'tsid':26849,'onid':8572,'name':'RadioRomaTelevision'},{'sid':6806,'tsid':26849,'onid':8572,'name':'Radio Roma'}],'group_evidence':'https://www.litaliaindigitale.it/news-regionali/lazio-news/lazio-news-anno-2024/240918-mux-locale-1-lazio-passaggio-in-alta-definizione-per-t9/','base':'bca222b85cd872ed1a9099364a8ed2e0bc227e80','new_png':3,'complete_provider_names':1,'reference':ref,'source':'https://en.kingofsat.net/freqs.php?aff=zap&b=325&filtre=no&lim=80&ordre=freq&pos=9E&standard=Digital','identity_history':'https://www.agcom.it/sites/default/files/migration/delibera/Delibera%2066-23-CONS.pdf','donor_run':45563401111,'donors':donors,'archives':[]}
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
(out/'README.md').write_text('DORIA: legacy provider alias, exact doria found in Morpheus motor lamedb (blob 1604eb1f78ddf5ac6feee5739b7e9d54acc35fb3) for RadioRomaTelevision and Radio Roma, SID 6805/6806, TSID 26849, ONID 8572. AGCOM decision 66/23/CONS confirms transfer from Doria Srl to Andrea Amici in 2022. Current Radio Roma TV services belong to Amici Network group; use original supplied Amici Network identity via exact approved MASTER V9 donor in all three styles. Current field in other settings may differ. No previous PNG changed; no DTT or IPK change.\n')
print(json.dumps(report))
