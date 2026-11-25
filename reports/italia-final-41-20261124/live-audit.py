import json,hashlib,urllib.request,io,zipfile
from PIL import Image
from pathlib import Path
def get(u):
 with urllib.request.urlopen(u,timeout=90) as r:return r.read()
def sha(b):return hashlib.sha256(b).hexdigest()
root='https://raw.githubusercontent.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/main/'
m=get(root+'assets/warder/downloads.json');assets=json.loads(m)['assets']
expected={'transparent':('piconProv-220',1475,'18f5460f72285791b45a18402a6f832bd2d3d9aebd31ab722c1d366251f7590d'),'white':('piconProv-w',1387,'33c652c0b00221a39c8a1344b13021d15dd6833275c149ef4ef0f240615a82b2'),'black':('piconProv-b',1454,'aff04ce00aef14cb2974ad87004fb9595d4bf39032712832d8bf91abea536058')}
names=['TVN WBD','TVN_WBD','TIVIBU','ACISPORT TV','ACISPORT_TV','AUSTRIASAT','DIGITAL FREE','W1 WL DTH']
def fetch(a):
 b=get(a['url']);assert len(b)==a['size'] and sha(b)==a['sha256'];assert len(b)<=32*1024*1024
 with zipfile.ZipFile(io.BytesIO(b)) as z:
  assert z.testzip() is None and len(z.namelist())==a['png_count'];return {n:z.read(n) for n in z.namelist()}
result={}
for s,(key,count,digest) in expected.items():
 a=assets[key];assert a['png_count']==count and a['sha256']==digest
 data=fetch(a)
 if s=='white':
  v=assets[key+'-v2'];assert v['base_sha256']==digest and len(v['extensions'])==3
  for x in v['extensions']:
   extra=fetch(x);assert not set(extra)&set(data);data.update(extra)
  assert len(data)==v['png_count']==1451 and sum(map(len,data.values()))==v['unpacked_size']
 assert len(data)==len(set(k.casefold() for k in data))
 for name in names:
  b=data['piconProv/'+name+'.png'];assert Image.open(io.BytesIO(b)).size==(220,132)
 assert data['piconProv/TIVIBU.png']==data['piconProv/TIVUBU.png']
 if s=='transparent':
  for target,donor in [('AUSTRIASAT','HD AUSTRIA'),('DIGITAL FREE','KABEL DEUTSCHLAND'),('W1 WL DTH','NETERRA COMMUNICATIONS')]:assert data['piconProv/'+target+'.png']==data['piconProv/'+donor+'.png']
 result[s]={'count':len(data),'base_sha256':digest,'verified_names':names}
print(json.dumps(result));Path('live-provider-audit.json').write_text(json.dumps(result,indent=2))
