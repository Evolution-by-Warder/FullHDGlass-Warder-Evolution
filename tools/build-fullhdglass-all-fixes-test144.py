#!/usr/bin/env python3
"""Full FullHDGlass TEST144: first-boot HTTPS catalog on PATHS, zero world bytes in flash."""
import importlib.util
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("full_skin_test144_base",
    ROOT/"tools/build-fullhdglass-all-fixes-test139.py")
base=importlib.util.module_from_spec(spec)
spec.loader.exec_module(base)

VERSION="1.0.81-test144"
base.VERSION=VERSION
base.mod.RUNTIME_VERSION=VERSION
base.mod.PACKAGE_VERSION=VERSION+"-1"
base.mod.OUT_DIR=ROOT/"packages/fullhdglass-all-fixes-test144"
_source_control=base.mod.check_sources
def _clean_control_label():
    return _source_control().replace(
        "RADIO LIVE TEST138 - receiver trial",
        "Full skin TEST144 - external radio catalog and safe opkg upgrade")
base.mod.check_sources=_clean_control_label
plugin=base.mod.PLUGIN
extras={plugin+"/"+name for name in (
  "warderRadioCountry.py","warderRadioSingleCountry.py",
  "warderRadioBundleFetch.py","warderRadioCountryCleanup.py",
  "warderRadioWorld.py","warderRadioPackages.py","warderRadioOnlineLogos.py")}
base.more.update(extras)
base.mod.REQUIRED |= extras

def main():
    # Absolute rule: the 6,664,493 B world belongs on external PATHS.
    world=base.mod.SOURCE/"usr/share/enigma2/hd_glass17/radio-world/radio-countries-bouquets.zip"
    if world.exists():
        raise RuntimeError("World ZIP must never ship in receiver's internal flash")
    post=(ROOT/"source/control/postinst").read_text()
    pre=(ROOT/"source/control/preinst").read_text()
    if ('rm -f "$warder_bytecode"' in post or
            'warder_repair_tracked_missing_bytecode' not in pre):
        raise RuntimeError("Unsafe old opkg Python cache deletion still present")
    base.run()
    dest=base.mod.OUT_DIR
    manifest_path=dest/"fullhdglass-1.0.81-test139-manifest.json"
    doc=json.loads(manifest_path.read_text())
    assert doc["runtime_version"]==VERSION
    assert doc["package_version"]==VERSION+"-1"
    assert extras<=set(doc["bridge_files"])
    assert doc["size_bytes"]<22*1024*1024, "Unnecessarily huge TEST144 IPK"
    doc.update({
      "test_only":True,
      "version":VERSION,
      "production_modified":False,
      "initial_radio_country":"Enigma2 OSD language, only one radio live bouquet",
      "future_radio_country":"Saved explicit user choice; retained across restart",
      "radio_world_download":"Signed HTTPS world downloaded to configured external PATHS on first start",
      "world_sha256":"771953b41ceab46f8852f5e3219338cb1369d7f653ed7d329ad551e481f88d68",
      "world_country_count":224,
      "world_stations":48219,
      "approved_country_original_png":40837,
      "radio_logo_download":"One signed original selected country ZIP from immutable TEST release",
      "old_country_logo_cleanup":"Only SHA-owned and unmodified PNG are deleted; TV/SAT and user PNG protected",
      "opkg_upgrade_fix":"No premature Python .pyc deletion; only missing tracked CPython 3.13 .pyc stubs restored",
      "world_archive_bundled_in_ipk":False,
      "manual_world_test_data_zip_required":False
    })
    (dest/("fullhdglass-"+VERSION+"-manifest.json")).write_text(
        json.dumps(doc,ensure_ascii=False,sort_keys=True,indent=2)+"\n")
    manifest_path.unlink()
    print("COMPLETE FULLHDGLASS TEST144",doc["sha256"],doc["size_bytes"],flush=True)
if __name__=="__main__":
    main()
