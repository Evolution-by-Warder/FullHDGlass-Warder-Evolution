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

VERSION = "1.0.81-test148"
base.VERSION = VERSION
base.base.VERSION = VERSION
base.base.mod.RUNTIME_VERSION = VERSION
base.base.mod.PACKAGE_VERSION = VERSION + "-1"
base.base.mod.OUT_DIR = ROOT / "packages/fullhdglass-unified-radio-test148"

plugin = base.base.mod.PLUGIN
required_saver = {plugin + "/" + name for name in (
    "plugin.py", "screenSaver.py", "warderRadioSaverController.py",
    "warderRadioSaverLayout.py")}
base.base.mod.REQUIRED |= required_saver
base.base.more.update(required_saver)

# The TEST147 builder is intentionally reused, but its public package
# description must identify this as the TEST148 saver receiver trial.
_control = base.base.mod.check_sources
def _test148_control():
    return _control().replace(
        "Full skin TEST147 - external radio catalog and safe opkg upgrade",
        "Full skin TEST148 - unified RADIO OLED saver receiver trial")
base.base.mod.check_sources = _test148_control


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
        "feature": "Unified OLED radio saver for DVB, DAB and IPTV audio",
        "source_branch": "feature/unified-radio-screensaver-20261122",
        "pull_request": 130,
        "test_only": True,
        "production_modified": False,
        "saver_delays": [0, 10, 20, 30, 60],
        "receiver_validation": "pending",
    })
    manifest_path.write_text(
        json.dumps(manifest, sort_keys=True, indent=2, ensure_ascii=False)+"\n",
        encoding="utf-8")
    print("FULL SKIN TEST148", package_path, manifest["size_bytes"],
          manifest["sha256"], flush=True)


if __name__ == "__main__":
    main()
