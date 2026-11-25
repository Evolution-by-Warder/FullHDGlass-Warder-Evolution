import copy,hashlib,io,json,subprocess,sys,zipfile
from pathlib import Path
from PIL import Image
ROOT=Path(sys.argv[1]); DELTA=Path(sys.argv[2]); C=ROOT/'assets/warder/downloads/picons/channels'
def sha(b):return hashlib.sha256(b).hexdigest()
def dump(x):return (json.dumps(x,ensure_ascii=False,indent=2,sort_keys=True)+'\n').encode()
raw=DELTA.read_bytes();assert sha(raw)=='54fb58787a37863468be59aedc0d0492fb74d7077f17e3ba9c4bc2359fce0b52'
with zipfile.ZipFile(io.BytesIO(raw)) as z:
 assert z.testzip() is None and len(z.namelist())==37 and len(set(z.namelist()))==37
 approval=json.loads(z.read('manifest.json'));rows=approval['rows'];assert len(rows)==36
 assert approval['review_sha256']=='e62832ce710f9b98ced8466ed7905b2d8bf968497d38df445e854fc49abd2d73'
 refs={'1_0_1_42D_2_AA_5A0000_0_0_0.png','1_0_1_41F_5_AA_5A0000_0_0_0.png','1_0_1_3EF_5_AA_5A0000_0_0_0.png','1_0_1_450_6_AA_5A0000_0_0_0.png'}
 sizes={'50x30','220x132','400x240'};styles={'transparent','white','black'}
 expected={(r,s,t) for r in refs for s in sizes for t in styles}
 assert {(x['ref'],x['resolution'],x['style']) for x in rows}==expected
 data={}
 for x in rows:
  n='candidate/9E/'+x['resolution']+'/'+x['style']+'/'+x['ref'];assert x['path']==n
  b=z.read(n);assert sha(b)==x['sha256']
  with Image.open(io.BytesIO(b)) as im:assert im.format=='PNG' and im.size==tuple(map(int,x['resolution'].split('x')));im.load()
  data[n]=b
 assert set(z.namelist())==set(data)|{'manifest.json'}
m=(C/'manifest.json').read_bytes();assert sha(m)==approval['baseline_manifest_sha256']=='cfc08ab0120731b052cc4849992785e3395e70b2bf20506ad276cb9acf5e7e7f'
d=json.loads(m);old=copy.deepcopy(d);meta={p['filename']:p for p in d['parts']}
assert len(meta)==len(d['parts'])
assert (C/'SHA256SUMS').read_text()==sha(m)+'  manifest.json\n'+''.join(p['sha256']+'  '+p['filename']+'\n' for p in d['parts'])
targets=[p for p in d['packages'] if p['selector_id']=='90E'];assert len(targets)==9 and {(p['resolution'],p['family'][8:]) for p in targets}=={(s,t) for s in sizes for t in styles}
new={};remove=set();results=[]
for p in targets:
 s=p['resolution'];t=p['family'][8:];names=[u.rsplit('/',1)[-1] for u in p['parts']]
 chunks=[(C/n).read_bytes() for n in names]
 for n,b in zip(names,chunks):assert len(b)==meta[n]['bytes'] and sha(b)==meta[n]['sha256']
 before=b''.join(chunks);assert len(before)==p['bytes'] and sha(before)==p['sha256']
 replace={x['ref']:(data[x['path']],x['old_sha256']) for x in rows if x['resolution']==s and x['style']==t}
 assert set(replace)==refs
 buf=io.BytesIO()
 with zipfile.ZipFile(io.BytesIO(before)) as a,zipfile.ZipFile(buf,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
  assert a.testzip() is None and len(a.namelist())==p['png_count']==len(set(a.namelist()))
  assert refs<=set(a.namelist())
  for info in a.infolist():
   b=a.read(info.filename)
   if info.filename in replace:
    value,old_hash=replace[info.filename];assert sha(b)==old_hash,info.filename;b=value
   z.writestr(info,b)
 after=buf.getvalue()
 with zipfile.ZipFile(io.BytesIO(before)) as a,zipfile.ZipFile(io.BytesIO(after)) as z:
  assert z.testzip() is None and a.namelist()==z.namelist()
  assert all(z.read(n)==(replace[n][0] if n in replace else a.read(n)) for n in a.namelist())
 digest=sha(after);filename='warder-90e-'+s+'-'+t+'-'+digest[:16]+'.zip'
 urls=[];pos=0
 while pos<len(after):
  i=len(urls);n=filename+'.part%02d'%i;size=len(chunks[i]) if i<len(chunks) else 786432
  b=after[pos:pos+size];pos+=len(b);assert n not in meta and n not in new
  (C/n).write_bytes(b);new[n]={'filename':n,'bytes':len(b),'sha256':sha(b)};urls.append(p['parts'][0].rsplit('/',1)[0]+'/'+n)
 assert b''.join((C/u.rsplit('/',1)[-1]).read_bytes() for u in urls)==after
 remove.update(names);p.update(filename=filename,parts=urls,bytes=len(after),sha256=digest)
 results.append({'resolution':s,'style':t,'replaced':4,'preserved':p['png_count']-4,'sha256':digest,'parts':len(urls)})
others=[p for p in d['packages'] if p['selector_id']!='90E'];assert others==[p for p in old['packages'] if p['selector_id']!='90E']
assert not remove&{u.rsplit('/',1)[-1] for p in others for u in p['parts']}
d['parts']=sorted([v for n,v in meta.items() if n not in remove]+list(new.values()),key=lambda p:p['filename'])
result=dump(d);(C/'manifest.json').write_bytes(result)
(C/'SHA256SUMS').write_text(sha(result)+'  manifest.json\n'+''.join(p['sha256']+'  '+p['filename']+'\n' for p in d['parts']))
report={'state':'CANDIDATE_NOT_PUBLISHED','approved_delta_sha256':sha(raw),'manifest_sha256':sha(result),'packages':results,'replaced':36,'unrelated_packages_preserved':len(others),'new_parts':list(new)}
out=ROOT/'reports/azzurra-9e-verified-20261125';out.mkdir(parents=True,exist_ok=True);(out/'build.json').write_bytes(dump(report));print(json.dumps(report))
