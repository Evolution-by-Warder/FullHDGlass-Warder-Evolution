#!/usr/bin/env python3
"""Build a publication candidate, from an exact owner-approved delta and pinned live catalog."""
import argparse, copy, hashlib, io, json, urllib.request, zipfile
from pathlib import Path
from PIL import Image

BASE='a568467cc3fc05dae0c3c00bca9c3a6c56e0dd64'
MANIFEST_SHA='f5dc88ab1ae5664823e94849cd5f90596bc9d56b7207782d45f56efcd08f7d0d'
DELTA_SHA='5fb0217df0d7e73c931092e858faa2f37c73aeb01632ece28f3c99e805822846'
LIVE='https://raw.githubusercontent.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/main/assets/warder/downloads/picons/channels/'
PINNED=LIVE.replace('/main/','/'+BASE+'/')
SIZES=('50x30','220x132','400x240')
STYLES=('transparent','white','black')
REFS={'1_0_16_1392_50E1_217C_EEEE0000_0_0_0.png','1_0_19_1392_50E1_217C_EEEE0000_0_0_0.png',*('1_0_1_'+str(i)+'_A002_217C_EEEE0000_0_0_0.png' for i in (1,2,4,5))}
def sha(b):return hashlib.sha256(b).hexdigest()
def dump(x):return (json.dumps(x,ensure_ascii=False,indent=2,sort_keys=True)+'\n').encode()
def require(ok,msg):
 if not ok:raise ValueError(msg)
def get(n):
 require('/' not in n and '\\' not in n,'Unsafe part name')
 with urllib.request.urlopen(PINNED+n,timeout=90) as r:
  raw=r.read(20*1024*1024+1)
 require(0<len(raw)<=20*1024*1024,n)
 return raw
def pngcheck(b,dim):
 with Image.open(io.BytesIO(b)) as im:
  require(im.format=='PNG' and im.size==dim,'Unexpected PNG dimensions or format')
  im.verify()
def validate_delta(raw):
 require(sha(raw)==DELTA_SHA,'Approved delta archive SHA mismatch')
 expected={f'{sz}/{style}/{n}' for sz in SIZES for style in STYLES for n in REFS}
 with zipfile.ZipFile(io.BytesIO(raw)) as z:
  require(z.testzip() is None and len(z.namelist())==55 and set(z.namelist())==expected|{'manifest.json'},'Delta member mismatch')
  m=json.loads(z.read('manifest.json'))
  require(set(m['variants'])==expected,'Unexpected delta manifest')
  data={n:z.read(n) for n in expected}
  for n,b in data.items():
   require(sha(b)==m['variants'][n],n)
   pngcheck(b,tuple(map(int,n.split('/')[0].split('x'))))
  for sz in SIZES:
   for style in STYLES:
    prefix=f'{sz}/{style}/1_0_'
    require(data[prefix+'16_1392_50E1_217C_EEEE0000_0_0_0.png']==data[prefix+'19_1392_50E1_217C_EEEE0000_0_0_0.png'],'Italia 7 alias pixels changed')
 return data
