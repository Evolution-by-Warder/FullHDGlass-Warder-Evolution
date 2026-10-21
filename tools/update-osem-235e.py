#!/usr/bin/env python3
"""Put the approved Osem PNGs into every full 23.5E colour package."""
import ast
import copy
import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path
import shutil
import stat
import tempfile
import zipfile

ROOT = Path(__file__).resolve().parents[1]
PKG = ROOT / "source/package-root/usr/lib/enigma2/python/Plugins/Extensions/setupGlass17"
SOURCE_REF = "21868a9d27eeb2feda632788b0452a327e97cb98"
APPROVED = {
    "transparent": "221f697e25e469082cfff855e7a71222fd7af85b5c64537342106fe098551687",
    "white": "d5f802a1df6dec2c3de66c547e33df631b07579781b7b08d65403278530d18d8",
    "black": "b0f744945100b31623bf667c26b0fa9b421c14b5afd13d09e8b205b6d558d3a5",
}
NAMES = {f"1_0_{kind}_5318_C96_3_EB0000_0_0_0.png" for kind in ("1", "16")}


def sha(data):
    return hashlib.sha256(data).hexdigest()


def main():
    spec = importlib.util.spec_from_file_location("sync", PKG / "warderPiconSync.py")
    sync = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(sync)
    tree = ast.parse((PKG / "plugin.py").read_bytes())
    method = next(n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef) and n.name == "_warderInstallChannelArchive")
    scope = dict(warderPiconSync=sync, os=os, shutil=shutil, stat=stat, tempfile=tempfile, zipfile=zipfile)
    exec(compile(ast.Module(body=[method], type_ignores=[]), str(PKG / "plugin.py"), "exec"), scope)
    installer = scope["_warderInstallChannelArchive"]
    report = []
    for suffix in ("", "test-candidate"):
        directory = ROOT / "assets/warder/downloads/picons/channels" / suffix
        manifest = directory / "manifest.json"
        doc = json.loads(manifest.read_text())
        before = copy.deepcopy(doc)
        sums = directory / "SHA256SUMS"
        checksums = {line.split()[-1]: line.split()[0] for line in sums.read_text().splitlines()}
        for package in doc["packages"]:
            if package["selector_id"] != "235E":
                continue
            style = package["family"].removeprefix("channel-")
            source = ROOT / ".approved-picons/picons/23.5e/canal-plus-sk" / style
            png = (source / "1_0_16_5318_C96_3_EB0000_0_0_0.png").read_bytes()
            assert sha(png) == APPROVED[style]
            paths = [directory / url.rsplit("/", 1)[1] for url in package["parts"]]
            old = b"".join(path.read_bytes() for path in paths)
            assert len(old) == package["bytes"] and sha(old) == package["sha256"]
            original = zipfile.ZipFile(io.BytesIO(old))
            old_files = {name: original.read(name) for name in original.namelist()}
            assert NAMES & old_files.keys(), "Osem missing from input archive"
            output = io.BytesIO()
            with zipfile.ZipFile(output, "w") as archive:
                archive.comment = original.comment
                for entry in original.infolist():
                    archive.writestr(entry, png if entry.filename in NAMES else old_files[entry.filename])
                for name in sorted(NAMES - old_files.keys()):
                    entry = zipfile.ZipInfo(name, date_time=(2026, 10, 21, 0, 0, 0))
                    entry.compress_type = zipfile.ZIP_DEFLATED
                    entry.create_system = 3
                    entry.external_attr = 0o100644 << 16
                    archive.writestr(entry, png)
            data = output.getvalue()
            result = zipfile.ZipFile(io.BytesIO(data))
            assert set(result.namelist()) == old_files.keys() | NAMES
            for name in result.namelist():
                assert result.read(name) == (png if name in NAMES else old_files[name]), name
            # Exercise replacement with the actual receiver installer.
            with tempfile.TemporaryDirectory() as temp:
                local = Path(temp) / "archive.zip"
                local.write_bytes(data)
                dest = Path(temp) / "picon"
                dest.mkdir()
                for name in NAMES:
                    (dest / name).write_bytes(b"obsolete")
                installed, available = installer(None, str(local), str(dest))
                assert installed == available == set(result.namelist())
                assert all((dest / name).read_bytes() == png for name in NAMES)
            filename = "warder-235e-channel-%s-%s.zip" % (style, sha(data)[:16])
            url_root = package["parts"][0].rsplit("/", 1)[0] + "/"
            parts = []
            records = []
            for number, start in enumerate(range(0, len(data), 18 * 1024 * 1024)):
                part_name = filename + ".part%02d" % number
                chunk = data[start:start + 18 * 1024 * 1024]
                (directory / part_name).write_bytes(chunk)
                parts.append(url_root + part_name)
                records.append(dict(filename=part_name, bytes=len(chunk), sha256=sha(chunk)))
                checksums[part_name] = sha(chunk)
            old_part_names = {path.name for path in paths}
            doc["parts"] = [p for p in doc["parts"] if p["filename"] not in old_part_names] + records
            package.update(filename=filename, bytes=len(data), sha256=sha(data), parts=parts,
                           png_count=len(result.namelist()))
            if "included_references" in package:
                package["included_references"] = sorted(name[:-4] for name in result.namelist())
            report.append(dict(catalog=suffix or "production", style=style, png_count=len(result.namelist()),
                               filename=filename, package_sha256=sha(data), png_sha256=sha(png),
                               replaced=[n for n in sorted(NAMES & old_files.keys()) if old_files[n] != png],
                               added=sorted(NAMES - old_files.keys())))
        assert [p for p in doc["packages"] if p["selector_id"] != "235E"] == [p for p in before["packages"] if p["selector_id"] != "235E"]
        doc["approved_osem_235e_source"] = dict(repository="Evolution-by-Warder/PiconHub-Warder-Evolution", ref=SOURCE_REF)
        source_id = "production" if not suffix else "test-candidate"
        assert not sync.validate_publication_manifest(doc, source_id)
        manifest.write_text(json.dumps(doc, sort_keys=True, indent=2) + "\n")
        sums.write_text("\n".join(f"{digest}  {name}" for name, digest in sorted(checksums.items())) + "\n")
    path = ROOT / "reports/osem-235e-approved-update-20261021.json"
    path.parent.mkdir(exist_ok=True)
    path.write_text(json.dumps(report, sort_keys=True, indent=2) + "\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
