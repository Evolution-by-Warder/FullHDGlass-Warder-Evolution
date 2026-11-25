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
discovery=[]
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as ex:results=list(ex.map(run,sources))
distinct={}
for r in results:
 for f in r.get('files',[]):
  for x in f['matches']:
   k=json.dumps(x,sort_keys=True,ensure_ascii=False);distinct.setdefault(k,set()).add(r['source'])
report={'sources':results,'discovery':discovery,'distinct_matches':[dict(json.loads(k),sources=sorted(v)) for k,v in distinct.items()]}
(P/'result.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
print(json.dumps({'sources':[{**{k:v for k,v in r.items() if k!='files'},'files':[{k:v for k,v in f.items() if k!='matches'} for f in r.get('files',[])]} for r in results],'matches':report['distinct_matches']},ensure_ascii=False))
print('Readable archives:',sum(bool(r.get('files')) for r in results))
