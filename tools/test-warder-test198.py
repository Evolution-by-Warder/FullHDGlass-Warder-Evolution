#!/usr/bin/env python3
"""TEST199 regressions for canonical task positions and separate package selectors."""
import importlib.util, tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SYNC=ROOT/"source/package-root/usr/lib/enigma2/python/Plugins/Extensions/setupGlass17/warderPiconSync.py"
PLUGIN=ROOT/"source/package-root/usr/lib/enigma2/python/Plugins/Extensions/setupGlass17/plugin.py"
spec=importlib.util.spec_from_file_location("warderPiconSync_test199",str(SYNC))
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
candidateBase="https://raw.githubusercontent.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/warder-modernization-work/assets/warder/downloads/picons/channels/test-candidate/"

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
   publication={"persistent":True,"manifest_url":m.RUNTIME_MANIFEST_URL})
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
  "url":"https://raw.githubusercontent.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/warder-modernization-work/assets/warder/downloads/picons/channels/test-candidate/"+selector+"-transparent.zip"}
 packages.append(package)
manifest={"schema":1,"generated_from":{"repository":"Evolution-by-Warder/PiconHub-Warder-Evolution","ref":"0123456789abcdef"},
 "delivery":"direct","packages":packages}
assert m.validate_publication_manifest(manifest)==[]
candidate_runtime=m.publication_from_manifest(m.RUNTIME_MANIFEST_URL,manifest)
assert candidate_runtime["persistent"] is True and candidate_runtime["manifest_url"]==m.RUNTIME_MANIFEST_URL
assert m._trusted_https_url(candidateBase+"warder-160e-channel-transparent.zip.part00")
assert not m._trusted_https_url("https://raw.githubusercontent.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/warder-modernization-work/assets/warder/downloads/picons/channels/other/warder-160e.zip.part00")
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
 publication={"persistent":True,"manifest_url":m.RUNTIME_MANIFEST_URL})
assert provider_queue["positions"]==["16.0E"]
assert provider_queue["package_selectors"]==["ANTIKSAT"]
assert provider_queue["package_selectors"]!=["160E"]
# 0.8W generic position cannot be fulfilled by a provider-only manifest unless that provider was selected.
freesat={"schema":1,"generated_from":manifest["generated_from"],"delivery":"direct","packages":[{
 "selector_id":"FREESAT","orbital_position":"0.8w","family":"channel-transparent","resolution":"220x132",
 "filename":"freesat.zip","bytes":10,"sha256":"b"*64,
 "url":"https://raw.githubusercontent.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/warder-modernization-work/assets/warder/downloads/picons/channels/test-candidate/freesat.zip"}]}
generic08=m.set_task_position_bindings(m.default_preferences(),[m.task_binding_for_display_label("(0.8W) Thor 5,6,7/Intelsat 10-02")])
generic08.update({"resolution":"220x132","style":"transparent","destination":str(Path(td)/"picon"),
 "update_mode":m.UPDATE_MODE_FULL,"prepared":True})
generic08_queue=m.build_runtime_queue(generic08,enigma2_dir=str(Path(td)/"empty"),
 publication={"persistent":True,"manifest_url":m.RUNTIME_MANIFEST_URL})
no_fallback=m.plan_runtime_packages(freesat,generic08_queue)
assert no_fallback["state"]=="partial" and no_fallback["packages"]==[]
assert no_fallback["missing_selectors"]==["08W"]

# Candidate manifest includes the generic 0.8W package and keeps its canonical identity.
candidate_08=dict(manifest)
candidate_08["packages"]=list(manifest["packages"])+[{
 "selector_id":"08W","orbital_position":"0.8w","family":"channel-transparent","resolution":"220x132",
 "filename":"warder-08w-channel-transparent.zip","bytes":10,"sha256":"c"*64,
 "url":candidateBase+"warder-08w-channel-transparent.zip"}]
