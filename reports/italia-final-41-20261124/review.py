import hashlib, io, json, urllib.request, urllib.parse, zipfile
from pathlib import Path
from PIL import Image, ImageDraw
import cairosvg
import numpy as np
P=Path(__file__).parent
data=json.loads((P/'remaining.json').read_text())
out=P/'review-output';out.mkdir(exist_ok=True)
def sha(b):return hashlib.sha256(b).hexdigest()
def get(u):
 req=urllib.request.Request(u,headers={'User-Agent':'WarderEvolution/1.0 (public logo review; https://warder-evolution.eu)'})
 with urllib.request.urlopen(req,timeout=25) as r:
  b=r.read(2_000_001);assert len(b)<=2_000_000
  return b
templates={}
for style,h in [('white','c6ae4a808a65ffc8e6458336fccbfe4216de1e832ec0a9abf800907f2f783589'),('black','61e69f7fc46e340453bf74ccd7af6ac9d8eba9f8e232884659e1ea99f6abf3fe')]:
 b=get('https://raw.githubusercontent.com/Evolution-by-Warder/PiconHub-Warder-Evolution/27df64cf3884d1190c9016a0fcdac2866c5b5f7e/plugin/artwork/templates/picons/'+style+'-sablona.png')
 assert sha(b)==h
 templates[style]=Image.open(io.BytesIO(b)).convert('RGBA')
 assert templates[style].size==(220,132)
records=[];errors=[];images=[]
for c in data['candidates']:
 try:
  file=c['file'];h=hashlib.md5(file.encode()).hexdigest()
  url='https://upload.wikimedia.org/wikipedia/commons/'+h[0]+'/'+h[:2]+'/'+urllib.parse.quote(file)
  b=get(url)
  if c.get('sha1'):assert hashlib.sha1(b).hexdigest()==c['sha1']
  if file.endswith('.svg'):
   assert b'<svg' in b[:4000]
   # SVG rendering is sandboxed by CairoSVG (unsafe=False).
   raw=cairosvg.svg2png(bytestring=b,output_width=1000,unsafe=False)
  else:raw=b
  im=Image.open(io.BytesIO(raw)).convert('RGBA')
  assert im.getextrema()[3][0]<255 and im.getextrema()[3][1]>0
  im=im.crop(im.getbbox())
  im.thumbnail((196,108),Image.Resampling.LANCZOS)
  canvas=Image.new('RGBA',(220,132));canvas.alpha_composite(im,((220-im.width)//2,(132-im.height)//2))
  (out/'originals').mkdir(exist_ok=True);(out/'originals'/file).write_bytes(b)
  for name in c['names']:
   p=next(x for x in data['providers'] if x['name']==name)
   for style in p['missing']:
    if style=='transparent':final=canvas.copy()
    else:
     a=np.array(canvas);rgb=a[:,:,:3].astype(float);lo=rgb.min(2);hi=rgb.max(2);ch=hi-lo
     if style=='white':
      f=np.clip((lo-135)/90,0,1)*np.clip((40-ch)/30,0,1);rgb=rgb*(1-f[:,:,None])+np.array([28,32,38])*f[:,:,None]
     else:
      f=np.clip((105-hi)/80,0,1)*np.clip(ch/40,0,1);rgb=rgb*(1-f[:,:,None])+np.clip(rgb*1.7+22,0,255)*f[:,:,None]
     a[:,:,:3]=rgb.round().astype(np.uint8);final=Image.alpha_composite(templates[style],Image.fromarray(a))
    pth=out/style/name;pth.parent.mkdir(exist_ok=True);final.save(pth,optimize=True)
    assert Image.open(pth).size==(220,132)
    records.append(dict(name=name,style=style,sha256=sha(pth.read_bytes()),source_sha256=sha(b),source_url=url,state='REVIEW_NOT_PUBLISHED'))
    images.append((name,style,final))
 except Exception as e:
  errors.append(dict(names=c['names'],error=str(e)))
sheet=Image.new('RGB',(720,max(160,160*((len(images)+2)//3))),'#dddddd');d=ImageDraw.Draw(sheet)
for i,(name,style,im) in enumerate(images):
 x=i%3*240+10;y=i//3*160
 d.text((x,y+2),name+' / '+style,fill='black');sheet.paste(im,(x,y+20),im)
sheet.save(out/'contact-sheet.png')
(out/'result.json').write_text(json.dumps({'records':records,'errors':errors,'scope':data['scope']},indent=2)+'\n')
print(json.dumps({'rendered':len(records),'errors':errors}))
assert records,'No review PNG could be rendered'
