#!/usr/bin/env python3
"""Package-category and state-preservation regression coverage."""
import importlib.util
import json
from pathlib import Path
import os
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "source/package-root/usr/lib/enigma2/python/Plugins/Extensions/setupGlass17/warderPackageTransition.py"
spec = importlib.util.spec_from_file_location("transition_tests", PATH)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class TransitionTests(unittest.TestCase):
    def test_native_package_is_classified_as_installed_skin(self):
        control = dict(line.split(": ", 1) for line in (ROOT / "source/control/control").read_text().splitlines() if ": " in line)
        package = control["Package"]
        self.assertEqual(package.split("-", 3)[2:], ["skins", "fullhdglass-warder-evolution"])
        self.assertEqual(control["Section"], "skins")
        self.assertEqual(control["Provides"], "enigma2-skin-fullhdglass17")
        for field in ("Replaces", "Conflicts"):
            self.assertEqual(control[field], "enigma2-skin-fullhdglass17 (>= 1.0.18-1)")
        self.assertTrue((ROOT / "source/package-root/usr/share/enigma2/hd_glass17/skin.xml").is_file())

    def test_overlay_state_and_original_backups_survive_legacy_removal(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            expected = {}
            for number, path in enumerate(module.FILES):
                value = ("user state %s" % number).encode()
                target = module.local(root, path)
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(value)
                expected[path] = value
            settings = root / "etc/enigma2/settings"
            settings.write_bytes(b"config.skin.primary_skin=hd_glass17/skin.xml\ncustom=user\n")
            module.backup(root)
            # Model removal of package-owned files and the legacy postrm's
            # restoration/consumption of the original backup files.
            for path in module.FILES:
                module.local(root, path).unlink()
            module.restore(root)
            for path, value in expected.items():
                self.assertEqual(module.local(root, path).read_bytes(), value, path)
            self.assertEqual(settings.read_bytes(), b"config.skin.primary_skin=hd_glass17/skin.xml\ncustom=user\n")
            self.assertFalse(module.local(root, module.STATE).exists())
            module.restore(root)  # repeated configure is harmless

    def test_symlink_overlay_is_restored_as_the_original_link(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            target = module.local(root, module.FILES[0])
            target.parent.mkdir(parents=True)
            target.symlink_to("custom-overlay.xml")
            module.backup(root)
            target.unlink()
            target.write_text("new default")
            module.restore(root)
            self.assertTrue(target.is_symlink())
            self.assertEqual(os.readlink(str(target)), "custom-overlay.xml")

    def test_corrupt_snapshot_cannot_partially_replace_receiver_state(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            target = module.local(root, module.FILES[0])
            target.parent.mkdir(parents=True)
            target.write_text("user overlay")
            module.backup(root)
            (module.local(root, module.STATE) / "0").write_text("corrupted")
            target.write_text("installed default")
            with self.assertRaises(ValueError):
                module.restore(root)
            self.assertEqual(target.read_text(), "installed default")
            self.assertTrue(module.local(root, module.STATE).exists())

    def test_unlisted_snapshot_path_is_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            folder = module.local(temp, module.STATE)
            folder.mkdir(parents=True)
            (folder / "manifest.json").write_text(json.dumps({"schema": 1, "entries": [{"path": "/etc/passwd", "link": "bad"}]}))
            with self.assertRaises(ValueError):
                module.restore(temp)

    def test_native_install_refuses_an_unprepared_legacy_package(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            bindir = root / "bin"
            bindir.mkdir()
            opkg = bindir / "opkg"
            opkg.write_text("#!/bin/sh\nprintf '%s\\n' 'Package: enigma2-skin-fullhdglass17' 'Status: install ok installed'\n")
            opkg.chmod(0o755)
            skin = root / "usr/share/enigma2/skin_default/skin.xml"
            skin.parent.mkdir(parents=True)
            skin.write_text("parameters")
            script = (ROOT / "source/control/preinst").read_text()
            for prefix in ("/etc/", "/usr/", "/var/", "/tmp/"):
                script = script.replace(prefix, str(root) + prefix)
            result = subprocess.run(["sh", "-c", script, "preinst", "install"],
                                    env=dict(os.environ, PATH=str(bindir) + ":" + os.environ["PATH"]),
                                    capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("verified transition", result.stdout)


if __name__ == "__main__":
    unittest.main()

