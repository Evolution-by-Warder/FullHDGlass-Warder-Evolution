import hashlib,io,json,zipfile,urllib.request,importlib.util,shutil,tempfile,os,ast
from pathlib import Path
from types import SimpleNamespace
from PIL import Image
import numpy as np
from scipy.ndimage import label,binary_fill_holes
P=Path(__file__).parent
A=Path('assets/warder/downloads/picons/providers')
C=Path('assets/warder/downloads.json')
S=Path('source/package-root/usr/lib/enigma2/python/Plugins/Extensions/setupGlass17')
def sha(b):return hashlib.sha256(b).hexdigest()
def png(im):
 b=io.BytesIO();im.save(b,'PNG',optimize=True);return b.getvalue()
def image(b):return Image.open(io.BytesIO(b)).convert('RGBA')
def get(u):
 with urllib.request.urlopen(u,timeout=90) as r:return r.read()
source=(P/'source.zip').read_bytes();assert sha(source)=='d90c7a3daafe8a8734bcbe82ee193b9abfb1d78eaf0732edf6b45f3ad271b4d4'
with zipfile.ZipFile(io.BytesIO(source)) as z:
 assert z.testzip() is None
 plan=json.loads(z.read('plan.json'));fgzip=zipfile.ZipFile(io.BytesIO(z.read('foregrounds.zip')))
assert fgzip.testzip() is None and len(plan['records'])==71 and len(plan['remaining'])==36
M={}
for s,h in [('white','c6ae4a808a65ffc8e6458336fccbfe4216de1e832ec0a9abf800907f2f783589'),('black','61e69f7fc46e340453bf74ccd7af6ac9d8eba9f8e232884659e1ea99f6abf3fe')]:
 b=get('https://raw.githubusercontent.com/Evolution-by-Warder/PiconHub-Warder-Evolution/27df64cf3884d1190c9016a0fcdac2866c5b5f7e/plugin/artwork/templates/picons/'+s+'-sablona.png');assert sha(b)==h;M[s]=image(b)
def render(t,s,plate=False):
 if s=='transparent':return t
 a=np.array(t);rgb=a[:,:,:3].astype(float);lo=rgb.min(2);hi=rgb.max(2);ch=hi-lo
 if s=='white' and not plate:
  f=np.clip((lo-135)/90,0,1)*np.clip((40-ch)/30,0,1);rgb=rgb*(1-f[:,:,None])+np.array([28,32,38])*f[:,:,None]
 if s=='black' and not plate:
  f=np.clip((105-hi)/80,0,1)*np.clip(ch/40,0,1);rgb=rgb*(1-f[:,:,None])+np.clip(rgb*1.7+22,0,255)*f[:,:,None]
 a[:,:,:3]=rgb.round().astype(np.uint8);return Image.alpha_composite(M[s],Image.fromarray(a))
def tvp(im,s):
 if s=='transparent':return im
 a=np.asarray(im).copy();rgb=a[:,:,:3].astype(float);lo=rgb.min(2);hi=rgb.max(2);ch=hi-lo
 if s=='white':
  f=np.clip((lo-130)/90,0,1)*np.clip((40-ch)/30,0,1);f[:65]=0;rgb=rgb*(1-f[:,:,None])+np.array([28,32,38])*f[:,:,None]
 a[:,:,:3]=rgb.round().astype(np.uint8);return Image.alpha_composite(M[s],Image.fromarray(a))
def vb33(im,s):
 if s!='white':return render(im,s,True)
 a=np.asarray(im).copy();rgb=a[:,:,:3].astype(float);lo=rgb.min(2);hi=rgb.max(2);ch=hi-lo
 m=(a[:,:,3]>10)&(lo>120)&(ch<45);lab,_=label(m);sizes=np.bincount(lab.ravel());sizes[0]=0;badge=binary_fill_holes(lab==sizes.argmax());f=np.clip((lo-135)/90,0,1)*np.clip((40-ch)/30,0,1);f[badge]=0;rgb=rgb*(1-f[:,:,None])+np.array([28,32,38])*f[:,:,None];a[:,:,:3]=rgb.round().astype(np.uint8);return Image.alpha_composite(M[s],Image.fromarray(a))
delta={}
for rec in plan['records']:
 n=rec['name'];raw=fgzip.read(rec['foreground']+'.png');assert sha(raw)==rec['foreground'];t=image(raw);assert t.size==(220,132)
 for s,expected in rec['variants'].items():
  im=tvp(t,s) if rec['index']==85 else vb33(t,s) if rec['index']==101 else render(t,s,rec['plate'])
  b=png(im);assert sha(b)==expected['sha256'] and sha(im.convert('RGBA').tobytes())==expected['pixel_sha256'],(n,s)
  delta[s+'/piconProv/'+n]=b
