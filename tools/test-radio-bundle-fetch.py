#!/usr/bin/env python3
"""No-network tests for GitHub world snapshot and per-country logo delivery."""
from io import BytesIO
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'source/package-root/usr/lib/enigma2/python'))
from Plugins.Extensions.setupGlass17 import warderRadioBundleFetch as fetch
from Plugins.Extensions.setupGlass17 import warderRadioWorld as world
from Plugins.Extensions.setupGlass17 import warderRadioCountry as country
import importlib.util

def _fixture(name, path):
    spec=importlib.util.spec_from_file_location(name, ROOT/'tools'/path)
    mod=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

example=_fixture('radio_package_fixtures','test-radio-packages.py').example
snapshot=_fixture('radio_world_fixtures','test-radio-world.py').snapshot


class Response(BytesIO):
    def __init__(self, payload, url):
        super().__init__(payload)
        self.url=url
    def geturl(self):
        return self.url


class MockNetwork:
    def __init__(self, content, redirect=None):
        self.content=content
        self.redirect=redirect
        self.calls=[]
    def __call__(self, request, timeout=None):
        url=request.full_url
        self.calls.append(url)
        if url not in self.content:
            raise OSError('404')
        return Response(self.content[url],self.redirect or url)


class Tests(unittest.TestCase):
    def setUp(self):
        temp=tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root=Path(temp.name)
        self.paths=self.root/'hdg17_files'
        self.paths.mkdir()
        (self.paths/'picon').mkdir()
        self.etc=self.root/'enigma2'
        self.etc.mkdir()
        (self.etc/'settings').write_text('config.osd.language=fr_FR\n')
        (self.etc/'bouquets.radio').write_text('#NAME Bouquets (Radio)\n')
        self.archive,self.checksum=snapshot(self.root)
        self.countries={}
        source=self.root/'source'
        for code in ('ET','FR'):
            m=json.loads((source/f'manifests/{code}.json').read_text())
            raw=(source/f'logos/{code}.zip').read_bytes()
            self.countries[code]={'logo_package_complete':True,
                                  'logos':{'file':code+'.zip',
                                           'sha256':hashlib.sha256(raw).hexdigest(),
                                           'bytes':len(raw)}}
        self.feed={'schema':1,'source':'WarderRadio.RadioBrowser','complete':True,
                   'release_tag':'radio-country-20261119',
                   'country_count':2,
                   'world':{'file':'radio-countries-bouquets.zip',
                            'sha256':self.checksum,
                            'bytes':self.archive.stat().st_size},
                   'countries':self.countries}
        self._network()

    def _network(self, redirect=None):
        assets={fetch.LATEST_URL:json.dumps(self.feed).encode(),
                fetch.RELEASE_ROOT+self.feed['release_tag']+
                '/radio-countries-bouquets.zip':self.archive.read_bytes()}
        for code in ('ET','FR'):
            assets[fetch.RELEASE_ROOT+self.feed['release_tag']+'/'+code+'.zip']=(
                self.root/'source'/f'logos/{code}.zip').read_bytes()
        self.network=MockNetwork(assets,redirect)

    def test_fetch_once_then_country_switch_without_network(self):
        result=fetch.sync_world(self.paths,self.network,require_external=False)
        self.assertTrue(result['changed'])
        self.assertEqual(result['countries'],2)
        self.assertEqual(len(self.network.calls),2)
        result=fetch.sync_world(self.paths,self.network,require_external=False)
        self.assertEqual(result['skipped'],'already-current')
        self.assertEqual(len(self.network.calls),3)
        country.bootstrap(self.etc)
        switched=world.activate_from_world(self.paths,'FR',self.etc)
        self.assertEqual(switched['country'],'FR')
        self.assertTrue(switched['local'])
        self.assertEqual(len(self.network.calls),3)

    def test_fortnightly_update_is_persistent_across_receiver_reboots(self):
        now = 1800000000
        first=fetch.sync_world(self.paths,self.network,require_external=False,
                               state_directory=self.etc,now=now)
        self.assertTrue(first['changed'])
        self.assertEqual(len(self.network.calls),2)
        self.network.calls.clear()
        restart=fetch.sync_world(self.paths,self.network,require_external=False,
                                 state_directory=self.etc,now=now+5*24*3600)
        self.assertEqual(restart['skipped'],'not-due')
        self.assertEqual(restart['retry_after'],9*24*3600)
        self.assertEqual(self.network.calls,[])
        next_check=fetch.sync_world(self.paths,self.network,require_external=False,
                                    state_directory=self.etc,now=now+14*24*3600)
        self.assertEqual(next_check['skipped'],'already-current')
        self.assertEqual(self.network.calls,[fetch.LATEST_URL])
        again=fetch.sync_world(self.paths,self.network,require_external=False,
                               state_directory=self.etc,now=now+14*24*3600+60)
        self.assertEqual(again['skipped'],'not-due')

    def test_absent_release_retries_in_six_hours_not_on_each_gui_restart(self):
        now=1800000000
        self.network.content.pop(fetch.LATEST_URL)
        with self.assertRaises(OSError):
            fetch.sync_world(self.paths,self.network,require_external=False,
                             state_directory=self.etc,now=now)
        count=len(self.network.calls)
        deferred=fetch.sync_world(self.paths,self.network,require_external=False,
                                  state_directory=self.etc,now=now+600)
        self.assertEqual(deferred['skipped'],'not-due')
        self.assertEqual(deferred['retry_after'],fetch.SYNC_RETRY-600)
        self.assertEqual(len(self.network.calls),count)
        with self.assertRaises(OSError):
            fetch.sync_world(self.paths,self.network,require_external=False,
                             state_directory=self.etc,now=now+fetch.SYNC_RETRY)
        self.assertEqual(len(self.network.calls),count+1)

    def test_world_refresh_state_symlink_is_never_followed(self):
        personal=self.root/'personal.json'
        personal.write_text('private')
        (self.etc/fetch.SYNC_STATE).symlink_to(personal)
        reply=fetch.sync_world(self.paths,self.network,require_external=False,
                               state_directory=self.etc,now=1800000000)
        self.assertEqual(reply['skipped'],'unsafe-state')
        self.assertEqual(personal.read_text(),'private')
        self.assertEqual(self.network.calls,[])

    def test_only_selected_country_logo_zip_is_downloaded(self):
        fetch.sync_world(self.paths,self.network,require_external=False)
        country.bootstrap(self.etc)
        world.activate_from_world(self.paths,'FR',self.etc)
        self.network.calls.clear()
        result=fetch.sync_selected_logos(self.paths,self.etc,'FR',self.network,
                                        require_external=False)
        self.assertEqual(result['logos'],3)
        self.assertEqual(self.network.calls,[fetch.LATEST_URL,
            fetch.RELEASE_ROOT+self.feed['release_tag']+'/FR.zip'])
        self.assertEqual(len(list((self.paths/'picon/radio').glob('*.png'))),3)
        second=fetch.sync_selected_logos(self.paths,self.etc,'FR',self.network,
                                         require_external=False)
        self.assertEqual(second['skipped'],'already-current')
        self.assertEqual(self.network.calls[-1],fetch.LATEST_URL)

    def test_unmodified_logo_zip_is_loaded_from_older_immutable_release(self):
        previous='radio-country-20261119'
        current='radio-country-20261203'
        self.feed['release_tag']=current
        self.feed['countries']['FR']['logos']['asset_tag']=previous
        self._network()
        old_url=fetch.RELEASE_ROOT+previous+'/FR.zip'
        new_url=fetch.RELEASE_ROOT+current+'/FR.zip'
        self.network.content[old_url]=self.network.content.pop(new_url)
        fetch.sync_world(self.paths,self.network,require_external=False)
        country.bootstrap(self.etc)
        world.activate_from_world(self.paths,'FR',self.etc)
        self.network.calls.clear()
        result=fetch.sync_selected_logos(self.paths,self.etc,'FR',self.network,
                                         require_external=False)
        self.assertTrue(result['changed'])
        self.assertEqual(result['logos'],3)
        self.assertEqual(self.network.calls,[fetch.LATEST_URL,old_url])
        self.assertEqual(len(list((self.paths/'picon/radio').glob('*.png'))),3)
        self.assertEqual(fetch._asset(self.feed,'radio-countries-bouquets.zip'),
                         fetch.RELEASE_ROOT+current+'/radio-countries-bouquets.zip')
        with self.assertRaisesRegex(ValueError,'current release'):
            fetch._asset(self.feed,'radio-countries-bouquets.zip',previous)

    def test_malicious_or_future_country_asset_tag_does_not_fetch_any_zip(self):
        for unsafe in ('../../evil','radio-country-20990101','20261119',''):
            with self.subTest(unsafe=unsafe):
                self.feed['countries']['FR']['logos']['asset_tag']=unsafe
                self._network()
                with self.assertRaisesRegex(ValueError,'Incomplete country logo listing'):
                    fetch.sync_world(self.paths,self.network,require_external=False)
                self.assertEqual(self.network.calls,[fetch.LATEST_URL])
                self.assertFalse((self.paths/'radio-world').exists())

    def test_background_fetch_creates_missing_external_paths_picon_only(self):
        fetch.sync_world(self.paths,self.network,require_external=False)
        country.bootstrap(self.etc)
        world.activate_from_world(self.paths,'FR',self.etc)
        (self.paths/'picon').rmdir()
        self.assertFalse((self.paths/'picon').exists())
        result=fetch.sync_selected_logos(self.paths,self.etc,'FR',self.network,
                                         require_external=False)
        self.assertTrue(result['changed'])
        self.assertEqual(len(list((self.paths/'picon/radio').glob('*.png'))),3)

    def test_background_logo_request_for_old_country_does_not_replace_selection(self):
        fetch.sync_world(self.paths,self.network,require_external=False)
        country.bootstrap(self.etc)
        world.activate_from_world(self.paths,'FR',self.etc)
        self.network.calls.clear()
        result=fetch.sync_selected_logos(self.paths,self.etc,'ET',self.network,
                                        require_external=False)
        self.assertEqual(result['skipped'],'no-longer-selected')
        self.assertEqual(self.network.calls,[])

    def test_logo_failure_preserves_existing_country_picons(self):
        fetch.sync_world(self.paths,self.network,require_external=False)
        country.bootstrap(self.etc)
        world.activate_from_world(self.paths,'FR',self.etc)
        fetch.sync_selected_logos(self.paths,self.etc,'FR',self.network,
                                 require_external=False)
        original={(p.name,p.read_bytes()) for p in (self.paths/'picon/radio').glob('*.png')}
        self.network.content.pop(fetch.RELEASE_ROOT+self.feed['release_tag']+'/ET.zip')
        world.activate_from_world(self.paths,'ET',self.etc)
        with self.assertRaises(OSError):
            fetch.sync_selected_logos(self.paths,self.etc,'ET',self.network,
                                     require_external=False)
        self.assertEqual({(p.name,p.read_bytes()) for p in
                          (self.paths/'picon/radio').glob('*.png')},original)

    def test_world_bad_digest_does_not_replace_owned_cache(self):
        fetch.sync_world(self.paths,self.network,require_external=False)
        original=(self.paths/'radio-world/bouquets/FR.radio').read_bytes()
        self.feed['world']['sha256']='f'*64
        self._network()
        with self.assertRaisesRegex(ValueError,'SHA-256 mismatch'):
            fetch.sync_world(self.paths,self.network,require_external=False)
        self.assertEqual((self.paths/'radio-world/bouquets/FR.radio').read_bytes(),
                         original)

    def test_published_country_count_mismatch_is_blocked_before_swap(self):
        self.feed['countries']['DE']=json.loads(
            json.dumps(self.feed['countries']['ET']))
        self.feed['countries']['DE']['logos']['file']='DE.zip'
        self.feed['country_count']=3
        self._network()
        with self.assertRaisesRegex(ValueError,'country index count mismatch'):
            fetch.sync_world(self.paths,self.network,require_external=False)
        self.assertFalse((self.paths/'radio-world').exists())

    def test_complete_world_feed_with_one_partial_logo_country_is_rejected(self):
        # A central complete=true flag is not sufficient; check every
        # participating country's original PNG ZIP attempt completeness.
        self.feed['countries']['ET']['logo_package_complete'] = False
        self._network()
        with self.assertRaisesRegex(ValueError, 'Incomplete country logo listing'):
            fetch.sync_world(self.paths,self.network,require_external=False)
        self.assertFalse((self.paths/'radio-world').exists())

    def test_incomplete_feed_refused(self):
        self.feed['complete']=False
        self._network()
        with self.assertRaisesRegex(ValueError,'Untrusted'):
            fetch.sync_world(self.paths,self.network,require_external=False)

    def test_arbitrary_external_redirect_refused(self):
        self._network('https://evil.invalid/payload')
        with self.assertRaisesRegex(ValueError,'redirect'):
            fetch.sync_world(self.paths,self.network,require_external=False)
        self.assertFalse((self.paths/'radio-world').exists())

    def test_external_disk_required_in_production(self):
        self.assertEqual(fetch.sync_world(self.paths,self.network)['skipped'],
                         'unsafe-storage')
        self.assertEqual(self.network.calls,[])

if __name__=='__main__':
    unittest.main(verbosity=2)
