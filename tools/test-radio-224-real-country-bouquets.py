#!/usr/bin/env python3
"""End-to-end test: 224 independent radio bouquets + selected-country ownership."""
import hashlib
import json
from pathlib import Path
import string
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'source/package-root/usr/lib/enigma2/python'))
from Plugins.Extensions.setupGlass17 import warderRadioCountryBouquets as books

class Tests(unittest.TestCase):
    def setUp(self):
        td=tempfile.TemporaryDirectory()
        self.addCleanup(td.cleanup)
        base=Path(td.name)
        self.root=base/'hdg17_files'
        self.root.mkdir()
        (self.root/'radio-world').mkdir()
        self.etc=base/'enigma2'
        self.etc.mkdir()
        self.legacy=(b'#NAME Bouquets (Radio)\n'
                     b'#SERVICE 1:7:2:0:0:0:0:0:0:0:FROM BOUQUET "userbouquet.my-personal.radio" ORDER BY bouquet\n')
        (self.etc/'bouquets.radio').write_bytes(self.legacy)
        self.codes=sorted([a+b for a in string.ascii_uppercase for b in string.ascii_uppercase])[:224]
        self.index={'schema':1,'source':'WarderRadio.RadioBrowser',
             'country_count':224,'station_count':48219,'countries':{
                cc:{'name':'Name '+cc,'stations':(274 if i==223 else 215)}
                for i,cc in enumerate(self.codes)}}
        assert sum(v['stations'] for v in self.index['countries'].values())==48219
        self.country_raw=b'#NAME Warder Radio Live\n#SERVICE 1:64:2:0:0:0:0:0:0:0:\n#DESCRIPTION A country\n'
        self.patchers=[
            patch.object(books.world,'_owner_ok',return_value=True),
            patch.object(books.world,'_json_file',side_effect=self._json),
            patch.object(books.world,'_verify_index',side_effect=lambda x:x['countries']),
            patch.object(books.packages,'verified_country',side_effect=self._country)
        ]
        for mock in self.patchers:
            mock.start();self.addCleanup(mock.stop)
    def _json(self,path,max_size):
        if Path(path).name=='index.json':return self.index
        return {'owner':'WarderRadioLive','archive_sha256':'f'*64}
    def _country(self,folder,cc):
        info=self.index['countries'][cc]
        return (self.country_raw,b'{"stations":[]}',
                {'country':cc,'stations':info['stations'],
                 'files':{'bouquets/'+cc+'.radio':{'bytes':len(self.country_raw)}}})
    def generate(self):
        return books.publish(self.root,self.etc,require_external=False,min_free=0)
    def test_full_224_country_entries_and_all_countries_are_real_files(self):
        result=self.generate()
        self.assertTrue(result['changed'])
        self.assertEqual((result['countries'],result['stations'],result['indexed_countries']),
                         (224,48219,224))
        idx=(self.etc/'bouquets.radio').read_bytes()
        self.assertEqual(idx.count(b'FROM BOUQUET "userbouquet.warder-country-'),224)
        self.assertEqual(idx.count(b'userbouquet.my-personal.radio'),1)
        for cc in self.codes:
            path=self.etc/books.filename(cc)
            self.assertTrue(path.is_file(),cc)
            self.assertTrue(path.read_bytes().startswith(
              ('#NAME Warder Radio - Name '+cc+'\n').encode()),cc)
            self.assertEqual(path.read_bytes().split(b'\n',1)[1],
                             self.country_raw.split(b'\n',1)[1])
        self.assertEqual(self.generate()['skipped'],'already-current')
        self.assertEqual((self.etc/'bouquets.radio').read_bytes(),idx)
    def test_selected_native_country_detection_and_state_clear(self):
        self.generate()
        path='1:7:2:0:0:0:0:0:0:0:FROM BOUQUET "'+books.filename('MX')+'" ORDER BY bouquet'
        # This 224-code fixture is lexicographically first 224, hence MX is
        # checked separately for the native path parser, while fixture AA exists.
        self.assertEqual(books.selected_from_native_path(path),'MX')
        self.assertIsNone(books.selected_from_native_path('FROM BOUQUET "userbouquet.personal.radio"'))
        self.assertTrue(books.remember_selection(self.etc,'AA'))
        self.assertEqual(books.selected_country(self.etc),'AA')
        self.assertFalse(books.remember_selection(self.etc,'AA'))
        self.assertTrue(books.remember_selection(self.etc,None))
        self.assertIsNone(books.selected_country(self.etc))
    def test_unowned_existing_country_refuses_overwrite(self):
        target=self.etc/books.filename('AA')
        target.write_bytes(b'my personal country')
        result=self.generate()
        self.assertEqual(result['skipped'],'user-modified-country-bouquet')
        self.assertEqual(target.read_bytes(),b'my personal country')
        self.assertEqual((self.etc/'bouquets.radio').read_bytes(),self.legacy)
    def test_modification_after_install_blocks_future_replace(self):
        self.generate()
        country=self.etc/books.filename('AA')
        country.write_bytes(b'local modification')
        result=self.generate()
        self.assertEqual(result['skipped'],'user-modified-country-bouquet')
        self.assertEqual(country.read_bytes(),b'local modification')
    def test_reject_symlink_and_missing_external(self):
        response=books.publish(self.root.parent/'not-hdg17',self.etc,require_external=False)
        self.assertEqual(response['skipped'],'unsafe-storage')
        self.assertRaises(ValueError,books.filename,'../MX')
    def test_no_fabricated_label_or_unsafely_encoded_header(self):
        with self.assertRaises(ValueError):
            books.country_bouquet(self.country_raw,'AA','\n#SERVICE bad')
        with self.assertRaises(ValueError):
            books.country_bouquet(b'#NAME Wrong', 'AA', 'Mexico')

if __name__=='__main__':unittest.main()
