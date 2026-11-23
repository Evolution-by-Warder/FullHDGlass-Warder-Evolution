#!/usr/bin/env python3
"""Deterministic, offline package retention tests. Never touches project files."""
import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

SOURCE = Path(__file__).with_name("retain-fullhdglass-stable.py")
SPEC = importlib.util.spec_from_file_location("warder_retention", SOURCE)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)

RUNTIME_VERSION = "source/package-root/usr/lib/enigma2/python/Plugins/Extensions/setupGlass17/version"


class FourVersionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / "packages").mkdir()
        version = self.root / RUNTIME_VERSION
        version.parent.mkdir(parents=True)
        version.write_text("1.0.84\n")
        self.package("enigma2-skin-fullhdglass-warder-evolution_1.0.18_all.ipk")
        for v in ("1.0.72", "1.0.79", "1.0.80", "1.0.82", "1.0.83", "1.0.84"):
            self.package("enigma2-plugin-skins-fullhdglass_" + v + "_all.ipk")
        newest = "enigma2-plugin-skins-fullhdglass_1.0.84_all.ipk"
        newest_hash = self.digest(newest)
        url = "https://raw.githubusercontent.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/main/packages/" + newest
        self.json("update-production.json", {"version": "1.0.84", "package_url": url, "sha256": newest_hash})
        self.json("update-test.json", {"version": "1.0.84", "package_url": url, "sha256": newest_hash})
        self.json("update.json", {"version": "1.0.18", "package_url":
            "https://raw.githubusercontent.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/main/packages/enigma2-skin-fullhdglass-warder-evolution_1.0.18_all.ipk"})

    def json(self, name, data):
        (self.root / name).write_text(json.dumps(data))

    def package(self, name):
        path = self.root / "packages" / name
        path.write_bytes(("sample " + name).encode())
        sha = hashlib.sha256(path.read_bytes()).hexdigest()
        (path.parent / (name + ".sha256")).write_text(sha + "  " + name + "\n")

    def digest(self, name):
        return hashlib.sha256((self.root / "packages" / name).read_bytes()).hexdigest()

    def test_prunes_only_old_stable_pair(self):
        result = MODULE.plan(self.root)
        self.assertEqual(result["stable"], ["1.0.84", "1.0.83", "1.0.82", "1.0.80"])
        self.assertEqual(result["exceptions"], ["1.0.72"])
        self.assertEqual(len(result["remove"]), 2)
        self.assertEqual({p.name for p in result["remove"]}, {
            "enigma2-plugin-skins-fullhdglass_1.0.79_all.ipk",
            "enigma2-plugin-skins-fullhdglass_1.0.79_all.ipk.sha256"})
        self.assertTrue((self.root / "packages/enigma2-skin-fullhdglass-warder-evolution_1.0.18_all.ipk").is_file())

    def test_old_test_feed_blocks_pruning(self):
        p = self.root / "update-test.json"
        data = json.loads(p.read_text()); data["version"] = "1.0.69"; self.json("update-test.json", data)
        with self.assertRaises(ValueError):
            MODULE.plan(self.root)

    def test_legacy_bootstrap_cannot_be_lost(self):
        (self.root / "packages/enigma2-skin-fullhdglass-warder-evolution_1.0.18_all.ipk").unlink()
        with self.assertRaises(ValueError):
            MODULE.plan(self.root)

    def test_mismatched_latest_checksum_fails(self):
        p = self.root / "update-test.json"
        data = json.loads(p.read_text()); data["sha256"] = "a" * 64
        self.json("update-test.json", data)
        with self.assertRaises(ValueError):
            MODULE.plan(self.root)

    def test_orphan_checksum_fails(self):
        (self.root / "packages/enigma2-plugin-skins-fullhdglass_1.0.79_all.ipk").unlink()
        with self.assertRaises(ValueError):
            MODULE.plan(self.root)


if __name__ == "__main__":
    unittest.main()
