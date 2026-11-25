import hashlib,json,io,zipfile,sys
from pathlib import Path
from PIL import Image
P=Path(sys.argv[1]);review=Path(sys.argv[2]);out=P/'reports/italia-tvn-wbd-20261125';out.mkdir(parents=True,exist_ok=True)
A=P/'assets/warder/downloads/picons/providers'; C=P/'assets/warder/downloads.json';catalog=json.loads(C.read_text());assets=catalog['assets']
def sha(b):return hashlib.sha256(b).hexdigest()
def valid_png(b):
 im=Image.open(io.BytesIO(b));im.load();assert im.size==(220,132) and im.mode=='RGBA'
def verify(path,a):
 b=path.read_bytes();assert len(b)==a['size'] and sha(b)==a['sha256'];z=zipfile.ZipFile(io.BytesIO(b));assert z.testzip() is None and len(z.namelist())==a['png_count'];assert len({n.casefold() for n in z.namelist()})==len(z.namelist());return b,z
def pack(values,base=None):
 b=io.BytesIO(base or b'')
 with zipfile.ZipFile(b,'a' if base else 'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
  for n,d in sorted(values.items()):z.writestr(zipfile.ZipInfo(n,(1980,1,1,0,0,0)),d,compress_type=zipfile.ZIP_DEFLATED,compresslevel=9)
 return b.getvalue()
assert assets['piconProv-220']['sha256']=='cba12a408d19a8093cf9fb93f0d218405e5ad0fb7d13373e9cb33f356520cbb1'
assert assets['piconProv-b']['sha256']=='c203ef2cebed4e1466c8cff40d6cc82b869fa92b177c1df12f6af3f81c3ebfde'
assert assets['piconProv-w']['sha256']=='491ff2a8d28c3e6fe06f6eb426a83617794b0574c9593b7392bfb4e788fb19c2'
source=(review/'originals/TVNWBD.png').read_bytes();assert sha(source)=='e69e8d48075ae9cfad036fe633dc56ba1e295e8bf59cfae68c10437eeb9fe6e1'
(out/'TVNWBD-original.png').write_bytes(source)
spec={'transparent':('piconProv-220',['TVN WBD.png','TVN_WBD.png'],'ad0141dd2fe0321be6a73c72660cdb78fad2b936fc595b70c4a29603005db50c'),'white':('piconProv-w',['TVN WBD.png','TVN_WBD.png'],'5b543d97925e9c7b2cb6c1278b5e41f3d49e349a965c3c1d0a1c4b7001f777b0'),'black':('piconProv-b',['TVN WBD.png'],'4586a2a417ee0b00c6ad5dc1c62da5ee4c1b07420a20c469b9fd117db7fac1cd')}
report={'base':'32d253f7329329e31c3b9d4f56221597ef680e8a','review_run':45558356776,'source_sha256':sha(source),'new_png':5,'names':2,'archives':[]}
for s,(key,names,expected) in spec.items():
 a=assets[key];path=A/s/'piconProv.zip';before,z=verify(path,a);orig=set(z.namelist())
 delta={}
 for n in names:
  b=(review/s/n).read_bytes();assert sha(b)==expected;valid_png(b);delta['piconProv/'+n]=b
 # existing Tivibu and aliases preserved; copy evidence for separate brand review.
 for n in z.namelist():
  if n.rsplit('/',1)[-1].upper() in ('TIVIBU.PNG','TIVUBU.PNG','TVN_WBD.PNG','TVN WBD.PNG'):
   ep=Path('evidence')/s/n.rsplit('/',1)[-1];ep.parent.mkdir(parents=True,exist_ok=True);ep.write_bytes(z.read(n))
 if s=='white':
  v=assets[key+'-v2'];assert v['base_sha256']==a['sha256'] and len(v['extensions'])==1
  old_ext=v['extensions'][0];extpath=A/s/'extension-01'/'piconProv.zip';extbefore,extz=verify(extpath,old_ext)
  assert old_ext['sha256']=='e362e8636b23ec203e954a381ccadffb76420b4bb28bb320f0bd4a8f8e28c6d7'
  orig|=set(extz.namelist());assert len(orig)==v['png_count'];assert not ({n.casefold() for n in orig}&{n.casefold() for n in delta})
  new=pack(delta);np=A/s/'extension-02'/'piconProv.zip';assert not np.exists();np.parent.mkdir(parents=True);np.write_bytes(new)
  item=dict(old_ext);item.update(png_count=len(delta),size=len(new),sha256=sha(new),url=old_ext['url'].replace('extension-01','extension-02'));v['extensions'].append(item);v['png_count']+=len(delta);v['unpacked_size']+=sum(map(len,delta.values()))
  assert path.read_bytes()==before and extpath.read_bytes()==extbefore
  with zipfile.ZipFile(io.BytesIO(new)) as nz:assert nz.testzip() is None and set(nz.namelist())==set(delta) and all(nz.read(n)==b for n,b in delta.items())
  report['archives'].append(dict(style=s,count=v['png_count'],new_extension_sha256=sha(new),new_extension_bytes=len(new),old_archives_unchanged=True))
 else:
  assert not ({n.casefold() for n in orig}&{n.casefold() for n in delta})
  new=pack(delta,before);assert len(new)<=32*1024*1024
  with zipfile.ZipFile(io.BytesIO(new)) as nz:
   assert nz.testzip() is None and set(nz.namelist())==orig|set(delta)
   assert all(nz.read(n)==z.read(n) for n in orig) and all(nz.read(n)==b for n,b in delta.items())
  path.write_bytes(new);a.update(png_count=len(orig)+len(delta),sha256=sha(new),size=len(new))
  report['archives'].append(dict(style=s,count=a['png_count'],sha256=sha(new),bytes=len(new),old_png_unchanged=True))
C.write_text(json.dumps(catalog,ensure_ascii=False,indent=2)+'\n')
(out/'build.json').write_text(json.dumps(report,indent=2)+'\n')
(out/'README.md').write_text('Owner-approved continuation of Italian provider processing. Five TVN WBD alias variants, exact previously visually reviewed PNGs from run 45558356776; original source preserved, no existing PNG changed. DTT and other providers unchanged. Remaining: 34 provider names (TIVIBU pending legacy variant review, ACI pending cleaner logo) and 5 DTT references. Publication requires successful PR checks and live verification.\n')
print(json.dumps(report))
