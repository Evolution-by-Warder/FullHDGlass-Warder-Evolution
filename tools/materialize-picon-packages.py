#!/usr/bin/env python3
"""Materialize deterministic FullHDGlass channel-picon ZIPs from a checked-out Warder Master tree.

No resizing/rerendering is performed. Only transparent/black/white source files
are copied. Same-name files with identical bytes deduplicate; different bytes
hard-fail. The output ZIP metadata is normalized for reproducibility.
"""

from __future__ import annotations
import argparse, hashlib, json, zipfile, struct, sys
from pathlib import Path

VARIANTS = {
    "channel-transparent": "transparent",
    "channel-black": "black",
    "channel-white": "white",
}
ZIP_TIME = (2020, 1, 1, 0, 0, 0)


def collect(root: Path, warder_key: str, variant: str):
    chosen = {}
    origins = {}
    for key in warder_key.split("|"):
        base = root / "picons" / key
        if not base.exists():
            raise SystemExit("missing Warder source tree: %s" % base)
        for p in sorted(base.rglob("*.png")):
            if variant not in p.parts:
                continue
            name = p.name
            data = p.read_bytes()
            digest = hashlib.sha256(data).hexdigest()
            if name in chosen and chosen[name][0] != digest:
                raise SystemExit("CONFLICT %s %s: %s != %s" % (variant, name, origins[name], p))
            chosen.setdefault(name, (digest, data))
            origins.setdefault(name, str(p))
    return chosen


def png_resolution(data, source="<memory>"):
    if len(data) < 24 or data[:8] != b"\\x89PNG\\r\\n\\x1a\\n" or data[12:16] != b"IHDR":
        raise ValueError("invalid PNG source: %s" % source)
    width, height = struct.unpack(">II", data[16:24])
    return "%dx%d" % (width, height)

def package_resolution(files):
    values = {png_resolution(item[1], name) for name, item in files.items()}
    if len(values) != 1:
        raise SystemExit("mixed PNG resolutions in one package: %s" % sorted(values))
    return next(iter(values))

def write_zip(path: Path, files):
    path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
        for name in sorted(files):
            zi = zipfile.ZipInfo(name, ZIP_TIME)
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o100644 << 16
            zi.create_system = 3
            zf.writestr(zi, files[name][1])
    data = path.read_bytes()
    return len(data), hashlib.sha256(data).hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--source-root", required=True, type=Path)
    ap.add_argument("--plan", required=True, type=Path)
    ap.add_argument("--output-dir", required=True, type=Path)
    ap.add_argument("--manifest", required=True, type=Path)
    ap.add_argument("--source-commit", required=True)
    ap.add_argument("--base-url", required=True)
    args = ap.parse_args()
    plan = json.loads(args.plan.read_text(encoding="utf-8"))
    packages = []
    blocked = []
    for sel in plan["selectors"]:
        if sel["state"] != "READY":
            continue
        for family in sel["eligible_families"]:
            variant = VARIANTS[family]
            files = collect(args.source_root, sel["warder_key"], variant)
            expected = int(sel["service_identities"])
            if len(files) != expected:
                raise SystemExit("%s/%s expected %d unique picons, got %d" % (sel["selector_id"], family, expected, len(files)))
            try:
                resolution = package_resolution(files)
            except ValueError as err:
                reason = str(err)
                print("BLOCKED %s/%s: %s" % (sel["selector_id"], family, reason), file=sys.stderr)
                blocked.append({"selector_id": sel["selector_id"], "family": family, "reason": reason})
                continue
            filename = "warder-%s-%s.zip" % (sel["selector_id"].lower(), family)
            size, sha = write_zip(args.output_dir / filename, files)
            packages.append({
                "selector_id": sel["selector_id"], "family": family,
                "warder_key": sel["warder_key"], "filename": filename,
                "resolution": resolution, "bytes": size, "sha256": sha,
                "url": args.base_url.rstrip("/") + "/" + filename,
            })
    manifest = {
        "schema": 1,
        "generated_from": {
            "repository": "Evolution-by-Warder/PiconHub-Warder-Evolution",
            "ref": args.source_commit,
        },
        "packages": packages,
        "blocked_packages": blocked,
    }
    args.manifest.parent.mkdir(parents=True, exist_ok=True)
    args.manifest.write_text(json.dumps(manifest, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    print("materialized %d deterministic packages; blocked %d" % (len(packages), len(blocked)))


if __name__ == "__main__":
    main()
