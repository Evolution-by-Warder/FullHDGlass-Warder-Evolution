#!/usr/bin/env python3
"""Validate the Warder channel-picon cut-over contract without switching runtime."""
from pathlib import Path
import csv, json, sys

ROOT=Path(__file__).resolve().parents[1]
MAP=ROOT/"assets/warder/picon-satlist-mapping.tsv"
COV=ROOT/"assets/warder/picon-warder-master-coverage.tsv"
COL=ROOT/"assets/warder/picon-collision-audit.tsv"
errors=[]

def rows(p):
    with p.open(encoding="utf-8",newline="") as f: return list(csv.DictReader(f,delimiter="\t"))

mapping=rows(MAP); coverage={r["selector_id"]:r for r in rows(COV)}
collisions=rows(COL)
if len(mapping)!=57: errors.append("SATLIST mapping must contain 57 selectors, got %d"%len(mapping))
matched=[r for r in mapping if r["warder_master_state"]=="MATCHED"]
missing=[r for r in mapping if r["warder_master_state"]=="MISSING"]
if (len(matched),len(missing))!=(40,17): errors.append("expected 40 MATCHED / 17 MISSING, got %d / %d"%(len(matched),len(missing)))
for r in matched:
    c=coverage.get(r["selector_id"])
    if not c: errors.append("missing coverage for "+r["selector_id"]); continue
    for v in ("transparent","black","white"):
        if int(c[v])<=0: errors.append("%s has no %s source"%(r["selector_id"],v))
conflict_ids=set()
for r in collisions:
    if r["selector_id"] not in ("ALL_OTHER_MATCHED","TOTAL") and int(r["conflicting_names"]):
        conflict_ids.add(r["selector_id"])
if conflict_ids!={"FREESAT","ANTIKSAT"}:
    errors.append("expected conflict selectors FREESAT/ANTIKSAT, got "+repr(sorted(conflict_ids)))

# Runtime remains intentionally legacy until packages are persistently published.
plugin=(ROOT/"source/package-root/usr/lib/enigma2/python/Plugins/Extensions/setupGlass17/plugin.py").read_text(encoding="utf-8")
if "https://picon.cz/download/%s/" not in plugin:
    errors.append("runtime picon.cz route changed before Warder package publication")
if errors:
    for e in errors: print("ERROR:",e)
    sys.exit(1)
print("PASS channel-picon cut-over contract: 57 selectors; 40 matched; 38 ready; 2 conflict-blocked; 17 missing; runtime switch still locked")
