#!/usr/bin/env python3
"""Validate the two-phase channel-picon cut-over safety contract."""
from pathlib import Path
import json, sys
ROOT=Path(__file__).resolve().parents[1]
build=json.loads((ROOT/"assets/warder/channel-picon-build.json").read_text())
plan=json.loads((ROOT/"assets/warder/channel-picon-publication-plan.json").read_text())
plugin=(ROOT/"source/package-root/usr/lib/enigma2/python/Plugins/Extensions/setupGlass17/plugin.py").read_text(encoding="utf-8")
runtime=(ROOT/"source/package-root/usr/lib/enigma2/python/Plugins/Extensions/setupGlass17/warderPiconSync.py").read_text(encoding="utf-8")
errors=[]
legacy_resolver="url = self._legacyPiconArchiveUrl(k[x][1])"
if build.get("state")=="BUILT_NOT_PUBLISHED":
    if build.get("runtime_cutover") is not False: errors.append("unpublished build cannot enable runtime cutover")
    if legacy_resolver not in plugin: errors.append("preserved legacy resolver missing before persistent publication")
if plan.get("publication_performed") is False and legacy not in plugin:
    errors.append("prepared-only plan must retain legacy fallback")
if build.get("state")=="PUBLISHED":
    p=build.get("publication",{})
    if p.get("state")!="PUBLISHED" or p.get("persistent") is not True: errors.append("PUBLISHED requires persistent evidence")
runtime_cutover=bool(build.get("runtime_cutover"))
publication=build.get("publication",{})
code_enabled="RUNTIME_PUBLICATION_ENABLED = True" in runtime
if code_enabled != runtime_cutover:
    errors.append("runtime code switch must exactly match recorded runtime_cutover")
if not runtime_cutover and 'RUNTIME_MANIFEST_URL = ""' not in runtime:
    errors.append("locked runtime must not advertise a manifest URL")
if not runtime_cutover and "RUNTIME_PUBLICATION_ENABLED = False" not in runtime:
    errors.append("locked runtime must explicitly disable Warder publication")
if not runtime_cutover and "RUNTIME_PUBLICATION_ENABLED = True" in runtime:
    errors.append("locked runtime contains an enabled Warder publication switch")
if runtime_cutover:
    if build.get("state")!="PUBLISHED":
        errors.append("runtime cutover requires build state PUBLISHED")
    if publication.get("state")!="PUBLISHED" or publication.get("persistent") is not True:
        errors.append("runtime cutover requires persistent published backend")
    if not publication.get("manifest_url") or not publication.get("base_url"):
        errors.append("runtime cutover requires manifest/base URLs")
    if plan.get("publication_performed") is not True:
        errors.append("runtime cutover requires completed publication plan")
    # This validator runs on warder-modernization-work: its TEST runtime must
    # consume the separately persisted, validated candidate, while production
    # publication evidence continues to point at stable main.
    candidate_url="https://raw.githubusercontent.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/warder-modernization-work/assets/warder/downloads/picons/channels/test-candidate/manifest.json"
    if ('RUNTIME_MANIFEST_URL = "'+candidate_url+'"') not in runtime:
        errors.append("TEST runtime must consume the work-branch candidate manifest")
    candidate_path=ROOT/"assets/warder/downloads/picons/channels/test-candidate"
    candidate_manifest=candidate_path/"manifest.json"
    if not candidate_manifest.is_file():
        errors.append("persisted TEST candidate manifest is missing")
    else:
        try:
            cm=json.loads(candidate_manifest.read_text(encoding="utf-8"))
            packages=cm.get("packages",[])
            if len(packages)!=120:
                errors.append("TEST candidate must contain 120 generic packages")
            expected={"160E":("16.0e",2),"08W":("0.8w",3)}
            for selector,(position,excluded_count) in expected.items():
                rows=[p for p in packages if p.get("selector_id")==selector]
                if len(rows)!=3 or any(p.get("orbital_position")!=position for p in rows):
                    errors.append("TEST generic candidate has wrong binding/family coverage for "+selector)
                if any(len(p.get("ambiguous_exclusions",[]))!=excluded_count for p in rows):
                    errors.append("TEST generic candidate has wrong ambiguous exclusion count for "+selector)
            part_names={u.rsplit("/",1)[-1] for p in packages for u in p.get("parts",[])}
            disk_parts={p.name for p in candidate_path.glob("*.part*")}
            if not part_names or part_names!=disk_parts:
                errors.append("TEST candidate manifest part coverage differs from persisted files")
        except Exception as exc:
            errors.append("TEST candidate manifest is invalid: "+str(exc))
else:
    # Before the reviewed runtime switch, the preserved pinned legacy resolver remains mandatory.
    if legacy not in plugin:
        errors.append("legacy fallback removed before reviewed runtime cutover")
# Deliberately do not auto-enable runtime cutover here: publication and runtime switch are separate reviewed changes.
if errors:
    for e in errors: print("ERROR:",e)
    sys.exit(1)
print("PASS two-phase cut-over safety: publication and runtime switch are state-consistent and separately validated")
