#!/usr/bin/env python3
"""Targeted TEST198 contract for choices, destinations, update semantics and reset."""
import ast
import importlib.util
import json
import os
import tempfile
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
PKG = ROOT / "source/package-root"
PLUGIN = PKG / "usr/lib/enigma2/python/Plugins/Extensions/setupGlass17/plugin.py"
SYNC = PKG / "usr/lib/enigma2/python/Plugins/Extensions/setupGlass17/warderPiconSync.py"
CATALOG = ROOT / "assets/warder/downloads.json"
spec = importlib.util.spec_from_file_location("warderPiconSync_test196", str(SYNC))
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
source = PLUGIN.read_text(encoding="utf-8")
sync_source = SYNC.read_text(encoding="utf-8")

# A new session begins without implicit channel resolution, color, or update mode.
prefs = m.default_preferences()
assert prefs["positions"] == []
assert prefs["package_selectors"] == [] and prefs["position_bindings"] == []
assert prefs["resolution"] is None and prefs["style"] is None and prefs["update_mode"] is None
assert prefs["destination"] == "/usr/share/enigma2/picon"
assert not m.channel_preferences_ready(prefs)
assert m.reset_working_preferences({"positions": ["SKYLINK"]}) == m.default_preferences()
assert m.channel_style_supported("220x132", "transparent")
assert m.channel_style_supported("220x132", "black") and m.channel_style_supported("220x132", "white")
assert m.channel_style_supported("50x30", "black") and m.channel_style_supported("50x30", "white")
assert not m.channel_style_supported("50x30", "transparent")
assert m.channel_style_supported("400x240", "transparent")
assert [x[0] for x in m.CHANNEL_RESOLUTION_CHOICES] == ["50x30", "220x132", "400x240"]
assert "150x90" not in [x[0] for x in m.CHANNEL_RESOLUTION_CHOICES]
assert "710 x 682" in source and '("large-selection", "CHSPiconbig")' in source

# Each update mode has distinct bouquet and install semantics while staying scoped to chosen orbits.
with tempfile.TemporaryDirectory() as tmp:
    root = Path(tmp)
    (root / "bouquets.tv").write_text('#SERVICE 1:7:1:0:0:0:0:0:0:0:FROM BOUQUET "tv.userbouquet" ORDER BY bouquet\n')
    (root / "bouquets.radio").write_text('#SERVICE 1:7:1:0:0:0:0:0:0:0:FROM BOUQUET "radio.userbouquet" ORDER BY bouquet\n')
    (root / "tv.userbouquet").write_text("#SERVICE 1:0:1:1328:CA2:3:EB0000:0:0:0:\n#SERVICE 1:0:1:101:1:1:A00000:0:0:0:\n")
    (root / "radio.userbouquet").write_text("#SERVICE 1:0:1:100:1:1:A00000:0:0:0:\n")
    selector_ids = ["SKYLINK", "ANTIKSAT"]
    bindings = [m.task_binding_for_package_selector(x) for x in selector_ids]
    tv = m.build_sync_request(tmp, ["23.5e", "16.0e"], "transparent", "220x132")
    tv_radio = m.build_sync_request(tmp, ["23.5e", "16.0e"], "transparent", "220x132", include_radio=True)
    assert tv["mode"] == m.UPDATE_MODE_SYNC_TV and len(tv["services"]) == 2
    assert tv_radio["mode"] == m.UPDATE_MODE_SYNC_TV_RADIO and len(tv_radio["services"]) == 3
    base = m.set_task_position_bindings({"resolution": "220x132", "style": "transparent", "destination": "/media/hdd/picon", "prepared": True}, bindings)
    queues = {}
    for mode, count in ((m.UPDATE_MODE_SYNC_TV, 2), (m.UPDATE_MODE_SYNC_TV_RADIO, 3),
                        (m.UPDATE_MODE_REPLACE_ALL, 0), (m.UPDATE_MODE_INCREMENTAL, 0)):
        current = dict(base, update_mode=mode)
        queue = m.build_runtime_queue(current, tmp, {"persistent": True, "manifest_url": m.RUNTIME_MANIFEST_URL})
        assert queue["state"] == m.READY and queue["service_count"] == count
        assert set(queue["positions"]) == {"23.5E", "16.0E"}
        assert set(queue["package_selectors"]) == {"SKYLINK", "ANTIKSAT"}
        queues[mode] = queue
    assert m.wanted_picon_names(queues[m.UPDATE_MODE_SYNC_TV]) == {
        "1_0_1_1328_CA2_3_EB0000_0_0_0.png", "1_0_1_101_1_1_A00000_0_0_0.png"}
    assert len(m.wanted_picon_names(queues[m.UPDATE_MODE_SYNC_TV_RADIO])) == 3
    assert m.wanted_picon_names(queues[m.UPDATE_MODE_REPLACE_ALL]) is None
    assert m.wanted_picon_names(queues[m.UPDATE_MODE_INCREMENTAL]) is None
    # No mode can broaden a selected-position set to the entire manifest.
    manifest = {"schema": 1, "generated_from": {"repository": "Evolution-by-Warder/PiconHub-Warder-Evolution", "ref": "a"*40},
        "delivery": "direct", "parts": [], "packages": []}
    for sid, key in (("SKYLINK", "23.5e"), ("ANTIKSAT", "16.0e"), ("192E", "19.2e")):
        manifest["packages"].append({"selector_id": sid, "family": "channel-transparent", "warder_key": key,
            "filename": sid+".zip", "resolution": "220x132", "bytes": 10, "sha256": "a"*64,
            "url": "https://raw.githubusercontent.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/main/assets/warder/downloads/picons/channels/"+sid+".zip"})
    for mode in (m.UPDATE_MODE_REPLACE_ALL, m.UPDATE_MODE_INCREMENTAL):
        plan = m.plan_runtime_packages(manifest, queues[mode])
        assert [p["selector_id"] for p in plan["packages"]] == ["ANTIKSAT", "SKYLINK"]

