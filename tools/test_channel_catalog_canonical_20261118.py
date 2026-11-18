"""Audit public satellite/provider channel parts consumed by both installed Warder clients.

No IPK creation, downloads, graphics conversion or runtime mutation.
"""
import hashlib
import json
from pathlib import Path
import re
import runpy
import subprocess
import unittest
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
CHANNELS = ROOT / "assets/warder/downloads/picons/channels"
MANIFEST = CHANNELS / "manifest.json"
SUMS = CHANNELS / "SHA256SUMS"
REPORT = ROOT / "reports/channel-catalog-canonical-parts-20261118.json"
SKIN_SYNC = ROOT / "source/package-root/usr/lib/enigma2/python/Plugins/Extensions/setupGlass17/warderPiconSync.py"
PICONHUB_SYNC = ROOT / "external/piconhub/plugin/src/Plugins/Extensions/WarderPiconHub/warder_skin_sync.py"
EXPECTED = "https://raw.githubusercontent.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/main/assets/warder/downloads/picons/channels/"


def read():
    return json.loads(MANIFEST.read_text(encoding="utf-8"))


class CanonicalManifest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.doc = read()
        cls.meta = {p["filename"]: p for p in cls.doc["parts"]}
        cls.report = json.loads(REPORT.read_text(encoding="utf-8"))

    def test_all_downloads_are_safe_sequential_content_addressed_parts(self):
        d = self.doc
        self.assertEqual(d["delivery"], "raw-github-parts")
        self.assertEqual(len(d["parts"]), len(self.meta))
        self.assertEqual(len(d["packages"]), 498)
        self.assertEqual(len(self.meta), 2131)
        used = set()
        for p in d["packages"]:
            self.assertTrue(re.fullmatch(r"[0-9a-f]{64}", p["sha256"]))
            urls = p["parts"]
            self.assertTrue(urls)
            total = 0
            for n, url in enumerate(urls):
                expected = p["filename"] + ".part%02d" % n
                self.assertEqual(url, EXPECTED + expected,
                                 (p["selector_id"], p["resolution"], p["family"], n))
                self.assertNotIn(expected, used)
                self.assertIn(expected, self.meta)
                part = self.meta[expected]
                self.assertTrue(0 < part["bytes"] <= 20 * 1024 * 1024)
                self.assertRegex(part["sha256"], r"^[0-9a-f]{64}$")
                total += part["bytes"]
                used.add(expected)
            self.assertEqual(p["bytes"], total)
        self.assertEqual(used, set(self.meta))

    def test_canalplus_sk_cz_all_18_variants_remain_intact(self):
        providers = ("CANALPLUS_SK", "CANALPLUS_CZ")
        sizes = ("50x30", "220x132", "400x240")
        styles = ("channel-transparent", "channel-black", "channel-white")
        found = {(p["selector_id"], p["resolution"], p["family"])
                 for p in self.doc["packages"] if p["selector_id"] in providers}
        self.assertEqual(found, {(provider, size, style)
                                 for provider in providers for size in sizes for style in styles})
        self.assertEqual(self.report["provider_canalplus_sk_cz_package_count"], 18)

    def test_sha256sum_index_matches_manifest_and_all_part_metadata(self):
        lines = SUMS.read_text(encoding="utf-8").splitlines()
        self.assertEqual(len(lines), len(self.meta) + 1)
        entries = dict(line.split("  ", 1) for line in lines)
        self.assertEqual(len(entries), len(lines))
        actual = {filename: digest for digest, filename in
                  (line.split("  ", 1) for line in lines)}
        self.assertEqual(actual.pop("manifest.json"),
                         hashlib.sha256(MANIFEST.read_bytes()).hexdigest())
        self.assertEqual(actual, {p["filename"]: p["sha256"] for p in self.doc["parts"]})

    def test_skin_and_piconhub_installed_validator_accept_whole_catalogue(self):
        for source in (SKIN_SYNC, PICONHUB_SYNC):
            with self.subTest(client=str(source)):
                self.assertTrue(source.is_file(), "Client source must be checked out for dual-client test")
                mod = runpy.run_path(str(source))
                errors = mod["validate_publication_manifest"](self.doc, mod["RUNTIME_MANIFEST_URL"])
                self.assertEqual(errors, [], errors[:8])

    def test_82_aliases_reuse_identical_existing_git_blob_without_picon_changes(self):
        aliases = self.report["aliases"]
        self.assertEqual(len(aliases), 82)
        self.assertEqual(self.report["packages_corrected"], 20)
        self.assertEqual(self.report["package_count"], len(self.doc["packages"]))
        self.assertEqual(self.report["part_count"], len(self.meta))
        self.assertEqual(set(self.report["affected_selectors"]),
                         {"150W", "192E", "360E", "08W"})
        for item in aliases:
            old = "assets/warder/downloads/picons/channels/" + item["old"]
            new = "assets/warder/downloads/picons/channels/" + item["new"]
            before = subprocess.check_output(["git", "rev-parse", "HEAD:" + old], cwd=ROOT,
                                              text=True).strip()
            after = subprocess.check_output(["git", "rev-parse", "HEAD:" + new], cwd=ROOT,
                                             text=True).strip()
            self.assertEqual(before, after)
            self.assertEqual(after, item["blob_sha"])
            self.assertEqual(self.meta[item["new"]]["bytes"], item["bytes"])


if __name__ == "__main__":
    unittest.main()
