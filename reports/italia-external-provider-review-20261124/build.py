import hashlib,io,json,urllib.request,zipfile
from pathlib import Path
from PIL import Image
import cairosvg
from concurrent.futures import ThreadPoolExecutor
ROOT=Path(__file__).parent
out=Path('external-review');out.mkdir(exist_ok=True)
def get(u):
 with urllib.request.urlopen(u,timeout=45) as r:return r.read()
def sha(b):return hashlib.sha256(b).hexdigest()
def gitsha(b):return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
repo='https://raw.githubusercontent.com/picons/picons/6f1df44e1a9ac40db54355afc548135c5dbbe5d8/build-source/logos/'
base='https://raw.githubusercontent.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/024d891698d68a71adc4e978e5eeb730444cce60/assets/warder/downloads/picons/providers/'
master='https://raw.githubusercontent.com/Evolution-by-Warder/PiconHub-Warder-Evolution/27df64cf3884d1190c9016a0fcdac2866c5b5f7e/plugin/artwork/templates/picons/'
styles=['transparent','white','black']
frames={}
inventory={}
for s,h in [('white','c6ae4a808a65ffc8e6458336fccbfe4216de1e832ec0a9abf800907f2f783589'),('black','61e69f7fc46e340453bf74ccd7af6ac9d8eba9f8e232884659e1ea99f6abf3fe')]:
 b=get(master+s+'-sablona.png');assert sha(b)==h;frames[s]=Image.open(io.BytesIO(b)).convert('RGBA')
for s in styles:
 with zipfile.ZipFile(io.BytesIO(get(base+s+'/piconProv.zip'))) as z: inventory[s]=set(z.namelist())
plan=json.loads((ROOT/'plan.json').read_text())
def load(x):
 try:
  b=get(repo+x['path']);assert gitsha(b)==x['git_sha']
  im=Image.open(io.BytesIO(cairosvg.svg2png(bytestring=b,output_width=600) if x['path'].endswith('.svg') else b)).convert('RGBA')
  assert im.getchannel('A').getextrema()[0]==0,'opaque source'
  bbox=im.getchannel('A').getbbox();assert bbox;im=im.crop(bbox);im.thumbnail((192,104),Image.Resampling.LANCZOS)
  return x,b,im,None
 except Exception as e:return x,None,None,str(e)
records=[]
with zipfile.ZipFile(out/'Warder_External_Provider_REVIEW.zip','w',zipfile.ZIP_DEFLATED) as z:
 with ThreadPoolExecutor(max_workers=8) as ex:
  for x,b,im,e in ex.map(load,plan):
   if e:records.append({**x,'error':e});continue
   z.writestr('sources/'+x['path'],b)
   for n in x['targets']:
    rec={'name':n,'source':x['path'],'source_git_sha':x['git_sha'],'source_sha256':sha(b),'status':'REVIEW_ONLY','variants':{}}
    for s in styles:
     if 'piconProv/'+n in inventory[s]:continue
     canvas=Image.new('RGBA',(220,132)) if s=='transparent' else frames[s].copy()
     canvas.alpha_composite(im,((220-im.width)//2,(132-im.height)//2));buf=io.BytesIO();canvas.save(buf,format='PNG',optimize=True)
     path=f'variants/{s}/piconProv/{n}';data=buf.getvalue();z.writestr(path,data);rec['variants'][s]={'path':path,'sha256':sha(data)}
    records.append(rec)
 z.writestr('register.json',json.dumps(records,ensure_ascii=False,indent=2))
 z.writestr('README.txt','REVIEW only. Candidate identity must be checked visually against user-supplied original; no production writes. External source picons/picons commit 6f1df44e1a9ac40db54355afc548135c5dbbe5d8 (GPL-3.0 repository; logos may carry separate brand rights).')
with zipfile.ZipFile(out/'Warder_External_Provider_REVIEW.zip') as z:assert z.testzip() is None
print(json.dumps({'candidate_names':sum('name'in x for x in records),'variants':sum(len(x.get('variants',{})) for x in records),'errors':[x for x in records if 'error'in x]},ensure_ascii=False))
