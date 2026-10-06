#!/usr/bin/env python3
import hashlib
import importlib.util
import json
import os
import struct
import tempfile
import zipfile
from pathlib import Path

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PKG = Path(ROOT) / "source/package-root"
MODULE = os.path.join(ROOT, "source/package-root/usr/lib/enigma2/python/Plugins/Extensions/setupGlass17/warderPiconSync.py")
spec = importlib.util.spec_from_file_location("warderPiconSync", MODULE)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
with open(MODULE, "r") as h:
    sync_source = h.read()

assert m.normalize_service_reference("1:0:1:1328:CA2:3:EB0000:0:0:0:") == "1_0_1_1328_CA2_3_EB0000_0_0_0"
assert m.normalize_service_reference("1_0_1_1328_CA2_3_EB0000_0_0_0") == "1_0_1_1328_CA2_3_EB0000_0_0_0"
assert m.normalize_service_reference("#SERVICE 1:0:1:1328:CA2:3:EB0000:0:0:0:") == "1_0_1_1328_CA2_3_EB0000_0_0_0"
assert m.normalize_service_reference("garbage") == ""
assert m.service_orbital_position("1:0:1:1328:CA2:3:EB0000:0:0:0:") == "23.5e"
assert m.service_orbital_position("1:0:1:1:1:1:C00000:0:0:0:") == "19.2e"
assert m.position_token("23.5E") == "23.5e"
assert m.position_token("(23.5E) Skylink") != "23.5e"
assert m.position_token("0.8W") == "0.8w"
assert m.position_token("dtt") == "dtt"
assert m.position_token("19.2e") == "19.2e"
runtime_pub = m.runtime_publication()
assert runtime_pub["persistent"] is True
assert runtime_pub["manifest_url"] == "https://raw.githubusercontent.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/warder-modernization-work/assets/warder/downloads/picons/channels/test-candidate/manifest.json"
assert m.safe_archive_member("1_0_1_A_B_C_D_0_0_0.png") is True
assert m.safe_archive_member("../escape.png") is False
assert m.safe_archive_member("/absolute.png") is False
assert m.selector_id_for_display_label("(0.8W) Freesat") == "FREESAT"
assert m.selector_id_for_display_label("(0.8W) Digi / Telly") == "DIGI_TELLY"
assert m.selector_id_for_display_label("(0.8W) Thor 5,6,7/Intelsat 10-02") == "08W"
assert m.selector_id_for_display_label("(23.5E) Skylink") == "SKYLINK"
assert m.selector_id_for_display_label("(23.5E) Astra 3B") == "235E"
assert m.valid_position_selection(["ANTIKSAT", "SKYLINK"])
assert not m.valid_position_selection([])
assert not m.valid_position_selection(["UNKNOWN"])

with tempfile.TemporaryDirectory() as d:
    with open(os.path.join(d, "bouquets.tv"), "w") as h:
        h.write('#SERVICE 1:7:1:0:0:0:0:0:0:0:FROM BOUQUET "userbouquet.warder.tv" ORDER BY bouquet\n')
    with open(os.path.join(d, "userbouquet.warder.tv"), "w") as h:
        h.write("#NAME Warder test\n")
        h.write("#SERVICE 1:0:1:1328:CA2:3:EB0000:0:0:0:\n")
        h.write("#DESCRIPTION Skylink sample\n")
        h.write("#SERVICE 1:0:1:1:1:1:C00000:0:0:0:\n")
        h.write("#SERVICE 1:0:1:100:1:1:A00000:0:0:0:\n")
        h.write("#SERVICE 1:0:1:1328:CA2:3:EB0000:0:0:0:\n")
    refs = m.bouquet_services(d)
    assert refs == [
        "1_0_1_1328_CA2_3_EB0000_0_0_0",
        "1_0_1_1_1_1_C00000_0_0_0",
        "1_0_1_100_1_1_A00000_0_0_0",
    ]
    req = m.build_sync_request(d, ["16.0e", "23.5e"], "transparent", "220x132")
    assert req["mode"] == "sync-tv-lists"
    assert [x["service_reference"] for x in req["services"]] == [
        "1_0_1_1328_CA2_3_EB0000_0_0_0", "1_0_1_100_1_1_A00000_0_0_0"]
    assert {x["position"] for x in req["services"]} == {"16.0e", "23.5e"}
    assert all(x["position"] in ("16.0e", "23.5e") for x in req["services"])
    try:
        m.build_sync_request(d, [], "transparent", "220x132")
    except ValueError as error:
        assert str(error) == "no-satellite-position-selected"
    else:
        raise AssertionError("empty manual selection must fail closed")

