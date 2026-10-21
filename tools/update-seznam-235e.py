#!/usr/bin/env python3
"""Replace only approved Seznam PNGs in existing 23.5E delivery packages."""
import copy
import hashlib
import io
import json
from pathlib import Path
import zipfile

ROOT = Path(__file__).resolve().parents[1]
SOURCE_REF = "21868a9d27eeb2feda632788b0452a327e97cb98"
APPROVED = {
    "transparent": "63524ee93947529496b55f3dc2e7be347606ef2e4a1da554678ed472a8337620",
    "white": "65e47da50dbf70abf38a8c94248e8d5606d91ba61267178c467611dce4c48ef1",
    "black": "329d977f16960b0de17342e862b8507706db65bdfd46a52093d0016d0bc1d6c0",
}
NAMES = {f"1_0_{kind}_335B_C93_3_EB0000_0_0_0.png" for kind in ("1", "19")}


def sha(data):
    return hashlib.sha256(data).hexdigest()


def main():
    source = ROOT / ".approved-picons/picons/23.5e/canal-plus-cz"
    evidence = []
    for suffix in ("", "test-candidate"):
        base = ROOT / "assets/warder/downloads/picons/channels" / suffix
        manifest = base / "manifest.json"
        doc = json.loads(manifest.read_text())
        before = copy.deepcopy(doc)
        touched = {}
        for package in doc["packages"]:
            if package["selector_id"] != "235E":
                continue
            style = package["family"].removeprefix("channel-")
            png = (source / style / "1_0_1_335B_C93_3_EB0000_0_0_0.png").read_bytes()
            assert sha(png) == APPROVED[style]
            paths = [base / url.rsplit("/", 1)[1] for url in package["parts"]]
            old = b"".join(path.read_bytes() for path in paths)
            assert len(old) == package["bytes"] and sha(old) == package["sha256"]
            archive = zipfile.ZipFile(io.BytesIO(old))
            assert NAMES <= set(archive.namelist())
            old_files = {name: archive.read(name) for name in archive.namelist()}
            changed = sorted(name for name in NAMES if old_files[name] != png)
            new = old
            if changed:
                output = io.BytesIO()
                with zipfile.ZipFile(output, "w") as out:
                    out.comment = archive.comment
                    for entry in archive.infolist():
                        out.writestr(entry, png if entry.filename in NAMES else old_files[entry.filename])
                new = output.getvalue()
            result = zipfile.ZipFile(io.BytesIO(new))
            assert result.namelist() == archive.namelist()
            for name, data in old_files.items():
                assert result.read(name) == (png if name in NAMES else data), name
            # Preserve the original split boundary and number of parts.
            boundary = max(path.stat().st_size for path in paths)
            chunks = [new[n:n + boundary] for n in range(0, len(new), boundary)]
            assert len(chunks) == len(paths)
            for path, chunk in zip(paths, chunks):
                path.write_bytes(chunk)
                part = next(p for p in doc["parts"] if p["filename"] == path.name)
                part.update(bytes=len(chunk), sha256=sha(chunk))
                touched[path.name] = sha(chunk)
            package.update(bytes=len(new), sha256=sha(new))
            evidence.append(dict(catalog=suffix or "production", style=style,
                                 changed_pngs=changed, verified_pngs=sorted(NAMES),
                                 png_sha256=sha(png), package_sha256=sha(new)))
        assert len([p for p in doc["packages"] if p["selector_id"] == "235E"]) == 3
        assert [p for p in doc["packages"] if p["selector_id"] != "235E"] == [p for p in before["packages"] if p["selector_id"] != "235E"]
        doc["approved_seznam_235e_update"] = dict(repository="Evolution-by-Warder/PiconHub-Warder-Evolution", ref=SOURCE_REF)
        manifest.write_text(json.dumps(doc, indent=2, sort_keys=True) + "\n")
        sums = base / "SHA256SUMS"
        lines = []
        for line in sums.read_text().splitlines():
            digest, name = line.split(None, 1)
            name = name.lstrip(" *")
            lines.append(f"{touched.get(name, digest)}  {name}")
        sums.write_text("\n".join(lines) + "\n")
    report = ROOT / "reports/seznam-235e-approved-update-20261021.json"
    report.parent.mkdir(exist_ok=True)
    report.write_text(json.dumps(evidence, indent=2, sort_keys=True) + "\n")
    print(json.dumps(evidence, indent=2))


if __name__ == "__main__":
    main()
