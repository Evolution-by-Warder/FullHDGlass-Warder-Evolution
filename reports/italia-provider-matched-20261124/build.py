import hashlib,io,json,zipfile,struct
from pathlib import Path
ROOT=Path(__file__).parent;plan=json.loads((ROOT/'plan.json').read_text())
def sha(b):return hashlib.sha256(b).hexdigest()
catpath=Path('assets/warder/downloads.json');cat=json.loads(catpath.read_text());assets=cat.get('assets',cat)
records=[]
with zipfile.ZipFile('external-review/Warder_External_Provider_REVIEW.zip') as src:
 assert src.testzip() is None
 for s,key in [('transparent','piconProv-220'),('white','piconProv-w'),('black','piconProv-b')]:
  path=Path('assets/warder/downloads/picons/providers')/s/'piconProv.zip'
  before=path.read_bytes();meta=assets[key];assert sha(before)==meta['sha256']==plan['baseline'][s]['sha256']
  additions={}
  with zipfile.ZipFile(io.BytesIO(before)) as z:
   assert z.testzip() is None;assert len(z.namelist())==plan['baseline'][s]['count']
   if s=='transparent':
    for n,h in plan['targets'].items():
     data=src.read('variants/transparent/piconProv/'+n);assert sha(data)==h;additions['piconProv/'+n]=data
   else:
    additions['piconProv/AFN.png']=z.read('piconProv/'+plan['afn_donor'])
   old=set(z.namelist()); assert not {n.casefold() for n in old}&{n.casefold() for n in additions}
   assert all(b[:8]==bytes.fromhex('89504e470d0a1a0a') and struct.unpack('>II',b[16:24])==(220,132) for b in additions.values())
  buf=io.BytesIO(before)
  with zipfile.ZipFile(buf,'a',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
   for n,b in sorted(additions.items()):z.writestr(zipfile.ZipInfo(n,(1980,1,1,0,0,0)),b,compress_type=zipfile.ZIP_DEFLATED)
  after=buf.getvalue()
  with zipfile.ZipFile(io.BytesIO(before)) as a,zipfile.ZipFile(io.BytesIO(after)) as z:
   assert z.testzip() is None and set(z.namelist())==set(a.namelist())|set(additions)
   assert all(a.read(n)==z.read(n) for n in a.namelist())
   assert all(z.read(n)==b for n,b in additions.items())
  assert len(after)<32*1024*1024
  path.write_bytes(after);meta.update(sha256=sha(after),size=len(after),png_count=len(old)+len(additions))
  records.append({'style':s,'added':len(additions),'count':meta['png_count'],'sha256':meta['sha256'],'preserved':len(old),'names':list(additions)})
catpath.write_text(json.dumps(cat,ensure_ascii=False,indent=2)+'\n')
assert sum(x['added'] for x in records)==10
(ROOT/'build.json').write_text(json.dumps(records,indent=2)+'\n');print(json.dumps(records))
