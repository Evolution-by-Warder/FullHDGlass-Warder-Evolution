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

# 2026-11-25: static inspection of the author's official plugin; never execute it.
import tarfile,html,urllib.parse,subprocess,tempfile
from html.parser import HTMLParser
base='https://gioppygio.it/'
plugin=base+'update_new/enigma2-plugin-extensions-gioppygio_2.6_all.ipk'
report={'sources':[],'discovery':[],'static_candidates':[],'errors':[]}
links=set()
def collect(text,origin):
 text=html.unescape(text).replace('\\/','/')
 for v in re.findall(r'https?://[^\s"\'<>\\]+',text):
  v=v.rstrip(');,]')
  if urllib.parse.urlparse(v).hostname in ('gioppygio.it','www.gioppygio.it'):links.add(v)
 for v in re.findall(r"""(?:href|src)\s*=\s*["']([^"']+)["']""",text,re.I):
  u=urllib.parse.urljoin(origin,v)
  if urllib.parse.urlparse(u).hostname in ('gioppygio.it','www.gioppygio.it'):links.add(u)
 for v in re.findall(r"""["']([^"'\n]{3,180}\.(?:zip|json|xml|txt|csv|php|js))["']""",text,re.I):
  if not v.startswith(('http','//')) and not any(c in v for c in ('{','}','%',' ')):
   u=urllib.parse.urljoin(origin,v)
   if urllib.parse.urlparse(u).hostname in ('gioppygio.it','www.gioppygio.it'):links.add(u)
def record(url):
 try:
  b=get(url);report['discovery'].append({'url':url,'bytes':len(b),'sha256':sha(b)})
  return b
 except Exception as e:report['errors'].append({'url':url,'error':repr(e)});return None
for path in ('enigma2-1.html','picons-dtt.html','plugin.html'):
 u=base+path;b=record(u)
 if b:collect(b.decode('utf8','replace'),u)
raw=record(plugin)
if raw:
 try:
  with tempfile.TemporaryDirectory() as td:
   f=Path(td)/'plugin.ipk';f.write_bytes(raw)
   if raw.startswith(b'!<arch>\n'):
    names=subprocess.check_output(['ar','t',str(f)],text=True).splitlines()
    name=next(n for n in names if n.startswith('data.tar'))
    data=subprocess.check_output(['ar','p',str(f),name])
   else:
    with tarfile.open(fileobj=io.BytesIO(raw),mode='r:*') as t:
     m=next(m for m in t.getmembers() if m.name.rsplit('/',1)[-1].startswith('data.tar'))
     data=t.extractfile(m).read()
   with tarfile.open(fileobj=io.BytesIO(data),mode='r:*') as t:
    for m in t.getmembers():
     if not m.isfile() or m.size>2*1024*1024 or not re.search(r'\.(py|xml|json|txt|cfg|conf|list|ini)$',m.name,re.I):continue
     txt=t.extractfile(m).read().decode('utf8','replace')
     collect(txt,base)
     relevant=[line.strip()[:450] for line in txt.splitlines() if re.search(r'gioppygio\.it|palermo|firenze|toscana|dtt.*(?:zip|xml|json|url)|(?:zip|xml|json|url).*dtt',line,re.I)]
     if relevant:report['static_candidates'].append({'file':m.name,'lines':relevant[:60]})
 except Exception as e:report['errors'].append({'stage':'static IPK unpack','error':repr(e)})
# Inspect only explicit public same-origin catalogue/script URLs, not guessed endpoints.
seen=set()
for _ in range(2):
 candidates=sorted(u for u in links if u not in seen and re.search(r'\.(?:json|xml|txt|csv|js)(?:\?|$)|(?:settings|setting|dtt).*\.php',u,re.I) and not re.search(r'jquery|bootstrap|analytics|cookie|x5engine|search|login',u,re.I))[:12]
 if not candidates:break
 for u in candidates:
  seen.add(u);b=record(u)
  if b:collect(b.decode('utf8','replace'),u)
zips=sorted(u for u in links if re.search(r'\.zip(?:\?|$)',u,re.I) and re.search(r'palermo|firenze|toscana|sicilia|dtt',u,re.I) and not re.search(r'picon',u,re.I))
report['discovered_links']=sorted(links)[:200]
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as ex:report['sources']=list(ex.map(run,[(u,u) for u in zips[:15]]))
(P/'result.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
print(json.dumps(report,ensure_ascii=False)[:60000])
