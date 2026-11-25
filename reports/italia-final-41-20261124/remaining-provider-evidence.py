import json,hashlib,urllib.request,io,zipfile,re,concurrent.futures
from pathlib import Path
P=Path('remaining-provider-audit');P.mkdir(exist_ok=True)
pending={'1 CENT','AN','BBC WORLD','DORIA','FREE TV','GTSS','MULTIPROGRAM','NT','RETECAPRI TRTN','SERVICE N','SHARAVOZ','TV SYSTEM'}
names=re.compile(r'AMICI NETWORK|TELEACRAS|ANTENNA.?3|ITALIA 7|SHARAVOZ|LIGHTSAT|SATELLITE SERVICE ITALY',re.I)
wanted={(0x1392,0x50e1,0x217c),*((i,0xa002,0x217c) for i in (1,2,4,5))}
sources={'Italia':13,'Sicilia':26,'Lombardia':19,'Lazio':16,'Campania':22,'Piemonte':25,'Sardegna':27,'Romagna':28}
previous={'Italia':'b44bc9affcc9f9263f8a77fd9391387fa6865f15645fcef12a08462b8dad20de','Sicilia':'d230880a1a0eaa325c05a811062218077be565a88835697615bd0785d31b990c','Lombardia':'982284c11439260b24d04645fb59cbc1e1c796f75e5568d80bdb38af41b36b94','Lazio':'9fb4854abdc1c0ceb7f54942068b2ab64526b0ee29afae8a88d7878895660bdd','Campania':'6e0200d75d990485f3a2907f556650f4d9b4ba553550fcb5b92b0e0a0b00d3b9','Piemonte':'2735c372f0c75ebaa8f5610650d1a74a1145abadcde3ade68686b4f2e3ac48e7','Sardegna':'3fb3100deb957d57bd345979f5d176582d638098871c8d17bf249076f37f790d','Romagna':'a3c06c11109fe26ed20c0577487a2c0f963f0937db67773455271f9121ed8ad0'}
def run(item):
 name,i=item;url=f'https://www.vhannibal.net/download_setting.php?action=download&id={i}'
 try:
  req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'})
  with urllib.request.urlopen(req,timeout=35) as r:b=r.read(8*1024*1024+1)
  assert len(b)<=8*1024*1024
  h=hashlib.sha256(b).hexdigest()
  with zipfile.ZipFile(io.BytesIO(b)) as z:
   ls=[x for x in z.namelist() if x.rsplit('/',1)[-1]=='lamedb'];assert len(ls)==1
   raw=z.read(ls[0]).decode('utf8','replace')
  assert '/4/' in raw.splitlines()[0] or '/5/' in raw.splitlines()[0]
  rows=[];lines=raw.splitlines()
  for idx,line in enumerate(lines[:-2]):
   if not re.fullmatch(r'[0-9a-fA-F]{1,4}:[0-9a-fA-F]{8}:[0-9a-fA-F]{1,4}:[0-9a-fA-F]{1,4}:[0-9]+:[0-9]+(?::[0-9]+)?',line):continue
   x=line.split(':');sid,ns,tid,onid=map(lambda v:int(v,16),x[:4]);typ=int(x[4]);service=lines[idx+1];prov=lines[idx+2].split(',')[0].removeprefix('p:').strip()
   if prov.upper() in pending or names.search(service) or (sid,tid,onid) in wanted or (tid,onid)==(0xa002,0x217c):
    rows.append({'sid':sid,'namespace':f'{ns:08x}','tsid':tid,'onid':onid,'type':typ,'service':service,'provider':prov})
  return {'source':name,'url':url,'sha256':h,'changed':h!=previous[name],'matches':rows}
 except Exception as e:return {'source':name,'error':repr(e)}
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:results=list(ex.map(run,sources.items()))
(P/'result.json').write_text(json.dumps(results,ensure_ascii=False,indent=2))
# Print only distinct factual rows and source digest comparison, not the full settings file.
distinct={}
for r in results:
 for x in r.get('matches',[]):
  k=json.dumps(x,sort_keys=True,ensure_ascii=False);distinct.setdefault(k,[]).append(r['source'])
print(json.dumps({'sources':[{k:v for k,v in r.items() if k!='matches'} for r in results],'rows':[dict(json.loads(k),sources=v) for k,v in distinct.items()]},ensure_ascii=False))
assert all('error' not in r for r in results)
