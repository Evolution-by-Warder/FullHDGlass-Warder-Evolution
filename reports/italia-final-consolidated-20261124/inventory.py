import json,hashlib,io,zipfile,urllib.request,collections
from pathlib import Path
P=Path(__file__).parent;out=Path('consolidated');out.mkdir(exist_ok=True)
def get(u):
 with urllib.request.urlopen(u,timeout=90) as r:return r.read()
def sha(b):return hashlib.sha256(b).hexdigest()
R='https://raw.githubusercontent.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/286291aaac56f78015c7d147bcafc4ade8604a6c/'
C='assets/warder/downloads/picons/channels/'
raw=get(R+C+'manifest.json');assert sha(raw)=='4541dea07b011d2cac2981c5b8203ebae7e363c85e481316a4cf6c0b04d9b6a6';(out/'manifest.json').write_bytes(raw)
cat=get(R+'assets/warder/downloads.json');(out/'downloads.json').write_bytes(cat);a=json.loads(cat);a=a.get('assets',a)
inv={}
for s,k,count in [('transparent','piconProv-220',1297),('white','piconProv-w',1346),('black','piconProv-b',1371)]:
 raw=get(R+'assets/warder/downloads/picons/providers/'+s+'/piconProv.zip');assert sha(raw)==a[k]['sha256']
 (out/(s+'.zip')).write_bytes(raw)
 with zipfile.ZipFile(io.BytesIO(raw)) as z:
  assert z.testzip() is None and len(z.namelist())==count
  inv[s]={n.removeprefix('piconProv/'):sha(z.read(n)) for n in z.namelist()}
common=set.intersection(*(set(x) for x in inv.values()))
by=collections.defaultdict(list)
for n in common:by[inv['white'][n],inv['black'][n]].append(n)
rows=json.loads((P/'remaining.json').read_text());report=[]
for row in rows:
 n=row['name']
 if row['kind']!='PROVIDER':continue
 missing=[s for s in inv if n not in inv[s]]
 donors=by.get((inv['white'].get(n),inv['black'].get(n)),[])
 report.append({**row,'missing':missing,'exact_WB_donors':sorted(donors)})
(out/'inventory.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
(out/'remaining.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2))
print(json.dumps({'remaining':len(rows),'provider_names':len(report),'missing_variants':sum(len(x['missing']) for x in report),'exact_WB_donors':[{'name':x['name'],'donors':x['exact_WB_donors']} for x in report if x['exact_WB_donors'] and x['missing']]},ensure_ascii=False))
