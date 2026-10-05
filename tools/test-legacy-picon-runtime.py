#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PKG = ROOT / "source/package-root"
PLUGIN = (PKG / "usr/lib/enigma2/python/Plugins/Extensions/setupGlass17/plugin.py").read_text(encoding="utf-8")
CATALOG = json.loads((PKG / "usr/lib/enigma2/python/Plugins/Extensions/setupGlass17/legacyPiconArchives.json").read_text(encoding="utf-8"))
PREFIX = "https://raw.githubusercontent.com/Evolution-by-Warder/Trezor/9cdda4ab414e7d50a97ca9285db8ebbb75fba615/archives/chocholousek-picons/originals/"

assert CATALOG["schema"] == 1
assert CATALOG["source"]["repository"] == "Evolution-by-Warder/Trezor"
assert CATALOG["source"]["commit"] == "9cdda4ab414e7d50a97ca9285db8ebbb75fba615"
assert CATALOG["source"]["path"] == "archives/chocholousek-picons/originals"
assert CATALOG["mapped"] == 370 and CATALOG["unmapped"] == 29
assert CATALOG["policy"]["preserve_legacy_ids"] is True
assert CATALOG["policy"]["guess_missing"] is False
assert CATALOG["policy"]["picon_cz_fallback"] is False
assert len(CATALOG["archives"]) == 370
assert len(CATALOG["unresolved"]) == 29
expected_unresolved = {
    "2096","3626","1757","1305","4258","4006","1161",
    "2018","3558","1675","1228","4190","3938","1077",
    "2120",
    "2124","3650","1785","1332","4282","4030","1188",
    "2131","3656","1792","1339","4288","4036","1195",
}
assert {x["legacy_id"] for x in CATALOG["unresolved"]} == expected_unresolved
assert not (set(CATALOG["archives"]) & expected_unresolved)
assert all(x["url"].rsplit("/", 1)[-1] == x["filename"] for x in CATALOG["archives"].values())
assert all("/" not in x["filename"] and "\\" not in x["filename"] and ".." not in x["filename"] for x in CATALOG["archives"].values())
assert all(x["url"] == PREFIX + x["filename"] for x in CATALOG["archives"].values())
assert all(x["url"].startswith(PREFIX) and x["url"].endswith(".7z") for x in CATALOG["archives"].values())
assert not any("picon.cz" in x["url"] for x in CATALOG["archives"].values())
assert len({x["legacy_id"] for x in CATALOG["unresolved"]}) == 29
assert "def _legacyPiconArchiveUrl(self, legacy_id):" in PLUGIN
assert "url = self._legacyPiconArchiveUrl(k[x][1])" in PLUGIN
assert 'catalog.get("mapped") == 370' in PLUGIN
assert 'catalog.get("unmapped") == 29' in PLUGIN
assert 'catalog.get("source", {}).get("commit") == "9cdda4ab414e7d50a97ca9285db8ebbb75fba615"' in PLUGIN
assert 'self._warderLegacyPiconArchives = catalog.get("archives", {}) if valid else {}' in PLUGIN
down_multi = PLUGIN.split("def downMulti(self, k, Ddir):", 1)[1].split("\n\tdef ", 1)[0]
assert "https://picon.cz/download/%s/" not in down_multi
assert "Preserved legacy archive is not available in Warder migration catalogue" in down_multi
print("Legacy picon runtime migration: PASS (370 pinned, 29 fail-closed)")
