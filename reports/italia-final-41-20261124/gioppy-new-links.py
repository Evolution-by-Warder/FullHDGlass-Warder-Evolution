import json,hashlib,urllib.request,io,zipfile,re,concurrent.futures
from pathlib import Path
P=Path('cross-source-audit');P.mkdir(exist_ok=True)
pending={'1 CENT','BBC WORLD','FREE TV','MULTIPROGRAM','NT','SERVICE N','SHARAVOZ','TV SYSTEM'}
names=re.compile(r'AMICI NETWORK|TELEACRAS|ITALIA.?7|ITALIA SETTE|SHARAVOZ|LIGHTSAT|SATELLITE SERVICE ITALY|TELEONE|BBC WORLD',re.I)
wanted={(0x1392,0x50e1,0x217c),*((i,0xa002,0x217c) for i in (1,2,3,4,5))}
def get(url):
 req=urllib.request.Request(url,headers={'User-Agent':'WarderEvolution/1.0'})
 with urllib.request.urlopen(req,timeout=35) as r:
  b=r.read(12*1024*1024+1)
 assert len(b)<=12*1024*1024
 return b
sources=[["GioppyGio Motor 8 Nov 2026","https://gioppygio.it/settings/e2/GioppyGio_E2_Motor_75E-45W_08-11-2026.zip"],["GioppyGio Motor 1 Nov 2026","https://gioppygio.it/settings/e2/GioppyGio_E2_Motor_75E-45W_01-11-2026.zip"],["GioppyGio Palermo Dual 1 Dec 2025","https://gioppygio.it/settings/e2+dtt/Palermo/GioppyGio_E2_Dual_13E+19E+DTT-Palermo_01-12-2025.zip"],["GioppyGio Palermo Motor 1 Oct 2025","https://gioppygio.it/settings/e2+dtt/Palermo/GioppyGio_E2_Motor_45W+75E+DTT-Palermo_01-10-2025.zip"]]
old={'Vhannibal Motor Italia':'b44bc9affcc9f9263f8a77fd9391387fa6865f15645fcef12a08462b8dad20de','Vhannibal Motor Sicilia':'d230880a1a0eaa325c05a811062218077be565a88835697615bd0785d31b990c','Vhannibal Motor Romagna':'a3c06c11109fe26ed20c0577487a2c0f963f0937db67773455271f9121ed8ad0'}
def sha(b):return hashlib.sha256(b).hexdigest()
def parse(raw):
 lines=raw.decode('utf8','replace').splitlines();rows=[];count=0
 if not lines or not ('/4/' in lines[0] or '/5/' in lines[0]):raise ValueError('not lamedb format 4/5')
 def add(parts,service,prov):
  nonlocal count
  sid,ns,tid,onid=(int(v,16) for v in parts[:4]);typ=int(parts[4]);count+=1
  if prov.upper() in pending or names.search(service) or (sid,tid,onid) in wanted or (tid,onid)==(0xa002,0x217c):
   rows.append({'sid':sid,'namespace':f'{ns:08x}','tsid':tid,'onid':onid,'type':typ,'service':service,'provider':prov,'terrestrial':(ns>>16)==0xeeee})
 if '/4/' in lines[0]:
  for i,line in enumerate(lines[:-2]):
   if re.fullmatch(r'[0-9a-fA-F]{1,4}:[0-9a-fA-F]{8}:[0-9a-fA-F]{1,4}:[0-9a-fA-F]{1,4}:[0-9]+:[0-9]+(?::[0-9]+)?',line):
    add(line.split(':'),lines[i+1],next((x[2:].strip() for x in lines[i+2].split(',') if x.startswith('p:')),''))
 else:
  for line in lines:
   m=re.match(r'^s:([^,]+),"((?:[^"\\]|\\.)*)"(?:,(.*))?$',line)
   if m:
    prov=next((x[2:] for x in (m[3] or '').split(',') if x.startswith('p:')),'')
    add(m[1].split(':'),m[2],prov.strip())
 assert count>0
 return count,rows
def run(item):
 name,url=item
 try:
  b=get(url);h=sha(b);changed=old.get(name)!=h
  if not changed:return {'source':name,'url':url,'sha256':h,'unchanged':True,'previous_audit':45566981706}
  inputs=[]
  if zipfile.is_zipfile(io.BytesIO(b)):
   with zipfile.ZipFile(io.BytesIO(b)) as z:
    for k in z.namelist():
     if k.rsplit('/',1)[-1] in ('lamedb','lamedb5'):inputs.append((k,z.read(k)))
  else:inputs=[('lamedb',b)]
  assert inputs
  files=[]
  for k,raw in inputs:
   count,rows=parse(raw);files.append({'name':k,'sha256':sha(raw),'services':count,'matches':rows})
  return {'source':name,'url':url,'sha256':h,'files':files}
 except Exception as e:return {'source':name,'url':url,'error':repr(e)}


# Static public catalog audit, no plugin execution.
import tarfile, html, urllib.parse, subprocess, tempfile, ast
report={'sources':[],'discovery':[],'static':[],'errors':[],'catalogues':[]}
urls=set()
def retrieve(url):
 try:
  b=get(url);report['discovery'].append({'url':url,'bytes':len(b),'sha256':sha(b)});return b
 except Exception as e:report['errors'].append({'url':url,'error':repr(e)});return None
