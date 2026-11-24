#!/usr/bin/env python3
"""Add only individually reviewed aliases using already published artwork."""
import hashlib,io,json,struct,zipfile,re
from pathlib import Path
ROOT=Path(".")
R=ROOT/"reports/italia-user-20261124"
C=ROOT/"assets/warder/downloads/picons/channels"
A=ROOT/"assets/warder/downloads/picons/providers"
CAT=ROOT/"assets/warder/downloads.json"
S="https://raw.githubusercontent.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/main/assets/warder/downloads/picons/channels/"
def sha(raw):return hashlib.sha256(raw).hexdigest()
def dump(obj):return (json.dumps(obj,ensure_ascii=False,indent=2,sort_keys=True)+"\n").encode()
def gitsha(raw):return hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\0"+raw).hexdigest()
def req(v,msg):
 if not v:raise ValueError(msg)
def png(raw,size):
 return raw[:8]==b"\x89PNG\r\n\x1a\n" and struct.unpack(">II",raw[16:24])==size
def append(raw,add,dim):
 stream=io.BytesIO(raw)
 with zipfile.ZipFile(stream,"a") as z:
  old=z.namelist();req(len(old)==len(set(old)) and z.testzip() is None,"invalid original zip")
  for target,donor in sorted(add.items()):
   req(target not in old and target.casefold() not in {x.casefold() for x in old},target)
   data=z.read(donor);req(png(data,dim),donor)
   z.writestr(zipfile.ZipInfo(target,(1980,1,1,0,0,0)),data)
 out=stream.getvalue()
 with zipfile.ZipFile(io.BytesIO(raw)) as before,zipfile.ZipFile(io.BytesIO(out)) as after:
  req(after.testzip() is None,"CRC");req(set(after.namelist())==set(before.namelist())|set(add),"names")
  req(len(after.namelist())==len(set(after.namelist())),"duplicate")
  for name in before.namelist():req(after.read(name)==before.read(name),name)
  for target,donor in add.items():req(after.read(target)==before.read(donor),target)
 return out,len(old)
plan=json.loads((R/"plan.json").read_bytes());raw=(C/"manifest.json").read_bytes();req(sha(raw)==plan["baseline"],"baseline changed")
doc=json.loads(raw);meta={x["filename"]:x for x in doc["parts"]};oldmeta=dict(meta);oldcount=len(meta)
recipe=json.loads((ROOT/"reports/dtt-italia-20261123/recipe.json").read_bytes())["selectors"]["DTT_ITALIA"]
def identity(n):return tuple(n.removesuffix(".png").split("_")[3:6])
dtt={}
for n in plan["dtt"]:
 candidates=[k+".png" for k in recipe if identity(k)==identity(n)]
 req(len(candidates)==1 and n not in candidates,n);dtt[n]=candidates[0]
report={"dtt":[],"providers":[],"dtt_alias_map":dtt,"unchanged_catalogue_entries":0}
old_packages=[p.copy() for p in doc["packages"] if p["selector_id"]!="DTT_ITALIA"]
for p in doc["packages"]:
 if p["selector_id"]!="DTT_ITALIA":continue
 original_names=[u.rsplit("/",1)[-1] for u in p["parts"]]
 chunks=[]
 for n in original_names:
  b=(C/n).read_bytes();req(len(b)==meta[n]["bytes"] and sha(b)==meta[n]["sha256"],n);chunks.append(b)
 before=b"".join(chunks);req(sha(before)==p["sha256"],p["filename"])
 dim=tuple(map(int,p["resolution"].split("x")));after,count=append(before,dtt,dim);req(count==285,"DTT count")
 digest=sha(after);name="warder-dtt-italia-"+p["resolution"]+"-"+p["family"][8:]+"-"+digest[:16]+".zip"
 # Preserve the canonical number of parts; original interior chunks remain byte-identical wherever possible.
 pos=0;urls=[]
 for i,old in enumerate(chunks):
  n=name+".part%02d"%i
  b=after[pos:] if i==len(chunks)-1 else after[pos:pos+len(old)];pos+=len(b)
  req(0<len(b)<=20*1024*1024,n);(C/n).write_bytes(b);meta[n]={"filename":n,"bytes":len(b),"sha256":sha(b)};urls.append(S+n)
 req(pos==len(after),"parts");req(b"".join((C/u.rsplit("/",1)[-1]).read_bytes() for u in urls)==after,"reassembly")
 for n in original_names:meta.pop(n)
 p.update(filename=name,sha256=digest,bytes=len(after),png_count=count+len(dtt),parts=urls)
 report["dtt"].append({"size":p["resolution"],"style":p["family"][8:],"sha256":digest,"filename":name,"added":len(dtt),"preserved":count,"parts":len(urls)})
req(len(report["dtt"])==9 and len(meta)==oldcount==2224,"catalog count")
req(old_packages==[p for p in doc["packages"] if p["selector_id"]!="DTT_ITALIA"],"other package changed")
for p in old_packages:
 for u in p["parts"]:
  n=u.rsplit("/",1)[-1];req(meta[n]==oldmeta[n],n)
doc["parts"]=sorted(meta.values(),key=lambda p:p["filename"]);m=dump(doc);(C/"manifest.json").write_bytes(m)
sums=(sha(m)+"  manifest.json\n"+"".join(p["sha256"]+"  "+p["filename"]+"\n" for p in doc["parts"])).encode();(C/"SHA256SUMS").write_bytes(sums)
report["manifest_sha256"]=sha(m);report["manifest_git_sha"]=gitsha(m);report["sums_git_sha"]=gitsha(sums);report["unchanged_catalogue_entries"]=len(old_packages)
cat=json.loads(CAT.read_bytes());assets=cat.get("assets",cat)
for style,key in [("transparent","piconProv-220"),("white","piconProv-w"),("black","piconProv-b")]:
 p=assets[key];path=A/style/"piconProv.zip";before=path.read_bytes();req(sha(before)==p["sha256"] and len(before)==p["size"],style)
 add={"piconProv/"+r["target"]:"piconProv/"+r["donor"] for r in plan["providers"] if style in r["styles"]}
 req(all(not t.casefold().endswith("/skylink.png") for t in add),"protected retired logo")
 after,count=append(before,add,(220,132));req(count==p["png_count"],style);req(len(after)<32*1024*1024,"receiver size limit")
 path.write_bytes(after);p.update(sha256=sha(after),size=len(after),png_count=count+len(add))
 report["providers"].append({"style":style,"added":len(add),"preserved":count,"sha256":sha(after),"bytes":len(after),"png_count":count+len(add)})
CAT.write_text(json.dumps(cat,ensure_ascii=False,indent=2)+"\n")
req(sum(x["added"] for x in report["dtt"])==216 and sum(x["added"] for x in report["providers"])==99,"counts")
# Existing hard-coded integration gates remain exact, not weakened.
for filename in (".github/workflows/verify-fullhdglass-integrated-20261122.yml",".github/workflows/fullhdglass-stable-1.0.82-preflight.yml"):
 path=ROOT/filename;t=path.read_text();req(t.count("4663357339c7a59ea19f8ced89309749d340e1d2")==1 and t.count("dcedf2615908a07626a5741fb6ab4efcb3eb228e")==1,filename)
 path.write_text(t.replace("4663357339c7a59ea19f8ced89309749d340e1d2",gitsha(m)).replace("dcedf2615908a07626a5741fb6ab4efcb3eb228e",gitsha(sums)))
(R/"build.json").write_bytes(dump(report))
print(json.dumps(report,ensure_ascii=False))
