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
assert m.runtime_publication()["persistent"] is False
assert m.runtime_publication()["manifest_url"] is None
assert m.safe_archive_member("1_0_1_A_B_C_D_0_0_0.png") is True
assert m.safe_archive_member("../escape.png") is False
assert m.safe_archive_member("/absolute.png") is False
assert m.selector_id("(0.8W) Freesat") == "FREESAT"
assert m.selector_id("(0.8W) Digi / Telly") == "DIGI_TELLY"
assert m.selector_id("(0.8W) Thor 5,6,7/Intelsat 10-02") == "08W"
assert m.selector_id("(23.5E) Skylink") == "SKYLINK"
assert m.selector_id("(23.5E) Astra 3B") == "235E"

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
    filtered = m.build_sync_request(d, ["23.5e"], "transparent", "220x132")
    assert all(x["position"] == "23.5e" for x in filtered["services"])

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
assert "token = label" in plugin_source
assert 'self._setWarderPiconPrepared("wp-pos")' in plugin_source
assert "self._setWarderPiconPrepared(self.warderChoiceRow)" in plugin_source
assert "warderPiconSync.build_runtime_queue(self.warderPiconPrefs, publication=warderPiconSync.runtime_publication())" in plugin_source
assert "warderPiconSync.PUBLICATION_LOCKED" in plugin_source
assert "_warderFetchChannelJob" in plugin_source
assert "_warderInstallChannelArchive" in plugin_source
assert "os.replace(tmp, os.path.join(dest, name))" in plugin_source
assert "def _warderLoadChannelManifest" in plugin_source
assert "def _warderRunChannelQueue" in plugin_source
assert 'self.dwnJob = _("Warder channel picons")' in plugin_source
assert "self.warderChannelInstalled.update(installed)" in plugin_source
assert "missing_files = sorted(wanted - installed_set)" in plugin_source
assert '_("Missing upstream:")' in plugin_source
assert "self.dwnTimer.start(10)" not in plugin_source
assert "self.dwnTimer.start(25, True)" in plugin_source
assert 'return _("ERROR") + ": " + _("Missing upstream:")' in plugin_source
assert 'self.warderChannelState = "idle"' in plugin_source
assert 'self.warderChannelState = "running"' in plugin_source
assert 'self.warderChannelState = "error"' in plugin_source
assert "shutil.disk_usage(destination)" in plugin_source
assert "unsafe Warder picon ZIP compression ratio" in plugin_source
assert "invalid Warder channel part size" in plugin_source
assert "oversized Warder channel download" in plugin_source
assert 'legacy_pending = any(self.menuListAll[x][4] == "d" and self.menuListAll[x][0] not in self.warderPiconRows for x in self.menuListAll)' in plugin_source
assert 'self.warderChannelState = "locked"' in plugin_source
assert 'if self.warderChannelState != "locked":' in plugin_source
assert 'if self.menuListAll[x][4] == "d" and self.menuListAll[x][0] not in self.warderPiconRows:' in plugin_source
assert 'self.warderPiconPrefs.get("prepared") and self.warderChannelState not in ("locked", "error")' in plugin_source
assert '("done", "error", "locked")' in plugin_source
error_branch = plugin_source[plugin_source.index("except Exception as err:", plugin_source.index("def dwnLoop")):plugin_source.index("\n\t\t\t\telse:", plugin_source.index("except Exception as err:", plugin_source.index("def dwnLoop")))]
assert 'self.warderPiconPrefs["prepared"] = False' not in error_branch
assert 'self.menuListAll[row][4] = "x"' not in error_branch
missing_branch = plugin_source[plugin_source.index("if missing_files:"):plugin_source.index('return _("SUCCESSFUL")', plugin_source.index("if missing_files:"))]
assert 'self.warderChannelState = "error"' in missing_branch
assert 'self.warderPiconPrefs["prepared"] = False' not in missing_branch
assert 'self.warderPiconPrefs["prepared"] = False' in plugin_source
assert 'self.warderChannelState = "done"' in plugin_source
assert 'no TV bouquet services found for Warder selective sync' in plugin_source
assert ".is_dir()" not in plugin_source[plugin_source.index("def _warderInstallChannelArchive"):plugin_source.index("def downMulti")]

