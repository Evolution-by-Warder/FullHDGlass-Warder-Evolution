import pathlib,json,hashlib,io,zipfile,concurrent.futures,gzip,time,struct
from PIL import Image
B=pathlib.Path('audit-cache');O=pathlib.Path('audit-output/packages');O.mkdir(parents=True,exist_ok=True)
M=json.load(open('manifest.json'));spec={x['filename']:x for x in M['parts']}
def ref(n):
 f=pathlib.PurePosixPath(n).stem.split('_')
 if len(f)!=10:return None
 try:return '_'.join(f'{int(x,16):X}' for x in f)
 except ValueError:return None

def process(p):
 dest=O/(p['filename']+'.json.gz')
 if dest.exists():return json.loads(gzip.decompress(dest.read_bytes()))['summary']
 bs=[]
 for u in p['parts']:
  n=u.rsplit('/',1)[-1];v=(B/n).read_bytes();s=spec[n];assert len(v)==s['bytes'] and hashlib.sha256(v).hexdigest()==s['sha256'];bs.append(v)
 raw=b''.join(bs);assert len(raw)==p['bytes'] and hashlib.sha256(raw).hexdigest()==p['sha256'];rows=[];issues=[]
 with zipfile.ZipFile(io.BytesIO(raw))as z:
  names=z.namelist();assert len(names)==len(set(names))
  for n in names:
   if not n.lower().endswith('.png'):continue
   v=z.read(n);r=ref(n)
   if r is None:issues.append({'member':n,'issue':'INVALID_REFERENCE'})
   with Image.open(io.BytesIO(v))as im:
    im.load();size=im.size;rgba=im.convert('RGBA');px=hashlib.sha256(rgba.tobytes()).hexdigest();bbox=rgba.getchannel('A').getbbox()
    if size!=tuple(map(int,p['resolution'].split('x'))):issues.append({'member':n,'issue':'WRONG_DIMENSIONS','actual':size})
    if not bbox:issues.append({'member':n,'issue':'EMPTY_ALPHA'})
   rows.append({'reference':r,'member':n,'sha256':hashlib.sha256(v).hexdigest(),'rgba_sha256':px,'size':size})
  assert z.testzip()is None
 summary={k:p[k] for k in ('filename','selector_id','resolution','family','warder_key','sha256')};summary.update(png_count=len(rows),declared_png_count=p.get('png_count'),issues=issues,status='VERIFIED' if not issues else 'ISSUES')
 dest.write_bytes(gzip.compress(json.dumps({'summary':summary,'rows':rows},separators=(',',':')).encode(),mtime=0));print('VERIFIED',p['selector_id'],p['resolution'],p['family'],len(rows),len(issues),flush=True);return summary
if __name__=='__main__':
 remaining={p['filename']:p for p in M['packages']};summaries=[]
 while remaining:
  ready=[p for p in remaining.values()if all((B/u.rsplit('/',1)[-1]).exists()and (B/u.rsplit('/',1)[-1]).stat().st_size==spec[u.rsplit('/',1)[-1]]['bytes'] for u in p['parts'])]
  if not ready:time.sleep(3);continue
  with concurrent.futures.ThreadPoolExecutor(max_workers=4)as pool:
   for p,s in zip(ready,pool.map(process,ready)):summaries.append(s);remaining.pop(p['filename'])
  pathlib.Path('audit-output/package-summary.json').write_text(json.dumps(summaries,indent=2));print('PACKAGES',len(summaries),len(M['packages']),flush=True)
