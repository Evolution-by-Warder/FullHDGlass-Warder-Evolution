#!/usr/bin/env python3
"""Offline regression tests: live bouquet, identity and bounded on-demand picons."""
import importlib.util
import json
from pathlib import Path
import sys
import tempfile
from types import ModuleType, SimpleNamespace
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
P = ROOT / 'source/package-root/usr/lib/enigma2/python/Plugins/Extensions/setupGlass17'
pkg = ModuleType('warder_live_tests')
pkg.__path__ = [str(P)]
sys.modules[pkg.__name__] = pkg
spec = importlib.util.spec_from_file_location(pkg.__name__ + '.warderRadioLive', P / 'warderRadioLive.py')
live = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = live
spec.loader.exec_module(live)
NOW = 1800000000
UUID_SK = '12345678-1234-1234-1234-123456789abc'
UUID_CZ = '22345678-1234-1234-1234-123456789abc'


def station(uuid, name='Test Rádio', url='https://radio.example.org/live', **extra):
    return dict(stationuuid=uuid, name=name, url=url, favicon='https://radio.example.org/logo.png', **extra)


class Browser:
    def __init__(self, offline=False):
        self.calls = []
        self.offline = offline

    def page(self, country, offset):
        self.calls.append((country, offset))
        uuid = {'SK': UUID_SK, 'CZ': UUID_CZ, 'DE': '32345678-1234-1234-1234-123456789abc'}.get(country, UUID_CZ)
        return SimpleNamespace(rows=[station(uuid, country + ' Rádio')], more=False, offline=self.offline)


class LogoStore:
    def __init__(self, path):
        self.path = path
        self.calls = []

    def get(self, item):
        self.calls.append(item['stationuuid'])
        return str(self.path)


class LiveTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.bouquet = self.root / live.FILE
        self.index = self.root / 'bouquets.radio'
        self.legacy = self.root / 'userbouquet.warder.radio'
        self.legacy.write_bytes(b'#NAME Warder Radio Streams\n#SERVICE 1:64:2:0:0:0:0:0:0:0:\n')

    def test_stable_identity_and_url_is_encoded(self):
        first = live._entry(station(UUID_SK))
        second = live._entry(station(UUID_SK, url='https://new.example.org/stream'))
        self.assertEqual(first['stem'], second['stem'])
        self.assertNotEqual(first['url'], second['url'])
        self.assertTrue(first['stem'].startswith('4097_0_2_'))
        self.assertIn('https%3A//radio.example.org/live', live._service(first))
        self.assertEqual(live._entry(station(UUID_CZ))['stem'] == first['stem'], False)
        with self.assertRaises(ValueError):
            live.service_stem('unknown')

    def test_live_bouquet_keeps_legacy_and_other_user_bouquets(self):
        personal = b'#NAME My radios\n#SERVICE 1:7:2:0:0:0:0:0:0:0:FROM BOUQUET "userbouquet.personal.radio" ORDER BY bouquet\n'
        self.index.write_bytes(personal)
        browser = Browser()
        self.assertEqual(live.refresh(self.root, NOW, browser)['stations'], 2)
        self.assertEqual(browser.calls, [('SK', 0), ('CZ', 0)])
        data = self.bouquet.read_text()
        self.assertIn('#NAME Warder Radio Live', data)
        self.assertIn('#DESCRIPTION SK', data)
        self.assertIn('#DESCRIPTION CZ', data)
        self.assertEqual(data.count('#SERVICE 4097:0:2:'), 2)
        self.assertEqual(self.legacy.read_bytes(), b'#NAME Warder Radio Streams\n#SERVICE 1:64:2:0:0:0:0:0:0:0:\n')
        index = self.index.read_bytes()
        self.assertTrue(index.startswith(personal))
        self.assertEqual(index.count(live.INDEX_LINE), 1)
        mapping = json.loads((self.root / live.DATA_FILE).read_text())
        self.assertEqual(len(mapping['stations']), 2)

    def test_no_network_during_daily_interval(self):
        live.refresh(self.root, NOW, Browser())
        browser = Browser()
        result = live.refresh(self.root, NOW + 3600, browser)
        self.assertEqual(result['skipped'], 'not-due')
        self.assertEqual(browser.calls, [])
        self.assertEqual(self.index.read_bytes().count(live.INDEX_LINE), 1)

    def test_offline_keeps_last_good_bouquet(self):
        live.refresh(self.root, NOW, Browser())
        original = self.bouquet.read_bytes()
        with self.assertRaises(OSError):
            live.refresh(self.root, NOW + live.DAY + 1, Browser(offline=True))
        self.assertEqual(original, self.bouquet.read_bytes())
        self.assertEqual(live.refresh(self.root, NOW + live.DAY + 2, Browser())['skipped'], 'not-due')

    def test_user_edited_or_symlink_bouquet_never_overwritten(self):
        self.bouquet.write_bytes(b'#NAME Personal bouquet\n')
        result = live.refresh(self.root, NOW, Browser())
        self.assertEqual(result['skipped'], 'unmanaged')
        self.assertEqual(self.bouquet.read_bytes(), b'#NAME Personal bouquet\n')
        self.bouquet.unlink()
        self.bouquet.symlink_to(self.legacy)
        result = live.refresh(self.root, NOW, Browser())
        self.assertEqual(result['skipped'], 'unsafe-path')
        self.assertTrue(self.bouquet.is_symlink())

    def test_selected_online_country_is_included(self):
        plugin = self.root / 'warder-radio'
        plugin.mkdir()
        (plugin / 'state.json').write_text(json.dumps({'online_country': 'DE'}))
        browser = Browser()
        live.refresh(self.root, NOW, browser)
        self.assertEqual(browser.calls, [('SK', 0), ('CZ', 0), ('DE', 0)])
        self.assertIn('#DESCRIPTION DE', self.bouquet.read_text())

    def test_picon_single_station_exact_and_no_overwrite(self):
        live.refresh(self.root, NOW, Browser())
        mapping = json.loads((self.root / live.DATA_FILE).read_text())
        stem = mapping['stations'][0]['stem']
        icon_dir = self.root / 'picon'
        icon_dir.mkdir()
        source = self.root / 'logo.png'
        source.write_bytes(b'\x89PNG\r\n\x1a\nexample image')
        logos = LogoStore(source)
        result = live.get_icon(stem, self.root, logos, icon_dir)
        self.assertTrue(result['changed'])
        native = icon_dir / (stem + '.png')
        alias = icon_dir / ('1' + stem[4:] + '.png')
        self.assertEqual(native.read_bytes(), source.read_bytes())
        self.assertEqual(alias.read_bytes(), source.read_bytes())
        self.assertEqual(logos.calls, [UUID_SK])
        self.assertEqual(live.get_icon(stem, self.root, logos, icon_dir)['skipped'], 'already-present')
        self.assertEqual(logos.calls, [UUID_SK])
        self.assertEqual(len(list(icon_dir.iterdir())), 2)

    def test_approved_existing_picon_is_never_replaced(self):
        live.refresh(self.root, NOW, Browser())
        stem = json.loads((self.root / live.DATA_FILE).read_text())['stations'][0]['stem']
        icons = self.root / 'picon'
        icons.mkdir()
        approved = icons / ('1' + stem[4:] + '.png')
        approved.write_bytes(b'owner-approved')
        source = self.root / 'logo.png'
        source.write_bytes(b'\x89PNG\r\n\x1a\nexample image')
        store = LogoStore(source)
        self.assertEqual(live.get_icon(stem, self.root, store, icons)['skipped'], 'already-present')
        self.assertEqual(approved.read_bytes(), b'owner-approved')
        self.assertEqual(store.calls, [])

    def test_user_modified_cached_picon_is_preserved(self):
        live.refresh(self.root, NOW, Browser())
        stem = json.loads((self.root / live.DATA_FILE).read_text())['stations'][0]['stem']
        folder = self.root / 'picon'
        folder.mkdir()
        source = self.root / 'logo.png'
        source.write_bytes(b'\x89PNG\r\n\x1a\noriginal image')
        store = LogoStore(source)
        self.assertTrue(live.get_icon(stem, self.root, store, folder)['changed'])
        path = folder / (stem + '.png')
        path.write_bytes(b'approved replacement')
        source.write_bytes(b'\x89PNG\r\n\x1a\nchanged source')
        self.assertEqual(live.get_icon(stem, self.root, store, folder)['skipped'], 'already-present')
        self.assertEqual(path.read_bytes(), b'approved replacement')

    def test_owned_logo_refreshes_after_ttl(self):
        live.refresh(self.root, NOW, Browser())
        stem = json.loads((self.root / live.DATA_FILE).read_text())['stations'][0]['stem']
        folder = self.root / 'picon'
        folder.mkdir()
        source = self.root / 'logo.png'
        source.write_bytes(b'\x89PNG\r\n\x1a\ninitial logo')
        store = LogoStore(source)
        with patch.object(live.time, 'time', return_value=NOW):
            self.assertTrue(live.get_icon(stem, self.root, store, folder)['changed'])
        old = (folder / (stem + '.png')).read_bytes()
        source.write_bytes(b'\x89PNG\r\n\x1a\nupdated logo')
        with patch.object(live.time, 'time', return_value=NOW + 8 * live.DAY):
            self.assertTrue(live.get_icon(stem, self.root, store, folder)['changed'])
        self.assertNotEqual(old, (folder / (stem + '.png')).read_bytes())
        self.assertEqual((folder / ('1' + stem[4:] + '.png')).read_bytes(), source.read_bytes())

    def test_picon_directory_rejects_image_flash(self):
        with patch.object(live.os, 'stat', wraps=live.os.stat) as stat:
            self.assertIsNone(live._picon_dir())
            self.assertTrue(stat.called)

    def test_invalid_reference_does_not_download(self):
        source = self.root / 'logo.png'
        source.write_bytes(b'\x89PNG\r\n\x1a\nexample image')
        store = LogoStore(source)
        self.assertEqual(live.get_icon('../../personal', self.root, store, self.root)['skipped'], 'invalid-stem')
        self.assertEqual(store.calls, [])

    def test_no_automatic_picon_file_without_station_selection(self):
        live.refresh(self.root, NOW, Browser())
        self.assertFalse((self.root / live.ICON_STATE).exists())

    def test_update_preserves_service_identity_for_changed_stream(self):
        live.refresh(self.root, NOW, Browser())
        first = self.bouquet.read_text()
        class NewBrowser(Browser):
            def page(self, country, offset):
                result = super().page(country, offset)
                result.rows[0]['url'] = 'https://new.example.org/stream'
                return result
        live.refresh(self.root, NOW + live.DAY + 1, NewBrowser())
        second = self.bouquet.read_text()
        self.assertNotEqual(first, second)
        self.assertIn('https%3A//new.example.org/stream', second)
        self.assertEqual(first.split('#SERVICE 4097:0:2:')[1].split(':', 7)[:7],
                         second.split('#SERVICE 4097:0:2:')[1].split(':', 7)[:7])

    def test_visible_channel_requests_exact_picon_without_gui_network(self):
        live.refresh(self.root, NOW, Browser())
        row = json.loads((self.root / live.DATA_FILE).read_text())['stations'][1]
        stem = row['stem']
        class Call:
            def __init__(self):
                self.cancelled = False
            def active(self):
                return not self.cancelled
            def cancel(self):
                self.cancelled = True
        class Loop:
            def __init__(self):
                self.calls = []
            def callLater(self, seconds, callback):
                self.calls.append((seconds, callback))
                return Call()
        loop = Loop()
        with patch.object(live, 'DIRECTORY', self.root):
            ctl = live.Controller(loop, lambda: None)
            try:
                self.assertIn(stem, ctl.known_icons)
                reference = stem.replace('_', ':') + ':https%3A//radio.example.org/live'
                with patch.object(live, '_controller', ctl):
                    live.request_picon(reference)
                    self.assertEqual(ctl.icon_queue[0], stem)
                    self.assertIn(0.3, [seconds for seconds, _ in loop.calls])
                    before = len(loop.calls)
                    live.request_picon(reference)
                    self.assertEqual(len(loop.calls), before)
                    live.request_picon('4097:0:2:1:2:3:4:0:0:0:https%3A//unmanaged')
                    self.assertEqual(ctl.icon_queue[0], stem)
            finally:
                ctl.close()

    def test_channel_picon_fallback_wires_only_live_radio_on_miss(self):
        code = (P / 'warderChannelPicons.py').read_text()
        self.assertIn('from Plugins.Extensions.setupGlass17.warderRadioLive import request_picon', code)
        self.assertIn('if custom_folder is None:', code)

    def test_no_touched_radio_plugin_state(self):
        plugin = self.root / 'warder-radio'
        plugin.mkdir()
        state = plugin / 'state.json'
        state.write_text(json.dumps({'favourites': ['owner']}) + '\n')
        live.refresh(self.root, NOW, Browser())
        self.assertEqual(json.loads(state.read_text())['favourites'], ['owner'])


if __name__ == '__main__':
    unittest.main()
