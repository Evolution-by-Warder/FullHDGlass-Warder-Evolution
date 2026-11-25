import hashlib,io,json,sys,zipfile,urllib.request,re
from pathlib import Path
from PIL import Image
P=Path(sys.argv[1]);R=Path(sys.argv[2]);work=Path(__file__).parent;out=P/'reports/italia-vr-eclutch-20261125';out.mkdir(parents=True,exist_ok=True)
A=P/'assets/warder/downloads/picons/providers';C=P/'assets/warder/downloads.json';catalog=json.loads(C.read_text());assets=catalog['assets']
def sha(b):return hashlib.sha256(b).hexdigest()
def verify(path,a):
 b=path.read_bytes();assert len(b)==a['size'] and sha(b)==a['sha256'];z=zipfile.ZipFile(io.BytesIO(b));assert z.testzip() is None and len(z.namelist())==a['png_count'];return b,z
def pack(values,base=None):
 b=io.BytesIO(base or b'')
 with zipfile.ZipFile(b,'a' if base else 'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
  for n,d in sorted(values.items()):z.writestr(zipfile.ZipInfo(n,(1980,1,1,0,0,0)),d,compress_type=zipfile.ZIP_DEFLATED,compresslevel=9)
 return b.getvalue()
def valid(b):
 im=Image.open(io.BytesIO(b));im.load();assert im.size==(220,132) and im.mode=='RGBA'
def n(s):return 'piconProv/'+s+'.png'
keys={'transparent':'piconProv-220','white':'piconProv-w','black':'piconProv-b'}
hashes={'transparent':'18f5460f72285791b45a18402a6f832bd2d3d9aebd31ab722c1d366251f7590d','white':'33c652c0b00221a39c8a1344b13021d15dd6833275c149ef4ef0f240615a82b2','black':'aff04ce00aef14cb2974ad87004fb9595d4bf39032712832d8bf91abea536058'}
baseline={};allstyle={};deltas={s:{} for s in keys}
for s,key in keys.items():
 a=assets[key];assert a['sha256']==hashes[s];path=A/s/'piconProv.zip';raw,z=verify(path,a)
 values={k:z.read(k) for k in z.namelist()};baseline[s]=(raw,z,path)
 if s=='white':
  v=assets[key+'-v2'];assert v['base_sha256']==hashes[s] and len(v['extensions'])==3
  for i,e in enumerate(v['extensions'],1):
   b,ez=verify(A/s/f'extension-{i:02d}'/'piconProv.zip',e);assert not set(ez.namelist())&set(values);values.update({k:ez.read(k) for k in ez.namelist()})
  assert len(values)==v['png_count'] and sum(map(len,values.values()))==v['unpacked_size']
 allstyle[s]=values
 b=(R/'dtt-donor-review'/s/'1_0_1_5A_A000_217C_EEEE0000_0_0_0.png').read_bytes()
 assert sha(b)=={'transparent':'d1ce20c22aa669745e59bf8f82d510c89f2f93cffb5b81c29c7ea601ed4294c1','white':'382f05c5b58a5f6b8ab88564231a7233fe45e73be30328ed96fd070fec4bee14','black':'1375148432ca8ddac3761784bec533eb55d534bc99a555686166f741c6b34a5c'}[s]
 valid(b);assert n('VIDEO REGIONE') not in values;deltas[s][n('VIDEO REGIONE')]=b
 (out/(s+'-VIDEO-REGIONE.png')).write_bytes(b)
def get(url):
 req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'})
 with urllib.request.urlopen(req,timeout=30) as r:
  assert r.status==200;return r.read(3000001)
review=Path('next-logo-review');review.mkdir(exist_ok=True)
url='https://eclutch.tv/wp-content/uploads/2023/08/ESports-Logo-1000-x-500-px.png'
eclutch={}
try:
 b=get(url);assert len(b)<3000001
 im=Image.open(io.BytesIO(b)).convert('RGBA');a=im.getchannel('A');assert a.getextrema()[0]<255 and a.getextrema()[1]==255
 im=im.crop(a.getbbox());im.thumbnail((194,108),Image.Resampling.LANCZOS)
 fg=Image.new('RGBA',(220,132));fg.alpha_composite(im,((220-im.width)//2,(132-im.height)//2))
 (out/'ECLUTCH-official-source.png').write_bytes(b)
 for s in keys:
  logo=fg.copy()
  if s=='transparent':dst=logo
  else:
   t=(work/(s+'-sablona.png')).read_bytes()
   assert sha(t)=={'white':'c6ae4a808a65ffc8e6458336fccbfe4216de1e832ec0a9abf800907f2f783589','black':'61e69f7fc46e340453bf74ccd7af6ac9d8eba9f8e232884659e1ea99f6abf3fe'}[s]
   if s=='white':
    px=logo.load()
    for y in range(132):
     for x in range(220):
      r,g,bb,aa=px[x,y]
      if min(r,g,bb)>160 and max(r,g,bb)-min(r,g,bb)<25: px[x,y]=(28,32,38,aa)
   dst=Image.alpha_composite(Image.open(io.BytesIO(t)).convert('RGBA'),logo)
  buf=io.BytesIO();dst.save(buf,'PNG',optimize=True);d=buf.getvalue();valid(d);assert n('ECLUTCH') not in allstyle[s]
  deltas[s][n('ECLUTCH')]=d;(out/(s+'-ECLUTCH.png')).write_bytes(d)
 eclutch={'status':'BUILT_REVIEW_REQUIRED','source':url,'source_sha256':sha(b)}
except Exception as exc:
 for s in keys:deltas[s].pop(n('ECLUTCH'),None)
 eclutch={'status':'HOLD','error':str(exc)}
report={'base':'5bcd4ac8f39e681265f0c5de6b99af90d5e3eb37','new_png':sum(map(len,deltas.values())),'complete_provider_names':1+(eclutch['status']=='BUILT_REVIEW_REQUIRED'),'video_regione_reference':'1_0_1_5A_A000_217C_EEEE0000_0_0_0.png','video_regione_source':'https://www.vrsicilia.it/chi-siamo/','video_regione_rebrand':'https://www.litaliaindigitale.it/news-regionali/sicilia-news/220729-mux-locale-1-sicilia-passaggio-in-hd-per-antenna-sicilia-telecolor-e-sicilia-channel-nuovo-logo-per-trm-e-video-regione-tva-telenormanna-in-4-3/','eclutch':eclutch,'archives':[]}
for s,key in keys.items():
 d=deltas[s];old=allstyle[s];assert not {k.casefold() for k in d}&{k.casefold() for k in old}
 a=assets[key];raw,z,path=baseline[s]
 if s=='white':
  v=assets[key+'-v2'];e=dict(v['extensions'][-1]);b=pack(d);np=A/s/'extension-04'/'piconProv.zip';assert not np.exists();np.parent.mkdir(parents=True);np.write_bytes(b)
  e.update(png_count=len(d),size=len(b),sha256=sha(b),url=e['url'].replace('extension-03','extension-04'));v['extensions'].append(e);v['png_count']+=len(d);v['unpacked_size']+=sum(map(len,d.values()))
  assert path.read_bytes()==raw
  with zipfile.ZipFile(io.BytesIO(b)) as nz:assert nz.testzip() is None and set(nz.namelist())==set(d) and all(nz.read(k)==v for k,v in d.items())
  report['archives'].append(dict(style=s,count=v['png_count'],new_extension_sha256=sha(b),new_extension_bytes=len(b),previous_archives_unchanged=True))
 else:
  b=pack(d,raw);assert len(b)<=32*1024*1024
  with zipfile.ZipFile(io.BytesIO(b)) as nz:
   assert nz.testzip() is None and set(nz.namelist())==set(old)|set(d)
   assert all(nz.read(k)==v for k,v in old.items()) and all(nz.read(k)==v for k,v in d.items())
  path.write_bytes(b);a.update(size=len(b),sha256=sha(b),png_count=len(old)+len(d))
  report['archives'].append(dict(style=s,count=a['png_count'],sha256=sha(b),bytes=len(b),old_png_unchanged=True))
C.write_text(json.dumps(catalog,ensure_ascii=False,indent=2)+'\n')
(out/'build.json').write_text(json.dumps(report,indent=2)+'\n')
(out/'README.md').write_text('Video Regione: exact approved VR14 donor and confirmed rebrand. ECLUTCH: official source, white contrast correction; visual review before merge. No existing PNG replaced. No DTT or IPK change.\n')
print(json.dumps(report))
import re,urllib.parse
sites={'ASSOCIAZIONE DREAMER':'https://www.associazionedigitaldreamers.it/','RADIO MATER DAB':'https://www.radiomater.org/','TELERADIOPACE':'https://www.teleradiopace.tv/','TELEPACE':'https://www.telepace.it/'}
found={}
for name,url in sites.items():
 try:
  html=get(url).decode('utf-8','replace');images=[]
  for m in re.finditer(r"""(?:src|data-src|content)=["']([^"']+)["']""",html,re.I):
   u=urllib.parse.urljoin(url,m.group(1))
   if re.search(r'logo|brand|marchio|dreamers|mater|telepace',u,re.I) and re.search(r'\.(?:png|svg|webp|jpe?g)(?:\?|$)',u,re.I) and urllib.parse.urlsplit(u).netloc==urllib.parse.urlsplit(url).netloc and u not in images:images.append(u)
  found[name]=[]
  for i,u in enumerate(images[:4]):
   try:
    b=get(u);assert len(b)<3000001
    suf=urllib.parse.urlsplit(u).path.rsplit('.',1)[-1].lower();(review/(re.sub(r'[^A-Z0-9]','_',name)+'_'+str(i)+'.'+suf)).write_bytes(b)
    found[name].append({'url':u,'sha256':sha(b)})
   except Exception:pass
 except Exception as exc:found[name]=[{'error':str(exc)}]
(review/'sources.json').write_text(json.dumps(found,indent=2))