def unpack_ipk(raw):
 with tempfile.TemporaryDirectory() as td:
  f=Path(td)/'a.ipk';f.write_bytes(raw)
  if raw.startswith(b'!<arch>\n'):
   names=subprocess.check_output(['ar','t',str(f)],text=True).splitlines();data=subprocess.check_output(['ar','p',str(f),next(n for n in names if n.startswith('data.tar'))])
  else:
   with tarfile.open(fileobj=io.BytesIO(raw),mode='r:*') as t:data=t.extractfile(next(m for m in t.getmembers() if m.name.rsplit('/',1)[-1].startswith('data.tar'))).read()
  return data
def read_archive(url,raw):
 inputs=[]
 try:
  if zipfile.is_zipfile(io.BytesIO(raw)):
   with zipfile.ZipFile(io.BytesIO(raw)) as z:
    for k in z.namelist():
     if k.rsplit('/',1)[-1] in ('lamedb','lamedb5'):inputs.append((k,z.read(k)))
  else:
   if raw.startswith(b'!<arch>\n'):raw=unpack_ipk(raw)
   with tarfile.open(fileobj=io.BytesIO(raw),mode='r:*') as t:
    for m in t.getmembers():
     if m.isfile() and m.name.rsplit('/',1)[-1] in ('lamedb','lamedb5') and m.size<4000000:inputs.append((m.name,t.extractfile(m).read()))
  files=[]
  for k,b in inputs:
   count,rows=parse(b);files.append({'name':k,'sha256':sha(b),'services':count,'matches':rows})
  report['sources'].append({'url':url,'files':files})
 except Exception as e:report['errors'].append({'url':url,'error':repr(e)})
# Actual GioppyGio plugin source strings and assignment context, rather than local file paths.
u='https://gioppygio.it/update_new/enigma2-plugin-extensions-gioppygio_2.6_all.ipk'
raw=retrieve(u)
if raw:
 try:
  data=unpack_ipk(raw)
  with tarfile.open(fileobj=io.BytesIO(data),mode='r:*') as t:
   for m in t.getmembers():
    if not m.isfile() or not m.name.endswith('.py') or m.size>2000000:continue
    if not re.search(r'/(?:Setting|plugin|update|config|download|constants|catalog|network|utils|settings_store)\.py$',m.name,re.I):continue
    txt=t.extractfile(m).read().decode('utf8','replace')
    try:tree=ast.parse(txt)
    except SyntaxError:continue
    constants=[]
    for n in ast.walk(tree):
     if isinstance(n,ast.Constant) and isinstance(n.value,str) and re.search(r'https?://|\.json$|\.txt$|\.xml$|\.csv$|\.zip$|\.php$|listaE2|setting|catalog',n.value,re.I) and len(n.value)<450:constants.append(n.value)
    lines=[l.strip()[:1500] for l in txt.splitlines() if re.search(r'link_dtt|url.*setting|setting.*url|pathsite|catalog|requests\.get|urlopen|_ALLOWED_LINK_PREFIXES',l,re.I)]
    if m.name.endswith('/settings_store.py'):
     report['static'].append({'file':m.name,'source':txt[:24000]})
     for n in ast.walk(tree):
      if isinstance(n,ast.Constant) and isinstance(n.value,str) and re.match(r'^https?://(?:picons\.)?(?:www\.)?gioppygio\.it/',n.value,re.I) and len(n.value)<400:urls.add(n.value)
     for n in ast.walk(tree):
      if isinstance(n,ast.Assign) and any(isinstance(v,ast.Name) and v.id=='XML_URL' for v in n.targets):
       report['xml_url_expression']=ast.unparse(n.value)
    else:
     report['static'].append({'file':m.name,'constants':sorted(set(constants))[:100],'lines':lines[:35]})
 except Exception as e:report['errors'].append({'stage':'IPK static inspection','error':repr(e)})

import xml.etree.ElementTree as ET
def approved(u):
 try:return urllib.parse.urlparse(u).scheme in ('http','https') and urllib.parse.urlparse(u).hostname in ('gioppygio.it','www.gioppygio.it','picons.gioppygio.it')
 except:return False
def catalog(u):
 raw=retrieve(u)
 if not raw:return []
 txt=html.unescape(raw.decode('utf8','replace'))
 report['catalogues'].append({'url':u,'excerpt':txt[:16000]})
 found=set()
 for v in re.findall(r'https?://[^\s"\'<>]+',txt):
  if approved(v) and re.search(r'\.zip(?:\?|$)',v,re.I):found.add(v)
 try:
  root=ET.fromstring(raw)
  for e in root.iter():
   for v in list(e.attrib.values())+[e.text or '']:
    v=v.strip()
    if re.search(r'\.zip(?:\?|$)',v,re.I):
     a=urllib.parse.urljoin(u,v)
     if approved(a):found.add(a)
 except ET.ParseError:pass
 return sorted(found)
found=set()
for u in sorted(urls):
 if re.search(r'xml|json|manifest|setting|catalog',u,re.I) and not u.endswith('/'):found.update(catalog(u))
report['archives']=sorted(found)
selected=sorted(v for v in found if re.search(r'palermo|sicilia|toscana|firenze|dtt',v,re.I))[:35]
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as ex:report['sources']=list(ex.map(run,[(u,u) for u in selected]))
(P/'result.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
print(json.dumps(report,ensure_ascii=False)[:100000])
