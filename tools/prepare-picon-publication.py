#!/usr/bin/env python3
"""Prepare split, integrity-recorded channel-picon publication files."""
from pathlib import Path
import argparse, hashlib, json

def digest(path):
    h=hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda:f.read(1024*1024),b""):
            h.update(chunk)
    return h.hexdigest()

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--input",required=True,type=Path)
    ap.add_argument("--manifest",required=True,type=Path)
    ap.add_argument("--output",required=True,type=Path)
    ap.add_argument("--base-url",required=True)
    ap.add_argument("--part-bytes",type=int,default=20*1024*1024)
    a=ap.parse_args()
    if not 0<a.part_bytes<=25*1024*1024:
        raise SystemExit("part size must be 1..25 MiB")
    src=json.loads(a.manifest.read_text(encoding="utf-8"))
    packages=src.get("packages",[])
    if len(packages)!=114:
        raise SystemExit("expected 114 packages")
    if src.get("blocked_packages"):
        raise SystemExit("refusing publication with blocked source packages")
    a.output.mkdir(parents=True,exist_ok=True)
    output_packages=[]
    part_records=[]
    for p in packages:
        name=p["filename"]
        source=a.input/name
        if not source.is_file():
            raise SystemExit("missing "+name)
        if source.stat().st_size!=p["bytes"] or digest(source)!=p["sha256"]:
            raise SystemExit("source mismatch "+name)
        urls=[]
        with source.open("rb") as stream:
            index=0
            while True:
                data=stream.read(a.part_bytes)
                if not data:
                    break
                part_name="%s.part%02d"%(name,index)
                part_path=a.output/part_name
                part_path.write_bytes(data)
                urls.append(a.base_url.rstrip("/")+"/"+part_name)
                part_records.append({
                    "filename":part_name,
                    "bytes":len(data),
                    "sha256":hashlib.sha256(data).hexdigest(),
                })
                index+=1
        if not urls:
            raise SystemExit("empty "+name)
        output_packages.append({
            "selector_id":p["selector_id"],
            "family":p["family"],
            "warder_key":p["warder_key"],
            "resolution":p["resolution"],
            "filename":name,
            "bytes":p["bytes"],
            "sha256":p["sha256"],
            "parts":urls,
        })
    document={
        "schema":1,
        "generated_from":src["generated_from"],
        "delivery":"raw-github-parts",
        "packages":output_packages,
        "parts":part_records,
    }
    (a.output/"manifest.json").write_text(json.dumps(document,sort_keys=True,indent=2)+"\n",encoding="utf-8")
    (a.output/"SHA256SUMS").write_text(
        "".join("%s  %s\n"%(x["sha256"],x["filename"]) for x in part_records),
        encoding="ascii",
    )
    print("Prepared %d packages as %d persistent parts"%(len(output_packages),len(part_records)))

if __name__=="__main__":
    main()
