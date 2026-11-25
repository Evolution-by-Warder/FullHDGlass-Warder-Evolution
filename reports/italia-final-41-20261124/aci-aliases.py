import hashlib,io,json,sys,zipfile,urllib.request,re
from pathlib import Path
from PIL import Image
P=Path(sys.argv[1]);R=Path(sys.argv[2]);work=Path(__file__).parent;out=P/'reports/italia-aci-aliases-20261125';out.mkdir(parents=True,exist_ok=True)
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
hashes={'transparent':'d82907279fcb5c5b8318d04381ff72caf330d53db3d0b7905223fee848c2141f','white':'33c652c0b00221a39c8a1344b13021d15dd6833275c149ef4ef0f240615a82b2','black':'a799ec5b44d3aebe1c0da9d2f13b5ea4107269a0a8c4f9490f13b7269e654400'}
aci_hash={'transparent':'0e755cfd3b49a8cadc96ecaaaae8b104133b0b58e5ddec7b90371797e8760951','white':'2e6f044ff926bd26cd6baafcf286ac2fb982ae68987424333262d494a4065587','black':'8f631a66a8e38db30b9e8749bf4738554137cf6ed354e0d28a7c22121672215e'}
baseline={};allstyle={};deltas={s:{} for s in keys}
for s,key in keys.items():
 a=assets[key];assert a['sha256']==hashes[s];path=A/s/'piconProv.zip';raw,z=verify(path,a)
 values={k:z.read(k) for k in z.namelist()};baseline[s]=(raw,z,path)
 if s=='white':
  v=assets[key+'-v2'];assert v['base_sha256']==hashes[s] and len(v['extensions'])==2
  for i,e in enumerate(v['extensions'],1):
   b,ez=verify(A/s/f'extension-{i:02d}'/'piconProv.zip',e);assert not set(ez.namelist())&set(values);values.update({k:ez.read(k) for k in ez.namelist()})
  assert len(values)==v['png_count'] and sum(map(len,values.values()))==v['unpacked_size']
 allstyle[s]=values
 b=(R/'donor-review'/s/'ACI-Sport-TV-donor.png').read_bytes();assert sha(b)==aci_hash[s];valid(b)
 (out/(s+'-ACI-Sport-TV.png')).write_bytes(b)
 for target in ['ACISPORT TV','ACISPORT_TV']:
  if s=='black' and target=='ACISPORT_TV':assert n(target) in values;continue
  assert n(target) not in values;deltas[s][n(target)]=b
# Historical provider alias: both existing W and B must match the exact same donor bytes; no replacement.
aliases=[('AUSTRIASAT','HD AUSTRIA','https://www.prosiebensat1.com/en/newsroom/prosiebensat1-group-signs-contract-with-m7-group-to-start-four-austrian-hd-broadcasters-en-336230'),
('DIGITAL FREE','KABEL DEUTSCHLAND','https://www.dwdl.de/nachrichten/3078/kabel_deutschland_startet_am_2009_kabel_digital_free/'),
('W1 WL DTH','NETERRA COMMUNICATIONS','https://satkurier.pl/news/84505/0-8w-tiankov-tv-fta-w-nowej-platformie-w1.html')]
done=[];held=[]
for target,donor,source in aliases:
 try:
  assert all(allstyle[s][n(target)]==allstyle[s][n(donor)] for s in ('white','black'))
  b=allstyle['transparent'][n(donor)];valid(b);assert n(target) not in allstyle['transparent']
  deltas['transparent'][n(target)]=b;done.append({'target':target,'donor':donor,'source':source,'sha256':sha(b)})
 except (KeyError,AssertionError) as e:held.append({'target':target,'reason':'exact donor proof missing'})
