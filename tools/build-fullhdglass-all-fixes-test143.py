#!/usr/bin/env python3
"""FullHDGlass TEST143: complete skin, real 224-country world and safe curated radio ZIP delivery."""
import importlib.util,hashlib,json
from pathlib import Path
from zipfile import ZipFile

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("fullhdglass143",ROOT/"tools/build-fullhdglass-all-fixes-test139.py")
base=importlib.util.module_from_spec(spec)
spec.loader.exec_module(base)
VERSION="1.0.81-test143"
base.VERSION=VERSION
base.mod.RUNTIME_VERSION=VERSION
base.mod.PACKAGE_VERSION=VERSION+"-1"
base.mod.OUT_DIR=ROOT/"packages/fullhdglass-all-fixes-test143"
root=base.mod.PLUGIN
world_file="usr/share/enigma2/hd_glass17/radio-world/radio-countries-bouquets.zip"
world_sha="771953b41ceab46f8852f5e3219338cb1369d7f653ed7d329ad551e481f88d68"
extras={root+"/"+name for name in ("warderRadioCountry.py","warderRadioSingleCountry.py",
    "warderRadioBundledWorld.py","warderRadioWorld.py","warderRadioBundleFetch.py",
    "warderRadioCountryCleanup.py","warderRadioPackages.py","warderRadioOnlineLogos.py")}
extras.add(world_file)
base.more.update(extras)
base.mod.REQUIRED |= extras

def main():
    src=base.mod.SOURCE/world_file
    if not src.is_file() or src.is_symlink() or hashlib.sha256(src.read_bytes()).hexdigest()!=world_sha:
        raise ValueError("Missing or modified signed 224-country source world")
    with ZipFile(src) as z:
        idx=json.loads(z.read("index.json"))
    if (idx.get("country_count"),idx.get("station_count"),
        sum(c.get("logos_found",0) for c in idx["countries"].values()))!=(224,48219,40837):
        raise ValueError("Incorrect verified country and PNG inventory")
    base.run()
    dest=base.mod.OUT_DIR
    old=dest/"fullhdglass-1.0.81-test139-manifest.json"
    meta=json.loads(old.read_text())
    if meta.get("runtime_version")!=VERSION or not extras<=set(meta["bridge_files"]):
        raise ValueError("Incomplete complete-skin package content")
    meta.update(test_only=True,production_modified=False,reviewed_logos=40837,
        source_countries=224,source_stations=48219,radio_world_sha256=world_sha,
        active_country="OSD language initially, remembered user's choice afterwards",
        logo_destination="configured PATHS/picon/radio/CC",
        downloaded_old_country_cleanup="only verified Warder-owned PNGs",
        external_test_data_zip_required=False,
        source="signed 224-country TEST release radio-country-20261122")
    dest.joinpath("fullhdglass-"+VERSION+"-manifest.json").write_text(
        json.dumps(meta,ensure_ascii=False,indent=2,sort_keys=True)+"\n")
    old.unlink()
    print("COMPLETE TEST143",meta["sha256"],meta["size_bytes"],flush=True)
if __name__=="__main__":main()