with tempfile.TemporaryDirectory() as d:
    with open(os.path.join(d, "bouquets.tv"), "w") as h:
        h.write('#SERVICE 1:7:1:0:0:0:0:0:0:0:FROM BOUQUET "userbouquet.q.tv" ORDER BY bouquet\n')
    with open(os.path.join(d, "userbouquet.q.tv"), "w") as h:
        h.write("#SERVICE 1:0:1:1328:CA2:3:EB0000:0:0:0:\n")
        h.write("#SERVICE 1:0:1:1:1:1:C00000:0:0:0:\n")
    locked = m.build_runtime_queue(m.set_preference(m.default_preferences(), "positions", ["(23.5E) Skylink"]), d)
    assert locked["state"] == m.PUBLICATION_LOCKED
    assert locked["service_count"] == 1
    assert locked["services"][0]["position"] == "23.5e"
    ready = m.build_runtime_queue(m.default_preferences(), d, {"persistent": True, "manifest_url": "https://example.invalid/manifest.json"})
    assert ready["state"] == m.READY
    full = m.build_runtime_queue(m.set_preference(m.default_preferences(), "update_mode", "full"), d)
    assert full["mode"] == "full" and full["service_count"] == 0
    assert m.wanted_picon_names(full) is None
    wanted = m.wanted_picon_names(locked)
    assert wanted == {"1_0_1_1328_CA2_3_EB0000_0_0_0.png"}

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

valid_manifest = {
    "schema": 1,
    "generated_from": {"repository": "Evolution-by-Warder/PiconHub-Warder-Evolution", "ref": "2827fed5"},
    "delivery": "raw-github-parts",
    "packages": [{
        "selector_id": "235E", "family": "channel-transparent", "warder_key": "23.5e",
        "filename": "235E-transparent.zip", "resolution": "220x132", "bytes": 10, "sha256": "a" * 64,
        "parts": ["https://raw.githubusercontent.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/main/assets/warder/downloads/picons/channels/235E-transparent.zip.part00"],
    }],
    "parts": [{"filename": "235E-transparent.zip.part00", "bytes": 10, "sha256": "b" * 64}],
}
manifest_errors = m.validate_publication_manifest(valid_manifest)
assert manifest_errors == [], manifest_errors
sel = m.select_manifest_packages(valid_manifest, m.set_preference(m.default_preferences(), "positions", ["(23.5E) Astra 3B"]))
assert sel["state"] == "ready" and sel["selector_ids"] == ["235E"]
assert sel["packages"][0]["selector_id"] == "235E"
wrong_res = m.select_manifest_packages(valid_manifest, m.set_preference(m.default_preferences(), "resolution", "400x240"))
assert wrong_res["packages"] == []
provider_manifest = dict(valid_manifest)
provider_manifest["packages"] = [dict(valid_manifest["packages"][0], selector_id="FREESAT", warder_key="0.8w/freesat")]
provider_sel = m.select_manifest_packages(provider_manifest, m.set_preference(m.default_preferences(), "positions", ["(0.8W) Freesat"]))
assert provider_sel["selector_ids"] == ["FREESAT"] and len(provider_sel["packages"]) == 1
wrong_provider = m.select_manifest_packages(provider_manifest, m.set_preference(m.default_preferences(), "positions", ["(0.8W) Digi / Telly"]))
assert wrong_provider["state"] == "partial" and wrong_provider["missing_selectors"] == ["DIGI_TELLY"]
queue = {
    "mode": m.UPDATE_MODE_SYNC_TV, "positions_labels": [], "selector_ids": [],
    "style": "transparent", "resolution": "220x132",
    "services": [{"service_reference": "1_0_1_1328_CA2_3_EB0000_0_0_0", "position": "23.5e"}],
}
planned = m.plan_runtime_packages(valid_manifest, queue)
assert planned["state"] == "ready" and [p["selector_id"] for p in planned["packages"]] == ["235E"]
full_queue = dict(queue, mode=m.UPDATE_MODE_FULL, services=[])
full_planned = m.plan_runtime_packages(valid_manifest, full_queue)
assert len(full_planned["packages"]) == 1
empty_sync_queue = dict(queue, services=[], positions_labels=[], selector_ids=[])
empty_sync_planned = m.plan_runtime_packages(valid_manifest, empty_sync_queue)
assert empty_sync_planned["state"] == "ready" and empty_sync_planned["packages"] == []
assert m.build_download_jobs(valid_manifest, empty_sync_planned)["jobs"] == []
full_selected = dict(full_queue, positions_labels=["(23.5E) Astra 3B"], selector_ids=["235E"])
full_selected_planned = m.plan_runtime_packages(valid_manifest, full_selected)
assert [p["selector_id"] for p in full_selected_planned["packages"]] == ["235E"]
provider_queue = dict(queue, positions_labels=["(0.8W) Freesat"], selector_ids=["FREESAT"],
                      services=[{"service_reference": "1", "position": "0.8w"}])
