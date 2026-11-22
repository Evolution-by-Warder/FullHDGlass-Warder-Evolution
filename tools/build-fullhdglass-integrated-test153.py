#!/usr/bin/env python3
"""Build a full, test-only FullHDGlass IPK with the unified radio screensaver.

Reuses the receiver-tested TEST147 package recipe. Never touches production
feeds/releases or bundles the 224-country archive into receiver flash.
"""
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location(
    "warder_test147", ROOT / "tools/build-fullhdglass-all-fixes-test147.py")
base = importlib.util.module_from_spec(spec)
spec.loader.exec_module(base)

VERSION = "1.0.81-test153"
base.VERSION = VERSION
base.base.VERSION = VERSION
base.base.mod.RUNTIME_VERSION = VERSION
base.base.mod.PACKAGE_VERSION = VERSION + "-1"
base.base.mod.OUT_DIR = ROOT / "packages/fullhdglass-unified-radio-test153"

plugin = base.base.mod.PLUGIN
required_saver = {plugin + "/" + name for name in (
    "plugin.py", "screenSaver.py", "warderRadioSaverController.py",
    "warderRadioSaverLayout.py", "warderRadioRds.py")}
base.base.mod.REQUIRED |= required_saver
base.base.more.update(required_saver)

# The TEST147 builder is intentionally reused, but its public package
# description must identify this as the TEST153 saver receiver trial.
_control = base.base.mod.check_sources
def _test153_control():
    return _control().replace(
        "Full skin TEST147 - external radio catalog and safe opkg upgrade",
        "Full skin TEST153 - unified RADIO OLED saver receiver trial")
base.base.mod.check_sources = _test153_control


def main():
    # All tests below must be run with the pinned branch payload, not a
    # hand-picked two-file overlay of unknown installed version.
    base.main()
    destination = base.base.mod.OUT_DIR
    package_path = destination / (
        "enigma2-plugin-skins-fullhdglass_" + VERSION + "_all.ipk")
    manifest_path = destination / ("fullhdglass-" + VERSION + "-manifest.json")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert manifest["runtime_version"] == VERSION
    assert manifest["package_version"] == VERSION + "-1"
    assert required_saver <= set(manifest["bridge_files"])
    assert manifest["size_bytes"] < 22 * 1024 * 1024
    assert manifest["world_archive_bundled_in_ipk"] is False
    assert package_path.is_file()
    manifest.update({
        "feature": "Consolidated skin repairs, Radio Live, DVB/DAB/IPTV OLED saver, IPTV InfoBar channel-name fallback",
        "source_branch": "integration/fullhdglass-all-approved-radio-20261122",
        "base_main_sha": "7e72d6e2b6d70eeb095b770d34430b3f53af9a2b",
        "preserves_main_satellite_picon_catalogue": True,
        "full_compatibility_validation": "pending",
        "pull_request": 131,
        "test_only": True,
        "production_modified": False,
        "saver_delays": [0, 10, 20, 30, 60],
        "receiver_validation": "pending",
        "live_saver_station_logo": "same signed active-country picon resolver as native ServiceList",
    })
    manifest_path.write_text(
        json.dumps(manifest, sort_keys=True, indent=2, ensure_ascii=False)+"\n",
        encoding="utf-8")
    print("FULL SKIN TEST153", package_path, manifest["size_bytes"],
          manifest["sha256"], flush=True)


if __name__ == "__main__":
    main()
