"""Read-only production archive verification and handoff for local Italian source intake."""
import base64,hashlib,io,json,struct,zipfile,urllib.request
from pathlib import Path
ROOT=Path(".")
CHANNEL=ROOT/"assets/warder/downloads/picons/channels"
OUT=ROOT/"italia-production-baseline"
OUT.mkdir(exist_ok=True)
def sha(b):return hashlib.sha256(b).hexdigest()
def dump(p,o):p.write_text(json.dumps(o,ensure_ascii=False,indent=2)+"\n")
def check(b,h):assert sha(b)==h, (sha(b),h);return b
manifest=(CHANNEL/"manifest.json").read_bytes()
check(manifest,"40db67977de066be65fa8f37f5a73041aa1b337b7a5c9cdf40233edaf537094a")
m=json.loads(manifest); parts={p["filename"]:p for p in m["parts"]}
(OUT/"manifest.json").write_bytes(manifest)
pkg=[x for x in m["packages"] if x["selector_id"]=="DTT_ITALIA"]
assert len(pkg)==9
for p in pkg:
 b=bytearray()
 for url in p["parts"]:
  n=url.rsplit("/",1)[-1]; part=(CHANNEL/n).read_bytes(); assert len(part)==parts[n]["bytes"]; b.extend(check(part,parts[n]["sha256"]))
 check(b,p["sha256"])
 with zipfile.ZipFile(io.BytesIO(b)) as z:assert z.testzip() is None and len(z.namelist())==285
 (OUT/p["filename"]).write_bytes(b)
cat=json.loads((ROOT/"assets/warder/downloads.json").read_text()); assets=cat.get("assets",cat)
names={}
for key,style in [("piconProv-220","transparent"),("piconProv-w","white"),("piconProv-b","black")]:
 p=assets[key]; b=(ROOT/"assets/warder/downloads/picons/providers"/style/"piconProv.zip").read_bytes();check(b,p["sha256"])
 (OUT/("providers-"+style+".zip")).write_bytes(b)
 with zipfile.ZipFile(io.BytesIO(b)) as z:
  assert z.testzip() is None
  n={Path(x).name:sha(z.read(x)) for x in z.namelist() if x.lower().endswith(".png")}
  assert len(n)==p["png_count"],(style,len(n),p["png_count"])
  names[style]=n
  print("PROVIDER_BASELINE",style,len(n),p["sha256"])
dump(OUT/"provider-inventory.json",names)
# Bloom filter of exact filenames; negatives are definitive. Preserve exact
# names and hashes in inventory for subsequent positive confirmation.
bits=bytearray(4096)
for name in set().union(*(set(x) for x in names.values())):
 h=hashlib.sha256(name.encode()).digest()
 for k in range(7):
  i=int.from_bytes(h[2*k:2*k+2],"big")%32768;bits[i//8]|=1<<(i%8)
print("PROVIDER_BLOOM",base64.b64encode(bits).decode())
recipe=ROOT/"reports/dtt-italia-20261123/recipe.json"
(OUT/"recipe.json").write_bytes(recipe.read_bytes())
for style,blob in [("black","1dd0f479c3f3a2017377eb6bec33e948ffa0dda7"),("white","dd8d5860a5daec9a9cf0cd6c12b7f7c2c6428bc0")]:
 url="https://raw.githubusercontent.com/Evolution-by-Warder/PiconHub-Warder-Evolution/a4a473e64c786b639d319e0d47fb8f700c237c43/plugin/artwork/templates/picons/"+style+"-sablona.png"
 with urllib.request.urlopen(url,timeout=45) as r:b=r.read()
 assert hashlib.sha1(b"blob "+str(len(b)).encode()+b"\0"+b).hexdigest()==blob
 (OUT/(style+"-sablona.png")).write_bytes(b)
 print("MASTER_TEMPLATE",style,sha(b),struct.unpack(">II",b[16:24]))
print("DTT_BASELINE",len(pkg),"verified archives, all 285 exact names")
