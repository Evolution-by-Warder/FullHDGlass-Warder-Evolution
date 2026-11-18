"""Receiver-reported 1.0.80-2 upgrade: preserve four unrecognized Warder tail frames.

The real receiver reported 20 recognized frames and unmatched wait21..wait24.
Never delete non-catalogued bytes; save the entire mixed set outside the active
spinner directory before allowing native-image fallback or another theme.
"""
import importlib.util
import os
from pathlib import Path
import shutil
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "source/package-root/usr/lib/enigma2/python/Plugins/Extensions/setupGlass17"
SOURCE = ROOT / "source/package-root/usr/share/enigma2/hd_glass17"
spec = importlib.util.spec_from_file_location("spinner_mixed_receiver_regression", PLUGIN / "warderSpinner.py")
spinner = importlib.util.module_from_spec(spec)
spec.loader.exec_module(spinner)


def files(path):
    return {f.name: f.read_bytes() for f in path.iterdir()}


def foreign_tail(index):
    # Representative old, previously installed custom PNG: never regenerate
    # or delete these unknown bytes; only check real PNG signature in backend.
    return b"\x89PNG\r\n\x1a\n" + b"old-warder-frame-" + str(index).encode() + b"x" * 64


class UpgradeOverlayPreservationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "hd_glass17"
        self.root.mkdir()
        shutil.copytree(SOURCE / "spinner-themes", self.root / "spinner-themes")
        shutil.copytree(SOURCE / "spinner", self.root / "spinner")
        self.original = files(self.root / "spinner")

    def mix(self):
        for i in range(21, 25):
            (self.root / "spinner" / ("wait%d.png" % i)).write_bytes(foreign_tail(i))
        self.mixed = files(self.root / "spinner")
        self.assertEqual(len(self.mixed), 24)

    def backups(self):
        return sorted(self.root.glob(".warder-spinner-preserved-*"))

    def test_system_fallback_preserves_all_24_actual_bytes(self):
        self.mix()
        system = Path(self.temp.name) / "skin_default" / "spinner"
        system.mkdir(parents=True)
        (system / "wait1.png").write_bytes(b"image-owned")
        self.assertTrue(spinner.apply("system", self.root))
        self.assertFalse((self.root / "spinner").exists())
        self.assertEqual(len(self.backups()), 1)
        self.assertEqual(files(self.backups()[0]), self.mixed)
        self.assertEqual((system / "wait1.png").read_bytes(), b"image-owned")
        self.assertFalse(spinner.apply("system", self.root))
        # After the switch the owner can still choose packaged Warder 24 frames.
        self.assertTrue(spinner.apply("warder", self.root))
        self.assertEqual(files(self.backups()[0]), self.mixed)
        self.assertEqual(files(self.root / "spinner"), files(self.root / "spinner-themes/warder"))

    def test_switch_to_other_theme_preserves_mixed_set(self):
        self.mix()
        self.assertTrue(spinner.apply("dove", self.root))
        self.assertEqual(files(self.root / "spinner"), files(self.root / "spinner-themes/dove"))
        self.assertEqual(files(self.backups()[0]), self.mixed)
        self.assertFalse((self.root / ".warder-spinner-previous").exists())

    def test_failure_after_backup_move_restores_every_original_byte(self):
        self.mix()
        rename = os.rename
        def interrupted(src, dest):
            if Path(src).name.startswith(".warder-spinner-stage-"):
                raise OSError("injected error")
            return rename(src, dest)
        with patch.object(spinner.os, "rename", side_effect=interrupted):
            with self.assertRaises(OSError):
                spinner.apply("dove", self.root)
        self.assertEqual(files(self.root / "spinner"), self.mixed)
        self.assertFalse(self.backups())
        self.assertFalse(list(self.root.glob(".warder-spinner-stage-*")))

    def test_original_personal_image_or_extra_file_is_never_moved(self):
        self.mix()
        (self.root / "spinner" / "wait1.png").write_bytes(b"PERSONAL-IMAGE")
        before = files(self.root / "spinner")
        with self.assertRaises(ValueError):
            spinner.apply("system", self.root)
        self.assertEqual(files(self.root / "spinner"), before)
        self.assertFalse(self.backups())
        # A random user-owned text file must also fail closed.
        (self.root / "spinner" / "wait1.png").write_bytes(self.original["wait1.png"])
        (self.root / "spinner" / "notes.txt").write_text("personal")
        with self.assertRaises(ValueError):
            spinner.apply("system", self.root)
        self.assertFalse(self.backups())

    def test_symlinked_tail_is_not_taken_as_receiver_upgrade(self):
        self.mix()
        tail = self.root / "spinner" / "wait24.png"
        raw = tail.read_bytes()
        tail.unlink()
        outside = self.root / "private.png"
        outside.write_bytes(raw)
        tail.symlink_to(outside)
        with self.assertRaises(ValueError):
            spinner.apply("system", self.root)
        self.assertTrue(tail.is_symlink())
        self.assertFalse(self.backups())

    def test_previous_recovery_cannot_be_overwritten(self):
        self.mix()
        old = self.root / ".warder-spinner-preserved-01"
        old.mkdir()
        (old / "precious").write_bytes(b"preexisting")
        self.assertTrue(spinner.apply("system", self.root))
        self.assertEqual((old / "precious").read_bytes(), b"preexisting")
        self.assertEqual(files(self.root / ".warder-spinner-preserved-02"), self.mixed)

    def test_recognized_original_packaged_20_still_uses_normal_switch(self):
        self.assertTrue(spinner.apply("system", self.root))
        self.assertFalse(self.backups())
        self.assertFalse((self.root / "spinner").exists())

if __name__ == "__main__":
    unittest.main()
