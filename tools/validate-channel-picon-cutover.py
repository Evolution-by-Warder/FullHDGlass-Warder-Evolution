#!/usr/bin/env python3
"""Validate the Warder channel-picon cut-over contract without switching runtime."""
from pathlib import Path
import csv, json, sys, urllib.parse

ROOT=Path(__file__).resolve().parents[1]
MAP=ROOT/"assets/warder/picon-satlist-mapping.tsv"
COV=ROOT/"assets/warder/picon-warder-master-coverage.tsv"
COL=ROOT/"assets/warder/picon-collision-audit.tsv"
BUILD=ROOT/"assets/warder/channel-picon-build.json"
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

build=json.loads(BUILD.read_text(encoding="utf-8"))
contract=build.get("package_contract",{})
for key,value in {"selectors":57,"matched":40,"ready":38,"collision_blocked":2,"missing_source":17,"packages":114}.items():
    if contract.get(key)!=value: errors.append("verified build contract %s mismatch"%key)
if build.get("state") not in ("BUILT_NOT_PUBLISHED","PUBLISHED"):
    errors.append("channel-picon build state is invalid")
if build.get("runtime_cutover") is not False:
    errors.append("runtime cutover must remain false until an explicit separately validated cut-over change")
if build.get("workflow",{}).get("conclusion")!="success": errors.append("recorded channel-picon workflow is not successful")
if not str(build.get("artifact",{}).get("digest","")).startswith("sha256:"): errors.append("recorded artifact digest is missing")


# Persistent publication is a separate gate from successful materialization.
# A temporary Actions artifact must never be mistaken for a receiver backend.
publication=build.get("publication",{})
if build.get("state")=="BUILT_NOT_PUBLISHED":
    if publication.get("state") not in (None,"NOT_PUBLISHED"):
        errors.append("unpublished build advertises a publication state")
    if publication.get("manifest_url") or publication.get("base_url"):
        errors.append("unpublished build advertises persistent receiver URLs")
elif build.get("state")=="PUBLISHED":
    if publication.get("state")!="PUBLISHED":
        errors.append("published build is missing PUBLISHED publication evidence")
    if not publication.get("manifest_url") or not publication.get("base_url"):
        errors.append("published build is missing persistent manifest/base URL")
    if publication.get("persistent") is not True:
        errors.append("published build must explicitly mark persistent=true")
    if publication.get("required_packages")!=114:
        errors.append("published build must require exactly 114 packages")
    for key in ("manifest_url","base_url"):
        url=str(publication.get(key) or "")
        u=urllib.parse.urlparse(url)
        if u.scheme!="https" or u.netloc!="raw.githubusercontent.com":
            errors.append("published %s must use Warder HTTPS raw GitHub"%key)
        if "/warder-modernization-work/" in url:
            errors.append("published %s must not point at development branch"%key)
else:
    errors.append("unknown channel-picon build state: "+repr(build.get("state")))
if build.get("runtime_cutover") and build.get("state")!="PUBLISHED":
    errors.append("runtime cutover cannot be enabled before persistent publication")

# Runtime remains intentionally legacy until packages are persistently published.
plugin=(ROOT/"source/package-root/usr/lib/enigma2/python/Plugins/Extensions/setupGlass17/plugin.py").read_text(encoding="utf-8")
if "https://picon.cz/download/%s/" not in plugin:
    errors.append("runtime picon.cz route changed before Warder package publication")
if errors:
    for e in errors: print("ERROR:",e)
    sys.exit(1)
print("PASS channel-picon cut-over contract: 57 selectors; 40 matched; 38 ready; 2 conflict-blocked; 17 missing; runtime switch still locked")
