import hashlib,io,json,zipfile,struct
from pathlib import Path
ROOT=Path(__file__).parent;plan=json.loads((ROOT/'aliases.json').read_text())
def sha(b):return hashlib.sha256(b).hexdigest()
A=Path('assets/warder/downloads/picons/providers');catpath=Path('assets/warder/downloads.json');cat=json.loads(catpath.read_text());assets=cat.get('assets',cat)
names={'piconProv/'+n for n in plan['targets']};donor='piconProv/VIASAT.UA.png'
for s,k,h,c in [('white','piconProv-w','28a5341a7fc4d5cd7ef2d528f9ff2513c808c0844743c88d75b2fba828eb85b4',1340),('black','piconProv-b','7a82fd63620f9af04e0d11f34611110d6f42e23a2657469bb71d294882b1d4cd',1365)]:
 raw=(A/s/'piconProv.zip').read_bytes();assert sha(raw)==h==assets[k]['sha256']
 with zipfile.ZipFile(io.BytesIO(raw)) as z:
  assert len(z.namelist())==c and z.testzip() is None
  assert all(z.read(n)==z.read(donor) for n in names),(s,'existing variants differ')
path=A/'transparent'/'piconProv.zip';before=path.read_bytes();meta=assets['piconProv-220'];assert sha(before)==meta['sha256']=='024b1c70ac31e4b68dc69976e97e59dec8285b48ba2055d426a75944374ed4cc'
with zipfile.ZipFile(io.BytesIO(before)) as z:
 old=set(z.namelist());assert len(old)==1286 and z.testzip() is None;assert not {n.casefold() for n in old}&{n.casefold() for n in names}
 data=z.read(donor);assert data[:8]==bytes.fromhex('89504e470d0a1a0a') and struct.unpack('>II',data[16:24])==(220,132)
buf=io.BytesIO(before)
with zipfile.ZipFile(buf,'a',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
 for n in sorted(names):z.writestr(zipfile.ZipInfo(n,(1980,1,1,0,0,0)),data,compress_type=zipfile.ZIP_DEFLATED)
after=buf.getvalue()
with zipfile.ZipFile(io.BytesIO(before)) as a,zipfile.ZipFile(io.BytesIO(after)) as z:
 assert z.testzip() is None and set(z.namelist())==old|names
 assert all(z.read(n)==a.read(n) for n in old) and all(z.read(n)==data for n in names)
assert len(after)<32*1024*1024
path.write_bytes(after);meta.update(sha256=sha(after),size=len(after),png_count=len(old)+len(names));catpath.write_text(json.dumps(cat,ensure_ascii=False,indent=2)+'\n')
report={'names':plan['targets'],'added':len(names),'transparent_count':len(old)+len(names),'transparent_sha256':sha(after),'donor_sha256':sha(data),'preserved':len(old)}
(ROOT/'alias-build.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
