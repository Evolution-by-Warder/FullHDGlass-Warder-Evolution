#!/usr/bin/env python3
"""Inventory preserved Chocholousek compatibility archives without modifying them."""
from __future__ import annotations
import argparse, hashlib, json, re
from pathlib import Path

RX=re.compile(r"^(?P<family>.+?)-(?P<resolution>\\d+x\\d+)-(?P<selector>.+?)_by_chocholousek\\.7z$")

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--root",required=True,type=Path)
    ap.add_argument("--output",required=True,type=Path)
    args=ap.parse_args()
    rows=[]
    for p in sorted(args.root.glob("*.7z")):
        m=RX.match(p.name)
        if not m:
            raise SystemExit("unrecognized archive name: %s" % p.name)
        h=hashlib.sha256()
        with p.open("rb") as f:
            for block in iter(lambda:f.read(1024*1024),b""): h.update(block)
        rows.append(dict(m.groupdict(),filename=p.name,bytes=p.stat().st_size,sha256=h.hexdigest()))
    combos={}
    for r in rows:
        k=r["family"]+"|"+r["resolution"]
        combos[k]=combos.get(k,0)+1
    doc={"schema":1,"policy":{"lossless":True,"resize_or_rerender":False,"silent_substitution":False},
         "archive_count":len(rows),"archive_bytes":sum(r["bytes"] for r in rows),
         "selector_count":len(set(r["selector"] for r in rows)),
         "combinations":dict(sorted(combos.items())),"archives":rows}
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(doc,sort_keys=True,indent=2)+"\n",encoding="utf-8")
    print("legacy archive inventory: %d archives, %d selectors, %d bytes" %
          (doc["archive_count"],doc["selector_count"],doc["archive_bytes"]))

if __name__=="__main__": main()