prefs = m.default_preferences()
assert prefs["update_mode"] is None
assert prefs["style"] is None
assert prefs["resolution"] is None
assert prefs["destination"] == "/usr/share/enigma2/picon"
assert prefs["prepared"] is False
assert m.has_executable_action(prefs) is False
prefs = m.set_preference(prefs, "style", "black")
assert prefs["prepared"] is True
assert m.has_executable_action(prefs) is True
assert m.has_executable_action(m.default_preferences(), ordinary_selected=True) is True
assert [x[0] for x in m.UPDATE_MODES] == [m.UPDATE_MODE_SYNC_TV, m.UPDATE_MODE_SYNC_TV_RADIO, m.UPDATE_MODE_REPLACE_ALL, m.UPDATE_MODE_INCREMENTAL]
def configured(position, mode=m.UPDATE_MODE_SYNC_TV, destination="/media/hdd/picon", resolution="220x132", style="transparent"):
    bindings = [m.task_binding_for_package_selector(selector) for selector in position]
    state = m.set_task_position_bindings(m.default_preferences(), bindings)
    state.update({"resolution": resolution, "style": style, "destination": destination,
                  "update_mode": mode, "prepared": True})
    return state

prefs2 = m.set_task_position_bindings(m.default_preferences(), [
    m.task_binding_for_package_selector("SKYLINK"),
    m.task_binding_for_package_selector("DVB-T-SK-CZ")])
assert prefs2["positions"] == ["23.5E", "DTT"]
assert prefs2["package_selectors"] == ["SKYLINK", "DVB-T-SK-CZ"]
assert prefs2["prepared"] is True

PLUGIN = os.path.join(ROOT, "source/package-root/usr/lib/enigma2/python/Plugins/Extensions/setupGlass17/plugin.py")
with open(PLUGIN, "r") as h:
    plugin_source = h.read()
menu_start = plugin_source.index("\t\tself.menuListAll = {", plugin_source.index("class downloadMenu"))
menu_end = plugin_source.index("\n\t\t\t}", menu_start)
menu_block = plugin_source[menu_start:menu_end]
keys = [int(x) for x in __import__("re").findall(r"^\t\t\t(\d+):\[", menu_block, __import__("re").M)]
assert keys == list(range(len(keys))), keys
assert "CHSPiconbig" not in menu_block
assert "picon_400x240" not in menu_block and "picon_220x132" not in menu_block
assert 'binding = warderPiconSync.task_binding_for_display_label(label)' in plugin_source
selector_block = plugin_source.split("class warderPositionSelectorScr(Screen):", 1)[1].split("class styleSelectorScr(Screen):", 1)[0]
assert '"cancel": self.cancel, "red": self.cancel' in selector_block
assert "def cancel(self):" in selector_block and "self.close(None)" in selector_block
assert "def warderPositionAnswer(self, answer=None):" in plugin_source
assert "if answer is None or not isinstance(answer, (list, tuple)):" in plugin_source
assert "self.warderPositionSelectionAttempted = True" in plugin_source
assert 'if prepared and not warderPiconSync.valid_task_selection(self.warderPiconPrefs):' in plugin_source
assert "Select at least one satellite position." in plugin_source
assert '"No position selected"' in plugin_source
assert 'set_task_position_bindings(self.warderPiconPrefs, bindings)' in plugin_source
assert '_("Select at least one satellite position.")' in plugin_source
for icon in ('"wp-pos": "down/p4.png"', '"wp-res": "down/ba5.png"',
             '"wp-style": "down/warder-colour.png"', '"wp-dest": "down/warder-location.png"',
             '"wp-mode": "down/warder-sync.png"'):
    assert icon in plugin_source, icon