# Full replace only prunes stale PNG service names for selected satellite positions.
stale_235 = "1_0_1_1328_CA2_3_EB0000_0_0_0.png"
current_235 = "1_0_1_100_1_1_A00000_0_0_0.png"
other_192 = "1_0_1_1_1_1_C00000_0_0_0.png"
assert m.plan_stale_position_picons([stale_235, current_235, other_192, "logo.png"], ["23.5e"], [current_235]) == [stale_235]
assert m.plan_stale_position_picons([stale_235], [], []) == []

# Destination validation accepts only the explicit system picon directory under /usr.
assert m.validate_destination("/usr/share/enigma2/picon") == "/usr/share/enigma2/picon"
assert m.validate_destination("/usr/share/enigma2") is None
assert m.destination_storage_available("/usr/share/enigma2/picon")
real_ismount = m.os.path.ismount
try:
    m.os.path.ismount = lambda path: path == "/media/usb"
    assert not m.destination_storage_available("/media/hdd/picon")
    assert m.destination_storage_available("/media/usb/picon")
finally:
    m.os.path.ismount = real_ismount
with tempfile.TemporaryDirectory() as tmp:
    target = Path(tmp) / "target"
    target.mkdir()
    link = Path(tmp) / "link"
    link.symlink_to(target, target_is_directory=True)
    assert m.validate_destination(str(link)) is None
assert "/media/hdd/picon" in [path for path, _ in m.PICON_DESTINATIONS]
assert "/media/usb/picon" in [path for path, _ in m.PICON_DESTINATIONS]
assert "/media/sdcard/picon" in [path for path, _ in m.PICON_DESTINATIONS]
assert "/media/mmc/picon" in [path for path, _ in m.PICON_DESTINATIONS]
assert "/picon" in [path for path, _ in m.PICON_DESTINATIONS]
assert "dirBrowser" in source and "warderCustomLocationAnswer" in source
assert "Create picon directory?" in source and "Picon destination is not writable" in source
assert "destination_storage_available(destination)" in source
assert '"Selected storage is not mounted"' in source
assert 'not warderPiconSync.channel_style_supported(value, self.warderPiconPrefs["style"])' in source

# Auxiliary options are built fresh from available catalog keys; absent assets are never fabricated.
keys = set(json.loads(CATALOG.read_text(encoding="utf-8"))["assets"])
variants = m.auxiliary_variants(keys)
assert [key for key, _ in variants["piconProv"]] == ["piconProv-220", "piconProv-b", "piconProv-w"]
assert [key for key, _ in variants["piconSat"]] == ["piconSat-220", "piconSat-b", "piconSat-w"]
assert [key for key, _ in variants["piconCam"]] == ["piconCam-b", "piconCam-w"]
assert [key for key, _ in variants["piconWeather"]] == ["piconWeather-b", "piconWeather-w"]
assert "display += \" 220 x 132\"" not in source
assert "lambda *answer: self.warderAuxPiconAnswerFor(row, *answer)" in source