report={'base':'22e4ba3e6240db91b2dc50816c7f902c4dbb565e','new_png':sum(map(len,deltas.values())),'complete_provider_names':2+len(done),'aci_reference':'1_0_16_64D_2454_13E_820000_0_0_0.png','aci_source':'https://www.lyngsat.com/muxes/Hotbird-13G_Wide_12577-H.html','aci_donor_run':45559469078,'aliases':done,'held':held,'archives':[]}
for s,key in keys.items():
 d=deltas[s];old=allstyle[s];assert not {k.casefold() for k in d}&{k.casefold() for k in old}
 a=assets[key];raw,z,path=baseline[s]
 if s=='white':
  v=assets[key+'-v2'];e=dict(v['extensions'][-1]);b=pack(d);np=A/s/'extension-03'/'piconProv.zip';assert not np.exists();np.parent.mkdir(parents=True);np.write_bytes(b)
  e.update(png_count=len(d),size=len(b),sha256=sha(b),url=e['url'].replace('extension-02','extension-03'));v['extensions'].append(e);v['png_count']+=len(d);v['unpacked_size']+=sum(map(len,d.values()))
  assert path.read_bytes()==raw
  with zipfile.ZipFile(io.BytesIO(b)) as nz:assert nz.testzip() is None and set(nz.namelist())==set(d) and all(nz.read(k)==v for k,v in d.items())
  report['archives'].append(dict(style=s,count=v['png_count'],new_extension_sha256=sha(b),new_extension_bytes=len(b),previous_archives_unchanged=True))
 else:
  b=pack(d,raw);assert len(b)<=32*1024*1024
  with zipfile.ZipFile(io.BytesIO(b)) as nz:
   assert nz.testzip() is None and set(nz.namelist())==set(old)|set(d)
   assert all(nz.read(k)==v for k,v in old.items()) and all(nz.read(k)==v for k,v in d.items())
  path.write_bytes(b);a.update(size=len(b),sha256=sha(b),png_count=len(old)+len(d))
  report['archives'].append(dict(style=s,count=a['png_count'],sha256=sha(b),bytes=len(b),old_png_unchanged=True))
C.write_text(json.dumps(catalog,ensure_ascii=False,indent=2)+'\n')
(out/'build.json').write_text(json.dumps(report,indent=2)+'\n')
(out/'README.md').write_text('Owner-approved Italian continuation. Original clean ACI Sport TV donor from exact 13E reference and verified production archive, visually checked, no reconstruction. Added missing aliases, existing black ACISPORT_TV preserved. Other historical aliases only where both W/B equal approved donor byte-for-byte and public evidence supports identity. No DTT/IPK change. Hungarian AustriaSat variants not supplemented: Hungarian service ended 30 April 2016 per https://dtvnews.hu/hirek/megszunik-az-austriasat-magyarorszag-dth-szolgaltatasa; existing legacy PNGs retained.\n')
print(json.dumps(report))
# Candidate donor extraction from current DTT Italy for remaining matching station brands. Review only.
review=Path('dtt-donor-review');review.mkdir(exist_ok=True)
try:
 m=json.loads((P/'assets/warder/downloads/picons/channels/manifest.json').read_text())
 recipe=json.loads((P/'reports/dtt-italia-20261123/recipe.json').read_text())
 plan=json.loads((P/'reports/italia-dtt-vhannibal-19-20261124/plan.json').read_text())
 refs={}
 wanted=re.compile(r'tele.?pace|teleradio.?pace|telesette|video.?regione|radio.?mater|teleacras|7gold|sestarete|doria|europa.?7|eclutch|antenna.?3|tvc[m]|digital.?dream',re.I)
 for k,v in recipe['selectors']['DTT_ITALIA'].items():
  if wanted.search(v.get('name','')):refs[k+'.png']=v['name']
 for k,v in plan['refs'].items():
  if wanted.search(v):refs[k]=v
 meta={p['filename']:p for p in m['parts']};matches=[]
 def get(u):
  with urllib.request.urlopen(u,timeout=60) as r:return r.read()
 for p in m['packages']:
  if p['selector_id']!='DTT_ITALIA' or p['resolution']!='220x132':continue
  s=p['family'].split('-')[-1];chunks=[]
  for u in p['parts']:
   nn=u.rsplit('/',1)[-1];b=get('https://raw.githubusercontent.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/22e4ba3e6240db91b2dc50816c7f902c4dbb565e/assets/warder/downloads/picons/channels/'+nn);assert len(b)==meta[nn]['bytes'] and sha(b)==meta[nn]['sha256'];chunks.append(b)
  b=b''.join(chunks);assert sha(b)==p['sha256']
  with zipfile.ZipFile(io.BytesIO(b)) as z:
   for name in z.namelist():
    basename=name.rsplit('/',1)[-1];found=[(k,v) for k,v in refs.items() if basename==k or (not k.endswith('.png') and basename.startswith(k+'_'))]
    if not found:continue
    k,v=found[0];d=z.read(name);valid(d);dest=review/s;dest.mkdir(exist_ok=True);(dest/basename).write_bytes(d);matches.append({'style':s,'name':v,'ref':basename,'sha256':sha(d)})
 (review/'matches.json').write_text(json.dumps(matches,ensure_ascii=False,indent=2))
except Exception as e:(review/'error.txt').write_text(str(e))
