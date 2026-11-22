#!/usr/bin/env python3
"""Stable 224-country source and selected-logo delivery regressions, no internet."""
from io import BytesIO
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "source/package-root/usr/lib/enigma2/python"))
from Plugins.Extensions.setupGlass17 import warderRadioBundleFetch as fetch


class Response(BytesIO):
    def geturl(self):
        return fetch.LATEST_URL


class Tests(unittest.TestCase):
    def test_release_feed_uses_permanent_stable_main_not_test_work_branch(self):
        self.assertEqual(
            fetch.LATEST_URL,
            "https://raw.githubusercontent.com/Evolution-by-Warder/"
            "Radio-Warder-Evolution/main/assets/radio-country/latest.json")
        self.assertNotIn("test-20261122.json", fetch.LATEST_URL)
        self.assertNotIn("/feature/", fetch.LATEST_URL)

    def test_existing_14_day_cadence_and_external_storage_guards_untouched(self):
        self.assertEqual(fetch.SYNC_PERIOD, 14 * 24 * 3600)
        self.assertEqual(fetch.SYNC_RETRY, 6 * 3600)
        self.assertEqual(fetch.world.MAX_ARCHIVE, 256 * 1024 * 1024)
        self.assertEqual(fetch._asset(
            {"release_tag": "radio-country-20261122"},
            "radio-countries-bouquets.zip"),
            "https://github.com/Evolution-by-Warder/Radio-Warder-Evolution/"
            "releases/download/radio-country-20261122/radio-countries-bouquets.zip")

    def test_complete_224_country_feed_contract_from_main(self):
        codes = [chr(a) + chr(b) for a in range(65, 91)
                 for b in range(65, 91)][:224]
        code_entries = {c: {
            "name": c, "stations": 1, "logo_package_complete": True,
            "logos": {"file": c + ".zip", "bytes": 100, "sha256": "b" * 64}
        } for c in codes}
        country_data = {
            "schema": 1, "source": "WarderRadio.RadioBrowser",
            "complete": True, "release_tag": "radio-country-20261122",
            "country_count": 224, "station_count": 224,
            "world": {"file": "radio-countries-bouquets.zip",
                      "sha256": "771953b41ceab46f8852f5e3219338cb1369d7f653ed7d329ad551e481f88d68",
                      "bytes": 6664493},
            "countries": code_entries
        }
        expected = json.dumps(country_data).encode()
        calls = []
        def network(request, timeout=None):
            calls.append(request.full_url)
            return Response(expected)
        data = fetch._feed(network)
        self.assertEqual(data["country_count"], 224)
        self.assertEqual(len(data["countries"]), 224)
        self.assertEqual(calls, [fetch.LATEST_URL])
        self.assertEqual(fetch._asset(data, "AA.zip"),
                         fetch.RELEASE_ROOT + data["release_tag"] + "/AA.zip")

    def test_incomplete_224_country_catalogue_rejected(self):
        data = {
            "schema": 1, "source": "WarderRadio.RadioBrowser",
            "complete": False, "release_tag": "radio-country-20261122",
            "country_count": 224, "world": {"file": "radio-countries-bouquets.zip",
              "sha256": "a" * 64, "bytes": 200},
            "countries": {"SK": {"logo_package_complete": False,
                "logos": {"file": "SK.zip", "bytes": 2, "sha256": "a" * 64}}}
        }
        def network(request, timeout=None):
            return Response(json.dumps(data).encode())
        with self.assertRaisesRegex(ValueError, "incomplete release"):
            fetch._feed(network)

    def test_no_world_archive_or_multi_country_png_in_skin_payload(self):
        parent = ROOT / "source/package-root"
        found = [p for p in parent.rglob("radio-countries-bouquets.zip")]
        self.assertEqual(found, [])


if __name__ == "__main__":
    unittest.main(verbosity=2)
