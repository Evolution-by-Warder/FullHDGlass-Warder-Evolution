import hashlib,io,json,sys,zipfile,re,urllib.request,concurrent.futures
from pathlib import Path
from PIL import Image,ImageDraw
P=Path(sys.argv[1]);work=Path(__file__).parent;out=P/'reports/italia-tivibu-fix-20261125';out.mkdir(parents=True,exist_ok=True)
review=Path('donor-review');review.mkdir(exist_ok=True)
A=P/'assets/warder/downloads/picons/providers';C=P/'assets/warder/downloads.json';catalog=json.loads(C.read_text());assets=catalog['assets']
def sha(b):return hashlib.sha256(b).hexdigest()
def verify(path,a):
 b=path.read_bytes();assert len(b)==a['size'] and sha(b)==a['sha256'];z=zipfile.ZipFile(io.BytesIO(b));assert z.testzip() is None and len(z.namelist())==a['png_count'];return b,z
expected={'transparent':('piconProv-220','802268c5b346bd28ed41daab9b1160bdd0d3db5e85ab6684ef552a82ba8ae751','9766de9a2671c26c8fdd7118b096e85a11a60996a350100d73604ddf85ef68a2',None),'white':('piconProv-w','491ff2a8d28c3e6fe06f6eb426a83617794b0574c9593b7392bfb4e788fb19c2','10a164bef1be280bc6f0f5fc1ef5e4683e2c0a53a30d2b8d355ac851dec9d485','02bc6c295cb4650921e6b4f7c968e152ba1ff86cea9c12ff4a6cacc5c42d0b7d'),'black':('piconProv-b','04cbae751f5f7755058375e4cb9490a7c7770bb97aa45c40cb1a2204a26ff2f9','055b2c3556acdf84d6a997424baedd710b412aacf74479b843b41ba4cd1d7c2f','8907fe7764f7dec1a78a4ef996e8195b1a2ade1c8e92b4b5c897479bdac3c08d')}
target='piconProv/TIVIBU.png';donor='piconProv/TIVUBU.png'
report={'base':'1c9e1bfc3e669e2e3a8ecb1e780172e68e210d3a','new_png':1,'corrected_png':2,'identity_sources':['https://www.lyngsat.com/providers/tr/Tivibu.html','https://bireysel.turktelekom.com.tr/tivibu'],'archives':[]}
allstyle={}
for s,(key,base,donorhash,wronghash) in expected.items():
 a=assets[key];assert a['sha256']==base
 p=A/s/'piconProv.zip';before,z=verify(p,a);old={n:z.read(n) for n in z.namelist()}
 d=old[donor];assert sha(d)==donorhash and Image.open(io.BytesIO(d)).size==(220,132)
 if wronghash:assert sha(old[target])==wronghash
 else:assert target not in old and target.casefold() not in {n.casefold() for n in old}
 dest=review/s;dest.mkdir(exist_ok=True);(dest/'TIVIBU-correct.png').write_bytes(d)
 if wronghash:(dest/'TIVIBU-old-wrong.png').write_bytes(old[target])
 buf=io.BytesIO()
 with zipfile.ZipFile(buf,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as nz:
  for info in z.infolist():
   nz.writestr(info,d if info.filename==target else old[info.filename])
  if target not in old:nz.writestr(zipfile.ZipInfo(target,(1980,1,1,0,0,0)),d,compress_type=zipfile.ZIP_DEFLATED,compresslevel=9)
 after=buf.getvalue();assert len(after)<=32*1024*1024
 with zipfile.ZipFile(io.BytesIO(after)) as nz:
  assert nz.testzip() is None and set(nz.namelist())==set(old)|{target}
  assert len(nz.namelist())==len(set(nz.namelist())) and nz.read(target)==d
  assert all(nz.read(n)==b for n,b in old.items() if n!=target)
  values={n:nz.read(n) for n in nz.namelist()}
 if s=='white':
  v=assets[key+'-v2'];assert v['base_sha256']==base and len(v['extensions'])==2
  delta=len(d)-len(old[target]);v['base_sha256']=sha(after);v['unpacked_size']+=delta
  for i,e in enumerate(v['extensions'],1):
   eb,ez=verify(A/s/f'extension-{i:02d}'/'piconProv.zip',e);assert not set(ez.namelist())&set(values)
   values.update({n:ez.read(n) for n in ez.namelist()})
  assert len(values)==v['png_count'] and sum(map(len,values.values()))==v['unpacked_size']
 allstyle[s]=values
 p.write_bytes(after);a.update(size=len(after),sha256=sha(after),png_count=len(old)+(target not in old))
 report['archives'].append(dict(style=s,count=len(values),sha256=sha(after),bytes=len(after),donor_sha256=donorhash,old_wrong_sha256=wronghash,all_other_png_bytes_unchanged=True))
C.write_text(json.dumps(catalog,ensure_ascii=False,indent=2)+'\n')
(out/'build.json').write_text(json.dumps(report,indent=2)+'\n')
(out/'README.md').write_text('TIVIBU was incorrectly assigned Italian Tivusat artwork in W/B. Correct Turkish Tivibu brand confirmed by LyngSat and Türk Telekom; reused the previously approved existing TIVUBU donor exactly for all 3 styles. Only 2 confirmed erroneous images replaced; 1 new transparent PNG; all other PNG bytes preserved. No DTT/IPK changes.\n')
# Independent inventory of still-open names, using exact same-style donor bytes and name normalization. Never publish a candidate automatically.
pending=json.loads((work/'remaining.json').read_text())['providers'];audit=[]
def norm(n):return re.sub(r'[^A-Z0-9]','',n.upper().removesuffix('.PNG'))
for rec in pending:
 n=rec['name']
 if n in ('TVN WBD.png','TVN_WBD.png','TIVIBU.png'):continue
 t='piconProv/'+n;avail={s:t in a for s,a in allstyle.items()};same={}
 for s,a in allstyle.items():
  if t in a:same[s]=[k.rsplit('/',1)[-1] for k,b in a.items() if k!=t and b==a[t]]
 aliases=sorted({k.rsplit('/',1)[-1] for a in allstyle.values() for k in a if k!=t and norm(k.rsplit('/',1)[-1])==norm(n)})
 audit.append({'name':n,'available':avail,'exact_same_style_donors':same,'normalized_aliases':aliases})
(review/'provider-inventory.json').write_text(json.dumps(audit,indent=2)+'\n')
# ACI Sport TV: exact DVB tuple 1613/9300/318 on Hotbird (SID 64D, TSID 2454, ONID 13E).
# Search 220x132 archives by verified manifest; preserve original donor PNG bytes for visual check.
def get(u):
 with urllib.request.urlopen(u,timeout=75) as r:return r.read()
try:
 m=json.loads((P/'assets/warder/downloads/picons/channels/manifest.json').read_text())
 meta={p['filename']:p for p in m['parts']}
 packages=[p for p in m['packages'] if p['resolution']=='220x132' and p['selector_id'].upper() in ('130E','13.0E','13E','TIVUSAT','TIVU_SAT')]
 (review/'aci-package-candidates.json').write_text(json.dumps([{k:p.get(k) for k in ('selector_id','filename','family','png_count','bytes')} for p in packages],indent=2))
 results=[]
 for s in ['transparent','white','black']:
  subset=[p for p in packages if p['family'].lower().endswith(s)]
  subset.sort(key=lambda p:p['bytes'])
  for p in subset:
   chunks=[]
   for u in p['parts']:
    n=u.rsplit('/',1)[-1];b=get('https://raw.githubusercontent.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/1c9e1bfc3e669e2e3a8ecb1e780172e68e210d3a/assets/warder/downloads/picons/channels/'+n)
    assert len(b)==meta[n]['bytes'] and sha(b)==meta[n]['sha256'];chunks.append(b)
   b=b''.join(chunks);assert len(b)==p['bytes'] and sha(b)==p['sha256']
   with zipfile.ZipFile(io.BytesIO(b)) as z:
    matches=[n for n in z.namelist() if re.fullmatch(r'1_0_(?:1|16|19|11)_64D_2454_13E_820000_0_0_0\.png',n.rsplit('/',1)[-1],re.I)]
    if matches:
     n=matches[0];d=z.read(n);assert Image.open(io.BytesIO(d)).size==(220,132);dest=review/s;dest.mkdir(exist_ok=True);(dest/'ACI-Sport-TV-donor.png').write_bytes(d);results.append(dict(style=s,reference=n,selector=p['selector_id'],sha256=sha(d),archive_sha256=p['sha256']));break
 (review/'aci-donors.json').write_text(json.dumps(results,indent=2))
except Exception as e:
 (review/'aci-error.txt').write_text(str(e))
print(json.dumps(report))
