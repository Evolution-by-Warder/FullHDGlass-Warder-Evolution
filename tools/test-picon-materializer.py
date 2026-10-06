#!/usr/bin/env python3
"""Focused generic ambiguity, deduplication, provider isolation regression."""
import json,subprocess,sys,tempfile,struct,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SIG=bytes((137,80,78,71,13,10,26,10))+bytes((0,0,0,13))+b"IHDR"+struct.pack(">II",220,132)
amb16=["1_0_19_25A_C418_16E_A00000_0_0_0.png","1_0_19_458_526C_16E_A00000_0_0_0.png"]
amb08=["1_0_1_FAE_AF4_BB_E080000_0_0_0.png","1_0_1_FAF_AF4_BB_E080000_0_0_0.png","1_0_19_7725_2C1_600_E080000_0_0_0.png"]
with tempfile.TemporaryDirectory() as td:
 t=Path(td); src=t/"src"; out=t/"out"; selectors=[]
 def write(key,provider,variant,name,data):
  p=src/"picons"/key/provider/variant;p.mkdir(parents=True,exist_ok=True);(p/name).write_bytes(data)
 for pos,names,providers,sid in [("16.0e",amb16,["a1-broadcasting","antiksat"],"160E"),("0.8w",amb08,["freesat","magiosat"],"08W")]:
  for v in ("transparent","black","white"):
   for n in names:
    write(pos,providers[0],v,n,SIG+b"LEFT")
    write(pos,providers[1],v,n,SIG+b"RIGHT")
   # ordinary identity and same-content provider duplicate prove inclusion + deterministic dedup
   common="1_0_1_COMMON_1_1_1.png"
   write(pos,providers[0],v,common,SIG+b"COMMON")
   write(pos,providers[1],v,common,SIG+b"COMMON")
  selectors.append({"selector_id":sid,"kind":"satellite","orbital_position":pos,"warder_key":pos,"state":"READY",
   "eligible_families":["channel-transparent","channel-black","channel-white"],"service_identities":len(names)+1,
   "expected_unique_identities":{f:1 for f in ("channel-transparent","channel-black","channel-white")},
   "ambiguous_exclusions":{f:names for f in ("channel-transparent","channel-black","channel-white")}})
 # provider-specific package remains an independent one-provider tree
 for v in ("transparent","black","white"):
  write("16.0e/antiksat","",v,amb16[0],SIG+b"ANTIKSAT")
 selectors.append({"selector_id":"ANTIKSAT","kind":"provider","orbital_position":"16.0e","warder_key":"16.0e/antiksat",
   "state":"READY","eligible_families":["channel-transparent","channel-black","channel-white"],"service_identities":1,
   "expected_unique_identities":{f:1 for f in ("channel-transparent","channel-black","channel-white")},"ambiguous_exclusions":{}})
 plan=t/"plan.json";plan.write_text(json.dumps({"selectors":selectors}))
 manifest=t/"manifest.json"
 cmd=[sys.executable,str(ROOT/"tools/materialize-picon-packages.py"),"--source-root",str(src),"--plan",str(plan),
  "--output-dir",str(out),"--manifest",str(manifest),"--source-commit","0123456789abcdef",
  "--base-url","https://example.invalid/picons"]
 subprocess.check_call(cmd)
 data=json.loads(manifest.read_text()); assert len(data["packages"])==9
 for sid,names,pos in [("160E",amb16,"16.0e"),("08W",amb08,"0.8w")]:
  for family in ("channel-transparent","channel-black","channel-white"):
   pkg=next(x for x in data["packages"] if x["selector_id"]==sid and x["family"]==family)
   assert pkg["orbital_position"]==pos
   assert pkg["included_references"]==["1_0_1_COMMON_1_1_1"]
   assert len(pkg["same_content_deduplications"])==1
   assert sorted(x["filename"] for x in pkg["ambiguous_exclusions"])==sorted(names)
   with zipfile.ZipFile(out/pkg["filename"]) as z: assert z.namelist()==["1_0_1_COMMON_1_1_1.png"]
 # The provider package is not replaced by the generic selector and preserves its actual asset.
 for family in ("channel-transparent","channel-black","channel-white"):
  pkg=next(x for x in data["packages"] if x["selector_id"]=="ANTIKSAT" and x["family"]==family)
  assert pkg["orbital_position"]=="16.0e" and pkg["ambiguous_exclusions"]==[]
# Undocumented conflicts and generic fallback must fail closed.
 selectors[0]["ambiguous_exclusions"]["channel-transparent"]=[]
bad=t/"bad-plan.json";bad.write_text(json.dumps({"selectors":[selectors[0]}))
r=subprocess.run(cmd[:cmd.index("--plan")+1]+[str(bad)]+cmd[cmd.index("--output-dir"):],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
assert r.returncode!=0 and "UNDOCUMENTED COLLISION" in r.stdout
print("Picon materializer collision regressions: PASS (16.0E: 2 excluded; 0.8W: 3 excluded; same-content dedup; provider isolation; no fallback)")
