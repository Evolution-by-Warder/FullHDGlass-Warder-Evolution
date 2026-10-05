#!/usr/bin/env python3
"""Validate a materialized Warder channel-picon publication tree before exposure."""
from pathlib import Path
import argparse, hashlib, json, sys, urllib.parse

def digest(path):
    h=hashlib.sha256()
    with path.open("rb") as f:
        for b in iter(lambda:f.read(1024*1024),b""): h.update(b)
    return h.hexdigest()

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--root",required=True,type=Path)
    ap.add_argument("--manifest",type=Path)
    ap.add_argument("--expected-source",required=True)
    ap.add_argument("--expected-base-url",required=True)
    ap.add_argument("--parts",action="store_true")
    a=ap.parse_args()
    mf=a.manifest or a.root/"manifest.json"
    errors=[]
    try: m=json.loads(mf.read_text(encoding="utf-8"))
    except Exception as e: raise SystemExit("manifest unreadable: %s"%e)
    if m.get("schema")!=1: errors.append("manifest schema must be 1")
    if m.get("generated_from",{}).get("ref")!=a.expected_source: errors.append("source ref mismatch")
    pkgs=m.get("packages",[])
    if len(pkgs)!=114: errors.append("expected 114 packages, got %d"%len(pkgs))
    names=[p.get("filename") for p in pkgs]
    if None in names or len(set(names))!=len(names): errors.append("package filenames are missing or duplicated")
    expected_base=a.expected_base_url.rstrip("/")
    manifest_names=set(names)
    disk={p.name for p in a.root.glob("*.zip")}
    if disk!=manifest_names:
        errors.append("publication ZIP set differs from manifest (missing=%r extra=%r)"%(sorted(manifest_names-disk),sorted(disk-manifest_names)))
    pairs=set()
    for p in pkgs:
        name=p.get("filename",""); path=a.root/name
        pair=(p.get("selector_id"),p.get("family"))
        if pair in pairs: errors.append("duplicate selector/family: %r"%(pair,))
        pairs.add(pair)
        if p.get("family") not in ("channel-transparent","channel-black","channel-white"): errors.append("invalid family for "+name)
        if a.parts:
            urls=p.get("parts",[])
            if not isinstance(urls,list) or not urls: errors.append("missing parts for "+name); urls=[]
            for n,url in enumerate(urls):
                if url!=expected_base+"/"+name+".part%02d"%n: errors.append("non-canonical part URL for "+name)
                u=urllib.parse.urlparse(url)
                if u.scheme!="https" or u.netloc!="raw.githubusercontent.com": errors.append("non-Warder HTTPS raw host for "+name)
        else:
            url=p.get("url","")
            if url!=expected_base+"/"+name: errors.append("non-canonical URL for "+name)
            u=urllib.parse.urlparse(url)
            if u.scheme!="https" or u.netloc!="raw.githubusercontent.com": errors.append("non-Warder HTTPS raw host for "+name)
        if not path.is_file(): continue
        size=path.stat().st_size
        if size!=p.get("bytes"): errors.append("size mismatch for "+name)
        if digest(path)!=p.get("sha256"): errors.append("sha256 mismatch for "+name)
    if len(pairs)!=114: errors.append("expected 114 unique selector/family pairs")
    if errors:
        for e in errors: print("ERROR:",e)
        sys.exit(1)
    print("PASS persistent publication payload: 114 packages, canonical URLs, sizes and SHA256 verified")
if __name__=="__main__": main()
