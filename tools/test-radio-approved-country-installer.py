#!/usr/bin/env python3
"""New original country ZIP contract: persistent selection and isolated picon paths."""
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'source/package-root/usr/lib/enigma2/python'))
from Plugins.Extensions.setupGlass17 import warderRadioPackages as pkg
spec=importlib.util.spec_from_file_location('signed_radio_fixture',ROOT/'tools/test-radio-packages.py')
fixture=importlib.util.module_from_spec(spec)
spec.loader.exec_module(fixture)

class Tests(unittest.TestCase):
    def setUp(self):
        td=tempfile.TemporaryDirectory()
        self.addCleanup(td.cleanup)
        root=Path(td.name)
        self.source=root/'signed-country-assets'
        self.source.mkdir()
        self.paths=root/'hdg17_files'/'picon'
        self.paths.mkdir(parents=True)
        fixture.example(self.source,'FR','France',3)
        fixture.example(self.source,'DE','Deutschland',2)
    def install(self,cc,callback=None):
        return pkg.install_country_logos(self.source,cc,self.paths,
            require_external=False,still_selected=callback)
    def test_originals_install_under_radio_country_and_leave_others_intact(self):
        (self.paths/'tv.png').write_bytes(b'untouched')
        first=self.install('FR')
        self.assertEqual((first['logos'],first['country']), (3,'FR'))
        assert first['source']=='approved-original-country-zip'
        fr=self.paths/'radio'/'FR'
        self.assertEqual(len(list(fr.glob('*.png'))),3)
        second=self.install('DE')
        self.assertEqual((second['country'],second['logos']),('DE',2))
        self.assertEqual(len(list(fr.glob('*.png'))),3)
        self.assertEqual(len(list((self.paths/'radio/DE').glob('*.png'))),2)
        self.assertEqual((self.paths/'tv.png').read_bytes(),b'untouched')
        self.assertEqual(self.install('FR')['skipped'],'already-current')
    def test_existing_owned_online_favicon_cache_is_replaced_only_if_clean(self):
        rows,_=fixture.example(self.source,'FR','France',3)
        folder=self.paths/'radio'/'FR'
        folder.mkdir(parents=True)
        online_name=rows[0]['stem']+'.png'
        online_bytes=fixture.PNG
        (folder/online_name).write_bytes(online_bytes)
        (folder/pkg.ONLINE_COUNTRY_OWNER).write_text(json.dumps({
            'owner':'WarderRadioOnline','country':'FR',
            'files':{online_name:hashlib.sha256(online_bytes).hexdigest()},
            'source_sha256':'f'*64,'cursor':1}))
        self.assertTrue(self.install('FR')['changed'])
        self.assertFalse((folder/pkg.ONLINE_COUNTRY_OWNER).exists())
        self.assertTrue((folder/pkg.COUNTRY_APPROVED_OWNER).is_file())
        self.assertEqual(len(list(folder.glob('*.png'))),3)
    def test_user_modified_png_blocks_entire_approved_swap(self):
        self.install('FR')
        marker=self.paths/'radio/FR'/pkg.COUNTRY_APPROVED_OWNER
        png=next((self.paths/'radio/FR').glob('*.png'))
        png.write_bytes(b'personal modification')
        self.assertEqual(self.install('FR')['skipped'],'user-modified-country-picons')
        self.assertEqual(png.read_bytes(),b'personal modification')
        self.assertTrue(marker.is_file())
    def test_switch_during_download_preserves_current_country(self):
        self.install('FR')
        before={p.name:p.read_bytes() for p in (self.paths/'radio/FR').glob('*')}
        skipped=self.install('FR',lambda country:False)
        # Identical approved original is never re-downloaded.
        self.assertEqual(skipped['skipped'],'already-current')
        # A second country cancelled before publication cannot create output.
        other=self.install('DE',lambda country:False)
        self.assertEqual(other['skipped'],'country-superseded')
        self.assertFalse((self.paths/'radio/DE').exists())
        self.assertEqual({p.name:p.read_bytes() for p in (self.paths/'radio/FR').glob('*')},before)
    def test_tampered_signed_zip_fails_without_overwriting_older_originals(self):
        self.install('FR')
        old=list((self.paths/'radio/FR').glob('*.png'))
        before={p.name:p.read_bytes() for p in old}
        (self.source/'logos/FR.zip').write_bytes(b'corrupted')
        with self.assertRaisesRegex(ValueError,'SHA-256 mismatch|Invalid country ZIP size'):
            self.install('FR')
        self.assertEqual({p.name:p.read_bytes() for p in old},before)
if __name__=='__main__':unittest.main()
