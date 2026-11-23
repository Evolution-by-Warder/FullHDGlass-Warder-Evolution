#!/usr/bin/env python3
"""Build the Italian candidate from a pinned catalogue and a reviewed reference map."""
import argparse
import hashlib
import io
import json
import re
import shutil
import struct
import tempfile
import zipfile
from contextlib import ExitStack
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "reports/dtt-italia-20261123"
CHANNELS = ROOT / "assets/warder/downloads/picons/channels"
SIZES = ("50x30", "220x132", "400x240")
STYLES = ("transparent", "white", "black")
URL = "https://raw.githubusercontent.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/main/assets/warder/downloads/picons/channels/"
REFERENCE = re.compile(r"1_0_(?:[0-9A-F]+_){7}0")
PNG = b"\x89PNG\r\n\x1a\n"


def sha(data):
    return hashlib.sha256(data).hexdigest()


def require(condition, detail):
    if not condition:
        raise ValueError(detail)


def dump(document):
    return (json.dumps(document, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode()


def build(input_dir, output, report_dir=REPORT):
    require(input_dir.resolve() != output.resolve(), "Output must be separate from the source catalog")
    recipe = json.loads((report_dir / "recipe.json").read_bytes())
    manifest = json.loads((input_dir / "manifest.json").read_bytes())
    parts = {p["filename"]: p for p in manifest["parts"]}
    indexed = {(p["selector_id"], p["resolution"], p["family"][8:]): p for p in manifest["packages"]}
    output.mkdir(parents=True, exist_ok=True)
    summary = []
    removable = set()
    additions = {}
    with ExitStack() as stack:
        art = {}
        for key, row in recipe["artwork"].items():
            data = (report_dir / "artwork" / (key + ".zip")).read_bytes()
            require(sha(data) == row["sha256"], key)
            archive = stack.enter_context(zipfile.ZipFile(io.BytesIO(data)))
            require(sha(archive.read("original")) == key, key)
            art[key] = archive
        for size in SIZES:
            dimensions = tuple(map(int, size.split("x")))
            for style in STYLES:
                with tempfile.TemporaryDirectory() as temporary, ExitStack() as inputs:
                    donors = {}
                    for selector in ("90E", "50W", "130E"):
                        package = indexed[selector, size, style]
                        path = Path(temporary) / package["filename"]
                        with path.open("wb") as joined:
                            for url in package["parts"]:
                                name = url.rsplit("/", 1)[-1]
                                data = (input_dir / name).read_bytes()
                                require(sha(data) == parts[name]["sha256"] and len(data) == parts[name]["bytes"], name)
                                joined.write(data)
                        require(sha(path.read_bytes()) == package["sha256"] == recipe["base"][path.name], path.name)
                        donors[selector] = inputs.enter_context(zipfile.ZipFile(path))
                    for selector, refs in sorted(recipe["selectors"].items()):
                        old = indexed.get((selector, size, style))
                        path = Path(temporary) / "result.zip"
                        if old:
                            shutil.copyfile(Path(temporary) / old["filename"], path)
                        old_names = set(donors[selector].namelist()) if old else set()
                        changes = {}
                        for ref, row in refs.items():
                            require(REFERENCE.fullmatch(ref), ref)
                            name = ref + ".png"
                            if "artwork" in row:
                                source = row["artwork"]
                                variants = recipe["artwork"][source].get("variants_from", source)
                                raw = art[variants].read(size + "-" + style + ".png")
                            else:
                                raw = donors[row["selector"]].read(row["reference"] + ".png")
                            require(raw.startswith(PNG) and struct.unpack(">II", raw[16:24]) == dimensions, name)
                            if name not in old_names or donors[selector].read(name) != raw:
                                changes[name] = raw
                        # Retain the unmodified local records. Rebuild the central directory with one entry per SRP.
                        with zipfile.ZipFile(path, "a" if old else "w") as target:
                            target.filelist[:] = [i for i in target.filelist if i.filename not in changes]
                            for name, raw in sorted(changes.items()):
                                target.NameToInfo.pop(name, None)
                                target.writestr(zipfile.ZipInfo(name), raw)
                        with zipfile.ZipFile(path) as result:
                            names = set(result.namelist())
                            require(len(names) == len(result.infolist()) and result.testzip() is None, selector)
                            require(names == old_names | {r + ".png" for r in refs}, selector)
                            for name in names:
                                raw = result.read(name)
                                require(REFERENCE.fullmatch(name[:-4]) and raw.startswith(PNG) and
                                        struct.unpack(">II", raw[16:24]) == dimensions, name)
                                if name not in changes:
                                    require(raw == donors[selector].read(name), name)
                        blob = path.read_bytes()
                        digest = sha(blob)
                        filename = "warder-%s-%s-%s-%s.zip" % (selector.lower().replace("_", "-"), size, style, digest[:16])
                        package = dict(old or {"selector_id": selector, "resolution": size, "family": "channel-" + style,
                                               "warder_key": "dtt-italia"})
                        before = old["parts"] if old else []
                        removable.update(url.rsplit("/", 1)[-1] for url in before)
                        position = 0
                        urls = []
                        # Keep original 4 MiB chunks byte-identical wherever possible. Changed tails use smaller parts.
                        while position < len(blob):
                            number = len(urls)
                            name = filename + ".part%02d" % number
                            old_part = parts[before[number].rsplit("/", 1)[-1]] if number < len(before) else None
                            candidate = blob[position:position + old_part["bytes"]] if old_part else b""
                            if old_part and sha(candidate) == old_part["sha256"]:
                                chunk = candidate
                            else:
                                chunk = blob[position:position + 786432]
                            (output / name).write_bytes(chunk)
                            additions[name] = {"filename": name, "bytes": len(chunk), "sha256": sha(chunk)}
                            urls.append(URL + name)
                            position += len(chunk)
                        package.update(filename=filename, sha256=digest, bytes=len(blob), png_count=len(names), parts=urls)
                        indexed[selector, size, style] = package
                        summary.append(dict(selector=selector, resolution=size, style=style, references=len(refs),
                                            added=len(set(changes)-old_names), replaced=len(set(changes)&old_names),
                                            preserved=len(old_names-set(changes)), sha256=digest, filename=filename, parts=len(urls)))
                        path.unlink()
    manifest["packages"] = list(indexed.values())
    manifest["parts"] = sorted([p for n, p in parts.items() if n not in removable] + list(additions.values()), key=lambda p:p["filename"])
    metadata = dump(manifest)
    (output / "manifest.json").write_bytes(metadata)
    sums = [sha(metadata) + "  manifest.json"] + [p["sha256"] + "  " + p["filename"] for p in manifest["parts"]]
    (output / "SHA256SUMS").write_text("\n".join(sums) + "\n")
    return {"packages": summary, "catalog_packages": len(indexed), "catalog_parts": len(manifest["parts"]),
            "manifest_sha256": sha(metadata)}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=CHANNELS)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    args = parser.parse_args()
    args.report.write_bytes(dump(build(args.input, args.output)))
