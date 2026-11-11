#!/usr/bin/env python3
"""Regressions: own channel picons are read-only and independent of download paths."""
import importlib.util
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace as NS

ROOT = Path(__file__).resolve().parents[1]
HELPER = ROOT / "source/package-root/usr/lib/enigma2/python/Plugins/Extensions/setupGlass17/warderUserPicons.py"
CHANNELS = ROOT / "source/package-root/usr/lib/enigma2/python/Plugins/Extensions/setupGlass17/warderChannelPicons.py"

def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

user = load("warderUserPicons", HELPER)
channels = load("warderChannelPicons", CHANNELS)

class OwnPiconTests(unittest.TestCase):
    def settings(self, enabled=False, path="", expert=False, expert_path=""):
        v = lambda x: NS(value=x)
        return NS(plugins=NS(
            warderUserPicons=NS(enabled=v(enabled), path=v(path)),
            warderPiconExpert=NS(custom_destination=v(expert),
                                destination=v(expert_path))))

    def test_disabled_defaults_to_warder_storage(self):
        c = self.settings()
        self.assertEqual(user.selected_source(c), (False, ""))
        self.assertIsNone(user.custom_folder(c))

    def test_own_picons_override_expert_without_changing_expert(self):
        c = self.settings(True, "/media/hdd/picon", True, "/media/usb/other")
        self.assertEqual(user.selected_source(c), (True, "/media/hdd/picon"))
        self.assertEqual(c.plugins.warderPiconExpert.destination.value,
                         "/media/usb/other")

    def test_retired_download_destination_is_not_a_picon_source(self):
        c = self.settings(False, "", True, "/media/usb/old-download-location")
        self.assertEqual(user.selected_source(c), (False, ""))
        self.assertIsNone(user.custom_folder(c))
        self.assertEqual(c.plugins.warderPiconExpert.destination.value,
                         "/media/usb/old-download-location")

    def test_enabled_without_path_does_not_fall_back(self):
        c = self.settings(True, "", False)
        self.assertEqual(user.selected_source(c), (True, ""))
        self.assertEqual(user.custom_folder(c), "")
        with tempfile.TemporaryDirectory() as root:
            own = channels.find_picon(
                "1:0:1:2:3:4:5:0:0:0:", root, lambda ref: ref,
                lambda ref: "Demo", lambda x: x, custom_folder="")
            self.assertEqual(own, "")

    def test_own_picons_are_read_only_and_no_fallback_to_warder(self):
        with tempfile.TemporaryDirectory() as root:
            root = Path(root)
            own, warder = root / "mine", root / "hdg17_files"
            own.mkdir()
            (warder / "picon").mkdir(parents=True)
            name = "1_0_1_2_3_4_5_0_0_0"
            (own / (name + ".png")).write_bytes(b"custom")
            (warder / "picon" / (name + ".png")).write_bytes(b"warder")
            found = channels.find_picon(
                "1:0:1:2:3:4:5:0:0:0:", str(warder), lambda r: r,
                lambda r: "Demo", lambda x: x, custom_folder=str(own))
            self.assertEqual(found, str(own / (name + ".png")))
            (own / (name + ".png")).unlink()
            missing = channels.find_picon(
                "1:0:1:2:3:4:5:0:0:0:", str(warder), lambda r: r,
                lambda r: "Demo", lambda x: x, custom_folder=str(own))
            self.assertEqual(missing, "")
            self.assertEqual((warder / "picon" / (name + ".png")).read_bytes(), b"warder")

    def test_user_directory_lookup_never_creates_files(self):
        with tempfile.TemporaryDirectory() as root:
            self.assertEqual(user.find_png(root, "absent"), "")
            self.assertEqual(user.find_png(root, "../bad"), "")
            self.assertEqual(list(Path(root).iterdir()), [])

if __name__ == "__main__":
    unittest.main()