assert m.validate_publication_manifest(candidate_08)==[]
generic08_plan=m.plan_runtime_packages(candidate_08,generic08_queue)
assert generic08_plan["state"]=="ready"
assert generic08_queue["positions"]==["0.8W"]
assert [(p["selector_id"],p["orbital_position"]) for p in generic08_plan["packages"]]==[("08W","0.8w")]

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

# Error restoration protects every task field if any runtime step mutates transient state.
plugin_lifecycle=source[source.index("def _warderRunChannelQueue"):source.index("def _warderFetchChannelJob")]
assert "self.warderChannelTaskSnapshot = dict(self.warderPiconPrefs)" in plugin_lifecycle
assert 'preferences_after_task(snapshot, "error")' in plugin_lifecycle
reset_method=source[source.index("def resetWarderWorkingState"):source.index("def _warderRunChannelQueue")]
assert 'preferences_after_task(self.warderPiconPrefs, "success")' in reset_method

# Corrected resolution text remains gettext-driven in all 19 supported catalogs.
catalogs=sorted((ROOT/"source/package-root/usr/lib/enigma2/python/Plugins/Extensions/setupGlass17/locale").glob("*/LC_MESSAGES/setupGlass17.po"))
assert len(catalogs)==19,len(catalogs)
for catalog in catalogs:
 text=catalog.read_text(encoding="utf-8")
 assert 'msgid "220 x 132 - Picons"' in text,catalog
 assert 'msgid "220 x 132 - XPicons"' not in text,catalog
sk_catalog=(ROOT/"source/package-root/usr/lib/enigma2/python/Plugins/Extensions/setupGlass17/locale/sk/LC_MESSAGES/setupGlass17.po").read_text(encoding="utf-8")
assert 'msgstr "220 × 132 – Picony"' in sk_catalog
print("TEST199 canonical positions, separate package selectors, no fallback, result identity and lifecycle: PASS")


# TEST201 binds manifests, package parts, and redirects to one exact source descriptor.
candidate_source=m.publication_source(m.RUNTIME_MANIFEST_URL)
production_source=m.publication_source("production")
assert candidate_source["id"]=="test-candidate"
assert production_source["id"]=="production"
candidate_root=candidate_source["package_root"]
production_root=production_source["package_root"]
candidate_manifest_url=candidate_source["manifest_url"]
production_manifest_url=production_source["manifest_url"]
candidate_package=candidate_root+"warder-130e-channel-black.zip"
candidate_part=candidate_package+".part00"
production_package=production_root+"warder-130e-channel-black.zip"
production_part=production_package+".part00"
assert m.trusted_publication_url(candidate_package,candidate_manifest_url)
assert m.trusted_publication_url(candidate_part,candidate_manifest_url)
assert not m.trusted_publication_url(production_package,candidate_manifest_url)
assert m.trusted_publication_url(production_package,production_manifest_url)
assert m.trusted_publication_url(production_part,production_manifest_url)
assert not m.trusted_publication_url(candidate_package,production_manifest_url)
assert not m.trusted_publication_url(candidate_root+"../manifest.json",candidate_manifest_url)
assert not m.trusted_publication_url(candidate_package+"?raw=1",candidate_manifest_url)
assert not m.trusted_publication_url(candidate_package.replace("raw.githubusercontent.com","raw.githubusercontent.com.evil.test"),candidate_manifest_url)

def publication_fixture(root):
 return {"schema":1,"generated_from":manifest["generated_from"],"delivery":"raw-github-parts",
  "parts":[{"filename":"warder-130e-channel-black.zip.part00","bytes":4,"sha256":"d"*64}],
  "packages":[{"selector_id":"130E","orbital_position":"13.0e","family":"channel-black",
   "resolution":"220x132","filename":"warder-130e-channel-black.zip","bytes":4,"sha256":"e"*64,
   "parts":[root+"warder-130e-channel-black.zip.part00"]}]}
