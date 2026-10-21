#!/usr/bin/env python3
"""Copy the seven approved 23.5E black PNGs into both Canal+ packages."""
import copy
import hashlib
import io
import json
from pathlib import Path
import zipfile

ROOT = Path(__file__).resolve().parents[1]
SOURCE_REF = "31143f35ee537a9b7b1eaad766331cda71dc0c38"


def sha(data):
    return hashlib.sha256(data).hexdigest()


def main():
    source = ROOT / ".approved-picons"
    approval = json.loads((source / "migration/canalplus-approved-black-seven-20261022/manifest.json").read_text())
    rows = approval["picons"]
    assert len(rows) == 7 and approval["style"] == "black"
    report = []
    for suffix in ("", "test-candidate"):
        directory = ROOT / "assets/warder/downloads/picons/channels" / suffix
        manifest = directory / "manifest.json"
        doc = json.loads(manifest.read_text())
        before = copy.deepcopy(doc)
        sums = directory / "SHA256SUMS"
        checksums = {line.split()[-1]: line.split()[0] for line in sums.read_text().splitlines()}
        changed = 0
        for package in doc["packages"]:
            if package["selector_id"] not in ("CANALPLUS_SK", "CANALPLUS_CZ") or package["family"] != "channel-black":
                continue
            country = package["selector_id"][-2:].lower()
            old_path = directory / package["filename"]
            old = old_path.read_bytes()
            assert sha(old) == package["sha256"] and len(old) == package["bytes"]
            original = zipfile.ZipFile(io.BytesIO(old))
            old_files = {name: original.read(name) for name in original.namelist()}
            approved = {}
            for row in rows:
                name = row["filename"]
                png = (source / "picons/23.5e" / ("canal-plus-" + country) / "black" / name).read_bytes()
                assert sha(png) == row["sha256"], (country, name)
                approved[name] = png
            output = io.BytesIO()
            with zipfile.ZipFile(output, "w") as archive:
                archive.comment = original.comment
                for entry in original.infolist():
                    archive.writestr(entry, approved.get(entry.filename, old_files[entry.filename]))
                for name in sorted(approved.keys() - old_files.keys()):
                    entry = zipfile.ZipInfo(name, date_time=(2026, 10, 22, 0, 0, 0))
                    entry.compress_type = zipfile.ZIP_DEFLATED
                    entry.create_system = 3
                    entry.external_attr = 0o100644 << 16
                    archive.writestr(entry, approved[name])
            data = output.getvalue()
            result = zipfile.ZipFile(io.BytesIO(data))
            assert set(result.namelist()) == old_files.keys() | approved.keys()
            for name in result.namelist():
                assert result.read(name) == (approved[name] if name in approved else old_files[name])
            assert len(result.namelist()) == (228 if country == "sk" else 231)
            filename = "canalplus_%s_black_220x132_%s.zip" % (country, sha(data)[:16])
            (directory / filename).write_bytes(data)
            package.update(filename=filename, bytes=len(data), sha256=sha(data),
                           png_count=len(result.namelist()),
                           included_references=sorted(n[:-4] for n in result.namelist()),
                           source_ref=SOURCE_REF)
            package["url"] = package["url"].rsplit("/", 1)[0] + "/" + filename
            checksums[filename] = sha(data)
            report.append(dict(catalog=suffix or "production", country=country,
                               filename=filename, png_count=len(result.namelist()), sha256=sha(data),
                               replaced=sorted(approved.keys() & old_files.keys()),
                               added=sorted(approved.keys() - old_files.keys()),
                               verified_approved_pngs={n: sha(v) for n, v in approved.items()}))
            changed += 1
        assert changed == 2
        untouched = lambda d: [p for p in d["packages"] if not (p["selector_id"] in ("CANALPLUS_SK", "CANALPLUS_CZ") and p["family"] == "channel-black")]
        assert untouched(doc) == untouched(before)
        doc["approved_canalplus_seven_black_source"] = dict(repository="Evolution-by-Warder/PiconHub-Warder-Evolution", ref=SOURCE_REF)
        manifest.write_text(json.dumps(doc, indent=2, sort_keys=True) + "\n")
        sums.write_text("\n".join(f"{digest}  {name}" for name, digest in sorted(checksums.items())) + "\n")
    path = ROOT / "reports/canalplus-seven-black-approved-20261022.json"
    path.parent.mkdir(exist_ok=True)
    path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
