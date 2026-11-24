import json,hashlib,io,zipfile,urllib.request,collections,re,ast
from pathlib import Path
P=Path(__file__).parent;out=Path('remaining-161');out.mkdir(exist_ok=True)
def get(u):
 with urllib.request.urlopen(u,timeout=90) as r:return r.read()
def sha(b):return hashlib.sha256(b).hexdigest()
R='https://raw.githubusercontent.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/3c38ab56743b9642f6942a4ee1f692c534932ef9/'
Q='https://raw.githubusercontent.com/Evolution-by-Warder/PiconHub-Warder-Evolution/442737a26266cabd011ddbc8324203816adff1bb/'
rows=json.loads((P/'remaining.json').read_text());assert len(rows)==161
cat=get(R+'assets/warder/downloads.json');(out/'downloads.json').write_bytes(cat);a=json.loads(cat);a=a.get('assets',a)
inv={};zip_stats=[]
for s,k,count in [('transparent','piconProv-220',1367),('white','piconProv-w',1387),('black','piconProv-b',1402)]:
 raw=get(R+'assets/warder/downloads/picons/providers/'+s+'/piconProv.zip');assert sha(raw)==a[k]['sha256'];assert len(raw)==a[k]['size']
 (out/(s+'.zip')).write_bytes(raw)
 with zipfile.ZipFile(io.BytesIO(raw)) as z:
  assert z.testzip() is None and len(z.namelist())==count
  inv[s]={n.removeprefix('piconProv/'):sha(z.read(n)) for n in z.namelist()}
  assert len(inv[s])==count
  buf=io.BytesIO()
  with zipfile.ZipFile(buf,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as dest:
   for item in z.infolist():dest.writestr(item.filename,z.read(item),compress_type=zipfile.ZIP_DEFLATED,compresslevel=9)
  with zipfile.ZipFile(buf) as dest:assert dest.testzip() is None and all(sha(dest.read('piconProv/'+n))==h for n,h in inv[s].items())
  zip_stats.append({'style':s,'current':len(raw),'repacked':len(buf.getvalue()),'saved':len(raw)-len(buf.getvalue()),'reserve_after':32*1024*1024-len(buf.getvalue())})
provider=[{**x,'missing':[s for s in inv if x['name'] not in inv[s]]} for x in rows if x['kind']=='PROVIDER']
(out/'provider-inventory.json').write_text(json.dumps(provider,ensure_ascii=False,indent=2))
index_url='https://raw.githubusercontent.com/picons/picons/6f1df44e1a9ac40db54355afc548135c5dbbe5d8/build-source/srp.index'
index=get(index_url).decode('utf-8',errors='replace');lines=index.splitlines();matches=[]
for x in rows:
 if x['kind']!='DTT':continue
 n=x['name'].removesuffix('.png');f=n.split('_');pattern=re.compile(r'(?i)(?:^|\s)'+re.escape('_'.join(f[3:6]))+r'_',re.I)
 near=[l for l in lines if pattern.search(l) or ('_'+ '_'.join(f[3:6])+'_').casefold() in l.casefold()]
 exact=[l for l in near if n.casefold() in l.casefold()]
 matches.append({**x,'exact':exact,'same_sid_tsid_onid':near[:30]})
(out/'dtt-index-evidence.json').write_text(json.dumps(matches,ensure_ascii=False,indent=2))
# Locate client checks rather than guessing a receiver limit.
srcs=[('skin/plugin.py',R+'source/package-root/usr/lib/enigma2/python/Plugins/Extensions/setupGlass17/plugin.py'),('skin/warderCanonicalPicons.py',R+'source/package-root/usr/lib/enigma2/python/Plugins/Extensions/setupGlass17/warderCanonicalPicons.py'),('skin/warderPiconSync.py',R+'source/package-root/usr/lib/enigma2/python/Plugins/Extensions/setupGlass17/warderPiconSync.py'),('piconhub/warder_skin_sync.py',Q+'plugin/src/Plugins/Extensions/WarderPiconHub/warder_skin_sync.py'),('piconhub/warder_engine.py',Q+'plugin/src/Plugins/Extensions/WarderPiconHub/warder_engine.py'),('piconhub/warder_gui.py',Q+'plugin/src/Plugins/Extensions/WarderPiconHub/warder_gui.py')]
evidence={}
for n,u in srcs:
 try:
  t=get(u).decode('utf-8');ll=t.splitlines()
  terms=re.compile(r'32\s*\*\s*1024|33554432|32\s*<<|32\s*MiB|32\s*MB|def\s+\w*(?:AuxiliaryArchive|CanonicalPicon|[Dd]ownload[Aa]ux|[Ff]etch[Aa]ux)|canonical-220x132-v1')
  evidence[n]={'sha256':sha(t.encode()),'matches':[{'line':i+1,'context':'\n'.join(ll[max(0,i-5):i+8])} for i,l in enumerate(ll) if terms.search(l)]}
 except Exception as e:evidence[n]={'error':str(e)}
(out/'client-limit-evidence.json').write_text(json.dumps(evidence,ensure_ascii=False,indent=2))
print(json.dumps({'rows':len(rows),'providers':len(provider),'provider_missing_variants':sum(len(x['missing']) for x in provider),'repack':zip_stats,'DTT_same_triplet':[{'name':x['name'],'matches':x['same_sid_tsid_onid']} for x in matches if x['same_sid_tsid_onid']]},ensure_ascii=False))
