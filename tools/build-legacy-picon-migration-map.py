#!/usr/bin/env python3
"""Join FullHDGlass legacy numeric IDs to the preserved Chocholousek source manifest."""
from __future__ import annotations
import argparse,csv,json
from pathlib import Path

COLUMNS=("legacy_400x240","legacy_black_50x30","legacy_black","legacy_white_50x30","legacy_white","legacy_oled","legacy_220x132")

def read_tsv(p):
    with p.open(encoding="utf-8",newline="") as f:return list(csv.DictReader(f,delimiter="\t"))

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--mapping",required=True,type=Path)
    ap.add_argument("--source-manifest",required=True,type=Path)
    ap.add_argument("--output",required=True,type=Path)
    ap.add_argument("--runtime-output",type=Path)
    a=ap.parse_args()
    mapping=read_tsv(a.mapping); source=read_tsv(a.source_manifest)
    grouped={}
    for r in source:
        grouped.setdefault(r["id"],[]).append(r)
    by_id={}
    identity_fields=("filename","resolution","background","target","archive_type","provenance")
    for ident, candidates in grouped.items():
        identities={tuple(r.get(k,"") for k in identity_fields) for r in candidates}
        if len(identities)!=1:
            raise SystemExit("ambiguous duplicate legacy ID in source manifest: %s" % ident)
        by_id[ident]=candidates[0]
    rows=[]; missing=[]
    for m in mapping:
        for col in COLUMNS:
            ident=(m.get(col) or "").strip()
            if not ident: continue
            s=by_id.get(ident)
            row={"selector_id":m["selector_id"],"legacy_column":col,"legacy_id":ident,
                 "display_label":m["display_label"],"warder_key":m["warder_key"],
                 "warder_master_state":m["warder_master_state"]}
            if s:
                filename=s["filename"]
                if "/" in filename or "\\" in filename or ".." in filename or not filename.endswith(".7z"):
                    raise SystemExit("unsafe archived filename for legacy ID %s: %r" % (ident,filename))
                row.update({"state":"ARCHIVED_SOURCE","filename":s["filename"],"resolution":s["resolution"],
                            "background":s["background"],"archive_selector":s["target"],
                            "archive_type":s["archive_type"],"provenance":s["provenance"],
                            "warder_archive_url":"https://raw.githubusercontent.com/Evolution-by-Warder/Trezor/9cdda4ab414e7d50a97ca9285db8ebbb75fba615/archives/chocholousek-picons/originals/"+s["filename"]})
            else:
                row.update({"state":"NOT_IN_SOURCE_MANIFEST","filename":"","resolution":"",
                            "background":"","archive_selector":"","archive_type":"","provenance":"","warder_archive_url":""})
                missing.append((m["selector_id"],col,ident))
            rows.append(row)
    doc={"schema":1,"policy":{"preserve_legacy_ids":True,"guess_missing":False},
         "rows":rows,"mapped":sum(r["state"]=="ARCHIVED_SOURCE" for r in rows),
         "unmapped":len(missing)}
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(doc,sort_keys=True,indent=2)+chr(10),encoding="utf-8")
    if a.runtime_output:
        runtime={r["legacy_id"]:r["warder_archive_url"] for r in rows if r["state"]=="ARCHIVED_SOURCE"}
        a.runtime_output.parent.mkdir(parents=True,exist_ok=True)
        a.runtime_output.write_text(json.dumps({"schema":1,"source_commit":"9cdda4ab414e7d50a97ca9285db8ebbb75fba615","archives":runtime},sort_keys=True,separators=(",",":"))+chr(10),encoding="utf-8")
    print("legacy migration map: %d mapped, %d unresolved" % (doc["mapped"],doc["unmapped"]))

if __name__=="__main__":main()
