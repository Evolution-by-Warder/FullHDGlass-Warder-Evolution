#!/usr/bin/env python3
"""The visible Warder downloader must scroll; percentages must not spam rows."""
import importlib.util
import unittest
from pathlib import Path

path = (Path(__file__).resolve().parents[1] /
        "source/package-root/usr/lib/enigma2/python/Plugins/Extensions/setupGlass17/warderProgressLog.py")
spec = importlib.util.spec_from_file_location("warderProgressLog", path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
ProgressLog = module.ProgressLog


class ProgressLogTests(unittest.TestCase):
    def test_percent_updates_edit_only_current_line(self):
        log = ProgressLog(visible_lines=9)
        log.stage("Downloading: 23.5e / CANALPLUS_SK - 5%")
        log.stage("Downloading: 23.5e / CANALPLUS_SK - 58%")
        log.stage("Downloading: 23.5e / CANALPLUS_SK - 100%")
        self.assertEqual(len(log.entries), 1)
        self.assertIn("100%", log.tail())

    def test_next_satellite_appears_under_previous(self):
        log = ProgressLog()
        log.stage("Downloading: CANALPLUS_CZ - 28%")
        log.done("CANALPLUS_CZ - 98 picons")
        log.stage("Downloading: CANALPLUS_SK - 58%")
        self.assertEqual(log.entries[0], "[OK] CANALPLUS_CZ - 98 picons")
        self.assertEqual(log.entries[1], "[>>] Downloading: CANALPLUS_SK - 58%")

    def test_rows_scroll_up_with_bounded_visible_tail(self):
        log = ProgressLog(visible_lines=4, max_entries=9)
        for i in range(12):
            log.stage("File %d" % i)
            log.done("File %d verified" % i)
        self.assertEqual(len(log.entries), 9)
        visible = log.tail().splitlines()
        self.assertEqual(len(visible), 4)
        self.assertEqual(visible[0], "[OK] File 8 verified")
        self.assertEqual(visible[-1], "[OK] File 11 verified")

    def test_stage_transition_adds_new_line_without_loss(self):
        log = ProgressLog()
        log.stage("Downloading: pack - 100%")
        log.stage("Verifying: SHA-256")
        log.stage("Extracting: pack.zip")
        log.done("99 picons")
        self.assertEqual(len(log.entries), 3)
        self.assertTrue(log.entries[0].startswith("[>>] Downloading"))
        self.assertTrue(log.entries[1].startswith("[>>] Verifying"))
        self.assertEqual(log.entries[2], "[OK] 99 picons")

    def test_bytes_without_known_total_update_same_line(self):
        log = ProgressLog()
        log.stage("Legacy: 1.0 MiB")
        log.stage("Legacy: 2.5 MiB")
        self.assertEqual(len(log.entries), 1)

    def test_error_stays_in_history(self):
        log = ProgressLog()
        log.stage("Downloading: failed pack")
        log.done("SHA-256 mismatch", success=False)
        log.note("Download completed with errors")
        self.assertEqual(log.entries, ["[ERROR] SHA-256 mismatch",
                                      "Download completed with errors"])


if __name__ == "__main__":
    unittest.main()
