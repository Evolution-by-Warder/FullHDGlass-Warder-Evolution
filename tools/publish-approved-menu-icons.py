#!/usr/bin/env python3
"""Publish only the five user-approved Warder menu motifs into menuIconsBig.\nSparse-checkout compatible; prior stable archive is retained for rollback.\nProduction upload triggers the isolated sparse publisher.\n"""
import hashlib
import io
import json
import pathlib
import urllib.request
import zipfile

ROOT = pathlib.Path(__file__).resolve().parents[1]
CATALOG = ROOT / "assets/warder/downloads.json"
SRC = "https://raw.githubusercontent.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/main/assets/warder/downloads/ui/menu-icons-big/menuIconsBig.zip.parts/FINAL-221/"
OUT = ROOT / "assets/warder/downloads/ui/menu-icons-big/menuIconsBig.zip.parts/FINAL-WARDER-AUDITED-20261117"
PREFIX = "https://raw.githubusercontent.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/main/assets/warder/downloads/ui/menu-icons-big/menuIconsBig.zip.parts/FINAL-WARDER-AUDITED-20261117/"
BASE_HASH = "83f65a74001189e0febdd8ed988f3d607782ac36ca0d49b9dfc2890c9fddb3c1"
# One approved image per exact intended filename; no speculative aliases.
# The PiconHub graphic is retained under its owner-approved filename, but
# PiconHub only registers WHERE_PLUGINMENU (not WHERE_MENU).
# FullHDGlass menu shortcut IDs are configurable, while the setup asset is
# already part of the baseline and is replaced with its approved graphic.
APPROVED_NAMES = {
    "warder_gsu": "glass_sys_utils",
    "warder_piconhub": "PiconHub_Warder_Evolution",
    "warder_radio": "warder_radio_mainmenu",
    "warder_youtube": "warder_youtube_mainmenu",
    "warder_skin": "FHD_Glass17_Setup",
}


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def main():
    # Reassemble the already published, SHA-verified stable predecessor.
    base = bytearray()
    for i in range(86):
        url = SRC + "part%03d" % i
        with urllib.request.urlopen(url, timeout=60) as response:
            base.extend(response.read())
    assert sha256(base) == BASE_HASH, "Production baseline changed; refusing to publish"

    entries = {}
    with zipfile.ZipFile(io.BytesIO(base), "r") as old:
        assert old.testzip() is None, "Original ZIP CRC invalid"
        for info in old.infolist():
            if not info.is_dir():
                entries[info.filename] = old.read(info.filename)
    assert len(entries) == 125, "Unexpected original icon count"

    for original, name in APPROVED_NAMES.items():
        data = (ROOT / "assets/warder/menu-icon-overrides" / (original + ".png")).read_bytes()
        assert data.startswith(bytes((137, 80, 78, 71, 13, 10, 26, 10))), original + " is not a PNG"
        width = int.from_bytes(data[16:20], "big")
        height = int.from_bytes(data[20:24], "big")
        assert (width, height) == (810, 810), original + " has incorrect dimensions"
        entries["menuIconsBig/" + name + ".png"] = data

    assert len(entries) == 129, "Unexpected resulting PNG count"
    out_buffer = io.BytesIO()
    with zipfile.ZipFile(out_buffer, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=6) as new:
        for name, data in sorted(entries.items()):
            new.writestr(name, data)
    archive = out_buffer.getvalue()
    with zipfile.ZipFile(io.BytesIO(archive)) as check:
        assert check.testzip() is None and len(check.namelist()) == 129

    OUT.mkdir(parents=True, exist_ok=True)
    # The new destination is uniquely named. Never delete the old FINAL-221.
    paths = []
    for i, start in enumerate(range(0, len(archive), 750000)):
        name = "part%03d" % i
        (OUT / name).write_bytes(archive[start:start + 750000])
        paths.append(PREFIX + name)

    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    item = catalog["assets"]["menuiconsbig"] if "assets" in catalog else catalog["menuiconsbig"]
    item["filename"] = "menuIconsBig.zip"
    item["size"] = len(archive)
    item["sha256"] = sha256(archive)
    item["root"] = "menuIconsBig"
    item["parts"] = paths
    item["png_count"] = 129
    item["release_label"] = "owner-approved-exact-menu-ids-20261117"
    CATALOG.write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + chr(10), encoding="utf-8")
    print("Published", len(entries), "icons,", len(archive), "bytes,", len(paths), "parts; sha256", sha256(archive))


if __name__ == "__main__":
    main()
