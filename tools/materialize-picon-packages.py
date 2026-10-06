#!/usr/bin/env python3
"""Materialize deterministic packages, excluding only audited generic collisions."""
from __future__ import annotations
import argparse, hashlib, json, zipfile, struct, sys
from pathlib import Path
VARIANTS={"channel-transparent":"transparent","channel-black":"black","channel-white":"white"}
ZIP_TIME=(2020,1,1,0,0,0)

def collect(root:Path,warder_key:str,variant:str,kind:str,expected_exclusions):
    grouped={}
    for key in warder_key.split("|"):
        base=root/"picons"/key
        if not base.exists(): raise SystemExit("missing Warder source tree: %s"%base)
        for path in sorted(base.rglob("*.png")):
            if variant not in path.parts: continue
            data=path.read_bytes(); name=path.name
            grouped.setdefault(name,[]).append((hashlib.sha256(data).hexdigest(),data,str(path)))
    chosen={}; dedup=[]; ambiguous=[]
    expected=set(expected_exclusions or [])
    for name,items in sorted(grouped.items()):
        by_sha={}
        for sha,data,path in items: by_sha.setdefault(sha,[]).append((data,path))
        if len(by_sha)>1:
            if kind!="satellite": raise SystemExit("CONFLICT provider package %s %s: %s"%(variant,name,", ".join(sorted(by_sha))))
            if name not in expected: raise SystemExit("UNDOCUMENTED COLLISION %s %s"%(variant,name))
            ambiguous.append({"service_reference":name[:-4],"filename":name,
                "reason":"different-content-same-basename","candidates":[
                    {"sha256":sha,"source_paths":sorted(x[1] for x in values)}
                    for sha,values in sorted(by_sha.items())]})
            continue
        if name in expected: raise SystemExit("AUDITED COLLISION NOT PRESENT %s %s"%(variant,name))
        sha,values=next(iter(by_sha.items()))
        chosen[name]=(sha,values[0][0])
        if len(values)>1:
            dedup.append({"service_reference":name[:-4],"filename":name,"sha256":sha,
                "source_paths":sorted(x[1] for x in values)})
    observed={x["filename"] for x in ambiguous}
    if observed!=expected:
        raise SystemExit("collision exclusion audit mismatch: expected=%r observed=%r"%(sorted(expected),sorted(observed)))
    return chosen,dedup,ambiguous

def png_resolution(data,source="<memory>"):
    signature=bytes((137,80,78,71,13,10,26,10))
    if len(data)<24 or data[:8]!=signature or data[12:16]!=b"IHDR": raise ValueError("invalid PNG source: "+source)
    w,h=struct.unpack(">II",data[16:24]); return "%dx%d"%(w,h)

def package_resolution(files):
    values={png_resolution(item[1],name) for name,item in files.items()}
    if len(values)!=1: raise SystemExit("mixed PNG resolutions in one package: %s"%sorted(values))
    return next(iter(values))

def write_zip(path,files):
    path.parent.mkdir(parents=True,exist_ok=True)
    with zipfile.ZipFile(path,"w",compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for name in sorted(files):
            info=zipfile.ZipInfo(name,ZIP_TIME); info.compress_type=zipfile.ZIP_DEFLATED
            info.external_attr=0o100644<<16; info.create_system=3; z.writestr(info,files[name][1])
    data=path.read_bytes(); return len(data),hashlib.sha256(data).hexdigest()

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--source-root",required=True,type=Path); ap.add_argument("--plan",required=True,type=Path)
    ap.add_argument("--output-dir",required=True,type=Path); ap.add_argument("--manifest",required=True,type=Path)
    ap.add_argument("--source-commit",required=True); ap.add_argument("--base-url",required=True)
    a=ap.parse_args(); plan=json.loads(a.plan.read_text(encoding="utf-8")); packages=[]; blocked=[]
    for sel in plan["selectors"]:
        if sel["state"]!="READY": continue
        for family in sel["eligible_families"]:
            variant=VARIANTS[family]; expected=sel.get("ambiguous_exclusions",{}).get(family,[])
            files,deduplications,exclusions=collect(a.source_root,sel["warder_key"],variant,sel.get("kind",""),expected)
            wanted=int(sel.get("expected_unique_identities",{}).get(family,sel["service_identities"]))
            if len(files)!=wanted: raise SystemExit("%s/%s expected %d unique picons, got %d"%(sel["selector_id"],family,wanted,len(files)))
            try: resolution=package_resolution(files)
            except ValueError as err:
                blocked.append({"selector_id":sel["selector_id"],"family":family,"reason":str(err)}); continue
            filename="warder-%s-%s.zip"%(sel["selector_id"].lower(),family)
            size,sha=write_zip(a.output_dir/filename,files)
            packages.append({"selector_id":sel["selector_id"],"kind":sel["kind"],
                "orbital_position":sel.get("orbital_position"),"family":family,"warder_key":sel["warder_key"],
                "filename":filename,"resolution":resolution,"bytes":size,"sha256":sha,
                "url":a.base_url.rstrip("/")+"/"+filename,"included_references":sorted(n[:-4] for n in files),
                "same_content_deduplications":deduplications,"ambiguous_exclusions":exclusions})
    manifest={"schema":1,"generated_from":{"repository":"Evolution-by-Warder/PiconHub-Warder-Evolution","ref":a.source_commit},
        "policy":{"canonical_orbital_position_immutable":True,"provider_fallback":False,"cross_position_fallback":False},
        "packages":packages,"blocked_packages":blocked}
    a.manifest.parent.mkdir(parents=True,exist_ok=True)
    a.manifest.write_text(json.dumps(manifest,sort_keys=True,indent=2)+"\n",encoding="utf-8")
    print("materialized %d deterministic packages; blocked %d"%(len(packages),len(blocked)))
if __name__=="__main__": main()
