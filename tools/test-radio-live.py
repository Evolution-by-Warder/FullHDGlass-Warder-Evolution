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
native = ModuleType(pkg.__name__ + '.warderHelpPreview')
native._NativeLoop = object
sys.modules[native.__name__] = native
spec = importlib.util.spec_from_file_location(pkg.__name__ + '.warderRadioLive', P / 'warderRadioLive.py')
live = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = live
spec.loader.exec_module(live)
REAL_PICON_PNG = live._picon_png
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
        # Existing ownership tests use stub PNG headers; actual Pillow
        # geometry/alpha processing has a dedicated real-image test below.
        local_picon = patch.object(live, '_picon_png', side_effect=lambda payload: payload)
        local_picon.start()
        self.addCleanup(local_picon.stop)
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

    def test_malformed_uuid_and_untrusted_stream_urls_are_rejected(self):
        self.assertEqual(live.service_stem(UUID_SK),
                         live.service_stem(UUID_SK.replace('-', '').upper()))
        for malformed in ('x' * 36, '----' + '0' * 32, 'not-a-uuid'):
            with self.subTest(uuid=malformed), self.assertRaises(ValueError):
                live.service_stem(malformed)
        for url in ('http://', 'ftp://radio.example.org/stream',
                    'https://user:pass@radio.example.org/stream',
                    'https://radio.example.org:notaport/live',
                    'https://radio.example.org/line\nbreak'):
            with self.subTest(url=url), self.assertRaises(ValueError):
                live._entry(station(UUID_SK, url=url))

    def test_live_bouquet_keeps_legacy_and_other_user_bouquets(self):
        personal = b'#NAME My radios\n#SERVICE 1:7:2:0:0:0:0:0:0:0:FROM BOUQUET "userbouquet.personal.radio" ORDER BY bouquet\n'
        self.index.write_bytes(personal)
        browser = Browser()
        self.assertEqual(live.refresh(self.root, NOW, browser)['stations'], 2)
        self.assertEqual(browser.calls, [('SK', 0), ('CZ', 0)])
        data = self.bouquet.read_text()
        self.assertIn('#NAME Warder Radio Live', data)
        self.assertIn('#DESCRIPTION Slovensko', data)
        self.assertIn('#DESCRIPTION Čechy', data)
        self.assertEqual(data.count('#SERVICE 4097:0:2:'), 2)
        self.assertEqual(self.legacy.read_bytes(), b'#NAME Warder Radio Streams\n#SERVICE 1:64:2:0:0:0:0:0:0:0:\n')
        index = self.index.read_bytes()
        self.assertTrue(index.startswith(b'#NAME My radios\n' + live.INDEX_LINE))
        self.assertIn(personal.split(b'\n', 1)[1], index)
        self.assertEqual(index.count(live.INDEX_LINE), 1)
        mapping = json.loads((self.root / live.DATA_FILE).read_text())
        self.assertEqual(len(mapping['stations']), 2)

    def test_bootstrap_replaces_legacy_first_and_reclaims_old_files(self):
        sections = [
            ('Slovensko', 'SK'),
            ('Čechy', 'CZ'),
            ('Deutschland', 'DE'),
            ('France', 'FR'),
        ]
        old = [live.LEGACY_HEADER]
        for index, (country, code) in enumerate(sections, 1):
            old += [
                b'#SERVICE 1:64:2:0:0:0:0:0:0:0:\n',
                ('#DESCRIPTION ' + country + '\n').encode('utf-8'),
                ('#SERVICE 4097:0:2:%X:1:EC:0:0:0:0:https%%3a//radio.test/%s\n' %
                 (index, code)).encode('utf-8'),
                ('#DESCRIPTION ' + code + ' original\n').encode('utf-8'),
            ]
        original = b''.join(old)
        self.legacy.write_bytes(original)
        backup = self.root / (live.LEGACY_FILE + '.bak')
        backup.write_bytes(original)
        personal = (b'#SERVICE 1:7:2:0:0:0:0:0:0:0:FROM BOUQUET '
                    b'"userbouquet.my-radio.radio" ORDER BY bouquet\n')
        prior = (b'#SERVICE 1:7:2:0:0:0:0:0:0:0:FROM BOUQUET '
                 b'"userbouquet.warder.radio" ORDER BY bouquet\n')
        self.index.write_bytes(b'#NAME User Radio\n' + personal + prior)
        outcome = live.bootstrap(self.root)
        self.assertTrue(outcome['legacy_retired'])
        self.assertFalse(self.legacy.exists())
        self.assertFalse(backup.exists())
        result = self.bouquet.read_bytes()
        self.assertEqual(result, live.HEADER + original[len(live.LEGACY_HEADER):])
        self.assertEqual(len(live._sections(result)), 4)
        radio_index = self.index.read_bytes()
        self.assertEqual(radio_index, b'#NAME User Radio\n' + live.INDEX_LINE + personal)
        self.assertEqual(live.bootstrap(self.root)['changed'], False)
        self.assertFalse(self.legacy.exists())
        self.assertTrue(self.bouquet.exists())

    def test_stations_alphabetic_within_country_and_all_refs_preserved(self):
        """Rebuild a deliberately scrambled world bouquet; no station disappears."""
        records = [
            ('Žilinské rádio', 'https%3A//stream.test/zilina', 'A1'),
            ('Rádio Expres', 'https%3A//stream.test/expres', 'A2'),
            ('897', 'https%3A//stream.test/897', 'A3'),
            ('Československé rádio', 'https%3A//stream.test/cs', 'A4'),
            ('Áčko rádio', 'https%3A//stream.test/acko', 'A5'),
            ('Rádio Beta', 'https%3A//stream.test/beta', 'A6'),
        ]
        original = [live.LEGACY_HEADER,
                    b'#SERVICE 1:64:2:0:0:0:0:0:0:0:\n',
                    '#DESCRIPTION Slovensko\n'.encode('utf-8')]
        services = []
        for label, url, ref in records:
            service = ('#SERVICE 4097:0:2:%s:1:EC:0:0:0:0:%s\n' %
                       (ref, url)).encode('ascii')
            description = ('#DESCRIPTION %s\n' % label).encode('utf-8')
            original.extend([service, description])
            services.append(service + description)
        self.legacy.write_bytes(b''.join(original))
        result = live.bootstrap(self.root)
        self.assertTrue(result['legacy_retired'])
        self.assertFalse(self.legacy.exists())
        section = live._sections(self.bouquet.read_bytes())['Slovensko']
        lines = section.decode('utf-8').splitlines()
        names = [line.removeprefix('#DESCRIPTION ') for line in lines
                 if line.startswith('#DESCRIPTION ')][1:]
        self.assertEqual(names, ['897', 'Áčko rádio', 'Československé rádio',
                                 'Rádio Beta', 'Rádio Expres', 'Žilinské rádio'])
        for record in services:
            self.assertEqual(section.count(record), 1)
        self.assertEqual(section.count(b'#SERVICE 4097:'), len(records))
        self.assertFalse(live.bootstrap(self.root)['changed'])  # idempotent

    def test_rerender_sorts_existing_live_bouquet_on_reinstall(self):
        """An already managed test127 bouquet must be sorted by local bootstrap."""
        raw = (live.HEADER +
               b'#SERVICE 1:64:2:0:0:0:0:0:0:0:\n' +
               '#DESCRIPTION Slovensko\n'.encode('utf-8') +
               b'#SERVICE 4097:0:2:1:1:EC:0:0:0:0:https%3A//b.test\n'
               b'#DESCRIPTION Zeta\n'
               b'#SERVICE 4097:0:2:2:1:EC:0:0:0:0:https%3A//a.test\n'
               b'#DESCRIPTION Alfa\n')
        self.bouquet.write_bytes(raw)
        (self.root / live.STATE_FILE).write_text(json.dumps({
            'bouquet_sha256': __import__('hashlib').sha256(raw).hexdigest(),
            'bootstrap_generation': live.BOOTSTRAP_GENERATION
        }))
        outcome = live.bootstrap(self.root)
        self.assertTrue(outcome['changed'])
        names = self.bouquet.read_text().split('#DESCRIPTION ')[2:]
        self.assertEqual([x.split('\n', 1)[0] for x in names], ['Alfa', 'Zeta'])
        self.assertEqual(self.bouquet.read_bytes().count(b'#SERVICE 4097:'), 2)

    def test_sort_unknown_station_layout_does_not_modify_content(self):
        """Unsupported metadata patterns must be retained, never discarded."""
        section = (b'#SERVICE 1:64:2:0:0:0:0:0:0:0:\n'
                   b'#DESCRIPTION Group\n'
                   b'#SERVICE 4097:0:2:2:1:EC:0:0:0:0:https%3A//b.test\n'
                   b'#DESCRIPTION Beta\n'
                   b'#SOME-CUSTOM-SETTING stays with Beta\n'
                   b'#SERVICE 4097:0:2:1:1:EC:0:0:0:0:https%3A//a.test\n'
                   b'#DESCRIPTION Alfa\n')
        sorted_section = live._sorted_country_section(section)
        self.assertTrue(sorted_section.index(b'#DESCRIPTION Alfa') <
                        sorted_section.index(b'#DESCRIPTION Beta'))
        self.assertEqual(sorted_section.count(b'#SOME-CUSTOM-SETTING stays with Beta'), 1)
        self.assertTrue(sorted_section.endswith(b'#SOME-CUSTOM-SETTING stays with Beta\n'))
        corrupted = section.replace(b'#DESCRIPTION Alfa', b'#UNRECOGNIZED Alfa')
        self.assertEqual(live._sorted_country_section(corrupted), corrupted)

    def test_country_headings_alphabetical_after_slovakia_and_czechia(self):
        """Out-of-order historical countries must become sorted without losing data."""
        headings = ('Zulu', 'Österreich', 'Čechy', 'France', 'Slovensko',
                    'Deutschland', 'Åland Islands')
        sections = []
        original_parts = [live.LEGACY_HEADER]
        for number, label in enumerate(headings, 1):
            payload = (
                '#SERVICE 1:64:2:0:0:0:0:0:0:0:\n'
                '#DESCRIPTION ' + label + '\n'
                '#SERVICE 4097:0:2:%X:1:EC:0:0:0:0:https%%3A//station.example/%d\n' %
                (number, number) +
                '#DESCRIPTION Station %d\n' % number
            ).encode('utf-8')
            original_parts.append(payload)
        original = b''.join(original_parts)
        self.legacy.write_bytes(original)
        original_sections = live._sections(original)
        result = live.bootstrap(self.root)
        self.assertTrue(result['changed'])
        self.assertEqual(list(live._sections(self.bouquet.read_bytes())),
                         ['Slovensko', 'Čechy', 'Åland Islands', 'Deutschland',
                          'France', 'Österreich', 'Zulu'])
        self.assertEqual(live._sections(self.bouquet.read_bytes()), original_sections)
        self.assertFalse(self.legacy.exists())  # byte-identical country content
        self.assertEqual(self.bouquet.read_bytes().count(b'#SERVICE 4097:'), 7)
        self.assertEqual(live.bootstrap(self.root)['changed'], False)

    def test_live_updates_keep_alphabetical_country_order(self):
        """An online update must not append new countries at the end."""
        sections = [
            ('France', 1), ('Slovensko', 2), ('Čechy', 3), ('Österreich', 4)
        ]
        old = [live.LEGACY_HEADER]
        for label, number in sections:
            old.append((
                '#SERVICE 1:64:2:0:0:0:0:0:0:0:\n'
                '#DESCRIPTION ' + label + '\n'
                '#SERVICE 4097:0:2:%X:1:EC:0:0:0:0:https%%3A//radio.example/%d\n' %
                (number, number) +
                '#DESCRIPTION Original %d\n' % number
            ).encode('utf-8'))
        self.legacy.write_bytes(b''.join(old))
        live.bootstrap(self.root)
        sections_before = live._sections(self.bouquet.read_bytes())
        self.assertEqual(list(sections_before), ['Slovensko', 'Čechy',
                                                'France', 'Österreich'])
        online = {'Zambia': (
            b'#SERVICE 1:64:2:0:0:0:0:0:0:0:\n'
            b'#DESCRIPTION Zambia\n'
            b'#SERVICE 4097:0:2:9:1:EC:0:0:0:0:https%3A//zambia.example\n'
            b'#DESCRIPTION Zambia Radio\n'
        )}
        merged = live._combined(None, self.bouquet.read_bytes(), online)
        self.assertEqual(list(live._sections(merged)),
                         ['Slovensko', 'Čechy', 'France', 'Österreich', 'Zambia'])
        for label, body in sections_before.items():
            self.assertEqual(live._sections(merged)[label], body)

    def test_legacy_remains_if_any_country_would_be_lost(self):
        original = (live.LEGACY_HEADER +
                    b'#SERVICE 1:64:2:0:0:0:0:0:0:0:\n'
                    b'#DESCRIPTION Germany\n'
                    b'#SERVICE 4097:0:2:1:2:3:4:0:0:0:https%3A//example.org\n'
                    b'#DESCRIPTION Legacy radio\n')
        self.legacy.write_bytes(original)
        live.bootstrap(self.root)
        self.assertFalse(self.legacy.exists())
        # Recreate a managed legacy file with an additional country not copied
        # into the currently owned live target. Direct cleanup must reject it.
        extra = (b'#SERVICE 1:64:2:0:0:0:0:0:0:0:\n'
                 b'#DESCRIPTION Another country\n'
                 b'#SERVICE 4097:0:2:9:2:3:4:0:0:0:https%3A//other.example.org\n'
                 b'#DESCRIPTION Extra station\n')
        self.legacy.write_bytes(original + extra)
        self.assertFalse(live._retire_legacy(self.root))
        self.assertTrue(self.legacy.exists())

    def test_world_incremental_updates_keep_unvisited_countries(self):
        original = (live.LEGACY_HEADER +
                    b'#SERVICE 1:64:2:0:0:0:0:0:0:0:\n#DESCRIPTION Deutschland\n'
                    b'#SERVICE 4097:0:2:1:2:3:4:0:0:0:https%3A//de.example.org\n'
                    b'#DESCRIPTION Original DE\n'
                    b'#SERVICE 1:64:2:0:0:0:0:0:0:0:\n#DESCRIPTION France\n'
                    b'#SERVICE 4097:0:2:2:2:3:4:0:0:0:https%3A//fr.example.org\n'
                    b'#DESCRIPTION Original FR\n')
        self.legacy.write_bytes(original)
        live.bootstrap(self.root)
        class World(Browser):
            def facets(self):
                return SimpleNamespace(countries=['SK', 'CZ', 'DE', 'FR'], offline=False)
            def page(self, country, offset):
                self.calls.append((country, offset))
                ids = {'SK': UUID_SK, 'CZ': UUID_CZ,
                       'DE': '32345678-1234-1234-1234-123456789abc',
                       'FR': '42345678-1234-1234-1234-123456789abc'}
                return SimpleNamespace(rows=[station(ids[country], country + ' updated')],
                                       more=False, offline=False)
        browser = World()
        first = live.refresh(self.root, NOW, browser)
        self.assertFalse(first['world_complete'])
        self.assertEqual(first['world_total'], 4)
        self.assertEqual(len(live._sections(self.bouquet.read_bytes())), 4)
        self.assertIn('Original DE', self.bouquet.read_text())
        self.assertIn('Original FR', self.bouquet.read_text())
        second = live.refresh(self.root, NOW + live.WORLD_STEP_INTERVAL, browser)
        self.assertTrue(second['world_complete'])
        self.assertEqual(browser.calls, [('SK', 0), ('CZ', 0), ('DE', 0), ('FR', 0)])
        self.assertIn('DE updated', self.bouquet.read_text())
        self.assertIn('FR updated', self.bouquet.read_text())
        self.assertEqual(len(live._sections(self.bouquet.read_bytes())), 4)
        self.assertFalse(self.legacy.exists())

    def test_no_network_during_daily_interval(self):
        live.refresh(self.root, NOW, Browser())
        browser = Browser()
        result = live.refresh(self.root, NOW + 60, browser)
        self.assertEqual(result['skipped'], 'not-due')
        self.assertEqual(browser.calls, [])
        self.assertEqual(self.index.read_bytes().count(live.INDEX_LINE), 1)

    def test_offline_keeps_last_good_bouquet(self):
        live.refresh(self.root, NOW, Browser())
        original = self.bouquet.read_bytes()
        with self.assertRaises(OSError):
            live.refresh(self.root, NOW + live.WORLD_REFRESH_INTERVAL + 1, Browser(offline=True))
        self.assertEqual(original, self.bouquet.read_bytes())
        self.assertEqual(live.refresh(self.root, NOW + live.WORLD_REFRESH_INTERVAL + 2, Browser())['skipped'], 'not-due')

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

    def test_user_edit_with_managed_header_is_not_overwritten(self):
        live.refresh(self.root, NOW, Browser())
        content = self.bouquet.read_text()
        changed = content.replace('SK Rádio', 'My manually edited radio')
        self.bouquet.write_text(changed)
        output = live.refresh(self.root, NOW + live.DAY + 100, Browser())
        self.assertEqual(output['skipped'], 'owner-modified')
        self.assertEqual(self.bouquet.read_text(), changed)
        self.assertFalse((self.root / (live.FILE + '.bak')).exists())

    def test_selected_online_country_is_included(self):
        plugin = self.root / 'warder-radio'
        plugin.mkdir()
        (plugin / 'state.json').write_text(json.dumps({'online_country': 'DE'}))
        browser = Browser()
        live.refresh(self.root, NOW, browser)
        self.assertEqual(browser.calls, [('SK', 0), ('CZ', 0)])
        live.refresh(self.root, NOW + live.WORLD_STEP_INTERVAL, browser)
        self.assertEqual(browser.calls, [('SK', 0), ('CZ', 0), ('DE', 0)])
        self.assertIn('#DESCRIPTION DE', self.bouquet.read_text())

    def test_empty_optional_country_keeps_core_radio_bouquets(self):
        plugin = self.root / 'warder-radio'
        plugin.mkdir()
        (plugin / 'state.json').write_text(json.dumps({'online_country': 'DE'}))
        class EmptyOptional(Browser):
            def page(self, country, offset):
                if country == 'DE':
                    self.calls.append((country, offset))
                    return SimpleNamespace(rows=[], more=False, offline=False)
                return super().page(country, offset)
        browser = EmptyOptional()
        result = live.refresh(self.root, NOW, browser)
        self.assertEqual(result['stations'], 2)
        self.assertEqual(browser.calls, [('SK', 0), ('CZ', 0)])
        live.refresh(self.root, NOW + live.WORLD_STEP_INTERVAL, browser)
        self.assertEqual(browser.calls, [('SK', 0), ('CZ', 0), ('DE', 0)])
        self.assertNotIn('#DESCRIPTION DE', self.bouquet.read_text())
        self.assertEqual(self.bouquet.read_text().count('#SERVICE 4097:0:2:'), 2)

    def test_gui_does_not_create_radio_picon_folders(self):
        import ast
        tree = ast.parse((P / 'warderRadioLive.py').read_text())
        folder = next(node for node in tree.body if isinstance(node, ast.FunctionDef)
                      and node.name == '_skin_picon_directory')
        calls = [n for n in ast.walk(folder) if isinstance(n, ast.Call)]
        self.assertFalse(any(isinstance(n.func, ast.Attribute) and n.func.attr == 'mkdir'
                             for n in calls))

    def test_real_radio_logo_preserves_aspect_ratio_and_alpha(self):
        try:
            from PIL import Image
        except ImportError:
            self.skipTest('Pillow is optional on CI host; installed by Radio plugin on receiver')
        import io
        logo = Image.new('RGBA', (72, 72), (234, 55, 33, 255))
        original = io.BytesIO()
        logo.save(original, 'PNG')
        output = REAL_PICON_PNG(original.getvalue())
        with Image.open(io.BytesIO(output)) as rendered:
            self.assertEqual(rendered.size, (220, 132))
            self.assertEqual(rendered.mode, 'RGBA')
            self.assertEqual(rendered.getpixel((0, 0))[3], 0)
            self.assertEqual(rendered.getpixel((110, 66))[3], 255)
            # A 72x72 square logo should remain square, not stretched to 220x132.
            self.assertEqual(rendered.getpixel((30, 66))[3], 0)
        with self.assertRaises((OSError, ValueError)):
            REAL_PICON_PNG(b'not a PNG')

    def test_background_prefetch_only_selected_home_countries(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            states = [{'countrycode': code,
                       'stem': live.service_stem('%08x-1234-1234-1234-123456789abc' % i)}
                      for code, count in [('SK', 10), ('CZ', 10), ('DE', 30)]
                      for i in range(count)]
            (root / live.DATA_FILE).write_text(json.dumps({'stations': states}))
            class Call:
                def active(self): return True
                def cancel(self): pass
            class Loop:
                def callLater(self, *_): return Call()
            with patch.object(live, 'DIRECTORY', root):
                controller = live.Controller(Loop(), lambda: None)
                try:
                    self.assertEqual(len(controller.icon_queue), 24)  # 8 per mapped country max
                    self.assertTrue(all(x in controller.known_icons for x in controller.icon_queue))
                finally:
                    controller.close()

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
        live.refresh(self.root, NOW + live.WORLD_REFRESH_INTERVAL + 1, NewBrowser())
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

    def test_missing_disk_does_not_block_later_icon_attempt(self):
        live.refresh(self.root, NOW, Browser())
        row = json.loads((self.root / live.DATA_FILE).read_text())['stations'][0]
        stem = row['stem']
        reference = stem.replace('_', ':') + ':https%3A//radio.example.org/live'

        class Call:
            def active(self):
                return True
            def cancel(self):
                return None
        class Loop:
            def callLater(self, *_):
                return Call()

        queue = []
        with patch.object(live, 'DIRECTORY', self.root), patch.dict(
                sys.modules, {'NavigationInstance': SimpleNamespace(instance=None)}):
            controller = live.Controller(Loop(), lambda: None)
            controller._spawn = lambda _action, args, _done: (queue.append(args) or object())
            try:
                with patch.object(live, '_skin_picon_directory', return_value=None):
                    controller.enqueue_icon(reference)
                    controller.check_icon()
                self.assertNotIn(stem, controller.icon_requested)
                self.assertEqual(queue, [])
                folder = str(self.root / 'picon')
                with patch.object(live, '_skin_picon_directory', return_value=folder):
                    controller.enqueue_icon(reference)
                    self.assertEqual(controller.icon_queue[0], stem)
                    controller.check_icon()
                # Since country original ZIPs are available, no isolated
                # per-station Radio Browser HTTP should be started, even
                # after the external disk becomes available. The separate
                # country-world worker is responsible for the signed ZIP.
                self.assertEqual(queue, [])
                self.assertNotIn(stem, controller.icon_requested)
            finally:
                controller.close()

    def test_old_icon_queue_cannot_trigger_legacy_favicon_download(self):
        """A signed country original ZIP, not a legacy per-row request, owns the artwork."""
        live.refresh(self.root, NOW, Browser())
        stem = json.loads((self.root / live.DATA_FILE).read_text())['stations'][0]['stem']
        reference = stem.replace('_', ':') + ':https%3A//radio.example.org/live'

        class Call:
            def active(self):
                return True
            def cancel(self):
                return None
        class Loop:
            def callLater(self, *_):
                return Call()
        launches = []
        with patch.object(live, 'DIRECTORY', self.root), patch.object(
                live, '_radio_world_root', return_value=None), patch.dict(
                sys.modules, {'NavigationInstance': SimpleNamespace(instance=None)}):
            controller = live.Controller(Loop(), lambda: None)
            controller._spawn = lambda *args: launches.append(args) or object()
            try:
                with patch.object(live, '_skin_picon_directory', return_value=str(self.root / 'picon')):
                    with patch.object(live.time, 'monotonic', return_value=1000):
                        controller.enqueue_icon(reference)
                        controller.check_icon()
                    with patch.object(live.time, 'monotonic', return_value=1001):
                        controller.enqueue_icon(reference)
                        controller.check_icon()
                self.assertEqual(launches, [])
                self.assertNotIn(stem, controller.icon_requested)
                self.assertEqual(controller.icon_queue[0], stem)
            finally:
                controller.close()

    def test_channel_picon_fallback_wires_only_live_radio_on_miss(self):
        code = (P / 'warderChannelPicons.py').read_text()
        self.assertIn('from Plugins.Extensions.setupGlass17.warderRadioLive import request_picon', code)
        self.assertIn('if custom_folder is None:', code)

    def test_real_channel_picon_lookup_queues_only_missing_native_radio(self):
        spec = importlib.util.spec_from_file_location(
            'warder_live_tests.channel_lookup', P / 'warderChannelPicons.py')
        lookup = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(lookup)
        from types import ModuleType
        calls = []
        parents = ['Plugins', 'Plugins.Extensions', 'Plugins.Extensions.setupGlass17']
        modules = {name: ModuleType(name) for name in parents}
        module_name = 'Plugins.Extensions.setupGlass17.warderRadioLive'
        modules[module_name] = ModuleType(module_name)
        modules[module_name].request_picon = calls.append
        live.refresh(self.root, NOW, Browser())
        item = json.loads((self.root / live.DATA_FILE).read_text())['stations'][0]
        ref = item['stem'].replace('_', ':') + ':https%3A//radio.example.org/live'
        base = self.root / 'skin'
        icons = base / 'picon'
        icons.mkdir(parents=True)
        own = self.root / 'own'
        own.mkdir()
        args = (ref, str(base), lambda raw: raw, lambda _ref: 'Test Rádio',
                lambda name: name)
        with patch.dict(sys.modules, modules):
            self.assertEqual(lookup.find_picon(*args), '')
            self.assertEqual(calls, [ref])
            self.assertEqual(lookup.find_picon(*args, custom_folder=str(own)), '')
            self.assertEqual(calls, [ref])
            existing = icons / (item['stem'] + '.png')
            existing.write_bytes(b'user-approved logo')
            self.assertEqual(lookup.find_picon(*args), str(existing))
            self.assertEqual(calls, [ref])

    def test_new_install_starts_live_refresh_without_blocking_opkg(self):
        postinst = (ROOT / 'source/control/postinst').read_text()
        self.assertIn('warder_radio_country=/usr/lib/enigma2/python/Plugins/Extensions/setupGlass17/warderRadioCountry.py',
                      postinst)
        # Signed Live runtime is owned by FullHDGlass, never gated by the
        # optional standalone WarderRadio extension on older images.
        self.assertNotIn('warder_radio_browser=', postinst)
        self.assertIn('"$warder_radio_country" --bootstrap </dev/null >/dev/null 2>&1', postinst)
        # The GUI-start world worker fetches the SHA-verified country
        # catalogue to external PATHS, never the old 60-station API pages.
        self.assertNotIn('"$warder_radio_country" --refresh </dev/null >/dev/null 2>&1 &', postinst)

    def test_failed_test124_import_can_retry_immediately_on_test125(self):
        state = self.root / live.STATE_FILE
        state.write_text(json.dumps({'attempt': NOW - 120, 'bootstrap_generation': 'live124'}))
        browser = Browser()
        result = live.refresh(self.root, NOW, browser)
        self.assertTrue(result['changed'])
        self.assertEqual(browser.calls, [('SK', 0), ('CZ', 0)])
        self.assertEqual(json.loads(state.read_text())['bootstrap_generation'], live.BOOTSTRAP_GENERATION)

    def test_first_import_cooldown_is_fifteen_minutes(self):
        failing = Browser(offline=True)
        with self.assertRaises(OSError):
            live.refresh(self.root, NOW, failing)
        self.assertEqual(live.refresh(self.root, NOW + 1, Browser())['skipped'], 'not-due')
        self.assertTrue(live.refresh(self.root, NOW + live.INITIAL_RETRY, Browser())['changed'])

    def test_new_picon_redraws_only_visible_servicelist(self):
        """Fresh PNG is shown without zapping or a full bouquet database reload."""
        screens = ModuleType('Screens')
        infobar_module = ModuleType('Screens.InfoBar')
        redraws = []
        native_list = SimpleNamespace(refresh=lambda: redraws.append('redraw'))
        screen = SimpleNamespace(shown=True, servicelist=SimpleNamespace(l=native_list))
        infobar_module.InfoBar = SimpleNamespace(instance=SimpleNamespace(servicelist=screen))
        controller = live.Controller.__new__(live.Controller)
        controller.icon_worker = object()
        with patch.dict(sys.modules, {'Screens': screens, 'Screens.InfoBar': infobar_module}):
            controller.icon_done({'changed': True})
            self.assertIsNone(controller.icon_worker)
            self.assertEqual(redraws, ['redraw'])
            controller.icon_done({'changed': False})
            self.assertEqual(redraws, ['redraw'])
            screen.shown = False
            controller.icon_done({'changed': True})
            self.assertEqual(redraws, ['redraw'])

    def test_picon_diagnostics_only_reports_native_toggle_and_owned_counts(self):
        own = self.root / 'hdg17_files' / 'picon'
        own.mkdir(parents=True)
        (own / 'one.png').write_bytes(b'owner-owned')
        (self.root / 'settings').write_text(
            'config.skin.primary_skin=hd_glass17/skin.xml\n'
            'config.plugins.setupGlass17.par125=0\n'
            'config.plugins.setupGlass17.par124=' + str(self.root) + '/\n'
            'config.usage.service_icon_enable=false\n'
            'config.channelSelection.showPicon=false\n'
            'config.some.token=SECRET_SHOULD_NOT_LEAK\n'
        )
        result = live._radio_picon_diagnostics(self.root)
        self.assertTrue(result['skin_active'])
        self.assertEqual(result['picon_folder_png_count'], 1)
        self.assertEqual(result['native_picon_enabled_legacy'], 'false')
        self.assertEqual(result['native_picon_enabled_new'], 'false')
        self.assertNotIn('SECRET_SHOULD_NOT_LEAK', str(result))

    def test_diagnostic_is_read_only_and_reports_registration(self):
        with patch.object(live, '_plugin', side_effect=ImportError('stub')):
            status = live.diagnose(self.root)
        self.assertFalse(status['bouquet_exists'])
        self.assertFalse(status['registered_in_bouquets_radio'])
        self.assertIsNone(status['last_attempt'])
        live.refresh(self.root, NOW, Browser())
        (self.root / live.DIAG_FILE).write_text(json.dumps(
            {'result': 'ready', 'changed': True, 'stations': 2}))
        with patch.object(live, '_plugin', side_effect=ImportError('stub')):
            status = live.diagnose(self.root)
        self.assertTrue(status['bouquet_exists'])
        self.assertTrue(status['registered_in_bouquets_radio'])
        self.assertEqual(status['last_status']['result'], 'ready')

    def test_silent_refresh_records_sanitized_error(self):
        with patch.object(live, 'DIRECTORY', self.root), patch.object(
                live, 'refresh', side_effect=OSError('Radio Browser unavailable')):
            with self.assertRaises(OSError):
                live.refresh_with_status()
        status = json.loads((self.root / live.DIAG_FILE).read_text())
        self.assertEqual(status['result'], 'failed')
        self.assertEqual(status['reason'], 'radio-browser-unavailable')
        self.assertNotIn('url', str(status).lower())

    def test_gui_reloads_bouquet_written_by_postinst_even_when_not_due(self):
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
        loop, reloads = Loop(), []
        with patch.object(live, 'DIRECTORY', self.root):
            controller = live.Controller(loop, lambda: reloads.append(True))
            try:
                live.refresh(self.root, NOW, Browser())  # postinst finished between GUI checks
                controller.finished({'changed': False, 'skipped': 'not-due'})
                self.assertEqual(reloads, [True])
                self.assertFalse(controller.initial_reload)
                controller.finished({'changed': False, 'skipped': 'not-due'})
                self.assertEqual(reloads, [True])
            finally:
                controller.close()

    def test_no_touched_radio_plugin_state(self):
        plugin = self.root / 'warder-radio'
        plugin.mkdir()
        state = plugin / 'state.json'
        state.write_text(json.dumps({'favourites': ['owner']}) + '\n')
        live.refresh(self.root, NOW, Browser())
        self.assertEqual(json.loads(state.read_text())['favourites'], ['owner'])


if __name__ == '__main__':
    unittest.main()
