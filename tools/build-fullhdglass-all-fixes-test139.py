#!/usr/bin/env python3
"""Build FULL FullHDGlass Warder 1.0.81-test139 from current PR129 runtime.

No production files or update feeds are changed. Uses the existing proven
package builder for ALL owned skin/plugin assets, not a radio-only subset.
"""
import importlib.util
import json
from pathlib import Path
import re

ROOT=Path(__file__).resolve().parents[1]
mod_path=ROOT/"tools/build-radio-live-test-ipk.py"
spec=importlib.util.spec_from_file_location("fullhdglass_radio_live_builder",mod_path)
mod=importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

VERSION="1.0.81-test139"
mod.RUNTIME_VERSION=VERSION
mod.PACKAGE_VERSION=VERSION+"-1"
mod.OUT_DIR=ROOT/"packages/fullhdglass-all-fixes-test139"
more={
  mod.PLUGIN+"/warderRadioWorld.py",
  mod.PLUGIN+"/warderRadioPackages.py",
  mod.PLUGIN+"/warderRadioBundleFetch.py",
  mod.PLUGIN+"/warderStorageSafety.py",
  mod.PLUGIN+"/warderSettingsMenuPlacement.py",
  mod.PLUGIN+"/warderSpinnerScreen.py",
  "usr/lib/enigma2/python/Components/Renderer/WarderChannelEpgClip.py",
  "usr/share/enigma2/hd_glass17/skin.xml",
}
mod.REQUIRED=mod.REQUIRED|more

def run():
    # Explicitly refuse future base drift or staging any incomplete source.
    assert mod.check_sources()
    mod.main()
    old=mod.OUT_DIR/"radio-live-test138-manifest.json"
    data=json.loads(old.read_text(encoding="utf-8"))
    assert data["runtime_version"]==VERSION
    assert data["package_version"]==VERSION+"-1"
    assert data["package"]==mod.PACKAGE_ID
    path=mod.OUT_DIR/(mod.PKG_NAME+"_"+VERSION+"_all.ipk")
    assert path.is_file() and path.stat().st_size<48*1024*1024
    # Hard requirement: all committed FullHDGlass resources included, except
    # original source locales and four unapproved menu graphics by policy.
    from io import BytesIO
    import subprocess,tarfile
    raw=subprocess.check_output(["ar","p",str(path),"data.tar.gz"])
    with tarfile.open(fileobj=BytesIO(raw),mode="r:gz") as tar:
        names=set(name.removeprefix("./") for name in tar.getnames())
        assert more<=names,sorted(more-names)
        icon_prefix="usr/share/enigma2/hd_glass17/icons_factory/"
        assert len([n for n in names if n.startswith(icon_prefix) and n.endswith(".png")])==148
        assert not any("__pycache__" in n or n.endswith((".pyc",".pyo")) for n in names)
        assert not any(Path(n).name in mod.BLOCKED_GRAPHICS for n in names)
        assert tar.extractfile("./"+mod.VERSION_REL).read().decode().strip()==VERSION
    data.update({
      "test_only":True,
      "source_branch":"feature/radio-live-world-bundle-installer-20261119",
      "baseline":"FullHDGlass 1.0.80 plus all committed PR129 receiver improvements",
      "payload_type":"full_skin_and_setupGlass17",
      "radio_world_assets":"External 224-country RADIO REVIEW only; never bundled in IPK",
      "production_modified":False,
      "missing_uncommitted_artwork_not_claimed":True
    })
    out=mod.OUT_DIR/"fullhdglass-1.0.81-test139-manifest.json"
    out.write_text(json.dumps(data,sort_keys=True,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    old.unlink()
    print("FULL SKIN TEST139 BUILT",path,"bytes",path.stat().st_size,
          "files",data["file_count"],"sha256",data["sha256"],flush=True)

if __name__=="__main__":
    run()
