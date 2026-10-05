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
    a=ap.parse_args()
    mapping=read_tsv(a.mapping); source=read_tsv(a.source_manifest)
    by_id={r["id"]:r for r in source}
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
                row.update({"state":"ARCHIVED_SOURCE","filename":s["filename"],"resolution":s["resolution"],\n                            "background":s["background"],"archive_selector":s["target"],\n                            "archive_type":s["archive_type"],"provenance":s["provenance"],\n                            "warder_archive_url":"https://raw.githubusercontent.com/Evolution-by-Warder/Trezor/9cdda4ab414e7d50a97ca9285db8ebbb75fba615/archives/chocholousek-picons/originals/"+s["filename"]})
            else:
                row.update({"state":"NOT_IN_SOURCE_MANIFEST","filename":"","resolution":"",\n                            "background":"","archive_selector":"","archive_type":"","provenance":"","warder_archive_url":""})
                missing.append((m["selector_id"],col,ident))
            rows.append(row)
    doc={"schema":1,"policy":{"preserve_legacy_ids":True,"guess_missing":False},
         "rows":rows,"mapped":sum(r["state"]=="ARCHIVED_SOURCE" for r in rows),
         "unmapped":len(missing)}
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(doc,sort_keys=True,indent=2)+"\n",encoding="utf-8")
    print("legacy migration map: %d mapped, %d unresolved" % (doc["mapped"],doc["unmapped"]))

if __name__=="__main__":main()
