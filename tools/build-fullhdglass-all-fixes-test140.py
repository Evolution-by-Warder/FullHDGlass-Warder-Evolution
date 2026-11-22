#!/usr/bin/env python3
"""One full skin 1.0.81-test140 IPK: all owned committed skin fixes, 224 native
country bouquets, external verified source data and bounded online-logo fallback.

Does NOT package a half-gigabyte original-logo library in Enigma flash.
"""
import importlib.util,json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("warder_skin_builder",ROOT/"tools/build-fullhdglass-all-fixes-test139.py")
base=importlib.util.module_from_spec(spec)
spec.loader.exec_module(base)
VERSION="1.0.81-test140"
base.VERSION=VERSION
base.mod.RUNTIME_VERSION=VERSION
base.mod.PACKAGE_VERSION=VERSION+"-1"
base.mod.OUT_DIR=ROOT/"packages/fullhdglass-all-fixes-test140"
runtime=base.mod.PLUGIN
extras={
    runtime+"/warderRadioCountryBouquets.py",
    runtime+"/warderRadioOnlineLogos.py",
    runtime+"/warderRadioLocalTestAssets.py",
}
base.more.update(extras)
base.mod.REQUIRED|=extras
def main():
    base.run()
    output=base.mod.OUT_DIR
    old=output/"fullhdglass-1.0.81-test139-manifest.json"
    if not old.is_file():raise RuntimeError("Source test builder manifest missing")
    result=json.loads(old.read_text())
    assert result["runtime_version"]==VERSION
    assert result["package_version"]==VERSION+"-1"
    assert set(extras)<=set(result["bridge_files"])
    result.update(
        contains_real_independent_224_bouquets=True,
        external_test_world_sha256="771953b41ceab46f8852f5e3219338cb1369d7f653ed7d329ad551e481f88d68",
        external_mexico_picon_sha256="3b002149bfe8f132c3b368e00246a34d6dd462ee0fbc312b7d259daf7ff60eff",
        external_test_bundle_required_for_exact_curated_logos=True,
        other_country_original_zip_count_prebundled=0,
        original_40837_logo_library_bundled_in_flash=False,
        managed_country_list=224,
        artwork_fallback="on-demand verified Radio Browser station favicon per country",
        release_type="test-only",
        production_feed_modified=False
    )
    dest=output/("fullhdglass-"+VERSION+"-manifest.json")
    dest.write_text(json.dumps(result,indent=2,sort_keys=True,ensure_ascii=False)+"\n")
    old.unlink()
    print("FULLHDGLASS ALL AVAILABLE COMMITTED FIXES AND 224 COUNTRIES",VERSION,
          result['sha256'],result['size_bytes'],flush=True)
if __name__=="__main__":main()
