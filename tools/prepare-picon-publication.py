#!/usr/bin/env python3
"""Split materialized channel-picon ZIPs into GitHub-safe persistent raw assets.

This prepares publication files only. It never changes runtime or main.
"""
from pathlib import Path
import argparse, hashlib, json

def sha(path):
    h=hashlib.sha256()
    with path.open("rb") as f:
        for b in iter(lambda:f.read(1024*1024),b""): h.update(b)
    return h.hexdigest()

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--input",required=True,type=Path)
    ap.add_argument("--manifest",required=True,type=Path)
    ap.add_argument("--output",required=True,type=Path)
    ap.add_argument("--base-url",required=True)
    ap.add_argument("--part-bytes",type=int,default=20*1024*1024)
    a=ap.parse_args()
    if a.part_bytes<=0 or a.part_bytes>25*1024*1024: raise SystemExit("part size must be 1..25 MiB")
    src=json.loads(a.manifest.read_text(encoding="utf-8"))
    pkgs=src.get("packages",[])
    if len(pkgs)!=114: raise SystemExit("expected 114 packages")
    a.output.mkdir(parents=True,exist_ok=True)
    out=[]; part_records=[]
    for p in pkgs:
        name=p["filename"]; inp=a.input/name
        if not inp.is_file(): raise SystemExit("missing "+name)
        if inp.stat().st_size!=p["bytes"] or sha(inp)!=p["sha256"]: raise SystemExit("source mismatch "+name)
        urls=[]; idx=0
        with inp.open("rb") as f:
            while True:
                data=f.read(a.part_bytes)
                if not data: break
                pn="%s.part%02d"%(name,idx)
                q=a.output/pn; q.write_bytes(data)
                urls.append(a.base_url.rstrip("/")+"/"+pn)
                part_records.append({"filename":pn,"bytes":len(data),"sha256":hashlib.sha256(data).hexdigest()})
                idx+=1
        if not urls: raise SystemExit("empty "+name)
        out.append({
            "selector_id":p["selector_id"],"family":p["family"],"warder_key":p["warder_key"],
            "filename":name,"bytes":p["bytes"],"sha256":p["sha256"],"parts":urls,
        })
    doc={"schema":1,"generated_from":src["generated_from"],"delivery":"raw-github-parts","packages":out,"parts":part_records}\n    (a.output/"manifest.json").write_text(json.dumps(doc,sort_keys=True,indent=2)+"\\n",encoding="utf-8")\n    (a.output/"SHA256SUMS").write_text("".join("%s  %s\\n"%(x["sha256"],x["filename"]) for x in part_records),encoding="ascii")\n    print("Prepared %d packages as %d persistent parts"%(len(out),sum(len(x["parts"]) for x in out)))
if __name__=="__main__": main()
