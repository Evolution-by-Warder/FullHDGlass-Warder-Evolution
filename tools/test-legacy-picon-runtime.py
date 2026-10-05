#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PKG = ROOT / "source/package-root"
PLUGIN = (PKG / "usr/lib/enigma2/python/Plugins/Extensions/setupGlass17/plugin.py").read_text(encoding="utf-8")
CATALOG = json.loads((PKG / "usr/lib/enigma2/python/Plugins/Extensions/setupGlass17/legacyPiconArchives.json").read_text(encoding="utf-8"))
PREFIX = "https://raw.githubusercontent.com/Evolution-by-Warder/Trezor/9cdda4ab414e7d50a97ca9285db8ebbb75fba615/archives/chocholousek-picons/originals/"

assert CATALOG["schema"] == 1
assert CATALOG["mapped"] == 370 and CATALOG["unmapped"] == 29
assert CATALOG["policy"]["preserve_legacy_ids"] is True
assert CATALOG["policy"]["guess_missing"] is False
assert CATALOG["policy"]["picon_cz_fallback"] is False
assert len(CATALOG["archives"]) == 370
assert len(CATALOG["unresolved"]) == 29
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
