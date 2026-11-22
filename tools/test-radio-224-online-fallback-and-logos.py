#!/usr/bin/env python3
"""Test 224 independent country entries, first-page online loading, logo batches."""
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'source/package-root/usr/lib/enigma2/python'))
from Plugins.Extensions.setupGlass17 import warderRadioCountryBouquets as books
from Plugins.Extensions.setupGlass17 import warderRadioOnlineLogos as online
from Plugins.Extensions.setupGlass17 import warderRadioCountry as country
from Plugins.Extensions.setupGlass17 import warderRadioLive as live

CODES=[chr(65+i)+chr(65+j) for i in range(26) for j in range(26)][:224]

class Tests(unittest.TestCase):
    def setUp(self):
        temp=tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        base=Path(temp.name)
        self.external=base/'hdg17_files'
        self.external.mkdir()
        self.etc=base/'enigma2'
        self.etc.mkdir()
        (self.etc/'bouquets.radio').write_bytes(
            b'#NAME Bouquets (Radio)\n'
            b'#SERVICE 1:7:2:0:0:0:0:0:0:0:FROM BOUQUET "userbouquet.personal.radio" ORDER BY bouquet\n')
        self.mock=patch.object(country,'country_name',side_effect=lambda cc:cc)
        self.mock.start();self.addCleanup(self.mock.stop)
    def boot(self):
        return books.bootstrap_online(self.external,self.etc,available=CODES,
                                      require_external=False)
    def test_224_real_country_file_entries_no_personal_bouquet_overwrite(self):
        self.assertEqual(self.boot()['countries'],224)
        index=(self.etc/'bouquets.radio').read_bytes()
        self.assertEqual(index.count(b'FROM BOUQUET "userbouquet.warder-country-'),224)
        self.assertIn(b'FROM BOUQUET "userbouquet.personal.radio"',index)
        self.assertEqual(self.boot()['skipped'],'already-owned')
        self.assertEqual(index,(self.etc/'bouquets.radio').read_bytes())
    def test_pending_country_populates_its_own_bouquet_with_real_stream_refs(self):
        self.boot()
        code='AA'
        item={'name':'Test country AA station',
              'url':'https://radio.example.org/live','countrycode':code,
              'stationuuid':'aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa',
              'stem':live.service_stem('aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa'),
              'favicon':'https://station.example.org/logo.png'}
        prepared=live._bouquet([(code,[item])])
        (self.etc/live.FILE).write_bytes(prepared)
        (self.etc/live.DATA_FILE).write_bytes(live._json_bytes({'schema':1,'stations':[item]}))
        with patch.object(country,'_choice',return_value={'active':code}):
            result=books.update_from_online_country(self.etc,code)
        self.assertEqual(result['stations'],1)
        output=(self.etc/books.filename('AA')).read_bytes()
        self.assertTrue(output.startswith(b'#NAME Warder Radio - AA\n'))
        self.assertEqual(output.split(b'\n',1)[1],prepared.split(b'\n',1)[1])
        with patch.object(country,'_choice',return_value={'active':code}):
            self.assertEqual(books.update_from_online_country(self.etc,code)['skipped'],
                             'already-current')
    def test_external_online_logo_batch_downloads_without_mutating_tv_sat(self):
        self.boot()
        self.assertTrue(books.remember_selection(self.etc,'AA'))
        items=[]
        for i in range(33):
            uid='aaaaaaaa-aaaa-4aaa-8aaa-%012x'%i
            items.append({'countrycode':'AA','stationuuid':uid,
                          'name':'Different Station %d'%i,'url':'https://radio.example/%d'%i,
                          'stem':live.service_stem(uid),
                          'favicon':'https://broadcaster.example/%d.png'%i})
        data=self.etc/live.DATA_FILE
        data.write_bytes(live._json_bytes({'stations':items}))
        own=country._choice
        original=self.external/'picon'
        original.mkdir()
        (original/'tv-owned.png').write_bytes(b'untouchable')
        art=self.etc/'demo-logo.png'
        Image.new('RGB',(120,120),(50,70,150)).save(art,'PNG')
        class Source:
            def get(self,row):
                return str(art)
        with patch.object(country,'_choice',return_value={'active':'AA'}):
            first=online.sync_online_country(self.external,self.etc,'AA',
                        logos=Source(),max_batch=28,require_external=False)
            second=online.sync_online_country(self.external,self.etc,'AA',
                        logos=Source(),max_batch=28,require_external=False)
        self.assertTrue(first['incomplete'])
        self.assertEqual(first['scanned'],28)
        self.assertEqual(second['scanned'],33)
        self.assertFalse(second['incomplete'])
        self.assertEqual(second['logos'],33)
        self.assertEqual((original/'tv-owned.png').read_bytes(),b'untouchable')
        folder=original/'radio/AA'
        self.assertEqual(len(list(folder.glob('*.png'))),33)
        target=folder/(items[0]['stem']+'.png')
        target.write_bytes(b'edited by user')
        with patch.object(country,'_choice',return_value={'active':'AA'}):
            refusal=online.sync_online_country(self.external,self.etc,'AA',
                  logos=Source(),require_external=False)
        self.assertEqual(refusal['skipped'],'modified-online-logo')
        self.assertEqual(target.read_bytes(),b'edited by user')
    def test_refuse_incomplete_country_list_and_unselected_requests(self):
        self.assertEqual(books.bootstrap_online(self.external,self.etc,
          available=['SK'],require_external=False)['skipped'],'country-list-incomplete')
        self.boot()
        with patch.object(country,'_choice',return_value={'active':'AA'}):
            self.assertEqual(online.sync_online_country(self.external,self.etc,
                'AA',require_external=False)['skipped'],'country-not-selected')

if __name__=='__main__': unittest.main()