candidate_pub=m.publication_from_manifest(candidate_manifest_url,publication_fixture(candidate_root))
assert candidate_pub["persistent"] and candidate_pub["publication_source_id"]=="test-candidate"
assert not m.publication_from_manifest(candidate_manifest_url,publication_fixture(production_root))["persistent"]
production_pub=m.publication_from_manifest(production_manifest_url,publication_fixture(production_root))
assert production_pub["persistent"] and production_pub["publication_source_id"]=="production"
assert not m.publication_from_manifest(production_manifest_url,publication_fixture(candidate_root))["persistent"]
# The receiver job fetch method calls this exact helper for both the request and response URL.
plugin_text=PLUGIN.read_text(encoding="utf-8")
fetch_method=plugin_text[plugin_text.index("def _warderFetchChannelJob"):plugin_text.index("def _warderInstallChannelArchive")]
assert "trusted_publication_url(url, source_id)" in fetch_method
assert "trusted_publication_url(str(response.geturl()), source_id)" in fetch_method
assert 'job.get("publication_source_id")' in fetch_method
assert 'job.get("publication_root") != source.get("package_root")' in fetch_method

# Optional CI network gate downloads four real candidate packages and verifies
# redirected URL root, per-part HTTP size/SHA256, reassembly, package SHA/size and ZIP CRC.
if __import__("sys").argv[1:] == ["--candidate-network"]:
 import hashlib, io, json, urllib.request, zipfile
 def fetch_checked(url, size, sha, source_id):
  assert m.trusted_publication_url(url, source_id), ("untrusted request URL",url)
  request=urllib.request.Request(url,headers={"User-Agent":"FullHDGlass17-Warder-Evolution/TEST201-preflight"})
  with urllib.request.urlopen(request,timeout=60) as response:
   final_url=response.geturl()
   assert m.trusted_publication_url(final_url,source_id), ("cross-publication redirect",url,final_url)
   data=response.read(int(size)+1)
  assert len(data)==int(size), ("HTTP size mismatch",url,len(data),size)
  assert hashlib.sha256(data).hexdigest()==sha.lower(), ("HTTP SHA256 mismatch",url)
  return data
 with urllib.request.urlopen(candidate_manifest_url,timeout=45) as response:
  assert response.geturl()==candidate_manifest_url
  network_manifest=json.loads(response.read(4*1024*1024+1).decode("utf-8"))
 assert not m.validate_publication_manifest(network_manifest,candidate_manifest_url)
 assert network_manifest.get("delivery")=="raw-github-parts"
 part_index={item["filename"]:item for item in network_manifest["parts"]}
 for selector in ("130E","160E","192E","235E"):
  matches=[item for item in network_manifest["packages"] if item.get("selector_id")==selector
   and item.get("family")=="channel-black" and item.get("resolution")=="220x132"]
  assert len(matches)==1,(selector,len(matches))
  package=matches[0]
  payload=bytearray()
  for url in package["parts"]:
   name=url.rsplit("/",1)[-1]; meta=part_index[name]
   payload.extend(fetch_checked(url,meta["bytes"],meta["sha256"],"test-candidate"))
  assert len(payload)==package["bytes"],("reassembled size",selector)
  assert hashlib.sha256(payload).hexdigest()==package["sha256"].lower(),("reassembled SHA256",selector)
  with zipfile.ZipFile(io.BytesIO(payload),"r") as zf:
   assert zf.testzip() is None,("ZIP CRC failure",selector)
   members=[item for item in zf.infolist() if not item.filename.endswith("/")]
   assert members and all(m.safe_archive_member(item.filename) and item.filename.lower().endswith(".png") for item in members)
 print("TEST201 candidate HTTP size/SHA, multipart reassembly and ZIP integrity: PASS (130E/160E/192E/235E black)")
else:
 print("TEST201 publication-root regression via receiver URL validator: PASS")
