#!/usr/bin/env python3
"""Regression for publication count, canonical binding, provenance and ZIP coverage."""
import hashlib, json, subprocess, sys, tempfile, zipfile
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
PREP=ROOT/"tools/prepare-picon-publication.py"
VALIDATE=ROOT/"tools/validate-picon-publication.py"
MAPPING=ROOT/"assets/warder/picon-satlist-mapping.tsv"
SOURCE="2827fed5b2e6ae4697f08ca57a8c2298079d410f"
BASE="https://raw.githubusercontent.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/warder-modernization-work/assets/warder/downloads/picons/channels"

with tempfile.TemporaryDirectory(prefix="warder-publication-test-") as td:
    tmp=Path(td); source_dir=tmp/"source"; source_dir.mkdir()
    zip_path=source_dir/"warder-160e-channel-transparent.zip"
    with zipfile.ZipFile(zip_path,"w",compression=zipfile.ZIP_DEFLATED) as z:
        z.writestr("service_a.png",b"picon")
    data=zip_path.read_bytes()
    package={
        "selector_id":"160E","kind":"satellite","orbital_position":"16.0e",
        "family":"channel-transparent","warder_key":"16.0e","resolution":"220x132",
        "filename":zip_path.name,"bytes":len(data),"sha256":hashlib.sha256(data).hexdigest(),
        "included_references":["service_a"],
        "same_content_deduplications":[{"service_reference":"service_a","filename":"service_a.png","sha256":"a"*64,"source_paths":["picons/a/transparent/service_a.png","picons/b/transparent/service_a.png"]}],
        "ambiguous_exclusions":[{"service_reference":"ambiguous_ref","filename":"ambiguous_ref.png","reason":"different-content-same-basename","candidates":[{"sha256":"b"*64,"source_paths":["picons/a/transparent/ambiguous_ref.png"]},{"sha256":"c"*64,"source_paths":["picons/b/transparent/ambiguous_ref.png"]}]}]
    }
    manifest=tmp/"manifest.json"
    manifest.write_text(json.dumps({"schema":2,"generated_from":{"ref":SOURCE},"packages":[package],"blocked_packages":[]}),encoding="utf-8")
    out=tmp/"parts"
    base_args=["--input",str(source_dir),"--manifest",str(manifest),"--output",str(out),"--base-url",BASE]
    r=subprocess.run([sys.executable,str(PREP),*base_args,"--expected-packages","1"],capture_output=True,text=True)
    assert r.returncode==0,r.stdout+r.stderr
    split=out/"manifest.json"
    published=json.loads(split.read_text(encoding="utf-8"))
    p=published["packages"][0]
    assert p["orbital_position"]=="16.0e"
    assert p["included_references"]==["service_a"]
    assert p["same_content_deduplications"]==package["same_content_deduplications"]
    assert p["ambiguous_exclusions"]==package["ambiguous_exclusions"]
    args=[sys.executable,str(VALIDATE),"--root",str(out),"--expected-source",SOURCE,"--expected-base-url",BASE,"--expected-packages","1","--mapping",str(MAPPING),"--parts"]
    r=subprocess.run(args,capture_output=True,text=True)
    assert r.returncode==0,r.stdout+r.stderr
    p["included_references"]=["not_in_zip"]
    split.write_text(json.dumps(published),encoding="utf-8")
    r=subprocess.run(args,capture_output=True,text=True)
    assert r.returncode!=0 and "manifest coverage differs from physical ZIP" in r.stdout,r.stdout+r.stderr
    p["included_references"]=["service_a"]
    p["orbital_position"]="19.2e"
    split.write_text(json.dumps(published),encoding="utf-8")
    r=subprocess.run(args,capture_output=True,text=True)
    assert r.returncode!=0 and "canonical orbital-position binding mismatch" in r.stdout,r.stdout+r.stderr
    r=subprocess.run([sys.executable,str(PREP),*base_args],capture_output=True,text=True)
    assert r.returncode!=0 and "expected 114 packages, got 1" in r.stderr,r.stdout+r.stderr
print("Picon publication integrity regressions: PASS (metadata, ZIP coverage, orbital binding, explicit candidate count)")