provider_planned = m.plan_runtime_packages(provider_manifest, provider_queue)
assert [p["selector_id"] for p in provider_planned["packages"]] == ["FREESAT"]
jobs = m.build_download_jobs(valid_manifest, planned)
assert jobs["state"] == "ready" and len(jobs["jobs"]) == 1
assert jobs["jobs"][0]["bytes"] == 10 and jobs["jobs"][0]["sha256"] == "a" * 64
assert jobs["jobs"][0]["parts"][0]["bytes"] == 10
assert jobs["jobs"][0]["parts"][0]["sha256"] == "b" * 64
assert m.validate_destination("/media/hdd/picon") == "/media/hdd/picon"
assert m.validate_destination("relative/picon") is None
assert m.validate_destination("/") is None
pub = m.publication_from_manifest("https://raw.githubusercontent.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/main/assets/warder/downloads/picons/channels/manifest.json", valid_manifest)
assert pub["persistent"] is True and not pub["errors"]
bad = dict(valid_manifest)
bad["packages"] = [dict(valid_manifest["packages"][0])]
bad["packages"][0]["parts"] = ["https://evil.example/payload.part00"]
assert "untrusted part url" in m.validate_publication_manifest(bad)
bad_sha = dict(valid_manifest)
bad_sha["packages"] = [dict(valid_manifest["packages"][0], sha256="xyz")]
assert "invalid package sha256" in m.validate_publication_manifest(bad_sha)
assert m.publication_from_manifest("http://raw.githubusercontent.com/x/manifest.json", valid_manifest)["persistent"] is False
assert m.publication_from_manifest("https://raw.githubusercontent.com/Other/repo/main/assets/warder/downloads/picons/channels/manifest.json", valid_manifest)["persistent"] is False
assert m.publication_from_manifest("https://raw.githubusercontent.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/warder-modernization-work/assets/warder/downloads/picons/channels/manifest.json", valid_manifest)["persistent"] is False
duplicate = dict(valid_manifest)
duplicate["packages"] = [dict(valid_manifest["packages"][0]), dict(valid_manifest["packages"][0])]
assert "duplicate selector/family/resolution" in m.validate_publication_manifest(duplicate)
duplicate_part = dict(valid_manifest)
duplicate_part["packages"] = [dict(valid_manifest["packages"][0], parts=[
    valid_manifest["packages"][0]["parts"][0], valid_manifest["packages"][0]["parts"][0]])]
assert "duplicate package part" in m.validate_publication_manifest(duplicate_part)

print("Warder picon sync parser/planner/runtime-lock/manifest/collision/GUI wiring: PASS")
