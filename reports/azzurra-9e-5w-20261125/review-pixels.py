import concurrent.futures,hashlib,io,json,re,urllib.request,zipfile
from pathlib import Path
BASE='896a2fb62ba3e97769949172d4961e5932806e26'
RAW='https://raw.githubusercontent.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/'+BASE+'/'
C='assets/warder/downloads/picons/channels/'
P=Path('review-output');P.mkdir(exist_ok=True)
T=set('1_0_'+v+'_'+ns+'_0_0_0.PNG' for ns,vs in [('DDE0000','19_1AC_4FB0_55F 19_602_6_20FA 1F_132_4F4C_55F 1F_13A_4F4C_55F 1F_1F_2_217C 1_2BF_50DC_55F 1_2C2_50DC_55F 1_FAB_107_217C 1_FAC_107_217C 1_FAD_107_217C 1_FAE_107_217C 1_FAF_107_217C 1_FB1_107_217C 1_FB3_107_217C 1_FB5_107_217C'),('5A0000','16_19_204_1D 16_1C2A_384_110 16_1E_204_1D 16_2B_190_2324 16_3C_204_1D 16_6E_7918_217C 16_96_7918_217C 16_FA_204_1D 19_363_C35A_9E 19_365_C35A_9E 1F_4E_7918_217C 1F_4F_7918_217C 1_1B63_70E1_217C 1_1B66_70E1_217C 1_1F5_2134_9C 1_1F71_80E3_217C 1_1F9_2134_9C 1_26B_21_16 1_26B_21_B 1_26C_21_16 1_26C_21_B 1_26D_21_16 1_26D_21_B 1_26E_21_16 1_26E_21_B 1_26F_21_16 1_26F_21_B 1_278_21_16 1_278_21_B 1_776_1_64 1_7D2_20E1_217C 1_FA2_107_217C 1_FA3_107_217C 1_FA4_107_217C 1_FAC_107_217C 1_FAD_107_217C 1_FAE_107_217C 1_FAF_107_217C 1_FB1_107_217C 1_FB2_107_217C 1_FB3_107_217C 1_FB5_107_217C 1_FB7_107_217C 2_7D1_20E1_217C')] for v in vs.split())
def sha(b):return hashlib.sha256(b).hexdigest()
def fetch(url):
 with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'WarderEvolution/1.0'}),timeout=100) as r:return r.read()
def get(p):return fetch(RAW+p)
def write(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
sources=[]
for label,url in [('Vhannibal official Motor','https://www.vhannibal.net/download_setting.php?action=download&id=5'),('Vhannibal official Motor Italia','https://www.vhannibal.net/download_setting.php?action=download&id=13'),('Ciefp Motor','https://raw.githubusercontent.com/ciefp/ciefpsettings-enigma2/master/ciefp-E2-motor-75E-34W/lamedb'),('OE-alliance Motor','https://raw.githubusercontent.com/oe-alliance/oe-alliance-settings/master/vhannibal.motor/lamedb'),('Morpheus Motor','https://raw.githubusercontent.com/morpheus883/enigma2-settings/master/morph883_motor/lamedb')]:
 try:
  b=fetch(url)
  if zipfile.is_zipfile(io.BytesIO(b)):
   with zipfile.ZipFile(io.BytesIO(b)) as z:
    entries=[n for n in z.namelist() if n.rsplit('/',1)[-1]=='lamedb'];assert entries
    raw=z.read(entries[0])
  else:raw=b
  lines=raw.decode('utf8','replace').splitlines();assert lines[0].startswith('eDVB services') and 'end' in lines
  rows=[]
  for i,line in enumerate(lines[:-2]):
   if not re.fullmatch(r'[0-9a-fA-F]{1,4}:[0-9a-fA-F]{8}:[0-9a-fA-F]{1,4}:[0-9a-fA-F]{1,4}:[0-9]+:[0-9]+(?::[0-9]+)?',line):continue
   sid,ns,tid,onid,typ,*_=line.split(':');prov=re.search(r'(?:^|,)p:([^,]*)',lines[i+2]);provider=prov.group(1).strip() if prov else ''
   nsn=int(ns,16)
   if nsn>>16 in (90,3550):
    name='1_0_%X_%X_%X_%X_%X_0_0_0.PNG'%(int(typ),int(sid,16),int(tid,16),int(onid,16),nsn)
    rows.append({'ref':name,'service':lines[i+1],'provider':provider})
  sources.append({'source':label,'url':url,'sha256':sha(b),'lamedb_sha256':sha(raw),'rows':rows})
 except Exception as e:sources.append({'source':label,'url':url,'error':str(e)})
write(P/'settings-current.json',sources)
names={x['service'].strip().casefold() for s in sources for x in s.get('rows',[]) if x['ref'] in T}
donors={x['ref'] for s in sources for x in s.get('rows',[]) if x['service'].strip().casefold() in names and x['service'].strip() not in ('','...')}
# Also include existing exact pixel donors observed in the first audit.
donors.update('1_0_'+v+'_5A0000_0_0_0.PNG' for v in '16_205_2134_9C 16_46F_7_AA 19_46F_7_AA 1_205_2134_9C 16_21_204_1D 19_21_204_1D 1_21_204_1D'.split())
m=get(C+'manifest.json');assert sha(m)=='cfc08ab0120731b052cc4849992785e3395e70b2bf20506ad276cb9acf5e7e7f';d=json.loads(m);parts={p['filename']:p for p in d['parts']}
def audit(p):
 names=[x.rsplit('/',1)[-1] for x in p['parts']];chunks=[]
 for n in names:
  b=get(C+n);assert sha(b)==parts[n]['sha256'] and len(b)==parts[n]['bytes'];chunks.append(b)
 raw=b''.join(chunks);assert len(raw)==p['bytes'] and sha(raw)==p['sha256']
 key=p['selector_id']+'/'+p['resolution']+'/'+p['family']
 with zipfile.ZipFile(io.BytesIO(raw)) as z:
  assert z.testzip() is None
  count=0
  for n in z.namelist():
   if n.upper() in T|donors:
    dest=P/'donors'/key/n;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(z.read(n));count+=1
 if p['resolution']=='220x132' and p['family']=='channel-transparent':
  (P/(p['selector_id']+'-transparent.zip')).write_bytes(raw)
 return key,count
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex: counts=dict(ex.map(audit,[p for p in d['packages'] if p['selector_id'] in ('90E','50W')]))
for style,h in [('black','61e69f7fc46e340453bf74ccd7af6ac9d8eba9f8e232884659e1ea99f6abf3fe'),('white','c6ae4a808a65ffc8e6458336fccbfe4216de1e832ec0a9abf800907f2f783589')]:
 b=fetch('https://raw.githubusercontent.com/Evolution-by-Warder/PiconHub-Warder-Evolution/67f4be844b2236f9a5366187760f642a01a7f4d6/plugin/artwork/templates/picons/'+style+'-sablona.png');assert sha(b)==h;(P/(style+'-sablona.png')).write_bytes(b)
print(json.dumps({'counts':counts,'settings':[{k:v for k,v in s.items() if k!='rows'}|{'rows':len(s.get('rows',[]))} for s in sources],'donor_refs':len(donors)}))
