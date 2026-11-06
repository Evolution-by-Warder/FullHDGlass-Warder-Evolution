from pathlib import Path
import zipfile,hashlib,json,re,io,collections,gzip
from PIL import Image
B=Path('audit-cache');O=Path('audit-output');services=collections.defaultdict(list);source_manifest=[]
def digest(v):return hashlib.sha256(v).hexdigest()
def ref(n):
 f=Path(n).stem.split('_')
 if len(f)!=10:return None
 try:return '_'.join(f'{int(x,16):X}'for x in f)
 except ValueError:return None

def lamedb(v):
 lines=v.decode('utf-8','replace').splitlines();tps={};start=lines.index('transponders')+1;end=lines.index('end',start);i=start
 while i<end:
  key=lines[i].strip();i+=1;data=[]
  while i<end and lines[i].strip()!='/':data.append(lines[i].strip());i+=1
  i+=1
  try:tps[tuple(int(x,16)for x in key.split(':'))]=data
  except ValueError:continue
 i=lines.index('services')+1
 while i<len(lines)and lines[i].strip()!='end':
  f=lines[i].strip().split(':')
  if len(f)<5:i+=1;continue
  sid,ns,tsid,onid=[int(x,16)for x in f[:4]];typ=int(f[4],10);name=lines[i+1];attr=lines[i+2];i+=3
  key=(ns,tsid,onid);tp=tps.get(key,[]);sat=next((t for t in tp if t.startswith('s ')),None);orb=None
  if sat:
   val=int(sat[2:].split(':')[4]);val=val if val<1800 else val-3600;orb=f'{abs(val)/10:.1f}'+('e'if val>=0 else'w')
  r=f'1_0_{typ:X}_{sid:X}_{tsid:X}_{onid:X}_{ns:X}_0_0_0';provider=re.search(r'(?:^|,)p:([^,]*)',attr)
  yield {'reference':r,'name':name,'provider':provider.group(1)if provider else'','namespace':ns,'position':orb,'transponder':tp,'service_type':typ,'uid':[sid,tsid,onid,ns]}

paths=sorted(B.glob('official-*.zip'))+sorted(Path('originals').glob('*.zip'))
for p in paths:
 raw=p.read_bytes();z=zipfile.ZipFile(io.BytesIO(raw));assert z.testzip()is None;inventory={'source':p.name,'sha256':digest(raw),'bytes':len(raw),'members':len(z.namelist()),'lamedbs':[],'picon_items':0}
 for n in z.namelist():
  if Path(n).name!='lamedb':continue
  v=z.read(n);lh=digest(v);rows=list(lamedb(v));inventory['lamedbs'].append({'member':n,'sha256':digest(v),'services':len(rows),'satellite_tv':sum(x['position']is not None and x['service_type']not in(2,10)for x in rows)})
  for row in rows:services[row['reference']].append({**row,'settings_source':p.name,'lamedb_sha256':lh})
 picons=[]
 for n in z.namelist():
  if not n.lower().endswith('.png'):continue
  v=z.read(n)
  with Image.open(io.BytesIO(v))as im:
   im.load();rgba=im.convert('RGBA');size=im.size;pixel=digest(rgba.tobytes());bbox=rgba.getchannel('A').getbbox()
  picons.append({'member':n,'reference':ref(n),'sha256':digest(v),'rgba_sha256':pixel,'size':size,'empty':not bbox})
 if picons:
  inventory['picon_items']=len(picons);(O/(p.name+'.picons.json.gz')).write_bytes(gzip.compress(json.dumps(picons,separators=(',',':')).encode(),mtime=0))
 source_manifest.append(inventory)
(O/'sources.json').write_text(json.dumps(source_manifest,indent=2));(O/'services.json.gz').write_bytes(gzip.compress(json.dumps(services,separators=(',',':')).encode(),mtime=0))
current={x['reference']:x for x in json.loads(gzip.decompress((O/'official-1.zip.picons.json.gz').read_bytes()))if x['reference']};historical={}
for p in O.glob('PICON*.picons.json.gz'):
 for x in json.loads(gzip.decompress(p.read_bytes())):
  if x['reference']:historical[x['reference']]=x
plans={x['reference']:x for x in json.load(open('plans.json'))};prior={x.get('source_reference'):x for x in json.load(open(B/'source-dispositions.json'))};uid=collections.defaultdict(list)
for r,rows in services.items():
 if any(row['settings_source'].startswith('official-')and row['position']for row in rows):uid[tuple(r.split('_')[3:7])].append(r)
records=[]
for r,x in sorted({**historical,**current}.items()):
 rows=services.get(r,[]);fresh=[v for v in rows if v['settings_source'].startswith('official-')];sat=[v for v in fresh if v['position']];tv=[v for v in sat if v['service_type']not in(2,10)];aliases=uid.get(tuple(r.split('_')[3:7]),[])
 status='SATELLITE_TV'if tv else'RADIO_OUT_OF_SCOPE'if sat else'NON_SATELLITE'if fresh else'NO_CURRENT_SETTINGS_EVIDENCE'
 records.append({**x,'in_latest_picons':r in current,'in_nov3_picons':r in historical,'scope':status,'services':fresh,'unique_current_type_alias':aliases[0]if len(aliases)==1 and aliases[0]!=r else None,'accepted_prior':r in plans,'prior_disposition':prior.get(r)})
(O/'source-reference-ledger.json.gz').write_bytes(gzip.compress(json.dumps(records,separators=(',',':')).encode(),mtime=0))
summary={'sources':len(source_manifest),'current_picons':len(current),'historical_picons':len(historical),'union_picons':len(records),'new_picon_refs':sorted(current.keys()-historical.keys()),'removed_picon_refs':sorted(historical.keys()-current.keys()),'same_ref_changed_pixels':[r for r in current.keys()&historical.keys()if current[r]['rgba_sha256']!=historical[r]['rgba_sha256']],'scope_counts':dict(collections.Counter(x['scope']for x in records)),'settings_refs_without_source_png':[r for r,rows in services.items()if any(x['position']and x['service_type']not in(2,10)and x['settings_source'].startswith('official-')for x in rows)and r not in current]}
(O/'source-summary.json').write_text(json.dumps(summary,indent=2));print(json.dumps(summary,indent=2))
