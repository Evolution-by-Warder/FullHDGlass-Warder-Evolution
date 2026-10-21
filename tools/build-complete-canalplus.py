#!/usr/bin/env python3
"""Publish complete existing FastScan PNG sets, preserving each source byte."""
import copy
import hashlib
import io
import json
from pathlib import Path
import struct
import zipfile

ROOT = Path(__file__).resolve().parents[1]
SOURCE_REF = "21868a9d27eeb2feda632788b0452a327e97cb98"
COUNTS = {"sk": 226, "cz": 231}
STYLES = ("transparent", "white", "black")
BASE = "https://raw.githubusercontent.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/"


def sha(data):
    return hashlib.sha256(data).hexdigest()


def main():
    source = ROOT / ".approved-picons/picons/23.5e"
    delivery = ROOT / "assets/warder/downloads/picons/channels"
    candidate = json.loads((delivery / "test-candidate/manifest.json").read_text())
    templates = {p["selector_id"]: copy.deepcopy(p) for p in candidate["packages"]
                 if p["family"] == "channel-black" and p["selector_id"].startswith("CANALPLUS_")}
    packages = []
    payloads = {}
    report = []
    for country, count in COUNTS.items():
        refs = None
        country_data = {}
        for style in STYLES:
            files = sorted((source / ("canal-plus-" + country) / style).glob("*.png"))
            assert len(files) == count, (country, style, len(files))
            names = [p.name for p in files]
            assert refs is None or refs == names, "styles have different service references"
            refs = names
            expected = {p.name: p.read_bytes() for p in files}
            for name, data in expected.items():
                assert data[:8] == b"\x89PNG\r\n\x1a\n"
                assert struct.unpack(">II", data[16:24]) == (220, 132), name
            output = io.BytesIO()
            with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
                for name, data in expected.items():
                    entry = zipfile.ZipInfo(name, date_time=(2026, 10, 21, 0, 0, 0))
                    entry.compress_type = zipfile.ZIP_DEFLATED
                    entry.create_system = 3
                    entry.external_attr = 0o100644 << 16
                    archive.writestr(entry, data)
            data = output.getvalue()
            with zipfile.ZipFile(io.BytesIO(data)) as archive:
                assert archive.namelist() == names
                assert all(archive.read(n) == value for n, value in expected.items())
            selector = "CANALPLUS_" + country.upper()
            filename = "canalplus_%s_%s_220x132.zip" % (country, style)
            package = copy.deepcopy(templates[selector])
            package.update(family="channel-" + style, filename=filename,
                           bytes=len(data), sha256=sha(data), png_count=count,
                           included_references=[n[:-4] for n in names],
                           source_repository="Evolution-by-Warder/PiconHub-Warder-Evolution",
                           source_ref=SOURCE_REF)
            package.pop("parts", None)
            packages.append(package)
            payloads[filename] = data
            country_data[style] = expected
            report.append(dict(selector_id=selector, style=style, png_count=count,
                               sha256=sha(data), bytes=len(data), filename=filename))
        assert country_data["black"] != country_data["transparent"]
        assert country_data["white"] != country_data["transparent"]
    for suffix, branch in (("", "main"), ("test-candidate", "warder-modernization-work")):
        directory = delivery / suffix
        path = directory / "manifest.json"
        doc = json.loads(path.read_text())
        unchanged = [p for p in doc["packages"] if not p["selector_id"].startswith("CANALPLUS_")]
        replacement = []
        for template in packages:
            item = copy.deepcopy(template)
            item["url"] = BASE + branch + "/" + directory.relative_to(ROOT).as_posix() + "/" + item["filename"]
            (directory / item["filename"]).write_bytes(payloads[item["filename"]])
            replacement.append(item)
        doc["packages"] = sorted(unchanged + replacement,
                                 key=lambda p: (p["selector_id"], p["family"], p["filename"]))
        assert [p for p in doc["packages"] if not p["selector_id"].startswith("CANALPLUS_")] == sorted(unchanged, key=lambda p: (p["selector_id"], p["family"], p["filename"]))
        doc["complete_canalplus_fastscan_source"] = dict(repository="Evolution-by-Warder/PiconHub-Warder-Evolution", ref=SOURCE_REF)
        path.write_text(json.dumps(doc, indent=2, sort_keys=True) + "\n")
        sums = directory / "SHA256SUMS"
        lines = [line for line in sums.read_text().splitlines() if "canalplus_" not in line]
        lines.extend(f"{sha(data)}  {name}" for name, data in payloads.items())
        sums.write_text("\n".join(sorted(lines, key=lambda line: line.split()[-1])) + "\n")
    report_path = ROOT / "reports/canalplus-complete-fastscan-20261021.json"
    report_path.parent.mkdir(exist_ok=True)
    report_path.write_text(json.dumps(dict(source_ref=SOURCE_REF, packages=report), indent=2, sort_keys=True) + "\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