assert len(delta)==181
h=hashlib.sha256()
for n,b in sorted(delta.items()):h.update(n.encode()+b'\0'+image(b).tobytes())
assert h.hexdigest()==plan['pixel_digest']
catalog=json.loads(C.read_text());assets=catalog['assets']
baseline={'transparent':(1396,'cf86080a2ab95fea9992e982bbd7150abaee49d695a1de7f18d25c15fc0304ef'),'white':(1387,'491ff2a8d28c3e6fe06f6eb426a83617794b0574c9593b7392bfb4e788fb19c2'),'black':(1402,'6bba8b5bf63f5b27e5e506e45b2320f74a2395bdc4c225b8d07bfdcbb97f7a10')}
names={r['name'] for r in plan['records']};report={'source_sha256':sha(source),'pixel_digest':h.hexdigest(),'provider_names':len(names),'added':len(delta),'remaining_provider_names':len(plan['remaining']),'archives':[]}
def write_zip(values,base=None):
 out=io.BytesIO(base or b'')
 with zipfile.ZipFile(out,'a' if base else 'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
  for n,b in sorted(values.items()):z.writestr(zipfile.ZipInfo(n,(1980,1,1,0,0,0)),b,compress_type=zipfile.ZIP_DEFLATED,compresslevel=9)
 return out.getvalue()
for s,key in [('transparent','piconProv-220'),('white','piconProv-w'),('black','piconProv-b')]:
 path=A/s/'piconProv.zip';before=path.read_bytes();count,digest=baseline[s];a=assets[key];assert sha(before)==digest==a['sha256'] and len(before)==a['size']
 v={n.split('/',1)[1]:b for n,b in delta.items() if n.startswith(s+'/')}
 supplement=write_zip(v)
 expected=plan['statistics'][s];assert len(v)==expected['png_count'] and sha(supplement)==expected['sha256'] and len(supplement)==expected['size']
 with zipfile.ZipFile(io.BytesIO(before)) as old:
  assert old.testzip() is None and len(old.namelist())==count
  old_names=set(old.namelist());assert not {n.casefold() for n in v}&{n.casefold() for n in old_names}
  assert {'piconProv/'+n for n in names}<=old_names|set(v)
  expanded=sum(i.file_size for i in old.infolist())+sum(map(len,v.values()))
 if s=='white':
  # Keep the old white ZIP unchanged. Updated clients can install the optional separate extension.
  extpath=A/s/'extension-01'/'piconProv.zip';extpath.parent.mkdir(parents=True,exist_ok=True);extpath.write_bytes(supplement)
  ext=dict(a);ext.update(url=a['url'].replace('/white/piconProv.zip','/white/extension-01/piconProv.zip'),size=len(supplement),sha256=sha(supplement),png_count=len(v),delivery='canonical-220x132-v2')
  assert key+'-v2' not in assets
  assets[key+'-v2']={'delivery':'canonical-220x132-v2','root':'piconProv','resolution':[220,132],'base_asset_id':key,'base_sha256':digest,'extensions':[ext],'png_count':count+len(v),'unpacked_size':expanded}
  assert path.read_bytes()==before
  with zipfile.ZipFile(io.BytesIO(supplement)) as z:assert z.testzip() is None and set(z.namelist())==set(v) and all(z.read(n)==b for n,b in v.items())
  report['archives'].append({'style':s,'base_count':count,'base_sha256':digest,'base_size':len(before),'extension_count':len(v),'extension_sha256':sha(supplement),'extension_size':len(supplement),'complete_count':count+len(v),'unpacked_size':expanded,'legacy_unchanged':True})
 else:
  after=write_zip(v,before);assert len(after)<=32*1024*1024
  with zipfile.ZipFile(io.BytesIO(before)) as o,zipfile.ZipFile(io.BytesIO(after)) as z:
   assert z.testzip() is None and len(z.namelist())==count+len(v) and set(z.namelist())==old_names|set(v)
   assert all(z.read(n)==o.read(n) for n in old_names) and all(z.read(n)==b for n,b in v.items())
  path.write_bytes(after);a.update(size=len(after),sha256=sha(after),png_count=count+len(v))
  report['archives'].append({'style':s,'base_count':count,'added':len(v),'complete_count':count+len(v),'size':len(after),'sha256':sha(after),'old_png_bytes_preserved':True})
C.write_text(json.dumps(catalog,ensure_ascii=False,indent=2)+'\n')
# Actual installed old client loads the assets dictionary without validating unused keys.
# Exercise the exact shipped old and new canonical installers with real archives, including SHA and CRC.
def load(p,n):
 spec=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
canonical=load(S/'warderCanonicalPicons.py','canonical');sync=load(S/'warderPiconSync.py','sync')
with tempfile.TemporaryDirectory() as work:
 work=Path(work);dest=work/'piconProv';dest.mkdir();events=[]
 class Screen:
  zzz='original'
  def _warderAuxiliaryDestination(self,root):assert root=='piconProv';return str(dest)
  def _warderFetchAuxiliaryArchive(self,asset,p,progress=None):
   assert sync.trusted_auxiliary_url(asset['url'],asset['publication_source_id'])
   f=A/'white'/('extension-01/piconProv.zip' if 'extension-01' in asset['url'] else 'piconProv.zip')
   b=f.read_bytes();assert len(b)==asset['size']<=32*1024*1024 and sha(b)==asset['sha256'];Path(p).write_bytes(b)
   assert not sync.validate_auxiliary_archive(p,asset)
   if progress:progress(len(b),len(b))
  def cprmFiles(self,root):
   files=list((Path(self.zzz)/root).glob('*.png'))
   for f in files:shutil.copyfile(f,dest/f.name)
   return len(files),len(files)
  def _warderFilesMatch(self,a,b):return Path(a).read_bytes()==Path(b).read_bytes()
 screen=Screen()
 msg=canonical.install(screen,'aux-prov','white',lambda:('',assets),lambda x:x,stage=events.append)
 assert '1447/1447' in msg and len(list(dest.glob('*.png')))==1447 and screen.zzz=='original'
 assert all((dest/n).is_file() for n in names)
 assert not list(work.glob('.warder-provider-*'))
 # The original v1 record remains a complete verified ZIP under the existing cap.
 assert assets['piconProv-w']['sha256']==baseline['white'][1] and assets['piconProv-w']['size']<32*1024*1024
 report['integration_test']={'actual_white_install':msg,'legacy_base_valid':True,'target_stage_cleanup':True,'stages':events}
(P/'plan.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2)+'\n')
(P/'build.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(report,ensure_ascii=False))
