#!/usr/bin/env python3
"""Deterministic Warder channel package plan with exact collision exclusions.

Canonical orbital position comes from the audited source-tree key; selector_id
remains an independent technical package selector.
"""
from __future__ import annotations
import argparse, csv, json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MAPPING = ROOT / "assets/warder/picon-satlist-mapping.tsv"
DEFAULT_COVERAGE = ROOT / "assets/warder/picon-warder-master-coverage.tsv"
DEFAULT_COLLISIONS = ROOT / "assets/warder/picon-collision-audit.tsv"
DEFAULT_CONFLICTS = ROOT / "assets/warder/picon-collision-conflicts.tsv"
FAMILY_VARIANT = {"channel-transparent":"transparent","channel-black":"black","channel-white":"white"}
UNRESOLVED_FAMILIES = ("channel-400x240","channel-220x132","channel-black-50x30","channel-white-50x30","channel-oled")

def read_tsv(path):
    with path.open("r", encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh, delimiter="\t"))

def orbital_position(warder_key, kind):
    """Read the canonical position from the source-tree binding, never SATLIST icon IDs."""
    if kind == "dtt":
        return None
    value = str(warder_key or "").split("|", 1)[0].split("/", 1)[0].lower()
    return value if re.match(r"^[0-9]+(?:\.[0-9]+)?[ew]$", value) else None

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--mapping",type=Path,default=DEFAULT_MAPPING)
    ap.add_argument("--coverage",type=Path,default=DEFAULT_COVERAGE)
    ap.add_argument("--collisions",type=Path,default=DEFAULT_COLLISIONS)
    ap.add_argument("--conflicts",type=Path,default=DEFAULT_CONFLICTS)
    ap.add_argument("--output",type=Path)
    ap.add_argument("--source-ref",default="warder-master-production")
    a=ap.parse_args()
    mapping={r["selector_id"]:r for r in read_tsv(a.mapping)}
    coverage={r["selector_id"]:r for r in read_tsv(a.coverage)}
    conflict_rows=read_tsv(a.conflicts)
    refs={}
    for r in conflict_rows:
        sid=r["selector_id"]
        if sid in ("ALL_OTHER_MATCHED","TOTAL"): continue
        family={"transparent":"channel-transparent","black":"channel-black","white":"channel-white"}.get(r["variant"])
        if family:
            refs.setdefault(sid,{}).setdefault(family,set()).add(r["service_reference"])
    audit={r["selector_id"]:r for r in read_tsv(a.collisions) if r["selector_id"] not in ("ALL_OTHER_MATCHED","TOTAL")}
    selectors=[]
    for sid in sorted(mapping):
        m=mapping[sid]
        kind=m.get("kind","")
        position=orbital_position(m.get("warder_key"),kind)
        base={"selector_id":sid,"kind":kind,"orbital_position":position,"warder_key":m["warder_key"]}
        if m["warder_master_state"]!="MATCHED":
            selectors.append(dict(base,state="MISSING_SOURCE",eligible_families=[],
                blocked_families=list(FAMILY_VARIANT)+list(UNRESOLVED_FAMILIES),ambiguous_exclusions={}))
            continue
        c=coverage.get(sid)
        if not c: raise SystemExit("coverage missing for MATCHED selector: "+sid)
        if kind=="satellite" and not position: raise SystemExit("canonical orbital position missing for generic selector: "+sid)
        eligible=[]; blocked=list(UNRESOLVED_FAMILIES); exclusions={}
        for family,variant in FAMILY_VARIANT.items():
            if int(c[variant])<=0:
                blocked.append(family); continue
            audited_count=int(audit.get(sid,{}).get("conflicting_names",0)) if audit.get(sid,{}).get("variant")==variant else sum(int(x.get("conflicting_names",0)) for x in read_tsv(a.collisions) if x["selector_id"]==sid and x["variant"]==variant)
            expected=refs.get(sid,{}).get(family,set())
            if audited_count != len(expected):
                raise SystemExit("%s/%s collision audit refs mismatch: %d != %d"%(sid,family,audited_count,len(expected)))
            if expected and kind!="satellite":
                raise SystemExit("ambiguous service audit unexpectedly targets provider selector: %s/%s"%(sid,family))
            if expected: exclusions[family]=sorted(expected)
            eligible.append(family)
        expected_counts={family:int(c["service_identities"])-len(exclusions.get(family,[])) for family in eligible}
        selectors.append(dict(base,state="READY" if eligible else "BLOCKED",eligible_families=eligible,
            blocked_families=sorted(blocked),service_identities=int(c["service_identities"]),
            expected_unique_identities=expected_counts,ambiguous_exclusions=exclusions))
    doc={"schema":2,"authority":"PiconHub-Warder-Evolution/"+a.source_ref,
        "policy":{"deterministic":True,"same_content":"deduplicate-once","different_content":"exclude-only-audited-generic-service-reference",
        "provider_package_isolation":True,"selector_id_is_not_orbital_identity":True,"resize_or_rerender":False,"runtime_switch":False},
        "selectors":selectors}
    payload=json.dumps(doc,ensure_ascii=False,sort_keys=True,indent=2)+"\n"
    if a.output: a.output.parent.mkdir(parents=True,exist_ok=True); a.output.write_text(payload,encoding="utf-8")
    else: print(payload,end="")
if __name__=="__main__": main()
