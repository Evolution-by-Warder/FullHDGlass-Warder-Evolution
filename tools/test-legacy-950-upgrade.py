#!/usr/bin/env python3
"""Regression tests for guarded native upgrades from the original 9.50 family."""
from pathlib import Path
import os
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
PREINST = ROOT / "source/control/preinst"


class Legacy950UpgradeTests(unittest.TestCase):
    def prepare(self, root, with_prerm=False):
        info = root / "var/lib/opkg/info"
        info.mkdir(parents=True)
        old = info / "enigma2-skin-fullhdglass17.postrm"
        original = b'#!/bin/sh\nprintf "%s\\n" "$1" >> "' + str(root / "removed.log").encode() + b'"\n'
        old.write_bytes(original)
        old.chmod(0o755)
        if with_prerm:
            (info / "enigma2-skin-fullhdglass17.prerm").write_text("#!/bin/sh\nexit 0\n")
        bindir = root / "bin"
        bindir.mkdir()
        opkg = bindir / "opkg"
        opkg.write_text("#!/bin/sh\nprintf '%s\\n' 'Package: enigma2-skin-fullhdglass17' 'Status: install ok installed'\n")
        opkg.chmod(0o755)
        skin = root / "usr/share/enigma2/skin_default.xml"
        skin.parent.mkdir(parents=True)
        skin.write_text("<skin><parameters/></skin>\n")
        settings = root / "etc/enigma2/settings"
        settings.parent.mkdir(parents=True)
        settings.write_text("config.skin.primary_skin=hd_glass17/skin.xml\ncustom=user\n")
        script = PREINST.read_text()
        for prefix in ("/etc/", "/usr/", "/var/", "/tmp/"):
            script = script.replace(prefix, str(root) + prefix)
        fake_preinst = root / "preinst"
        fake_preinst.write_text(script)
        fake_preinst.chmod(0o755)
        env = dict(os.environ, PATH=str(bindir) + ":" + os.environ.get("PATH", ""))
        return fake_preinst, old, original, settings, env

    def test_known_and_unknown_950_revisions_guard_upgrade_not_remove(self):
        for version in ("9.50", "9.50-r12", "9.50-r12.2", "9.50-r99"):
            with self.subTest(version=version), tempfile.TemporaryDirectory() as td:
                root = Path(td)
                preinst, old, original, settings, env = self.prepare(root)
                result = subprocess.run(["sh", "-x", str(preinst), "upgrade", version],
                                        env=env, capture_output=True, text=True)
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                self.assertIn("Verified legacy upgrade preparation completed.", result.stdout)
                self.assertEqual((Path(str(old) + ".warder-original")).read_bytes(), original)
                self.assertEqual(settings.read_text(), "config.skin.primary_skin=hd_glass17/skin.xml\ncustom=user\n")
                run = subprocess.run(["sh", str(old), "upgrade"], check=True)
                self.assertFalse((root / "removed.log").exists())
                subprocess.run(["sh", str(old), "remove"], check=True)
                self.assertEqual((root / "removed.log").read_text(), "remove\n")
                again = subprocess.run(["sh", str(preinst), "upgrade", version],
                                       env=env, capture_output=True, text=True)
                self.assertEqual(again.returncode, 0, again.stdout + again.stderr)
                self.assertEqual((Path(str(old) + ".warder-original")).read_bytes(), original)

    def test_non_950_version_not_automatically_admitted(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            preinst, old, original, settings, env = self.prepare(root)
            result = subprocess.run(["sh", str(preinst), "upgrade", "9.49"],
                                    env=env, capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertEqual(old.read_bytes(), original)
            self.assertFalse(Path(str(old) + ".warder-original").exists())

    def test_unknown_prerm_blocks_instead_of_bypassing(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            preinst, old, original, settings, env = self.prepare(root, with_prerm=True)
            result = subprocess.run(["sh", str(preinst), "upgrade", "9.50-r12"],
                                    env=env, capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertEqual(old.read_bytes(), original)


if __name__ == "__main__":
    unittest.main()
