import json, hashlib, io, urllib.request, urllib.parse, zipfile
from pathlib import Path
from PIL import Image,ImageDraw
import cairosvg
from concurrent.futures import ThreadPoolExecutor
ROOT=Path(__file__).parent
plan=json.loads((ROOT/'plan.json').read_text())
def get(u,limit=8*1024*1024):
 req=urllib.request.Request(u,headers={'User-Agent':'WarderEvolution-LogoReview/1.0 (https://warder-evolution.eu/)'})
 with urllib.request.urlopen(req,timeout=30) as r:
  b=r.read(limit+1);assert len(b)<=limit
  return b
def sha(b):return hashlib.sha256(b).hexdigest()
def gitsha(b):return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
master='https://raw.githubusercontent.com/Evolution-by-Warder/PiconHub-Warder-Evolution/05f7e6e92f55c1476b1310287e9918f0968bf7ff/plugin/artwork/templates/picons/'
base='https://raw.githubusercontent.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/a0e41c797c0bf4584898dd33434cc000abbcbc41/assets/warder/downloads/picons/providers/'
styles=('transparent','white','black');frames={};inventory={}
for s,h in [('white','c6ae4a808a65ffc8e6458336fccbfe4216de1e832ec0a9abf800907f2f783589'),('black','61e69f7fc46e340453bf74ccd7af6ac9d8eba9f8e232884659e1ea99f6abf3fe')]:
 b=get(master+s+'-sablona.png');assert sha(b)==h;frames[s]=Image.open(io.BytesIO(b)).convert('RGBA');assert frames[s].size==(220,132)
for s,h in [('transparent','d751759b7783cd25de5cbc830ea1eec66c7837f9a7bcebcaa888ccca2528cf33'),('white','97ad98bb12a7efe46f79c36e9d22ca2a0d35a9481f4677cd1964c8aaefd5f308'),('black','6be9ea1c9c68e307a3aa5fc5c25c4a1afa9921ffa61602fad2c3f48baae88477')]:
 b=get(base+s+'/piconProv.zip',32*1024*1024);assert sha(b)==h
 with zipfile.ZipFile(io.BytesIO(b)) as z:inventory[s]=set(z.namelist())
def load(x):
 try:
  if x['type']=='commons':
   n=x['name'].replace(' ','_');h=hashlib.md5(n.encode()).hexdigest();url='https://upload.wikimedia.org/wikipedia/commons/'+h[0]+'/'+h[:2]+'/'+urllib.parse.quote(n)
  else:url=x['source']
  b=get(url)
  if 'git_sha' in x:assert gitsha(b)==x['git_sha']
  im=Image.open(io.BytesIO(cairosvg.svg2png(bytestring=b,output_width=700) if x['name'].endswith('.svg') else b)).convert('RGBA')
  assert im.getchannel('A').getextrema()[0]==0,'opaque source'
  bb=im.getchannel('A').getbbox();assert bb;im=im.crop(bb);im.thumbnail((192,104),Image.Resampling.LANCZOS)
  return x,b,im,url,None
 except Exception as e:return x,None,None,None,str(e)
out=Path('vector-review');out.mkdir(exist_ok=True);rows=[];samples=[]
with zipfile.ZipFile(out/'Warder_Vector_Provider_REVIEW.zip','w',zipfile.ZIP_DEFLATED) as z:
 with ThreadPoolExecutor(max_workers=5) as ex:
  for x,b,im,url,err in ex.map(load,plan):
   if err:rows.append({**x,'error':err});continue
   slug=sha(b)[:16];z.writestr('sources/'+slug+'-'+x['name'],b)
   marks={}
   for s in styles:
    c=Image.new('RGBA',(220,132)) if s=='transparent' else frames[s].copy()
    c.alpha_composite(im,((220-im.width)//2,(132-im.height)//2));buf=io.BytesIO();c.save(buf,format='PNG',optimize=True);marks[s]=buf.getvalue()
   for n in x['targets']:
    rec={'name':n,'source':x['source'],'download_url':url,'sha256':sha(b),'status':'REVIEW_ONLY','variants':{}}
    for s in styles:
     if 'piconProv/'+n in inventory[s]:continue
     path=f'variants/{slug}/{s}/piconProv/{n}';z.writestr(path,marks[s]);rec['variants'][s]={'path':path,'sha256':sha(marks[s])}
    rows.append(rec)
   samples.append((x['name'],marks))
 z.writestr('register.json',json.dumps(rows,ensure_ascii=False,indent=2))
 z.writestr('README.txt','Review only. Public brand sources and Git commit-pinned community sources. Check exact service/brand and contrast before publication. No production modifications.')
assert samples,'No usable logo downloaded'
sheet=Image.new('RGB',(660,152*len(samples)),(170,170,170));d=ImageDraw.Draw(sheet)
for i,(name,marks) in enumerate(samples):
 d.text((4,i*152),name,fill='black')
 for j,s in enumerate(styles):
  im=Image.open(io.BytesIO(marks[s])).convert('RGBA');sheet.paste(im,(j*220,i*152+19),im)
sheet.save(out/'contact.jpg',quality=90)
with zipfile.ZipFile(out/'Warder_Vector_Provider_REVIEW.zip') as z:assert z.testzip() is None
print(json.dumps({'sources_ok':len(samples),'unique_candidate_names':len({x['name'] for x in rows if 'variants' in x}),'variants':sum(len(x.get('variants',{})) for x in rows),'errors':[x for x in rows if 'error' in x]},ensure_ascii=False))
