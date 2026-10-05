#!/usr/bin/env python3
"""Fail-closed preflight for the prepared channel-picon publication boundary."""
from pathlib import Path
import json, sys
ROOT=Path(__file__).resolve().parents[1]
build=json.loads((ROOT/"assets/warder/channel-picon-build.json").read_text())
plan=json.loads((ROOT/"assets/warder/channel-picon-publication-plan.json").read_text())
errors=[]
if plan.get("state")!="PREPARED_NOT_PUBLISHED": errors.append("plan state")
if plan.get("runtime_cutover") is not False: errors.append("plan runtime cutover must be false")
if plan.get("publication_performed") is not False: errors.append("plan must remain unpublished")
if plan.get("contract",{}).get("packages")!=114: errors.append("package count")
if plan.get("contract",{}).get("parts")!=124: errors.append("part count")
if plan.get("contract",{}).get("delivery")!="raw-github-parts": errors.append("delivery")
if plan.get("integrity",{}).get("candidate")!="PASS": errors.append("candidate integrity")
if plan.get("integrity",{}).get("full_reassembly")!="PASS": errors.append("reassembly integrity")
if build.get("runtime_cutover") is not False: errors.append("build runtime cutover must be false")
p=build.get("publication",{})
if p.get("state")!="NOT_PUBLISHED" or p.get("persistent") is not False: errors.append("build publication lock")
if p.get("prepared_packages")!=114 or p.get("prepared_parts")!=124: errors.append("build prepared counts")
if p.get("reassembly_validation")!="PASS": errors.append("build reassembly evidence")
if plan.get("evidence",{}).get("workflow_run")!=build.get("workflow",{}).get("run_id"): errors.append("workflow evidence drift")
if plan.get("evidence",{}).get("artifact_id")!=build.get("artifact",{}).get("id"): errors.append("artifact evidence drift")
if plan.get("evidence",{}).get("artifact_bytes")!=build.get("artifact",{}).get("size_in_bytes"): errors.append("artifact byte-size evidence drift")
if plan.get("evidence",{}).get("artifact_digest")!=build.get("artifact",{}).get("digest"): errors.append("artifact digest evidence drift")
if build.get("workflow",{}).get("conclusion")!="success": errors.append("authoritative workflow is not successful")
if build.get("artifact",{}).get("size_in_bytes")!=615397302: errors.append("unexpected authoritative artifact size")
if errors:
    for e in errors: print("ERROR:",e)
    sys.exit(1)
print("PASS publication preflight: 114 packages / 124 parts / full reassembly evidence; publication and runtime cut-over locked")