# Success reset is gated on whole-run success. Failures retain the pending choice for retry.
dwn = source[source.index("def dwnLoop(self, txt=\"\")"):source.index("def dwnFin(self, answer=\"\")")]
assert "if self.warderOperationSucceeded and not self.warderOperationFailed:" in dwn
assert "self.resetWarderWorkingState()" in dwn
assert "self.warderFailedRows.add(row)" in source
assert "self.warderFailedRows.add(\"wp-pos\")" in dwn
assert "self.warderOperationFailed = False\n\t\tself.warderFailedRows = set()" in source
assert "def resetWarderWorkingState(self):" in source
assert 'preferences_after_task(self.warderPiconPrefs, "success")' in source
assert "warderPiconSync.success_summary" in source
assert "file(s) downloaded/updated" not in source[source.index("def _warderRunChannelQueue"):source.index("def _warderFetchChannelJob")]
assert "%d picons successfully updated" in sync_source
assert "def package_result_summary(" in sync_source

# Safe no-value/cancel callback contracts and preserved setup import-order fix.
for name in ("warderPositionAnswer", "warderPiconChoiceAnswer", "warderCustomLocationAnswer", "satSelcallback", "cleanAnswerNow"):
    assert name in source
assert "def warderAuxPiconAnswerFor(self, row, *answer):" in source
pos = source.index("class warderPositionSelectorScr(Screen):")
base = source.index("class satSelectorScr(Screen):")
assert base < pos and "skin = satSelectorScr.skin" in source[pos:pos+150]
for callback in ("warderPositionAnswer", "warderPiconChoiceAnswer", "warderCustomLocationAnswer"):
    tree = ast.parse(source)
    matches = [n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef) and n.name == callback]
    assert matches and (matches[0].args.vararg is not None or matches[0].args.defaults)

# Five distinct FullHDGlass icons share the same native 189x123 footprint.
icon_paths = ["down/p4.png", "down/ba5.png", "down/warder-colour.png", "down/warder-location.png", "down/warder-sync.png"]
icon_hashes = set()
for relative in icon_paths:
    path = PKG / "usr/share/enigma2/hd_glass17" / relative
    assert path.is_file(), relative
    with Image.open(path) as image:
        assert image.size == (189, 123), (relative, image.size)
    import hashlib
    icon_hashes.add(hashlib.sha256(path.read_bytes()).hexdigest())
assert len(icon_hashes) == 5
assert '"wp-style": "down/warder-colour.png"' in source
assert '"wp-dest": "down/warder-location.png"' in source
assert '"wp-mode": "down/warder-sync.png"' in source
assert "Provider logos" in source and "Satellite logos" in source
assert "TV platform and service provider logos." in source
assert "Satellite logos and graphical identifiers." in source
assert "ZZPicon-v" not in source

# Main setting names are explicitly present in every supported catalog and Slovak translations match.
sk = (PKG / "usr/lib/enigma2/python/Plugins/Extensions/setupGlass17/locale/sk/LC_MESSAGES/setupGlass17.po").read_text(encoding="utf-8")
for msgid, translation in (("Satellite positions", "Satelitné pozície"), ("Picon resolution", "Rozlíšenie piconov"),
                           ("Picon colour", "Farba piconov"), ("Picon location", "Umiestnenie piconov"),
                           ("Update method", "Metóda aktualizácie"),
                           ("Selected storage is not mounted", "Vybraté úložisko nie je pripojené")):
    assert 'msgid "'+msgid+'"' in sk and 'msgstr "'+translation+'"' in sk
catalogs = list((PKG / "usr/lib/enigma2/python/Plugins/Extensions/setupGlass17/locale").glob("*/LC_MESSAGES/setupGlass17.po"))
assert len(catalogs) == 19
for po in catalogs:
    text = po.read_text(encoding="utf-8")
    assert 'msgid "Update method"' in text and 'msgid "No colour selected"' in text
    for msgid in ("Provider logos", "Satellite logos", "%s / %s: %d picons updated; %d failures", "PARTIAL SUCCESS"):
        assert 'msgid "'+msgid+'"' in text

# Distinct count text is plural-aware by English gettext keys, with no "file(s)" wording.
summary = m.package_result_summary([
    {"selector_id":"160E","orbital_position":"16.0e","updated":198,"failures":0}
])
assert summary["status"] == "SUCCESSFUL" and summary["updated"] == 198 and summary["failures"] == 0
assert "198 picons updated" in summary["text"] and "services selected" not in summary["text"]
channel_queue = source[source.index("def _warderRunChannelQueue"):source.index("def _warderFetchChannelJob")]
assert "package_result_summary" in channel_queue and "coverage[\"outside_selected_packages\"]" not in channel_queue
assert "PARTIAL SUCCESS" in source[source.index("def _recordWarderOperationResult"):source.index("def resetWarderWorkingState")]
assert "down/i.png" not in source[source.index("warder_icons = {"):source.index("for x in self.menuListAll", source.index("warder_icons = {"))]
assert "Set of icons and prewievs" in source

print("TEST196 Warder settings, destinations, update modes, scoped replace, localization, callbacks and icons: PASS")
