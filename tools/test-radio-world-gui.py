#!/usr/bin/env python3
"""Offline GUI wiring of Radio Browser world snapshots and separate PNG ZIPs."""
import importlib.util
from pathlib import Path
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'source/package-root/usr/lib/enigma2/python'))
from Plugins.Extensions.setupGlass17 import warderRadioCountry as country
from Plugins.Extensions.setupGlass17 import warderRadioWorld as world
from Plugins.Extensions.setupGlass17 import warderRadioLive as live
from Plugins.Extensions.setupGlass17 import warderRadioPackages as packages
from Plugins.Extensions.setupGlass17 import warderChannelPicons as channel


def load_fixture(filename):
    spec = importlib.util.spec_from_file_location(
        'world_gui_fixtures_' + filename.replace('-', '_'), ROOT/'tools'/filename)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


snapshot = load_fixture('test-radio-world.py').snapshot


class Call:
    def __init__(self, delay=0):
        self.delay, self.cancelled = delay, False
    def active(self):
        return not self.cancelled
    def cancel(self):
        self.cancelled = True


class Loop:
    def __init__(self):
        self.calls = []
    def callLater(self, delay, callback):
        self.calls.append((delay, callback))
        return Call(delay)


class Tests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)
        self.paths = self.root/'hdg17_files'
        self.paths.mkdir()
        (self.paths/'picon').mkdir()
        self.etc = self.root/'enigma2'
        self.etc.mkdir()
        (self.etc/'settings').write_text('config.osd.language=fr_FR\n')
        (self.etc/'bouquets.radio').write_bytes(b'#NAME Bouquets (Radio)\n')
        archive, digest = snapshot(self.root)
        self.assertTrue(world.install_world(archive,digest,self.paths,False)['changed'])
        self.assertEqual(country.bootstrap(self.etc)['country'],'FR')
        self.previous_controller = live._controller
        self.addCleanup(setattr,live,'_controller',self.previous_controller)

    def controller(self):
        ctrl = live.Controller.__new__(live.Controller)
        ctrl.loop = Loop()
        ctrl.reload = lambda: None
        ctrl.session = None
        ctrl.pending = None
        ctrl.icon_timer = None
        ctrl.radio_refresh_timer = None
        ctrl.timeout = None
        ctrl.worker = None
        ctrl.icon_worker = None
        ctrl.world_worker = None
        ctrl.world_timer = None
        ctrl.world_timeout = None
        ctrl.closed = False
        ctrl.initial_reload = False
        ctrl.last_icon = None
        ctrl.icon_queue = []
        ctrl.known_icons = set()
        ctrl.icon_requested = {}
        ctrl.map_mtime = None
        ctrl.local_world_sha = None
        ctrl.active_local_key = None
        ctrl.local_worker_key = None
        ctrl.last_bulk_logo = None
        return ctrl

    def test_ready_countries_are_discovered_without_entire_map_scan(self):
        self.assertIsNotNone(world.cached_country(self.paths,'FR'))
        self.assertIsNotNone(world.cached_country(self.paths,'ET'))
        self.assertIsNone(world.cached_country(self.paths,'DE'))

    def test_country_menu_matches_installed_world_not_stale_plugin_names(self):
        with patch.object(live, '_radio_world_root', return_value=self.paths):
            choices = country.country_options()
        self.assertEqual({code for name, code in choices}, {'ET', 'FR'})
        self.assertIn(('Ethiopia', 'ET'), choices)
        # The name map may be incomplete, but the authoritative world index
        # must still expose every installed country.
        self.assertFalse(any(code == 'SK' for _, code in choices))

    def test_country_menu_retains_old_options_when_world_not_ready(self):
        with patch.object(live, '_radio_world_root', return_value=None):
            choices = country.country_options()
        self.assertTrue(choices)
        self.assertIn('SK', {code for _, code in choices})

    def test_gui_pending_choice_uses_local_subprocess_not_online_browser(self):
        selected = country.request_country('ET',self.etc)
        self.assertTrue(selected['accepted'])
        ctrl = self.controller()
        spawned = []
        ctrl._spawn = lambda kind,args,callback: spawned.append((kind,args)) or object()
        with patch.object(live,'DIRECTORY',self.etc), patch.object(live,'_radio_world_root',
                                                                   return_value=self.paths):
            ctrl.check()
            self.assertEqual(len(spawned),1)
            self.assertEqual(spawned[0],('local',['--activate-world','ET',str(self.paths)]))
            result = world.activate_from_world(self.paths,'ET',self.etc,
                                               require_requested=True)
            self.assertTrue(result['local'])
            ctrl._load_icon_map = lambda: None
            ctrl.finished(result)
        self.assertEqual(country.diagnose(self.etc)['active'],'ET')
        self.assertEqual(ctrl.active_local_key,( 'ET',world.cached_country(self.paths,'ET')))
        self.assertTrue(any(call[0] == .2 for call in ctrl.loop.calls))

    def test_changed_choice_while_local_worker_runs_cannot_activate_stale_country(self):
        country.request_country('ET',self.etc)
        country.request_country('FR',self.etc)
        target=self.etc/live.FILE
        original=target.read_bytes()
        stale=world.activate_from_world(self.paths,'ET',self.etc,
                                        require_requested=True)
        self.assertEqual(stale['skipped'],'country-superseded')
        self.assertEqual(target.read_bytes(),original)
        self.assertEqual(country.diagnose(self.etc)['active'],'FR')

    def test_radio_only_original_zip_overrides_default_picon_for_own_station(self):
        src=self.root/'source'
        from Plugins.Extensions.setupGlass17 import warderRadioPackages as packages
        one=load_fixture('test-radio-packages.py').example
        rows,_=one(src,'FR','France')
        result=packages.install_logos(src,'FR',self.paths/'picon',require_external=False)
        self.assertEqual(result['logos'],3)
        stem=rows[0]['stem']
        live._controller=SimpleNamespace(local_world_sha='a'*64,
                                         known_icons={stem})
        reference=stem.replace('_',':')+':https%3A//example.org/FR'
        found=channel.find_picon(reference,str(self.paths),lambda s:s,
            lambda ref:'', lambda name:name)
        self.assertEqual(found,str(self.paths/'picon'/'radio'/(stem+'.png')))
        # User-custom picons override any radio-zip logo.
        custom=self.root/'own'
        custom.mkdir()
        (custom/(stem+'.png')).write_bytes(b'preferred')
        found=channel.find_picon(reference,str(self.paths),lambda s:s,
            lambda ref:'',lambda name:name,custom_folder=str(custom))
        self.assertEqual(found,str(custom/(stem+'.png')))
        # A TV station with a foreign reference cannot pick a radio logo.
        tv='1:0:19:1F48:CA1:3:EB0000:0:0:0:'
        name=tv.rstrip(':').replace(':','_')
        path=self.paths/'picon'/(name+'.png')
        path.write_bytes(b'satellite')
        self.assertEqual(channel.find_picon(tv,str(self.paths),lambda s:s,
                          lambda ref:'',lambda name:name),str(path))

    def test_cached_country_logo_worker_downloads_country_zip_not_individual_png(self):
        ctrl=self.controller()
        output=[]
        ctrl._spawn=lambda action,args,cb: output.append((action,args)) or object()
        with patch.object(live,'DIRECTORY',self.etc), patch.object(live,'_radio_world_root',
                 return_value=self.paths), patch.object(live,'_radio_custom_picons_enabled',
                 return_value=False):
            ctrl.check_icon()
        self.assertEqual(output,[('logo_zip',['--logos-world','FR',str(self.paths)])])
        self.assertTrue(ctrl.local_world_sha)
        self.assertEqual(ctrl.icon_timer.delay,12)

    def test_explicit_own_picon_source_prevents_managed_radio_zip(self):
        ctrl=self.controller()
        output=[]
        ctrl._spawn=lambda action,args,cb: output.append((action,args)) or object()
        with patch.object(live,'DIRECTORY',self.etc), patch.object(live,'_radio_world_root',
                 return_value=self.paths), patch.object(live,'_radio_custom_picons_enabled',
                 return_value=True):
            ctrl.check_icon()
        self.assertEqual(output,[])

    def test_world_snapshot_sync_is_scheduled_on_worker_with_fortnightly_retry(self):
        ctrl=self.controller()
        output=[]
        ctrl._spawn=lambda action,args,cb: output.append((action,args)) or object()
        with patch.object(live,'_radio_world_root',return_value=self.paths):
            ctrl.check_world()
        self.assertEqual(output,[('world',['--sync-world',str(self.paths)])])
        ctrl.request_refresh=lambda:output.append(('refresh',[]))
        ctrl.world_done({'changed':True,'countries':2})
        self.assertEqual(output[-1],('refresh',[]))
        self.assertTrue(any(delay==14*live.DAY for delay,cb in ctrl.loop.calls))

    def test_offline_unavailable_world_does_not_break_existing_country(self):
        ctrl=self.controller()
        with patch.object(live,'_radio_world_root',return_value=None):
            ctrl.check_world()
        self.assertEqual(ctrl.world_timer.delay,3600)
        self.assertEqual(country.diagnose(self.etc)['active'],'FR')


if __name__=='__main__':
    unittest.main(verbosity=2)
