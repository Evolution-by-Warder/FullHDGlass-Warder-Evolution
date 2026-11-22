#!/usr/bin/env python3
"""Verify first OSD country, later stored user choice, and safe 224->1 migration."""
import string
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'source/package-root/usr/lib/enigma2/python'))
from Plugins.Extensions.setupGlass17 import warderRadioSingleCountry as single
from Plugins.Extensions.setupGlass17 import warderRadioCountry as country
from Plugins.Extensions.setupGlass17 import warderRadioCountryBouquets as legacy
from Plugins.Extensions.setupGlass17 import warderRadioLive as live
from Plugins.Extensions.setupGlass17 import warderRadioOnlineLogos as online
from Plugins.Extensions.setupGlass17 import warderRadioBundleFetch as fetch

class Tests(unittest.TestCase):
    def setUp(self):
        td=tempfile.TemporaryDirectory()
        self.addCleanup(td.cleanup)
        root=Path(td.name)
        self.root=root/'hdg17_files'
        self.root.mkdir()
        self.etc=root/'enigma2'
        self.etc.mkdir()
        (self.etc/'settings').write_text('config.osd.language=sk_SK\n')
        self.personal=(b'#NAME Bouquets (Radio)\n'
          b'#SERVICE 1:7:2:0:0:0:0:0:0:0:FROM BOUQUET "userbouquet.personal.radio" ORDER BY bouquet\n')
        (self.etc/'bouquets.radio').write_bytes(self.personal)
        from Plugins.Extensions.setupGlass17 import warderRadioBundleFetch
        mock=patch.object(warderRadioBundleFetch,'sync_world',
                         return_value={'changed':True,'countries':224,'stations':48219})
        mock.start()
        self.addCleanup(mock.stop)

    def test_first_osd_country_is_only_one_visible_radio_bouquet(self):
        out=single.sync(self.root,self.etc,require_external=False)
        self.assertEqual((out['country_choices'],out['active_bouquets'],out['initial_country']),
                         (224,1,'SK'))
        root=(self.etc/'bouquets.radio').read_bytes()
        self.assertEqual(root.count(b'userbouquet.warder.live.radio'),1)
        self.assertEqual(root.count(b'userbouquet.personal.radio'),1)
        self.assertNotIn(b'userbouquet.warder-country-',root)

    def test_user_selected_country_survives_reboot_and_language_change(self):
        single.sync(self.root,self.etc,require_external=False)
        self.assertTrue(country.request_country('DE',self.etc)['accepted'])
        self.assertEqual(country._choice(self.etc)['pending'],'DE')
        state=country._choice(self.etc)
        state['active']='DE'
        state.pop('pending',None)
        country._save_choice(self.etc,state)
        (self.etc/'settings').write_text('config.osd.language=fr_FR\n')
        country.bootstrap(self.etc)
        self.assertEqual(country.active_country(self.etc),'DE')
        self.assertTrue(online.selected('DE',self.etc))
        self.assertTrue(fetch._country_really_selected(self.etc,'DE'))
        self.assertFalse(online.selected('SK',self.etc))

    def test_old_224_test_bouquets_retire_and_remember_explicit_selection(self):
        codes=[a+b for a in string.ascii_uppercase for b in string.ascii_uppercase][:224]
        self.assertTrue(legacy.bootstrap_online(self.root,self.etc,codes,
                                                require_external=False)['changed'])
        self.assertTrue(legacy.remember_selection(self.etc,'AB'))
        result=single.sync(self.root,self.etc,require_external=False)
        self.assertEqual(result['old_test_bouquets']['retired_country_roots'],224)
        self.assertEqual(country._choice(self.etc)['pending'],'AB')
        root=(self.etc/'bouquets.radio').read_bytes()
        self.assertEqual(root.count(b'userbouquet.warder.live.radio'),1)
        self.assertEqual(root.count(b'userbouquet.personal.radio'),1)
        self.assertNotIn(b'userbouquet.warder-country-',root)

    def test_modified_old_country_fails_closed(self):
        codes=[a+b for a in string.ascii_uppercase for b in string.ascii_uppercase][:224]
        legacy.bootstrap_online(self.root,self.etc,codes,require_external=False)
        target=self.etc/legacy.filename('AA')
        target.write_bytes(b'user-edited content')
        before=(self.etc/'bouquets.radio').read_bytes()
        result=single.sync(self.root,self.etc,require_external=False)
        self.assertEqual(result['skipped'],'old-country-migration-blocked')
        self.assertEqual((self.etc/'bouquets.radio').read_bytes(),before)
        self.assertEqual(target.read_bytes(),b'user-edited content')

    def test_osd_country_logos_queued_at_startup_without_opening_radio_list(self):
        class Loop:
            def callLater(self,delay,callback):
                return object()
        worker=live.Controller.__new__(live.Controller)
        worker.closed=False
        worker.icon_worker=None
        worker.icon_timer=None
        worker.session=None
        worker.loop=Loop()
        worker.last_bulk_logo=None
        worker.local_world_sha=None
        calls=[]
        worker._spawn=lambda kind,args,cb:calls.append((kind,args)) or object()
        with patch.object(live,'DIRECTORY',self.etc),\
             patch.object(live,'_radio_world_root',return_value=self.root),\
             patch.object(live,'_radio_custom_picons_enabled',return_value=False),\
             patch('Plugins.Extensions.setupGlass17.warderRadioWorld.cached_country',
                   return_value='f'*64):
            worker.check_icon()
        self.assertEqual(calls,[('logo_zip',['--logos-world','SK',str(self.root)])])

if __name__=='__main__':
    unittest.main()