assert "warder_help.get(row_id" in plugin_source
assert "text=description" in plugin_source
assert 'self._setWarderPiconPrepared("wp-pos")' in plugin_source
assert "self._setWarderPiconPrepared(self.warderChoiceRow)" in plugin_source
assert "warderPiconSync.build_runtime_queue(self.warderPiconPrefs, publication=warderPiconSync.runtime_publication())" in plugin_source
assert "warderPiconSync.PUBLICATION_LOCKED" in plugin_source
assert "Warder channel picon publication is currently unavailable." in plugin_source
assert "prepared but not persistently published yet" not in plugin_source
assert "_warderFetchChannelJob" in plugin_source
assert "_warderInstallChannelArchive" in plugin_source
assert "os.replace(tmp, os.path.join(dest, name))" in plugin_source
assert "def _warderLoadChannelManifest" in plugin_source
assert "def _warderRunChannelQueue" in plugin_source
assert 'self.dwnJob = _("Warder channel picons")' in plugin_source
assert "self.warderChannelInstalled.update(installed)" in plugin_source
assert "classify_requested_picons(" in plugin_source
assert "self.warderChannelAvailable.update(available)" in plugin_source
assert '"outside_selected_packages"' in sync_source
assert "package_result_summary" in sync_source
assert '_("selected receiver services have no matching picon in the selected packages.")' not in plugin_source
assert "self.dwnTimer.start(10)" not in plugin_source
assert "self.dwnTimer.start(25, True)" in plugin_source
assert 'self.warderChannelState = "idle"' in plugin_source
assert 'self.warderChannelState = "running"' in plugin_source
assert 'self.warderChannelState = "error"' in plugin_source
assert "shutil.disk_usage(destination)" in plugin_source
assert plugin_source.count('os.path.islink(destination)') >= 2
assert 'queue["destination"] = destination' in plugin_source
assert 'raise ValueError("unsafe Warder picon destination")' in plugin_source
assert "unsafe Warder picon ZIP compression ratio" in plugin_source
assert "invalid Warder channel part size" in plugin_source
assert "oversized Warder channel download" in plugin_source
assert 'legacy_pending = any(self.menuListAll[x][4] == "d" and self.menuListAll[x][0] not in self.warderPiconRows for x in self.menuListAll)' in plugin_source
assert 'self.warderChannelState = "locked"' in plugin_source
assert 'if self.warderChannelState != "locked":' in plugin_source
assert 'if self.menuListAll[x][4] == "d" and self.menuListAll[x][0] not in self.warderPiconRows and self.menuListAll[x][0] not in self.warderFailedRows:' in plugin_source
dwn_loop = plugin_source.split("def dwnLoop(self, txt=\"\"):", 1)[1].split("\n\tdef dwnFin", 1)[0]
assert 'self.warderPiconPrefs.get("resolution") == "220x132"' in dwn_loop
assert 'self.warderChannelState not in ("locked", "error")' in dwn_loop
assert 'legacy_result = self.downMulti(self.warderLegacyChannelQueue, folder, False)' in dwn_loop
assert '("done", "error", "locked")' in plugin_source
error_branch = plugin_source[plugin_source.index("except Exception as err:", plugin_source.index("def dwnLoop")):plugin_source.index("\n\t\t\t\telse:", plugin_source.index("except Exception as err:", plugin_source.index("def dwnLoop")))]
assert 'self.warderPiconPrefs["prepared"] = False' not in error_branch
assert 'self.menuListAll[row][4] = "x"' not in error_branch
channel_result_block = plugin_source[plugin_source.index("def _warderRunChannelQueue"):plugin_source.index("def dwnLoop")]
assert "package_result_summary" in channel_result_block
assert "outside_selected_packages" not in channel_result_block
assert "PARTIAL SUCCESS" in plugin_source
assert 'self.warderPiconPrefs["prepared"] = False' in plugin_source
assert 'self.warderChannelState = "done"' in plugin_source
assert 'no selected TV or radio bouquet services found for Warder selective sync' in plugin_source
assert 'Warder channel selection resolved to no packages' in plugin_source
assert ".is_dir()" not in plugin_source[plugin_source.index("def _warderInstallChannelArchive"):plugin_source.index("def downMulti")]
run_block = plugin_source[plugin_source.index("def _warderRunChannelQueue"):plugin_source.index("def dwnLoop")]
install_block = plugin_source[plugin_source.index("def _warderInstallChannelArchive"):plugin_source.index("def downMulti")]
assert 'stat.S_ISLNK(mode)' in install_block
assert 'invalid Warder picon PNG signature' in install_block
assert 'signature != b"\\x89PNG\\r\\n\\x1a\\n"' in install_block
assert 'os.replace(tmp, os.path.join(dest, name))' in install_block
assert 'finally:' in run_block and 'os.unlink(archive)' in run_block
assert 'if not self.warderChannelJobs and not (queue.get("mode") in (warderPiconSync.UPDATE_MODE_SYNC_TV, warderPiconSync.UPDATE_MODE_SYNC_TV_RADIO) and not queue.get("services")):' in run_block

