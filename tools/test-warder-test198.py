#!/usr/bin/env python3
"""TEST199 regressions for canonical task positions and separate package selectors."""
import importlib.util, tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SYNC=ROOT/"source/package-root/usr/lib/enigma2/python/Plugins/Extensions/setupGlass17/warderPiconSync.py"
PLUGIN=ROOT/"source/package-root/usr/lib/enigma2/python/Plugins/Extensions/setupGlass17/plugin.py"
spec=importlib.util.spec_from_file_location("warderPiconSync_test199",str(SYNC))
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)

# The actual selectable labels bind canonical identity and package selector independently.
selected_labels=[
 "(13.0E) Hot Bird 13B/13C/13D",
 "(16.0E) Eutelsat 16A",
 "(19.2E) Astra 1KR,1L,1M,1N",
 "(23.5E) Astra 3B",
]
expected_positions=["13.0E","16.0E","19.2E","23.5E"]
expected_selectors=["130E","160E","192E","235E"]
bindings=[m.task_binding_for_display_label(label) for label in selected_labels]
assert all(bindings), bindings
prefs=m.set_task_position_bindings(m.default_preferences(),bindings)
assert prefs["positions"]==expected_positions
assert prefs["package_selectors"]==expected_selectors
assert prefs["position_bindings"]==[
 {"canonical_position":position,"package_selector":selector}
 for position,selector in zip(expected_positions,expected_selectors)]
assert m.task_positions_for_display(prefs)==expected_positions
assert m.valid_task_selection(prefs)
source=PLUGIN.read_text(encoding="utf-8")
row_block=source[source.index("def _warderRefreshRowText"):source.index("def _warderDisplayPath")]
assert "task_positions_for_display(prefs)" in row_block
assert 'join(positions[:4])' in row_block

# Every decimal orbital mapping, including 0.8W and 54.9E, keeps its canonical value.
for label,(selector,canonical) in m._SELECTOR_LABEL_BINDINGS.items():
 binding=m.task_binding_for_display_label(label)
 assert binding=={"canonical_position":canonical.upper(),"package_selector":selector}
for raw_position in ("0.8w", "4.8e", "54.9e"):
 label=next(label for label,(selector,position) in m._SELECTOR_LABEL_BINDINGS.items()
            if position==raw_position)
 binding=m.task_binding_for_display_label(label)
 canonical=raw_position.upper()
 assert binding["canonical_position"]==canonical
 prefs2=m.set_task_position_bindings(m.default_preferences(),[binding])
 assert m.task_positions_for_display(prefs2)==[canonical]
assert m.task_binding_for_display_label("(16.0E) Renamed GUI label") is None
assert m.task_binding_for_display_label("(16.0E) Antiksat")=={
 "canonical_position":"16.0E","package_selector":"ANTIKSAT"}
assert m.position_binding("(16.0E) Eutelsat 16A") is None

with tempfile.TemporaryDirectory() as td:
 prefs.update({"resolution":"220x132","style":"transparent","destination":str(Path(td)/"picon"),
               "update_mode":m.UPDATE_MODE_FULL,"prepared":True})
 queue=m.build_runtime_queue(prefs,enigma2_dir=str(Path(td)/"empty"),
   publication={"persistent":True,"manifest_url":"https://example.invalid/manifest.json"})
 assert queue["positions"]==expected_positions
 assert queue["package_selectors"]==expected_selectors
 assert queue["position_bindings"]==bindings
 mismatch=dict(queue,positions=["13.0E","16.0E","19.2E","21.5E"])
 bad=m.plan_runtime_packages({"schema":1,"generated_from":{"repository":"Evolution-by-Warder/PiconHub-Warder-Evolution","ref":"0123456789abcdef"},
   "delivery":"direct","packages":[]},mismatch)
 assert bad["state"]=="invalid-selection"
 assert "selector-position-binding-mismatch" in bad["errors"]

# Runtime package selection consumes each separate package selector within canonical positions.
packages=[]
for position,selector in zip(expected_positions,expected_selectors):
 package={
  "selector_id":selector,"orbital_position":position.lower(),"family":"channel-transparent",
  "resolution":"220x132","filename":selector+"-transparent.zip","bytes":10,"sha256":"a"*64,
  "url":"https://raw.githubusercontent.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/main/assets/warder/downloads/picons/channels/"+selector+"-transparent.zip"}
 packages.append(package)
