#!/usr/bin/env python3
"""Fail-closed preflight for the prepared channel-picon publication boundary."""
from pathlib import Path
import json, sys
ROOT=Path(__file__).resolve().parents[1]
build=json.loads((ROOT/"assets/warder/channel-picon-build.json").read_text())
plan=json.loads((ROOT/"assets/warder/channel-picon-publication-plan.json").read_text())
fingerprint=json.loads((ROOT/"assets/warder/channel-picon-content-fingerprint.json").read_text())
checkpoint=json.loads((ROOT/"assets/warder/channel-picon-prepublication-checkpoint.json").read_text())
errors=[]
if checkpoint.get("state")!="PRE_PUBLICATION_PASS": errors.append("pre-publication checkpoint state")
if checkpoint.get("production_branch_untouched") is not True: errors.append("checkpoint production branch guard")
if checkpoint.get("publication_performed") is not False or checkpoint.get("runtime_cutover") is not False or checkpoint.get("persistent_publication") is not False: errors.append("checkpoint must remain unpublished and runtime-locked")
checkpoint_contract=checkpoint.get("contract",{})
for key,value in {"selectors":57,"matched":40,"ready":38,"collision_blocked":2,"missing_source":17,"packages":114,"parts":124}.items():
    if checkpoint_contract.get(key)!=value: errors.append("checkpoint contract "+key)
if checkpoint_contract.get("families")!=["channel-transparent","channel-black","channel-white"]: errors.append("checkpoint families")
if checkpoint.get("content_fingerprint",{}).get("manifest_sha256")!=fingerprint.get("manifest_sha256") or checkpoint.get("content_fingerprint",{}).get("sha256sums_sha256")!=fingerprint.get("sha256sums_sha256"): errors.append("checkpoint content fingerprint drift")
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
if build.get("artifact",{}).get("size_in_bytes",0)<=0: errors.append("authoritative artifact size must be positive")
content=plan.get("content_evidence")
build_content=build.get("content_evidence")
if not isinstance(content,dict) or not isinstance(build_content,dict):
    errors.append("content evidence missing")
else:
    for key in ("manifest_sha256","sha256sums_sha256"):
        value=content.get(key)
        if not isinstance(value,str) or len(value)!=64 or any(c not in "0123456789abcdef" for c in value.lower()):
            errors.append("invalid content evidence "+key)
    if content.get("source_commit")!=plan.get("source_commit"):
        errors.append("content evidence source drift")
    if content.get("packages")!=plan.get("contract",{}).get("packages"):
        errors.append("content evidence package-count drift")
    if content!=build_content:
        errors.append("build/publication content evidence drift")
    if fingerprint.get("state")!="VERIFIED_BUILD_CONTENT":
        errors.append("content fingerprint state")
    expected_fingerprint={
        "source_commit": fingerprint.get("source_commit"),
        "packages": fingerprint.get("packages"),
        "manifest_sha256": fingerprint.get("manifest_sha256"),
        "sha256sums_sha256": fingerprint.get("sha256sums_sha256"),
    }
    if content!=expected_fingerprint:
        errors.append("publication content evidence differs from reproducible fingerprint")
    runs=fingerprint.get("evidence_runs",[])
    if not isinstance(runs,list) or len(set(runs))<2:
        errors.append("content fingerprint requires two independent evidence runs")
if errors:
    for e in errors: print("ERROR:",e)
    sys.exit(1)
print("PASS publication preflight: 114 packages / 124 parts / full reassembly evidence; publication and runtime cut-over locked")