def build(root,delta):
 C=root/'assets/warder/downloads/picons/channels'
 m=(C/'manifest.json').read_bytes();require(sha(m)==MANIFEST_SHA,'Production baseline manifest changed')
 doc=json.loads(m);old=copy.deepcopy(doc);meta={p['filename']:p for p in doc['parts']}
 require(len(meta)==len(doc['parts']),'Duplicate part metadata')
 expected_sums=sha(m)+'  manifest.json\n'+''.join(p['sha256']+'  '+p['filename']+'\n' for p in doc['parts'])
 require((C/'SHA256SUMS').read_text()==expected_sums,'Baseline SHA256SUMS mismatch')
 data=validate_delta(delta);newparts={};remove=set();rows=[]
 target=[p for p in doc['packages'] if p['selector_id']=='DTT_ITALIA']
 require({(p['resolution'],p['family']) for p in target}=={(s,'channel-'+c) for s in SIZES for c in STYLES} and len(target)==9,'DTT matrix mismatch')
 for p in target:
  res=p['resolution'];style=p['family'][8:];dim=tuple(map(int,res.split('x')))
  chunks=[];oldnames=[u.rsplit('/',1)[-1] for u in p['parts']]
  for n in oldnames:
   b=get(n);require(sha(b)==meta[n]['sha256'] and len(b)==meta[n]['bytes'],n);chunks.append(b)
  before=b''.join(chunks);require(sha(before)==p['sha256'] and len(before)==p['bytes'],'Baseline ZIP mismatch')
  additions={n:data[f'{res}/{style}/{n}'] for n in REFS}
  with zipfile.ZipFile(io.BytesIO(before)) as a:
   names=set(a.namelist());require(len(names)==len(a.namelist())==p['png_count']==342 and a.testzip() is None,'Baseline archive invalid')
   require(not {n.casefold() for n in names}&{n.casefold() for n in additions},'Do not overwrite existing picons')
   for n in names:pngcheck(a.read(n),dim)
  buf=io.BytesIO(before)
  with zipfile.ZipFile(buf,'a',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
   for n,b in sorted(additions.items()):z.writestr(zipfile.ZipInfo(n,(1980,1,1,0,0,0)),b,compress_type=zipfile.ZIP_DEFLATED,compresslevel=9)
  after=buf.getvalue()
  with zipfile.ZipFile(io.BytesIO(before)) as a,zipfile.ZipFile(io.BytesIO(after)) as z:
   require(z.testzip() is None and len(z.namelist())==348 and set(z.namelist())==names|REFS,'New ZIP invalid')
   require(all(z.read(n)==a.read(n) for n in names),'Existing PNG changed')
   require(all(z.read(n)==b for n,b in additions.items()),'Approved PNG changed')
  digest=sha(after);filename=f'warder-dtt-italia-{res}-{style}-{digest[:16]}.zip'
  pos=0;urls=[]
  # Use original part sizes where possible; additional tail split into 768 KiB parts.
  while pos<len(after):
   i=len(urls);size=len(chunks[i]) if i<len(chunks) else 786432
   b=after[pos:pos+size];pos+=len(b);name=filename+f'.part{i:02d}'
   require(name not in meta and name not in newparts and 0<len(b)<=20*1024*1024,'Unexpected part')
   (C/name).write_bytes(b);newparts[name]={'filename':name,'bytes':len(b),'sha256':sha(b)};urls.append(LIVE+name)
  require(b''.join((C/u.rsplit('/',1)[-1]).read_bytes() for u in urls)==after,'Split ZIP mismatch')
  remove.update(oldnames)
  p.update(filename=filename,sha256=digest,bytes=len(after),png_count=348,parts=urls)
  rows.append({'resolution':res,'style':style,'added':6,'preserved':342,'count':348,'filename':filename,'sha256':digest,'parts':len(urls)})
 other=[p for p in doc['packages'] if p['selector_id']!='DTT_ITALIA']
 require(other==[p for p in old['packages'] if p['selector_id']!='DTT_ITALIA'] and len(other)==498,'Unrelated package changed')
 used={u.rsplit('/',1)[-1] for p in other for u in p['parts']}
 require(not used&remove,'Old DTT part is shared by unrelated package')
 doc['parts']=sorted([v for n,v in meta.items() if n not in remove]+list(newparts.values()),key=lambda p:p['filename'])
 result=dump(doc);(C/'manifest.json').write_bytes(result)
 (C/'SHA256SUMS').write_text(sha(result)+'  manifest.json\n'+''.join(p['sha256']+'  '+p['filename']+'\n' for p in doc['parts']))
 report={'baseline':BASE,'baseline_manifest_sha256':MANIFEST_SHA,'delta_sha256':DELTA_SHA,'source_audit':45581127835,'preflight_audit':45582294840,'added':54,'preserved':3078,'untouched_other_packages':498,'manifest_sha256':sha(result),'packages':rows,'new_parts':list(newparts),'state':'CANDIDATE_NOT_MERGED'}
 out=root/'reports/italia-dtt-verified-20261125';out.mkdir(parents=True,exist_ok=True);(out/'build.json').write_bytes(dump(report))
 print(json.dumps(report))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('production',type=Path);p.add_argument('delta',type=Path);a=p.parse_args();build(a.production,a.delta.read_bytes())