manifest={"schema":1,"generated_from":{"repository":"Evolution-by-Warder/PiconHub-Warder-Evolution","ref":"0123456789abcdef"},
 "delivery":"direct","packages":packages}
assert m.validate_publication_manifest(manifest)==[]
plan=m.plan_runtime_packages(manifest,queue)
assert plan["state"]=="ready"
assert [x["selector_id"] for x in plan["packages"]]==expected_selectors
assert {x["orbital_position"] for x in plan["packages"]}=={x.lower() for x in expected_positions}

# 16.0E provider packages remain separate; neither provider nor nearby position can substitute.
provider=m.task_binding_for_display_label("(16.0E) Antiksat")
provider_prefs=m.set_task_position_bindings(m.default_preferences(),[provider])
provider_prefs.update({"resolution":"220x132","style":"transparent","destination":str(Path(td)/"picon"),
 "update_mode":m.UPDATE_MODE_FULL,"prepared":True})
provider_queue=m.build_runtime_queue(provider_prefs,enigma2_dir=str(Path(td)/"empty"),
 publication={"persistent":True,"manifest_url":"https://example.invalid/manifest.json"})
assert provider_queue["positions"]==["16.0E"]
assert provider_queue["package_selectors"]==["ANTIKSAT"]
assert provider_queue["package_selectors"]!=["160E"]
# 0.8W generic position cannot be fulfilled by a provider-only manifest unless that provider was selected.
freesat={"schema":1,"generated_from":manifest["generated_from"],"delivery":"direct","packages":[{
 "selector_id":"FREESAT","orbital_position":"0.8w","family":"channel-transparent","resolution":"220x132",
 "filename":"freesat.zip","bytes":10,"sha256":"b"*64,
 "url":"https://raw.githubusercontent.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/main/assets/warder/downloads/picons/channels/freesat.zip"}]}
generic08=m.set_task_position_bindings(m.default_preferences(),[m.task_binding_for_display_label("(0.8W) Thor 5,6,7/Intelsat 10-02")])
generic08.update({"resolution":"220x132","style":"transparent","destination":str(Path(td)/"picon"),
 "update_mode":m.UPDATE_MODE_FULL,"prepared":True})
generic08_queue=m.build_runtime_queue(generic08,enigma2_dir=str(Path(td)/"empty"),
 publication={"persistent":True,"manifest_url":"https://example.invalid/manifest.json"})
no_fallback=m.plan_runtime_packages(freesat,generic08_queue)
assert no_fallback["state"]=="partial" and no_fallback["packages"]==[]
assert no_fallback["missing_selectors"]==["08W"]

# Result rows use canonical positions and human-readable package labels, never technical IDs.
summary=m.package_result_summary([
 {"selector_id":"160E","orbital_position":"16.0e","updated":5,"failures":0},
 {"selector_id":"ANTIKSAT","orbital_position":"16.0e","updated":2,"failures":1},
 {"selector_id":"08W","orbital_position":"0.8w","updated":3,"failures":0},
])
assert summary["status"]=="PARTIAL SUCCESS"
assert summary["updated"]==10 and summary["failures"]==1
assert "16.0E / Eutelsat 16A: 5 picons updated; 0 failures" in summary["text"]
assert "16.0E / Antiksat: 2 picons updated; 1 failures" in summary["text"]
assert "0.8W / Thor 5,6,7/Intelsat 10-02: 3 picons updated; 0 failures" in summary["text"]
for selector in expected_selectors+["ANTIKSAT","08W"]:
 assert selector not in summary["text"]
assert "Total: 10 picons updated" in summary["text"] and "Failures: 1" in summary["text"]
assert m.package_result_summary([{"selector_id":"160E","orbital_position":"16.0e","updated":4,"failures":0}])["status"]=="SUCCESSFUL"
assert m.package_result_summary([{"selector_id":"160E","orbital_position":"16.0e","updated":0,"failures":1}])["status"]=="ERROR"

# Success clears task state; cancel and errors preserve the exact retryable state.
assert m.preferences_after_task(prefs,"cancel")==prefs
assert m.preferences_after_task(prefs,"error")==prefs
assert m.preferences_after_task(prefs,"success")==m.default_preferences()
print("TEST199 canonical positions, separate package selectors, no fallback, result identity and lifecycle: PASS")
