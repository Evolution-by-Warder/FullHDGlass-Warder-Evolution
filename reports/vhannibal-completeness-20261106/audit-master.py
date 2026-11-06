from pathlib import Path
import json,zipfile,io,hashlib,concurrent.futures,gzip,time
import numpy as np
from PIL import Image
O=Path('audit-output');D=O/'master';D.mkdir(exist_ok=True);M=json.load(open('manifest.json'))
def one(p):
 out=D/(p['filename']+'.json.gz')
 if out.exists():return
 master=Image.open(Path('audit-cache')/(p['family'].removeprefix('channel-')+'-sablona.png')).convert('RGBA');size=tuple(map(int,p['resolution'].split('x')))
 if size!=master.size:master=master.convert('RGBa').resize(size,Image.Resampling.LANCZOS).convert('RGBA')
 a=np.array(master);mask=np.ones((size[1],size[0]),dtype=bool);margin=max(1,round(3*size[0]/220));mask[margin:-margin,margin:-margin]=False;expected=a[mask];rows=[]
 raw=b''.join((Path('audit-cache')/u.rsplit('/',1)[-1]).read_bytes()for u in p['parts'])
 with zipfile.ZipFile(io.BytesIO(raw))as z:
  for n in z.namelist():
   if not n.endswith('.png'):continue
   im=Image.open(io.BytesIO(z.read(n))).convert('RGBA');ar=np.array(im)
   if im.size!=size:continue
   same=np.all(ar[mask]==expected);rows.append({'reference':Path(n).stem,'v9_outer_edge_exact':bool(same),'different_edge_pixels':int(np.any(ar[mask]!=expected,axis=1).sum())})
 out.write_bytes(gzip.compress(json.dumps({'package':p['filename'],'selector':p['selector_id'],'resolution':p['resolution'],'family':p['family'],'rows':rows},separators=(',',':')).encode(),mtime=0))
if __name__=='__main__':
 remaining=[p for p in M['packages']if p['family']in('channel-black','channel-white')]
 while remaining:
  ready=[p for p in remaining if (O/'packages'/(p['filename']+'.json.gz')).exists()]
  if not ready:time.sleep(3);continue
  with concurrent.futures.ThreadPoolExecutor(max_workers=4)as pool:list(pool.map(one,ready))
  remaining=[p for p in remaining if p not in ready];print('MASTER_PACKAGES',332-len(remaining),332,flush=True)
