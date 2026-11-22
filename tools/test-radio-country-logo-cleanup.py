#!/usr/bin/env python3
"""Country switch must remove ONLY original/online picons belonging to old radio country."""
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch
import importlib.util

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'source/package-root/usr/lib/enigma2/python'))
from Plugins.Extensions.setupGlass17 import warderRadioCountryCleanup as cleanup
from Plugins.Extensions.setupGlass17 import warderRadioCountry as country
from Plugins.Extensions.setupGlass17 import warderRadioPackages as packages
from Plugins.Extensions.setupGlass17 import warderRadioLive as live
from Plugins.Extensions.setupGlass17 import warderRadioOnlineLogos as online

spec=importlib.util.spec_from_file_location('cleanup_fixtures',ROOT/'tools/test-radio-packages.py')
fixtures=importlib.util.module_from_spec(spec)
spec.loader.exec_module(fixtures)

class Tests(unittest.TestCase):
    def setUp(self):
        ctx=tempfile.TemporaryDirectory()
        self.addCleanup(ctx.cleanup)
        self.base=Path(ctx.name)
        self.path=self.base/'hdg17_files'
        self.path.mkdir()
        self.picon=self.path/'picon'
        self.picon.mkdir()
        self.radio=self.picon/'radio'
        self.etc=self.base/'enigma2'
        self.etc.mkdir()
        (self.etc/'settings').write_text('config.osd.language=sk_SK\n')
        self.source=self.base/'country-assets'
        self.source.mkdir()
        fixtures.example(self.source,'FR','France',3)
        fixtures.example(self.source,'DE','Deutschland',2)
        self.active='FR'
        mock=patch.object(country,'active_country',side_effect=lambda directory:self.active)
        mock.start()
        self.addCleanup(mock.stop)

    def add_country(self,code):
        return packages.install_country_logos(self.source,code,self.picon,
                                               require_external=False)

    def test_only_active_country_is_retained_when_switching(self):
        self.add_country('FR')
        self.add_country('DE')
        self.assertEqual(len(list((self.radio/'FR').glob('*.png'))),3)
        self.assertEqual(len(list((self.radio/'DE').glob('*.png'))),2)
        television=self.picon/'1_0_1_TV.png'
        television.write_bytes(b'user owned TV')
        self.active='DE'
        result=cleanup.prune_inactive(self.path,'DE',self.etc,False)
        self.assertEqual(result['removed'],['FR'])
        self.assertFalse((self.radio/'FR').exists())
        self.assertEqual(len(list((self.radio/'DE').glob('*.png'))),2)
        self.assertEqual(television.read_bytes(),b'user owned TV')
        self.assertFalse(list(self.radio.glob('.warder-prune-*')))
        self.assertEqual(cleanup.prune_inactive(self.path,'DE',self.etc,False)['removed'],[])

    def test_user_modified_and_unowned_radio_logos_are_preserved(self):
        self.add_country('FR')
        self.add_country('DE')
        fr=next((self.radio/'FR').glob('*.png'))
        fr.write_bytes(b'personal PNG changes')
        external=self.radio/'CZ'
        external.mkdir()
        (external/'owner.png').write_bytes(b'custom')
        self.active='DE'
        result=cleanup.prune_inactive(self.path,'DE',self.etc,False)
        self.assertEqual(result['removed'],[])
        self.assertCountEqual(result['protected'],['FR','CZ'])
        self.assertEqual(fr.read_bytes(),b'personal PNG changes')
        self.assertEqual((external/'owner.png').read_bytes(),b'custom')

    def test_online_favicon_cache_is_cleaned_after_country_switch(self):
        cc='FR'
        target=self.radio/cc
        target.mkdir(parents=True)
        uuid='12345678-1234-1234-1234-000000000000'
        stem=live.service_stem(uuid)+'.png'
        png=b'\x89PNG\r\n\x1a\nOriginalOnlineLogo'
        (target/stem).write_bytes(png)
        (target/packages.ONLINE_COUNTRY_OWNER).write_text(json.dumps({
            'owner':'WarderRadioOnline','country':cc,
            'files':{stem:hashlib.sha256(png).hexdigest()},
            'cursor':1,'total_stations':2}))
        self.active='DE'
        result=cleanup.prune_inactive(self.path,'DE',self.etc,False)
        self.assertEqual(result['removed'],['FR'])
        self.assertFalse(target.exists())

    def test_new_selection_mid_cleanup_does_not_delete_old_country(self):
        self.add_country('FR')
        self.add_country('DE')
        self.active='DE'
        calls=[0]
        def selection(code):
            calls[0]+=1
            return calls[0]<3
        result=cleanup.prune_inactive(self.path,'DE',self.etc,False,selected=selection)
        self.assertEqual(result['removed'],[])
        self.assertIn('FR',result['protected'])
        self.assertTrue((self.radio/'FR').is_dir())
        self.assertFalse(list(self.radio.glob('.warder-prune-*')))

    def test_invalid_selection_cannot_delete_user_files(self):
        self.add_country('FR')
        self.assertEqual(cleanup.prune_inactive(self.path,'../DE',self.etc,False)['skipped'],
                         'unsafe-storage')
        self.assertEqual(cleanup.prune_inactive(self.path,'DE',self.etc,False)['skipped'],
                         'country-superseded')
        self.assertTrue((self.radio/'FR').exists())
        self.active='DE'
        symlink=self.radio/'SK'
        symlink.symlink_to(self.base,target_is_directory=True)
        result=cleanup.prune_inactive(self.path,'DE',self.etc,False)
        self.assertIn('SK',result['protected'])
        self.assertTrue(symlink.is_symlink())

if __name__=='__main__':
    unittest.main()
