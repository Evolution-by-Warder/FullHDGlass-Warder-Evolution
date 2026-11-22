#!/usr/bin/env python3
"""TEST141: built-in exact 224-country world needs no user ZIP or test folder."""
import hashlib
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'source/package-root/usr/lib/enigma2/python'))
from Plugins.Extensions.setupGlass17 import warderRadioBundledWorld as bundled

class Tests(unittest.TestCase):
    def setUp(self):
        t=tempfile.TemporaryDirectory()
        self.addCleanup(t.cleanup)
        root=Path(t.name)
        self.external=root/'hdg17_files'
        self.external.mkdir()
        self.testfile=root/'radio-countries-bouquets.zip'
        self.testfile.write_bytes(b'locally-supplied-224-world-fixture')
    def test_complete_offline_bundle_signature_and_exact_country_count(self):
        sha=hashlib.sha256(self.testfile.read_bytes()).hexdigest()
        with patch.object(bundled,'WORLD_SHA',sha),patch.object(
                bundled.world,'install_world',return_value={
                    'changed':True,'countries':224,'stations':48219}) as install:
            result=bundled.sync_world(self.external,False,self.testfile)
        self.assertEqual(result['countries'],224)
        self.assertEqual(install.call_args.args,
                         (self.testfile,sha,self.external))
        self.assertEqual(install.call_args.kwargs['expected_countries'],224)
        self.assertFalse(install.call_args.kwargs['require_external'])
    def test_bad_bytes_and_no_manual_testkit_bypass(self):
        with self.assertRaisesRegex(ValueError,'SHA mismatch'):
            bundled.sync_world(self.external,False,self.testfile)
        missing=self.testfile.with_name('not-present.zip')
        self.assertEqual(bundled.sync_world(self.external,False,missing)['skipped'],
                         'missing-bundled-world')
        self.assertFalse((self.external/'radio-country-test').exists())
    def test_default_pinned_source_inside_skin_and_no_hardcoded_media_mount(self):
        self.assertEqual(str(bundled.SOURCE),
            '/usr/share/enigma2/hd_glass17/radio-world/radio-countries-bouquets.zip')
        self.assertEqual(len(bundled.WORLD_SHA),64)
        self.assertNotIn('/media/hdd',str(bundled.SOURCE))
if __name__=='__main__':unittest.main()
