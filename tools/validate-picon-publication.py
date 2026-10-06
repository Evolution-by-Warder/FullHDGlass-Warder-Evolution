#!/usr/bin/env python3
"""Validate package identity, archive coverage and integrity for Warder picon publication."""
from pathlib import Path
import argparse, csv, hashlib, io, json, sys, urllib.parse, zipfile

def digest(path):
    h=hashlib.sha256()
    with path.open("rb") as f:
        for b in iter(lambda:f.read(1024*1024),b""): h.update(b)
    return h.hexdigest()

def expected_position(warder_key):
    keys=warder_key.split("|")
    positions={key.split("/",1)[0].lower() for key in keys}
    if len(positions)!=1:
        return None
    return next(iter(positions))

def check_archive(payload, package, name, errors):
    included=package.get("included_references")
    dedups=package.get("same_content_deduplications")
    exclusions=package.get("ambiguous_exclusions")
    if not isinstance(included,list) or not all(isinstance(x,str) for x in included):
        errors.append("missing included-reference inventory for "+name); return
    if len(included)!=len(set(included)):
        errors.append("duplicate included references in manifest for "+name)
    if not isinstance(dedups,list) or not isinstance(exclusions,list):
        errors.append("missing collision provenance for "+name); return
    try:
        with zipfile.ZipFile(io.BytesIO(payload)) as archive:
            members=archive.namelist()
            if len(members)!=len(set(members)):
                errors.append("duplicate ZIP member names for "+name)
            if any(Path(x).name!=x or x.startswith("/") or ".." in Path(x).parts for x in members):
                errors.append("unsafe ZIP member path for "+name)
            actual={Path(x).name[:-4] for x in members if x.lower().endswith(".png")}
            if actual!=set(included):
                errors.append("manifest coverage differs from physical ZIP for %s (missing=%r extra=%r)"%(name,sorted(set(included)-actual),sorted(actual-set(included))))
    except (OSError,zipfile.BadZipFile) as e:
        errors.append("invalid ZIP payload for %s: %s"%(name,e)); return
    refs=set(included)
    for item in dedups:
        ref=item.get("service_reference")
        if ref not in refs or not item.get("sha256") or len(item.get("source_paths",[]))<2:
            errors.append("invalid same-content dedup provenance for "+name)
    excluded=set()
    for item in exclusions:
        ref=item.get("service_reference")
        candidates=item.get("candidates",[])
        hashes={c.get("sha256") for c in candidates}
        if (not ref or item.get("reason")!="different-content-same-basename" or
            len(hashes)<2 or any(not c.get("source_paths") for c in candidates)):
            errors.append("invalid ambiguous-exclusion provenance for "+name)
        if ref in refs:
            errors.append("ambiguous service included in generic package "+name+": "+str(ref))
        excluded.add(ref)
    if package.get("kind")!="satellite" and exclusions:
        errors.append("provider package contains generic collision exclusions "+name)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--root",required=True,type=Path)
    ap.add_argument("--manifest",type=Path)
    ap.add_argument("--expected-source",required=True)
    ap.add_argument("--expected-base-url",required=True)
    ap.add_argument("--mapping",type=Path,default=Path(__file__).resolve().parents[1]/"assets/warder/picon-satlist-mapping.tsv")
    ap.add_argument("--parts",action="store_true")
    ap.add_argument("--production",action="store_true")
    ap.add_argument("--expected-packages",type=int,default=114)
    a=ap.parse_args()
    mf=a.manifest or a.root/"manifest.json"
    errors=[]
    try: m=json.loads(mf.read_text(encoding="utf-8"))
    except Exception as e: raise SystemExit("manifest unreadable: %s"%e)
    if m.get("schema")!=1: errors.append("manifest schema must be 1")
    if m.get("generated_from",{}).get("ref")!=a.expected_source: errors.append("source ref mismatch")
    try:
        with a.mapping.open(encoding="utf-8",newline="") as f:
            selector_map={row["selector_id"]:row for row in csv.DictReader(f,delimiter="\t")}
    except Exception as e:
        raise SystemExit("selector mapping unreadable: %s"%e)
    pkgs=m.get("packages",[])
    expected_packages=a.expected_packages
    if len(pkgs)!=expected_packages: errors.append("expected %d packages, got %d"%(expected_packages,len(pkgs)))
    names=[p.get("filename") for p in pkgs]
    if None in names or len(set(names))!=len(names): errors.append("package filenames are missing or duplicated")
    expected_base=a.expected_base_url.rstrip("/")
    if a.production:
        stable="https://raw.githubusercontent.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/main/assets/warder/downloads/picons/channels"
        if expected_base!=stable: errors.append("production base URL must equal stable Warder channel-picon path")
        if m.get("delivery")!="raw-github-parts": errors.append("production publication must use raw-github-parts delivery")
    manifest_names=set(names)
    part_meta={x.get("filename"):x for x in m.get("parts",[])} if a.parts else {}
    disk={p.name for p in a.root.glob("*.zip")}
    if not a.parts and disk!=manifest_names:
        errors.append("publication ZIP set differs from manifest (missing=%r extra=%r)"%(sorted(manifest_names-disk),sorted(disk-manifest_names)))
    pairs=set()
    for p in pkgs:
        name=p.get("filename",""); path=a.root/name
        pair=(p.get("selector_id"),p.get("family"),p.get("resolution"))
        if pair in pairs: errors.append("duplicate selector/family/resolution: %r"%(pair,))
        pairs.add(pair)
        if p.get("family") not in ("channel-transparent","channel-black","channel-white"): errors.append("invalid family for "+name)
        resolution=p.get("resolution")
        if not isinstance(resolution,str) or "x" not in resolution: errors.append("invalid resolution for "+name)
        selector=p.get("selector_id")
        row=selector_map.get(selector)
        if not row:
            errors.append("unknown selector identity for "+name)
        else:
            key=row.get("warder_key","")
            if p.get("kind")!=row.get("kind"): errors.append("selector kind mismatch for "+name)
            if p.get("warder_key")!=key: errors.append("selector source-key mismatch for "+name)
            pos=expected_position(key)
            if not pos or str(p.get("orbital_position","")).lower()!=pos:
                errors.append("canonical orbital-position binding mismatch for "+name)
        payload=None
        if a.parts:
            urls=p.get("parts",[])
            if not isinstance(urls,list) or not urls: errors.append("missing parts for "+name); urls=[]
            assembled=hashlib.sha256()
            chunks=[]; assembled_bytes=0
            for n,url in enumerate(urls):
                pn=name+".part%02d"%n
                if url!=expected_base+"/"+pn: errors.append("non-canonical part URL for "+name)
                u=urllib.parse.urlparse(url)
                if u.scheme!="https" or u.netloc!="raw.githubusercontent.com": errors.append("non-Warder HTTPS raw host for "+name)
                pp=a.root/pn
                meta=part_meta.get(pn)
                if not pp.is_file():
                    errors.append("missing part "+pn)
                elif not meta:
                    errors.append("missing part metadata "+pn)
                else:
                    if pp.stat().st_size!=meta.get("bytes"): errors.append("part size mismatch "+pn)
                    if digest(pp)!=meta.get("sha256"): errors.append("part sha256 mismatch "+pn)
                    data=pp.read_bytes(); chunks.append(data); assembled.update(data); assembled_bytes+=len(data)
            if urls:
                if assembled_bytes!=p.get("bytes"): errors.append("reassembled size mismatch "+name)
                if assembled.hexdigest()!=p.get("sha256"): errors.append("reassembled sha256 mismatch "+name)
                payload=b"".join(chunks)
        else:
            url=p.get("url","")
            if url!=expected_base+"/"+name: errors.append("non-canonical URL for "+name)
            u=urllib.parse.urlparse(url)
            if u.scheme!="https" or u.netloc!="raw.githubusercontent.com": errors.append("non-Warder HTTPS raw host for "+name)
            if not path.is_file(): continue
            size=path.stat().st_size
            if size!=p.get("bytes"): errors.append("size mismatch for "+name)
            if digest(path)!=p.get("sha256"): errors.append("sha256 mismatch for "+name)
            payload=path.read_bytes()
        if payload is not None: check_archive(payload,p,name,errors)
    if len(pairs)!=expected_packages: errors.append("expected %d unique selector/family/resolution tuples"%expected_packages)
    if a.parts:
        expected_parts={u.rsplit("/",1)[-1] for p in pkgs for u in p.get("parts",[])}
        disk_parts={p.name for p in a.root.glob("*.part*")}
        if expected_parts!=disk_parts: errors.append("part file set differs from manifest")
        if set(part_meta)!=expected_parts: errors.append("part metadata set differs from package parts")
    if errors:
        for e in errors: print("ERROR:",e)
        sys.exit(1)
    print("PASS persistent publication payload: %d packages, canonical positions, ZIP coverage, collision provenance and SHA256 verified"%expected_packages)
if __name__=="__main__": main()
