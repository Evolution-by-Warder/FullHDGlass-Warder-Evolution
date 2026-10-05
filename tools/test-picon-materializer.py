#!/usr/bin/env python3
import json, subprocess, sys, tempfile, struct
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
PNG_HEADER=bytes((137,80,78,71,13,10,26,10))+bytes((0,0,0,13))+b"IHDR"+struct.pack(">II",220,132)

with tempfile.TemporaryDirectory() as td:
    t=Path(td); src=t/"src"; out=t/"out"
    for variant in ("transparent","black","white"):
        p=src/"picons"/"1.0e"/"provider"/variant
        p.mkdir(parents=True)
        (p/"1_0_1_A_B_C_D_0_0_0.png").write_bytes(PNG_HEADER)
    plan={"selectors":[{"selector_id":"T1","warder_key":"1.0e","state":"READY",
          "eligible_families":["channel-transparent","channel-black","channel-white"],
          "blocked_families":[],"service_identities":1}]}
    pp=t/"plan.json"; pp.write_text(json.dumps(plan))
    man=t/"manifest.json"
    cmd=[sys.executable,str(ROOT/"tools/materialize-picon-packages.py"),"--source-root",str(src),
         "--plan",str(pp),"--output-dir",str(out),"--manifest",str(man),
         "--source-commit","0123456789abcdef","--base-url","https://example.invalid/picons"]
    subprocess.check_call(cmd)
    first={p.name:p.read_bytes() for p in out.glob("*.zip")}
    subprocess.check_call(cmd)
    second={p.name:p.read_bytes() for p in out.glob("*.zip")}
    assert first==second and len(first)==3
    m=json.loads(man.read_text())
    assert len(m["packages"])==3
    assert {p["resolution"] for p in m["packages"]}=={"220x132"}
    # Different bytes for the same service-reference across provider subtrees must fail.
    p=src/"picons"/"1.0e"/"other"/"transparent"; p.mkdir(parents=True)
    (p/"1_0_1_A_B_C_D_0_0_0.png").write_bytes(PNG_HEADER+b"DIFFERENT")
    r=subprocess.run(cmd,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
    assert r.returncode != 0 and "CONFLICT" in r.stdout
print("Picon materializer self-test: PASS")
