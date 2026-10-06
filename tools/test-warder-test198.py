#!/usr/bin/env python3
"""Focused TEST198 regressions for explicit position identity and honest results."""
import importlib.util, tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SYNC=ROOT/"source/package-root/usr/lib/enigma2/python/Plugins/Extensions/setupGlass17/warderPiconSync.py"
spec=importlib.util.spec_from_file_location("warderPiconSync_test198",str(SYNC))
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)

# The GUI item binds to a canonical domain position and a separate package selector.
generic=m.position_binding("160E")
provider=m.position_binding("ANTIKSAT")
assert generic=={"selector_id":"160E","orbital_position":"16.0e"}
assert provider=={"selector_id":"ANTIKSAT","orbital_position":"16.0e"}
assert generic["selector_id"]!=provider["selector_id"]
assert m.selector_id_for_display_label("(16.0E) Eutelsat 16A")=="160E"
assert m.selector_id_for_display_label("(16.0E) Renamed GUI label") is None
assert m.position_binding("(16.0E) Eutelsat 16A") is None
assert m.canonical_position_for_selector("160E")=="16.0e"
assert m.canonical_position_for_selector("ANTIKSAT")=="16.0e"
assert not m.valid_position_selection(["(16.0E) Eutelsat 16A"])
with tempfile.TemporaryDirectory() as td:
    prefs={"positions":["160E","08W"],
           "resolution":"220x132","style":"transparent","destination":str(Path(td)/"picon"),
           "update_mode":m.UPDATE_MODE_FULL,"prepared":True}
    queue=m.build_runtime_queue(prefs,enigma2_dir=str(Path(td)/"empty"),
        publication={"persistent":True,"manifest_url":"https://example.invalid/manifest.json"})
    assert set(queue["positions"])=={"16.0e","0.8w"}
    assert set(queue["selector_ids"])=={"160E","08W"}
    mismatch=dict(queue,positions=["19.2e"])
    bad=m.plan_runtime_packages({"schema":1,"generated_from":{"repository":"Evolution-by-Warder/PiconHub-Warder-Evolution","ref":"0123456789abcdef"},"delivery":"direct","packages":[]},mismatch)
    assert bad["state"]=="invalid-selection" and "selector-position-binding-mismatch" in bad["errors"]
    assert {x["selector_id"]:x["orbital_position"] for x in queue["position_bindings"]}=={"160E":"16.0e","08W":"0.8w"}

# A provider package cannot satisfy a request for the generic orbital package.
manifest={"schema":1,"generated_from":{"repository":"Evolution-by-Warder/PiconHub-Warder-Evolution","ref":"0123456789abcdef"},
 "delivery":"direct","packages":[{"selector_id":"FREESAT","orbital_position":"0.8w","family":"channel-transparent",
 "resolution":"220x132","filename":"freesat.zip","bytes":10,"sha256":"a"*64,
 "url":"https://raw.githubusercontent.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/main/assets/warder/downloads/picons/channels/freesat.zip"}]}
assert m.validate_publication_manifest(manifest)==[]
generic_queue={"mode":m.UPDATE_MODE_FULL,"positions":["0.8w"],"selector_ids":["08W"],"style":"transparent","resolution":"220x132","services":[]}
plan=m.plan_runtime_packages(manifest,generic_queue)
assert plan["state"]=="partial" and plan["missing_selectors"]==["08W"] and plan["packages"]==[]
wrong=dict(manifest);wrong["packages"]=[dict(manifest["packages"][0],orbital_position="16.0e")]
assert "incorrect canonical orbital position binding" in m.validate_publication_manifest(wrong)

# Result counts are measured per package/position; receiver-wide unmatched services are absent.
summary=m.package_result_summary([
 {"selector_id":"160E","orbital_position":"16.0e","updated":5,"failures":0},
 {"selector_id":"235E","orbital_position":"23.5e","updated":2,"failures":1},
])
assert summary["status"]=="PARTIAL SUCCESS"
assert summary["updated"]==7 and summary["failures"]==1
assert "16.0E / 160E: 5 picons updated; 0 failures" in summary["text"]
assert "23.5E / 235E: 2 picons updated; 1 failures" in summary["text"]
assert "Total: 7 picons updated" in summary["text"] and "Failures: 1" in summary["text"]
assert "services selected" not in summary["text"]
assert "matching picon" not in summary["text"]
assert m.package_result_summary([{"selector_id":"160E","orbital_position":"16.0e","updated":4,"failures":0}])["status"]=="SUCCESSFUL"
assert m.package_result_summary([{"selector_id":"160E","orbital_position":"16.0e","updated":0,"failures":1}])["status"]=="ERROR"

# Task choices reset only after success; cancel and error keep the exact retry state.
assert m.preferences_after_task(prefs,"cancel")==prefs
assert m.preferences_after_task(prefs,"error")==prefs
assert m.preferences_after_task(prefs,"success")==m.default_preferences()
print("TEST198 position binding, no provider fallback, per-package results and outcome lifecycle: PASS")
