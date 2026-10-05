#!/usr/bin/env python3
import importlib.util
import os
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODULE = os.path.join(ROOT, "source/package-root/usr/lib/enigma2/python/Plugins/Extensions/setupGlass17/warderPiconSync.py")
spec = importlib.util.spec_from_file_location("warderPiconSync", MODULE)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

assert m.normalize_service_reference("1:0:1:1328:CA2:3:EB0000:0:0:0:") == "1_0_1_1328_CA2_3_EB0000_0_0_0"
assert m.normalize_service_reference("#SERVICE 1:0:1:1328:CA2:3:EB0000:0:0:0:") == "1_0_1_1328_CA2_3_EB0000_0_0_0"
assert m.normalize_service_reference("garbage") == ""
assert m.service_orbital_position("1:0:1:1328:CA2:3:EB0000:0:0:0:") == "23.5e"
assert m.service_orbital_position("1:0:1:1:1:1:C00000:0:0:0:") == "19.2e"
assert m.position_token("(23.5E) Skylink") == "23.5e"
assert m.position_token("(0.8W) Freesat") == "0.8w"
assert m.position_token("DVB-T sk/cz") == "dtt"
assert m.position_token("19.2e") == "19.2e"

with tempfile.TemporaryDirectory() as d:
    with open(os.path.join(d, "bouquets.tv"), "w") as h:
        h.write('#SERVICE 1:7:1:0:0:0:0:0:0:0:FROM BOUQUET "userbouquet.warder.tv" ORDER BY bouquet\n')
    with open(os.path.join(d, "userbouquet.warder.tv"), "w") as h:
        h.write("#NAME Warder test\n")
        h.write("#SERVICE 1:0:1:1328:CA2:3:EB0000:0:0:0:\n")
        h.write("#DESCRIPTION Skylink sample\n")
        h.write("#SERVICE 1:0:1:1:1:1:C00000:0:0:0:\n")
        h.write("#SERVICE 1:0:1:1328:CA2:3:EB0000:0:0:0:\n")
    refs = m.bouquet_services(d)
    assert refs == [
        "1_0_1_1328_CA2_3_EB0000_0_0_0",
        "1_0_1_1_1_1_C00000_0_0_0",
    ]
    req = m.build_sync_request(d, ["23.5e"], "transparent", "220x132")
    assert req["mode"] == "sync-tv-lists"
    assert [x["service_reference"] for x in req["services"]] == ["1_0_1_1328_CA2_3_EB0000_0_0_0"]
    assert req["services"][0]["position"] == "23.5e"

prefs = m.default_preferences("/media/hdd/picon")
assert prefs["update_mode"] == "sync-tv-lists"
assert prefs["style"] == "transparent"
assert prefs["resolution"] == "220x132"
assert prefs["prepared"] is False
assert m.has_executable_action(prefs) is False
prefs = m.set_preference(prefs, "style", "black")
assert prefs["prepared"] is True
assert m.has_executable_action(prefs) is True
assert m.has_executable_action(m.default_preferences(), ordinary_selected=True) is True
assert [x[0] for x in m.UPDATE_MODES] == ["sync-tv-lists", "full"]
prefs2 = m.set_preference(m.default_preferences(), "positions", ["(23.5E) Skylink", "DVB-T sk/cz"])
assert prefs2["positions"] == ["(23.5E) Skylink", "DVB-T sk/cz"]
assert prefs2["prepared"] is True

PLUGIN = os.path.join(ROOT, "source/package-root/usr/lib/enigma2/python/Plugins/Extensions/setupGlass17/plugin.py")
with open(PLUGIN, "r") as h:
    plugin_source = h.read()
menu_start = plugin_source.index("\t\tself.menuListAll = {", plugin_source.index("class downloadMenu"))
menu_end = plugin_source.index("\n\t\t\t}", menu_start)
menu_block = plugin_source[menu_start:menu_end]
keys = [int(x) for x in __import__("re").findall(r"^\t\t\t(\d+):\[", menu_block, __import__("re").M)]
assert keys == list(range(len(keys))), keys
assert "warderPiconSync.position_token(label)" in plugin_source
assert 'self._setWarderPiconPrepared("wp-pos")' in plugin_source
assert "self._setWarderPiconPrepared(self.warderChoiceRow)" in plugin_source
assert "warderPiconSync.build_runtime_queue(self.warderPiconPrefs)" in plugin_source
assert "warderPiconSync.PUBLICATION_LOCKED" in plugin_source

with tempfile.TemporaryDirectory() as d:
    with open(os.path.join(d, "bouquets.tv"), "w") as h:
        h.write('#SERVICE 1:7:1:0:0:0:0:0:0:0:FROM BOUQUET "userbouquet.q.tv" ORDER BY bouquet\\n')
    with open(os.path.join(d, "userbouquet.q.tv"), "w") as h:
        h.write("#SERVICE 1:0:1:1328:CA2:3:EB0000:0:0:0:\\n")
        h.write("#SERVICE 1:0:1:1:1:1:C00000:0:0:0:\\n")
    locked = m.build_runtime_queue(m.set_preference(m.default_preferences(), "positions", ["(23.5E) Skylink"]), d)
    assert locked["state"] == m.PUBLICATION_LOCKED
    assert locked["service_count"] == 1
    assert locked["services"][0]["position"] == "23.5e"
    ready = m.build_runtime_queue(m.default_preferences(), d, {"persistent": True, "manifest_url": "https://example.invalid/manifest.json"})
    assert ready["state"] == m.READY
    full = m.build_runtime_queue(m.set_preference(m.default_preferences(), "update_mode", "full"), d)
    assert full["mode"] == "full" and full["service_count"] == 0

entries = [
    {"service_reference": "1:0:1:1328:CA2:3:EB0000:0:0:0:", "package": "a"},
    {"service_reference": "1:0:1:1:1:1:C00000:0:0:0:", "package": "b"},
]
idx, col = m.build_service_index(entries)
assert len(idx) == 2 and not col
assert m.resolve_service_entry(idx, col, entries[0]["service_reference"])["state"] == "matched"
collision_entries = entries + [{"service_reference": "1:0:1:1328:CA2:3:EB0000:0:0:0:", "package": "other"}]
idx, col = m.build_service_index(collision_entries)
assert "1_0_1_1328_CA2_3_EB0000_0_0_0" not in idx
assert m.resolve_service_entry(idx, col, entries[0]["service_reference"])["state"] == "collision-blocked"
assert m.resolve_service_entry(idx, col, "1:0:1:999:1:1:C00000:0:0:0:")["state"] == "missing"

print("Warder picon sync parser/planner/runtime-lock/collision/GUI wiring: PASS")
