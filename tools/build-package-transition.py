#!/usr/bin/env python3
"""Build and verify the legacy-identity bridge before the native skin package."""
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
PLUGIN = "source/package-root/usr/lib/enigma2/python/Plugins/Extensions/setupGlass17"
OLD = "enigma2-skin-fullhdglass17"
NEW = "enigma2-plugin-skins-fullhdglass-warder-evolution"


def main():
    approval = json.loads((ROOT / "docs/PRODUCTION-APPROVAL.json").read_text())
    target = approval["production_version"]
    bridge = approval["transition_version"]
    with tempfile.TemporaryDirectory(prefix="warder-bridge-") as temp:
        root = Path(temp)
        for folder in ("source", "tools", "design"):
            shutil.copytree(str(ROOT / folder), str(root / folder), ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
        for name in ("update.json", "update-test.json"):
            shutil.copy2(str(ROOT / name), str(root / name))
        gitdir = subprocess.check_output(["git", "rev-parse", "--absolute-git-dir"], cwd=ROOT, text=True).strip()
        (root / ".git").write_text("gitdir: " + gitdir + "\n")
        plugin = root / PLUGIN
        for name in ("plugin.py", "warderDialogSkins.py"):
            path = plugin / name
            path.write_text(path.read_text().replace(target, bridge))
        (plugin / "version").write_text(bridge + "\n")
        path = root / "source/control/control"
        lines = [line for line in path.read_text().splitlines() if not line.startswith(("Conflicts:", "Replaces:", "Provides:"))]
        path.write_text("\n".join(lines).replace("Package: " + NEW, "Package: " + OLD).replace("Version: " + target + "-1", "Version: " + bridge + "-1") + "\n")
        path = root / "source/control/preinst"
        path.write_text(path.read_text().replace("WARDER_PACKAGE_ID=" + NEW, "WARDER_PACKAGE_ID=" + OLD))
        subprocess.run(["python3", str(root / "tools/build-setup-style-test.py")], cwd=root, check=True)
        subprocess.run(["python3", str(root / "tools/verify-setup-style-ipk.py")], cwd=root, check=True)
        output = ROOT / "packages/bridge"
        output.mkdir(parents=True, exist_ok=True)
        for path in (root / "packages/test").iterdir():
            shutil.copy2(str(path), str(output / path.name))
        print("Verified transition package:", bridge)


if __name__ == "__main__":
    main()

