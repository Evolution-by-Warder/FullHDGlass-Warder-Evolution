#!/usr/bin/env python3
"""Validate the two-phase channel-picon cut-over safety contract."""
from pathlib import Path
import json, sys
ROOT=Path(__file__).resolve().parents[1]
build=json.loads((ROOT/"assets/warder/channel-picon-build.json").read_text())
plan=json.loads((ROOT/"assets/warder/channel-picon-publication-plan.json").read_text())
plugin=(ROOT/"source/package-root/usr/lib/enigma2/python/Plugins/Extensions/setupGlass17/plugin.py").read_text(encoding="utf-8")
errors=[]
legacy="https://picon.cz/download/%s/"
if build.get("state")=="BUILT_NOT_PUBLISHED":
    if build.get("runtime_cutover") is not False: errors.append("unpublished build cannot enable runtime cutover")
    if legacy not in plugin: errors.append("legacy fallback removed before persistent publication")
if plan.get("publication_performed") is False and legacy not in plugin:
    errors.append("prepared-only plan must retain legacy fallback")
if build.get("state")=="PUBLISHED":
    p=build.get("publication",{})
    if p.get("state")!="PUBLISHED" or p.get("persistent") is not True: errors.append("PUBLISHED requires persistent evidence")
runtime_cutover=bool(build.get("runtime_cutover"))
publication=build.get("publication",{})
if runtime_cutover:
    if build.get("state")!="PUBLISHED":
        errors.append("runtime cutover requires build state PUBLISHED")
    if publication.get("state")!="PUBLISHED" or publication.get("persistent") is not True:
        errors.append("runtime cutover requires persistent published backend")
    if not publication.get("manifest_url") or not publication.get("base_url"):
        errors.append("runtime cutover requires manifest/base URLs")
    if plan.get("publication_performed") is not True:
        errors.append("runtime cutover requires completed publication plan")
else:
    # Before the reviewed runtime switch, legacy remains a mandatory safety route.
    if legacy not in plugin:
        errors.append("legacy fallback removed before reviewed runtime cutover")
# Deliberately do not auto-enable runtime cutover here: publication and runtime switch are separate reviewed changes.
if errors:
    for e in errors: print("ERROR:",e)
    sys.exit(1)
print("PASS two-phase cut-over safety: publication and runtime switch remain separately gated")
