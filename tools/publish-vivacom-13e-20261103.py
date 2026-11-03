import io,json,hashlib,zipfile,urllib.request,pathlib
from PIL import Image
root=pathlib.Path("assets/warder/downloads/picons/channels")
url="https://raw.githubusercontent.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/main/assets/warder/downloads/picons/channels/"
refs=[("19","130","2648","19"),("1","14A","2648","19"),("1","145","2648","19"),("1","13AC","2710","19"),("1","13AD","2710","19"),("1","139","2648","19"),("19","138A","2710","19"),("1","140","2648","19"),("1","D0","25E4","16")]
def sha(b):return hashlib.sha256(b).hexdigest()
def get(u):
 with urllib.request.urlopen(urllib.request.Request(u,headers={"User-Agent":"Warder-PiconHub"}),timeout=120) as r:return r.read()
m=json.loads((root/"manifest.json").read_text())
parts={p["filename"]:p for p in m["parts"]}
new={}
for p in m["packages"]:
 if p["selector_id"]!="130E":continue
 size=p["resolution"];style=p["family"].removeprefix("channel-")
 chunks=[]
 for u in p["parts"]:
  b=get(u);v=parts[u.rsplit("/",1)[-1]]
  assert len(b)==v["bytes"] and sha(b)==v["sha256"]
  chunks.append(b)
 raw=b"".join(chunks)
 assert sha(raw)==p["sha256"]
 with zipfile.ZipFile(io.BytesIO(raw)) as z:
  names=z.namelist();extra={}
  for typ,sid,tsid,oldtype in refs:
   dst=f"1_0_{typ}_{sid}_{tsid}_13E_820000_0_0_0.png"
   src=f"1_0_{oldtype}_{sid}_{tsid}_D5_820000_0_0_0.png"
   assert dst not in names
   if src in names:data=z.read(src)
   else:
    source=f"https://raw.githubusercontent.com/Evolution-by-Warder/PiconHub-Warder-Evolution/main/picons/13.0e/vivacom/{style}/{src}"
    data=get(source)
    if size!="220x132":
     im=Image.open(io.BytesIO(data)).convert("RGBA").convert("RGBa")
     im=im.resize(tuple(map(int,size.split("x"))),Image.Resampling.LANCZOS).convert("RGBA")
     f=io.BytesIO();im.save(f,"PNG");data=f.getvalue()
   assert Image.open(io.BytesIO(data)).size==tuple(map(int,size.split("x")))
   extra[dst]=data
  out=io.BytesIO()
  with zipfile.ZipFile(out,"w",zipfile.ZIP_DEFLATED) as w:
   for n in sorted(set(names)|set(extra)):w.writestr(n,extra[n] if n in extra else z.read(n))
  packed=out.getvalue()
  with zipfile.ZipFile(io.BytesIO(packed)) as v:
   assert v.testzip() is None
   assert all(v.read(n)==z.read(n) for n in names)
   assert all(v.read(n)==data for n,data in extra.items())
 h=sha(packed);fn=f"warder-130e-{size}-{style}-{h[:16]}.zip"
 urls=[]
 for i in range(0,len(packed),16*1024*1024):
  chunk=packed[i:i+16*1024*1024];name=f"{fn}.part{i//(16*1024*1024):02d}"
  (root/name).write_bytes(chunk)
  new[name]={"filename":name,"bytes":len(chunk),"sha256":sha(chunk)}
  urls.append(url+name)
 p.update(filename=fn,sha256=h,bytes=len(packed),parts=urls,png_count=len(names)+9)
 p.pop("url",None)
 if "included_references" in p:p["included_references"]=sorted(set(p["included_references"])|{n[:-4] for n in extra})
 print(size,style,"+9",flush=True)
assert len(new)>=9
used={u.rsplit("/",1)[-1] for p in m["packages"] for u in p.get("parts",[])}
m["parts"]=sorted([p for p in m["parts"] if p["filename"] in used]+list(new.values()),key=lambda p:p["filename"])
(root/"manifest.json").write_text(json.dumps(m,sort_keys=True,indent=2)+"\n")
s=root/"SHA256SUMS";d={x.split()[-1]:x.split()[0] for x in s.read_text().splitlines() if x.strip()}
d.update({n:p["sha256"] for n,p in new.items()});d["manifest.json"]=sha((root/"manifest.json").read_bytes())
s.write_text("".join(f"{v}  {k}\n" for k,v in sorted(d.items())))
print("READY",len(new),"parts")
