import hashlib,io,json,zipfile,urllib.request,urllib.parse
from pathlib import Path
from PIL import Image,ImageFilter
import numpy as np
ROOT=Path(__file__).parent;plan=json.loads((ROOT/'plan.json').read_text())
def sha(b):return hashlib.sha256(b).hexdigest()
def get(url):
 with urllib.request.urlopen(url,timeout=60) as r:return r.read()
def image(b):
 im=Image.open(io.BytesIO(b)).convert('RGBA');assert im.size==(220,132);return im
def encode(im):
 buf=io.BytesIO();im.save(buf,format='PNG',optimize=True);return buf.getvalue()
styles=['transparent','white','black']
frames={}
master='https://raw.githubusercontent.com/Evolution-by-Warder/PiconHub-Warder-Evolution/27df64cf3884d1190c9016a0fcdac2866c5b5f7e/plugin/artwork/templates/picons/'
for s,h in [('white','c6ae4a808a65ffc8e6458336fccbfe4216de1e832ec0a9abf800907f2f783589'),('black','61e69f7fc46e340453bf74ccd7af6ac9d8eba9f8e232884659e1ea99f6abf3fe')]:
 b=get(master+s+'-sablona.png');assert sha(b)==h;frames[s]=image(b)
adapt={'CANALE 40.png','CANALE 40REG.png',"L'ALTRO CORRIERE.png",'MUXIP.png','ROMANTICA RADIO.png','TELERENT.png','VIDEOMEDIA-TN.png','VTS.png'}
def fg(logo,s,n,ext):
 x=np.array(logo);rgb=x[:,:,:3].astype(float);lo=rgb.min(2);hi=rgb.max(2);chroma=hi-lo
 if s=='white' and ((not ext and n in adapt) or (ext and n in {'PRIMANTENNA.png','VALENZA TV.png','VALENZA_TV.png'})):
  strength=np.clip((lo-150)/75,0,1)*np.clip((45-chroma)/30,0,1)
  if n.startswith('VALENZA'):strength[:96,:]=0
  new=rgb*(1-strength[:,:,None])+np.array([32,36,42])*strength[:,:,None];x[:,:,:3]=new.round().astype(np.uint8);return Image.fromarray(x)
 if ext and s=='black' and n in {'NOS.png','TELEPACE_TRENTO.png'}:
  strength=np.clip((105-hi)/70,0,1)*np.clip((40-chroma)/30,0,1)
  if n=='TELEPACE_TRENTO.png':strength[:,:90]=0
  new=rgb*(1-strength[:,:,None])+np.array([240,240,240])*strength[:,:,None];x[:,:,:3]=new.round().astype(np.uint8);return Image.fromarray(x)
 if ext and s=='black' and n in {'TEGENOVA.png','TVN24.png'}:
  edge=logo.getchannel('A').filter(ImageFilter.MaxFilter(3)).point(lambda v:round(v*.50));layer=Image.new('RGBA',logo.size,(224,231,242,0));layer.putalpha(edge);return Image.alpha_composite(layer,logo)
 return logo
delta={}
def render(n,raw,selected,ext):
 logo=image(raw)
 for s in selected:
  im=logo if s=='transparent' else Image.alpha_composite(frames[s],fg(logo,s,n,ext))
  delta[s+'/piconProv/'+n]=raw if s=='transparent' else encode(im)
user='https://raw.githubusercontent.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/'+plan['user_source_commit']+'/reports/italia-followup-20261124/provider-master-review/transparent/'
for n in plan['user_sources']:render(n,get(user+urllib.parse.quote(n)),styles,False)
with zipfile.ZipFile('external-review/Warder_External_Provider_REVIEW.zip') as z:
 records={x['name']:x for x in json.loads(z.read('register.json')) if 'name' in x}
 for n in plan['external_sources']:
  rec=records[n];raw=z.read(rec['variants']['transparent']['path']);assert sha(raw)==rec['variants']['transparent']['sha256'];render(n,raw,list(rec['variants']),True)
h=hashlib.sha256()
for n,b in sorted(delta.items()):h.update(n.encode()+b'\0'+image(b).tobytes())
assert len(delta)==72 and h.hexdigest()==plan['expected_pixels_sha256'],(len(delta),h.hexdigest())
catpath=Path('assets/warder/downloads.json');cat=json.loads(catpath.read_text());assets=cat.get('assets',cat);report=[]
for s,key,expected in [('transparent','piconProv-220',25),('white','piconProv-w',24),('black','piconProv-b',23)]:
 path=Path('assets/warder/downloads/picons/providers')/s/'piconProv.zip';before=path.read_bytes();meta=assets[key];assert sha(before)==meta['sha256']==plan['base'][s]['sha256'];add={n.split('/',1)[1]:b for n,b in delta.items() if n.startswith(s+'/')};assert len(add)==expected
 with zipfile.ZipFile(io.BytesIO(before)) as z:
  old=set(z.namelist());assert z.testzip() is None and len(old)==plan['base'][s]['count'];assert not {n.casefold() for n in old}&{n.casefold() for n in add}
 buf=io.BytesIO(before)
 with zipfile.ZipFile(buf,'a',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
  for n,b in sorted(add.items()):z.writestr(zipfile.ZipInfo(n,(1980,1,1,0,0,0)),b,compress_type=zipfile.ZIP_DEFLATED)
 after=buf.getvalue()
 with zipfile.ZipFile(io.BytesIO(before)) as a,zipfile.ZipFile(io.BytesIO(after)) as z:
  assert z.testzip() is None and set(z.namelist())==set(a.namelist())|set(add);assert all(z.read(n)==a.read(n) for n in a.namelist());assert all(z.read(n)==b for n,b in add.items())
  assert {'piconProv/'+n for n in plan['user_sources']+plan['external_sources']}<=set(z.namelist())
 assert len(after)<32*1024*1024
 path.write_bytes(after);meta.update(sha256=sha(after),size=len(after),png_count=len(old)+len(add));report.append({'style':s,'count':meta['png_count'],'added':len(add),'sha256':sha(after),'preserved':len(old)})
catpath.write_text(json.dumps(cat,ensure_ascii=False,indent=2)+'\n');(ROOT/'build.json').write_text(json.dumps({'pixel_sha256':h.hexdigest(),'archives':report,'names':plan['user_sources']+plan['external_sources']},ensure_ascii=False,indent=2)+'\n')
print(json.dumps(report))
