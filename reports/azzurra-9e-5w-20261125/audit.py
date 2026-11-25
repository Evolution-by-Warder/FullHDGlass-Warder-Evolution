import concurrent.futures,hashlib,io,json,re,urllib.request,zipfile
from pathlib import Path
from PIL import Image
BASE='896a2fb62ba3e97769949172d4961e5932806e26'
RAW='https://raw.githubusercontent.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/'+BASE+'/'
C='assets/warder/downloads/picons/channels/'
P=Path('audit-output');P.mkdir(exist_ok=True)
def sha(b):return hashlib.sha256(b).hexdigest()
def fetch(url):
 req=urllib.request.Request(url,headers={'User-Agent':'WarderEvolution/1.0'})
 with urllib.request.urlopen(req,timeout=90) as r:return r.read()
def get(p):return fetch(RAW+p)
def write(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
m=get(C+'manifest.json');assert sha(m)=='cfc08ab0120731b052cc4849992785e3395e70b2bf20506ad276cb9acf5e7e7f'
doc=json.loads(m);parts={v['filename']:v for v in doc['parts']}
targets=[v for v in doc['packages'] if v['selector_id'] in ('90E','50W')]
assert len(targets)==18
def audit(p):
 names=[x.rsplit('/',1)[-1] for x in p['parts']];chunks=[]
 for n in names:
  raw=get(C+n);assert sha(raw)==parts[n]['sha256'] and len(raw)==parts[n]['bytes'],n;chunks.append(raw)
 raw=b''.join(chunks);assert len(raw)==p['bytes'] and sha(raw)==p['sha256']
 result={}
 with zipfile.ZipFile(io.BytesIO(raw)) as z:
  assert z.testzip() is None and len(z.namelist())==p['png_count']==len(set(z.namelist()))
  for n in z.namelist():
   b=z.read(n)
   with Image.open(io.BytesIO(b)) as im:
    im.load();px=im.convert('RGBA');assert im.size==tuple(map(int,p['resolution'].split('x')))
    result[n]={'sha256':sha(b),'pixel_sha256':sha(px.tobytes()),'bytes':len(b),'crc32':z.getinfo(n).CRC,'alpha':list(px.getchannel('A').getextrema())}
 key=p['selector_id']+'/'+p['resolution']+'/'+p['family']
 return key,{'archive':p['filename'],'sha256':p['sha256'],'parts':len(names),'count':len(result),'entries':result}
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:out=dict(ex.map(audit,targets))
write(P/'production-index.json',out)
# Exact settings identities from official Motor archive; retain only selected positions and Rai Way provider names.
url='https://www.vhannibal.net/download_setting.php?action=download&id=1'
# Official Motor ID verified by fallback repository; prefer pinned current settings archive if readable.
settings=[]
for label,u in [('oe-alliance Motor','https://raw.githubusercontent.com/oe-alliance/oe-alliance-settings/master/vhannibal.motor/lamedb'),('Morpheus Motor','https://raw.githubusercontent.com/morpheus883/enigma2-settings/master/morph883_motor/lamedb'),('Ciefp Motor','https://raw.githubusercontent.com/ciefp/ciefpsettings-enigma2/master/ciefp-E2-motor-75E-34W/lamedb')]:
 try:
  b=fetch(u);lines=b.decode('utf8','replace').splitlines();assert lines[0].startswith('eDVB services') and 'end' in lines
  rows=[]
  for i,line in enumerate(lines[:-2]):
   if not re.fullmatch(r'[0-9a-fA-F]{1,4}:[0-9a-fA-F]{8}:[0-9a-fA-F]{1,4}:[0-9a-fA-F]{1,4}:[0-9]+:[0-9]+(?::[0-9]+)?',line):continue
   sid,ns,tid,onid,typ,*_=line.split(':');prov=re.search(r'(?:^|,)p:([^,]*)',lines[i+2]);provider=prov.group(1).strip() if prov else ''
   nsn=int(ns,16)
   if nsn>>16 in (90,3550) or provider.upper() in ('RAI WAY','RAIWAY'):
    name='1_0_%X_%X_%X_%X_%X_0_0_0.png'%(int(typ),int(sid,16),int(tid,16),int(onid,16),nsn)
    rows.append({'ref':name,'service':lines[i+1],'provider':provider})
  settings.append({'source':label,'url':u,'sha256':sha(b),'rows':rows})
 except Exception as e:settings.append({'source':label,'url':u,'error':str(e)})
write(P/'settings-index.json',settings)
catalog=json.loads(get('assets/warder/downloads.json'))['assets'];providers={}
for style,key in [('transparent','piconProv-220'),('white','piconProv-w'),('black','piconProv-b')]:
 desc=catalog[key];paths=[('assets/warder/downloads/picons/providers/'+style+'/piconProv.zip',desc)]
 if key+'-v2' in catalog:
  for i,e in enumerate(catalog[key+'-v2']['extensions'],1):paths.append(('assets/warder/downloads/picons/providers/'+style+'/extension-%02d/piconProv.zip'%i,e))
 found={};near=[];count=0
 for path,a in paths:
  raw=get(path);assert len(raw)==a['size'] and sha(raw)==a['sha256'],path
  with zipfile.ZipFile(io.BytesIO(raw)) as z:
   assert z.testzip() is None
   count+=len(z.namelist())
   for n in z.namelist():
    stem=Path(n).stem
    if 'RAI' in stem.upper() and 'WAY' in stem.upper():
     b=z.read(n);found[n]={'sha256':sha(b),'bytes':len(b)}
     target=P/'provider-donors'/style/Path(n).name;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(b)
 providers[style]={'count':count,'raiway':found}
write(P/'providers.json',providers)
summary={'baseline':BASE,'manifest_sha256':sha(m),'archives':{k:{x:y for x,y in v.items() if x!='entries'} for k,v in out.items()},'settings':[{k:v for k,v in s.items() if k!='rows'}|{'rows':len(s.get('rows',[]))} for s in settings],'providers':providers}
write(P/'summary.json',summary);print(json.dumps(summary,ensure_ascii=False))
