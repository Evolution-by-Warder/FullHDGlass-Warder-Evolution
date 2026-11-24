import hashlib,io,json,re,urllib.request,zipfile
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
P=Path(__file__).parent
targets=json.loads((P/'targets.json').read_text());results={}
sources=[(13,'Italia'),(26,'Sicilia'),(19,'Lombardia'),(16,'Lazio'),(22,'Campania'),(25,'Piemonte'),(27,'Sardegna'),(28,'Romagna')]
def scan(item):
 id,name=item;url='https://www.vhannibal.net/download_setting.php?action=download&id='+str(id)
 try:
  req=urllib.request.Request(url,headers={'User-Agent':'WarderEvolution settings reference verification'})
  with urllib.request.urlopen(req,timeout=45) as response:
   raw=response.read(32*1024*1024+1)
  assert len(raw)<=32*1024*1024
  z=zipfile.ZipFile(io.BytesIO(raw));assert z.testzip() is None
  files=[n for n in z.namelist() if n.rsplit('/',1)[-1]=='lamedb']
  assert files
  hits={n:[] for n in targets}
  for file in files:
   lines=z.read(file).decode('utf-8',errors='replace').splitlines()
   for i,l in enumerate(lines[:-2]):
    m=re.fullmatch(r'([0-9a-fA-F]{1,4}):([0-9a-fA-F]{8}):([0-9a-fA-F]{1,4}):([0-9a-fA-F]{1,4}):(\d+):\d+(?::\d+)?',l.strip())
    if not m:continue
    sid,ns,tsid,onid,typ=m.groups()
    for n in targets:
     f=n.removesuffix('.png').split('_')
     if (int(sid,16),int(tsid,16),int(onid,16))!=(int(f[3],16),int(f[4],16),int(f[5],16)):continue
     hits[n].append({'service':lines[i+1].strip(),'provider':lines[i+2].strip().split(',')[0],'namespace':ns,'type_hex':format(int(typ),'X'),'exact':int(typ)==int(f[2],16) and int(ns,16)==int(f[6],16)})
  return {'name':name,'url':url,'source_sha256':hashlib.sha256(raw).hexdigest(),'matches':{k:v for k,v in hits.items() if v},'status':'ok'}
 except Exception as e:return {'name':name,'url':url,'status':'error','error':str(e)}
with ThreadPoolExecutor(max_workers=3) as ex:results=list(ex.map(scan,sources))
# No setting files or bouquets are republished; only matches to submitted reference IDs.
out=Path('dtt-evidence');out.mkdir(exist_ok=True);(out/'matches.json').write_text(json.dumps(results,ensure_ascii=False,indent=2))
print(json.dumps(results,ensure_ascii=False))
assert any(x['status']=='ok' for x in results),'No readable source archive'