with tempfile.TemporaryDirectory() as d:
    with open(os.path.join(d, "bouquets.tv"), "w") as h:
        h.write('#SERVICE 1:7:1:0:0:0:0:0:0:0:FROM BOUQUET "userbouquet.q.tv" ORDER BY bouquet\n')
    with open(os.path.join(d, "userbouquet.q.tv"), "w") as h:
        h.write("#SERVICE 1:0:1:1328:CA2:3:EB0000:0:0:0:\n")
        h.write("#SERVICE 1:0:1:1:1:1:C00000:0:0:0:\n")
    channel_prefs = configured(["SKYLINK"])
    locked = m.build_runtime_queue(channel_prefs, d, {"persistent": False, "manifest_url": None})
    assert locked["state"] == m.PUBLICATION_LOCKED
    assert locked["service_count"] == 1
    assert locked["services"][0]["position"] == "23.5e"
    live = m.build_runtime_queue(channel_prefs, d, m.runtime_publication())
    assert live["state"] == m.READY
    assert live["service_count"] == 1
    ready = m.build_runtime_queue(channel_prefs, d, {"persistent": True, "manifest_url": "https://example.invalid/manifest.json"})
    assert ready["state"] == m.READY and ready["service_count"] == 1
    try:
        m.build_runtime_queue(m.default_preferences(), d, {"persistent": True, "manifest_url": "https://example.invalid/manifest.json"})
    except ValueError as error:
        assert str(error) == "no-satellite-position-selected"
    else:
        raise AssertionError("empty runtime selection must not become all positions")
    full_prefs = configured(["SKYLINK"], m.UPDATE_MODE_INCREMENTAL)
    full = m.build_runtime_queue(full_prefs, d)
    assert full["mode"] == m.UPDATE_MODE_INCREMENTAL and full["service_count"] == 0
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
oversized_manifest = dict(valid_manifest)
oversized_manifest["parts"] = [dict(valid_manifest["parts"][0], bytes=20 * 1024 * 1024 + 1)]
assert "invalid part metadata" in m.validate_publication_manifest(oversized_manifest)
mismatched_manifest = dict(valid_manifest)
mismatched_manifest["parts"] = [dict(valid_manifest["parts"][0], bytes=9)]
assert "package part size mismatch" in m.validate_publication_manifest(mismatched_manifest)
wrong_part_name_manifest = dict(valid_manifest)
wrong_part_name_manifest["packages"] = [dict(valid_manifest["packages"][0], parts=[
    "https://raw.githubusercontent.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/main/assets/warder/downloads/picons/channels/235E-transparent.zip.part01"
])]
wrong_part_name_manifest["parts"] = [dict(valid_manifest["parts"][0], filename="235E-transparent.zip.part01")]
assert "non-canonical package part" in m.validate_publication_manifest(wrong_part_name_manifest)
sel = m.select_manifest_packages(valid_manifest, configured(["235E"]))
assert sel["state"] == "ready" and sel["selector_ids"] == ["235E"]
assert sel["packages"][0]["selector_id"] == "235E"
wrong_res = m.select_manifest_packages(valid_manifest, configured(["235E"], resolution="400x240"))
assert wrong_res["packages"] == []
provider_manifest = dict(valid_manifest)
provider_manifest["packages"] = [dict(valid_manifest["packages"][0], selector_id="FREESAT", warder_key="0.8w/freesat")]
provider_sel = m.select_manifest_packages(provider_manifest, configured(["FREESAT"]))
assert provider_sel["selector_ids"] == ["FREESAT"] and len(provider_sel["packages"]) == 1
wrong_provider = m.select_manifest_packages(provider_manifest, configured(["DIGI_TELLY"]))
assert wrong_provider["state"] == "partial" and wrong_provider["missing_selectors"] == ["DIGI_TELLY"]
queue = {
    "mode": m.UPDATE_MODE_SYNC_TV, "positions": ["23.5E"], "package_selectors": ["235E"],
    "position_bindings": [m.task_binding_for_package_selector("235E")],
    "style": "transparent", "resolution": "220x132",
    "services": [{"service_reference": "1_0_1_1328_CA2_3_EB0000_0_0_0", "position": "23.5e"}],
}
planned = m.plan_runtime_packages(valid_manifest, queue)
assert planned["state"] == "ready" and [p["selector_id"] for p in planned["packages"]] == ["235E"]
full_queue = dict(queue, mode=m.UPDATE_MODE_FULL, services=[])
full_planned = m.plan_runtime_packages(valid_manifest, full_queue)
assert len(full_planned["packages"]) == 1
empty_sync_queue = dict(queue, services=[], positions=[], package_selectors=[], position_bindings=[])
empty_sync_planned = m.plan_runtime_packages(valid_manifest, empty_sync_queue)
assert empty_sync_planned["state"] == "invalid-selection" and empty_sync_planned["packages"] == []
assert m.build_download_jobs(valid_manifest, empty_sync_planned)["state"] == "invalid-plan"
bad_style = dict(queue, style="unknown")
assert m.plan_runtime_packages(valid_manifest, bad_style)["state"] == "invalid-preferences"
bad_resolution = dict(queue, resolution="../220x132")
assert m.plan_runtime_packages(valid_manifest, bad_resolution)["state"] == "invalid-preferences"
full_selected = dict(full_queue, positions=["23.5E"], package_selectors=["235E"], position_bindings=[m.task_binding_for_package_selector("235E")])
full_selected_planned = m.plan_runtime_packages(valid_manifest, full_selected)
assert [p["selector_id"] for p in full_selected_planned["packages"]] == ["235E"]
provider_queue = dict(queue, positions=["0.8W"], package_selectors=["FREESAT"], position_bindings=[m.task_binding_for_package_selector("FREESAT")],
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
assert m.validate_destination("/etc/enigma2") is None
assert m.validate_destination("/usr/share/enigma2") is None
assert m.validate_destination("/var/lib") is None
assert m.validate_destination("/media/hdd/picon") == "/media/hdd/picon"
identity_queue = {"mode": m.UPDATE_MODE_SYNC_TV, "services": [
    {"service_reference": "1:0:1:1328:CA2:3:EB0000:0:0:0:"},
    {"service_reference": "#SERVICE 1:0:1:1328:CA2:3:EB0000:0:0:0:"},
    {"service_reference": "garbage"},
]}
assert m.wanted_picon_names(identity_queue) == {"1_0_1_1328_CA2_3_EB0000_0_0_0.png"}
coverage = m.classify_requested_picons(
    {"a.png", "b.png", "outside.png"}, {"a.png", "b.png"}, {"a.png", "b.png"})
assert coverage["relevant"] == {"a.png", "b.png"}
assert coverage["outside_selected_packages"] == {"outside.png"}
assert coverage["missing"] == set()
coverage_missing = m.classify_requested_picons(
    {"a.png", "b.png"}, {"a.png", "b.png"}, {"a.png"})
assert coverage_missing["missing"] == {"b.png"}
full_coverage = m.classify_requested_picons(None, {"a.png", "b.png"}, {"a.png"})
assert full_coverage["missing"] == {"b.png"} and not full_coverage["outside_selected_packages"]
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
duplicate_errors = m.validate_publication_manifest(duplicate_part)
assert any(x in duplicate_errors for x in ("duplicate package part", "non-canonical package part")), duplicate_errors


# TEST194 production manifest entries: these two UI labels select provider-specific
# ZIPs, while service references at each orbital position can include other providers.
assert m.selected_selector_ids(["ANTIKSAT", "SKYLINK"]) == ["ANTIKSAT", "SKYLINK"]
selected_provider_entries = {
    "ANTIKSAT": "warder-antiksat-channel-transparent.zip",
    "SKYLINK": "warder-skylink-channel-transparent.zip",
}
assert set(selected_provider_entries) == {"ANTIKSAT", "SKYLINK"}
# Receiver report: 1,333 orbital-filtered services, 198 exact members in the
# selected provider packages. Only those 198 are relevant package matches.
receiver_names = set("service-%04d.png" % i for i in range(1333))
package_names = set("service-%04d.png" % i for i in range(198))
report_coverage = m.classify_requested_picons(receiver_names, package_names, package_names)
assert len(report_coverage["relevant"]) == 198
assert len(report_coverage["outside_selected_packages"]) == 1135
assert report_coverage["missing"] == set()

# The selector's cancel route passes explicit None; yellow Save returns a list.
assert 'self.close(None)' in selector_block
assert 'ret = [x[1] for x in self.list.getSelectionsList()]' in selector_block
assert 'self.close(ret)' in selector_block

# Localized descriptions, empty-selection status and result messages must exist
# in every setupGlass17 catalog; build-test-ipk.sh compiles all these PO files.
locale_root = PKG / "usr/lib/enigma2/python/Plugins/Extensions/setupGlass17/locale"
warder_msgids = (
    "Choose satellite positions for channel picon downloads and updates.",
    "Choose an available channel picon size and the large channel selection icon package.",
    "Choose a channel picon colour supported at the selected size.",
    "Choose where channel picons are downloaded and updated.",
    "Choose whether to sync picons from TV lists or download full selected packages.",
    "Choose the available provider picon variant.",
    "Choose the available satellite picon variant.",
    "Choose black or white CAM picons.",
    "Choose black or white weather information picons.",
    "Provider picons",
    "Satellite picons",
    "CAM picons",
    "Weather picons",
    "Large channel selection icons (710 x 682)",
    "No legacy picon archive is available for the selected positions and variant.",
    "Invalid picon destination",
    "No position selected",
    "Select at least one satellite position.",
    "Updated:",
    "Selected upstream picons were not installed:",
)
catalogs = sorted(locale_root.glob("*/LC_MESSAGES/setupGlass17.po"))
assert len(catalogs) == 19, len(catalogs)
for catalog in catalogs:
    po_text = catalog.read_text(encoding="utf-8")
    for msgid in warder_msgids:
        escaped = msgid.replace("\\", "\\\\").replace('"', '\\"')
        assert 'msgid "' + escaped + '"\nmsgstr "' in po_text, (catalog, msgid)

# The five distinct icon paths are packaged FullHDGlass assets.
icon_root = PKG / "usr/share/enigma2/hd_glass17"
for icon in ("icons/dish.png", "icons/i_fhd.png", "down/ba.png", "icons/folder.png", "icons/update.png",
             "down/p4p.png", "down/p4s.png", "down/bc.png", "down/bw.png"):
    assert (icon_root / icon).is_file(), icon
assert len({"icons/dish.png", "icons/i_fhd.png", "down/ba.png", "icons/folder.png", "icons/update.png"}) == 5

# Exact capability/asset matrix: legacy archive columns are scoped to the selected SATLIST rows.
assert m.CHANNEL_RESOLUTION_STYLES == {
    "50x30": ("black", "white"),
    "150x90": ("black", "white"),
    "220x132": ("transparent", "black", "white"),
    "400x240": ("transparent",),
}
assert m.channel_delivery_backend("220x132", "white") == "warder"
assert m.channel_delivery_backend("400x240", "transparent") == "pinned-legacy"
assert m.channel_delivery_backend("400x240", "white") is None
sat_rows = [
    ("(16.0E) Antiksat", "", "ANTIKSAT", "2133", "3658", "1794", "1342", "4290", "4038", "1197"),
    ("(23.5E) Skylink", "", "SKYLINK", "2146", "3670", "1809", "1356", "4302", "4050", "1211"),
]
selected = ["ANTIKSAT", "SKYLINK"]
assert m.plan_legacy_channel_archives(selected, sat_rows, "400x240", "transparent") == [
    (selected[0], "2133"), (selected[1], "2146")]
assert m.plan_legacy_channel_archives(selected, sat_rows, "50x30", "black") == [
    (selected[0], "3658"), (selected[1], "3670")]
assert m.plan_legacy_channel_archives(selected, sat_rows, "150x90", "white") == [
    (selected[0], "4290"), (selected[1], "4302")]
assert m.plan_legacy_channel_archives(selected, sat_rows, "220x132", "transparent") == [
    (selected[0], "1197"), (selected[1], "1211")]
for bad_positions, size, colour in (([], "220x132", "transparent"), (["UNKNOWN"], "220x132", "transparent"), (selected, "400x240", "black")):
    try:
        m.plan_legacy_channel_archives(bad_positions, sat_rows, size, colour)
    except ValueError:
        pass
    else:
        raise AssertionError((bad_positions, size, colour))
assert m.legacy_channel_destination("50x30") == "picon_50x30"
assert m.legacy_channel_destination("150x90") == "picon"
assert m.legacy_channel_destination("220x132") == "picon_220x132"
assert m.legacy_channel_destination("400x240") == "picon_400x240"

# Callback cancellation is explicit and the selection guard is evaluated before work starts.
assert "def warderPiconChoiceAnswer(self, answer=None):" in plugin_source
assert "def warderAuxPiconAnswerFor(self, row, *answer):" in plugin_source
assert "def satSelcallback(self, answer=None):" in plugin_source
assert "def cleanAnswerNow(self, answer=None):" in plugin_source
assert "self.openAuxPiconChoice(self.menuListAll[tmp][0])" in plugin_source
assert "if not self._legacyPiconArchiveUrl(archive_id):" in plugin_source
assert "plan_legacy_channel_archives(" in plugin_source
assert "build_sync_request(" in plugin_source
assert "if self.warderPiconPrefs.get(\"update_mode\") in (warderPiconSync.UPDATE_MODE_SYNC_TV, warderPiconSync.UPDATE_MODE_SYNC_TV_RADIO):" in plugin_source
assert "warderLegacyChannelWanted" in plugin_source
assert "classify_requested_picons(" in plugin_source
assert "def downMulti(self, k, Ddir, continue_loop=True):" in plugin_source
assert "legacy_result = self.downMulti(self.warderLegacyChannelQueue, folder, False)" in plugin_source
for row_id in ("aux-prov", "aux-sat", "aux-cam", "aux-weather"):
    assert row_id in plugin_source
assert "AUXILIARY_ASSET_KEYS" in plugin_source
assert "piconProv-220" in sync_source and "piconSat-220" in sync_source
assert "piconCam-b" in sync_source and "piconWeather-w" in sync_source
assert "CHSPiconbig" in plugin_source and "Large channel selection icons (710 x 682)" in plugin_source

# Validate the split large channel-selection package against its pinned catalogue
# metadata and inspect actual PNG dimensions before placing it in the resolution menu.
catalog_path = Path(ROOT) / "assets/warder/downloads.json"
catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
asset = catalog["assets"]["CHSPiconbig"]
archive = b""
for part in asset["parts"]:
    rel = part.split("/main/", 1)[1]
    archive += (Path(ROOT) / rel).read_bytes()
assert len(archive) == int(asset["size"]), (len(archive), asset["size"])
assert hashlib.sha256(archive).hexdigest() == asset["sha256"]
dimensions = set()
with zipfile.ZipFile(__import__("io").BytesIO(archive)) as package:
    for info in package.infolist():
        if info.filename.lower().endswith(".png") and not info.is_dir():
            header = package.read(info)[:24]
            assert header.startswith(b"\x89PNG\r\n\x1a\n"), info.filename
            dimensions.add(struct.unpack(">II", header[16:24]))
assert dimensions == {(710, 682)}, dimensions

print("Warder TEST195 legacy filtering, callbacks, empty-selection, UI, localization, and asset dimensions: PASS")
