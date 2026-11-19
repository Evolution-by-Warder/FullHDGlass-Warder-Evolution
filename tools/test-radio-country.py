#!/usr/bin/env python3
"""Offline tests for one-country Warder Radio Live and persistent country choice."""
import hashlib
import importlib
import json
from pathlib import Path
import sys
import tempfile
from types import ModuleType, SimpleNamespace
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
RUNTIME = ROOT / 'source/package-root/usr/lib/enigma2/python'
sys.path.insert(0, str(RUNTIME))
from Plugins.Extensions.setupGlass17 import warderRadioLive as live
from Plugins.Extensions.setupGlass17 import warderRadioCountry as country

NOW = 1800000000
UUIDS = {
    'SK': '12345678-1234-1234-1234-123456789abc',
    'CZ': '22345678-1234-1234-1234-123456789abc',
    'DE': '32345678-1234-1234-1234-123456789abc',
    'GB': '42345678-1234-1234-1234-123456789abc',
}


class Browser:
    def __init__(self, offline=False, with_pages=False):
        self.calls = []
        self.offline = offline
        self.with_pages = with_pages

    def page(self, country='', offset=0):
        self.calls.append((country, offset))
        if self.with_pages and offset < 180:
            more = True
        else:
            more = False
        uuid = UUIDS.get(country, UUIDS['SK'])
        rows = [
            {'stationuuid': uuid, 'name': 'Živé Rádio',
             'url': 'https://radio.example.org/live',
             'favicon': 'https://radio.example.org/logo.png'},
            {'stationuuid': '52345678-1234-1234-1234-123456789abc',
             'name': 'Áčko',
             'url': 'https://radio.example.org/other',
             'favicon': 'https://radio.example.org/logo2.png'},
        ]
        return SimpleNamespace(rows=rows, more=more, offline=self.offline)


def group(name, items):
    lines = [
        '#SERVICE 1:64:2:0:0:0:0:0:0:0:\n',
        '#DESCRIPTION ' + name + '\n'
    ]
    for i, label in enumerate(items, 1):
        lines += [
            '#SERVICE 4097:0:2:%X:1:AB:1:0:0:0:https%%3A//example.org/%s/%d\n' % (i, name, i),
            '#DESCRIPTION ' + label + '\n'
        ]
    return ''.join(lines).encode()


class CountryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.bouquet = self.root / live.FILE
        self.prefs = self.root / country.CHOICE_FILE
        self.index = self.root / 'bouquets.radio'
        self.index.write_bytes(
            b'#NAME Bouquets (Radio)\n'
            b'#SERVICE 1:7:2:0:0:0:0:0:0:0:FROM BOUQUET "userbouquet.personal.radio" ORDER BY bouquet\n'
            b'#SERVICE 1:7:2:0:0:0:0:0:0:0:FROM BOUQUET "userbouquet.warder.radio" ORDER BY bouquet\n'
        )
        self.legacy = self.root / live.LEGACY_FILE
        self.legacy.write_bytes(live.LEGACY_HEADER +
                                group('Slovensko', ('Zeta SK', 'Áčko SK')) +
                                group('Čechy', ('Bravo CZ',)) +
                                group('Deutschland', ('Zeta DE', 'Alfa DE')) +
                                group('United Kingdom', ('UK One',)))
        (self.root / 'settings').write_text('config.osd.language=sk_SK\n')

    def test_first_launch_country_matches_enigma_language(self):
        cases = {'sk_SK': 'SK', 'cs_CZ': 'CZ', 'de_DE': 'DE',
                 'en_US': 'GB', 'fr_FR': 'FR', 'it_IT': 'IT',
                 'pl_PL': 'PL', 'hu_HU': 'HU', 'ru_RU': 'RU',
                 'pt_PT': 'PT', 'zh_CN': 'CN', 'sq_AL': 'AL',
                 'fa_IR': 'IR', 'unknown': 'SK'}
        for locale, result in cases.items():
            (self.root / 'settings').write_text('config.osd.language=' + locale + '\n')
            with self.subTest(locale=locale):
                self.assertEqual(country.initial_country(self.root / 'settings'), result)

    def test_first_bootstrap_only_selected_country_and_personal_bouquet_untouched(self):
        (self.root / 'settings').write_text('config.osd.language=de_DE\n')
        result = country.bootstrap(self.root)
        self.assertTrue(result['changed'])
        self.assertEqual(result['country'], 'DE')
        sections = live._sections(self.bouquet.read_bytes())
        self.assertEqual(list(sections), ['Deutschland'])
        self.assertIn(b'#DESCRIPTION Alfa DE', sections['Deutschland'])
        self.assertNotIn(b'#DESCRIPTION Zeta SK', self.bouquet.read_bytes())
        self.assertEqual(self.index.read_bytes().count(live.INDEX_LINE), 1)
        self.assertIn(b'userbouquet.personal.radio', self.index.read_bytes())
        self.assertNotIn(b'FROM BOUQUET "userbouquet.warder.radio"', self.index.read_bytes())
        self.assertEqual(country.active_country(self.root), 'DE')

    def test_persisted_choice_overrides_changed_system_language_after_reboot(self):
        country.bootstrap(self.root)
        self.assertEqual(country.active_country(self.root), 'SK')
        (self.root / 'settings').write_text('config.osd.language=de_DE\n')
        country.bootstrap(self.root)
        self.assertEqual(country.active_country(self.root), 'SK')
        self.assertEqual(list(live._sections(self.bouquet.read_bytes())), ['Slovensko'])

    def test_requested_country_changes_only_after_successful_download(self):
        country.bootstrap(self.root)
        first = self.bouquet.read_bytes()
        result = country.request_country('CZ', self.root)
        self.assertTrue(result['accepted'])
        self.assertEqual(self.bouquet.read_bytes(), first)
        self.assertEqual(country.active_country(self.root), 'SK')
        result = country.refresh(self.root, now=NOW, browser=Browser(offline=True))
        self.assertEqual(result['skipped'], 'radio-browser-unavailable')
        self.assertEqual(self.bouquet.read_bytes(), first)
        self.assertEqual(country.active_country(self.root), 'SK')
        data = country._choice(self.root)
        self.assertEqual(data['pending'], 'CZ')
        result = country.refresh(self.root, now=NOW + country.RETRY, browser=Browser())
        self.assertTrue(result['changed'])
        self.assertEqual(result['country'], 'CZ')
        self.assertEqual(country.active_country(self.root), 'CZ')
        self.assertEqual(list(live._sections(self.bouquet.read_bytes())), [country.country_name('CZ')])
        self.assertFalse(country._choice(self.root).get('pending'))

    def test_reboot_uses_last_selected_country_even_if_osd_is_different(self):
        country.bootstrap(self.root)
        country.request_country('GB', self.root)
        country.refresh(self.root, now=NOW, browser=Browser())
        (self.root / 'settings').write_text('config.osd.language=fr_FR\n')
        country.bootstrap(self.root)
        self.assertEqual(country.active_country(self.root), 'GB')
        self.assertEqual(len(live._sections(self.bouquet.read_bytes())), 1)

    def test_new_bouquet_contains_station_names_in_alphabetic_order(self):
        country.bootstrap(self.root)
        country.refresh(self.root, now=NOW, browser=Browser())
        sections = live._sections(self.bouquet.read_bytes())
        self.assertEqual(len(sections), 1)
        values = next(iter(sections.values())).decode('utf-8')
        self.assertLess(values.find('#DESCRIPTION Áčko'), values.find('#DESCRIPTION Živé Rádio'))
        self.assertEqual(values.count('#SERVICE 4097:'), 2)
        rows = json.loads((self.root / live.DATA_FILE).read_text())['stations']
        self.assertEqual({x['countrycode'] for x in rows}, {'SK'})

    def test_only_one_country_queried_and_caches_only_that_country(self):
        country.bootstrap(self.root)
        request = country.request_country('DE', self.root)
        self.assertTrue(request['accepted'])
        browser = Browser()
        result = country.refresh(self.root, now=NOW, browser=browser)
        self.assertEqual(browser.calls, [('DE', 0)])
        self.assertEqual(result['stations'], 2)
        data = json.loads((self.root / live.DATA_FILE).read_text())
        self.assertTrue(all(row['countrycode'] == 'DE' for row in data['stations']))

    def test_incomplete_pages_resume_without_switching_or_losing_station(self):
        country.bootstrap(self.root)
        country.request_country('GB', self.root)
        before = self.bouquet.read_bytes()
        browser = Browser(with_pages=True)
        first = country.refresh(self.root, now=NOW, browser=browser)
        self.assertTrue(first['incomplete'])
        self.assertEqual(country.active_country(self.root), 'SK')
        self.assertEqual(self.bouquet.read_bytes(), before)
        second = country.refresh(self.root, now=NOW + country.STEP, browser=browser)
        self.assertTrue(second['changed'])
        self.assertEqual(country.active_country(self.root), 'GB')
        self.assertEqual(browser.calls, [('GB', 0), ('GB', 60), ('GB', 120), ('GB', 180)])
        self.assertEqual(len(live._sections(self.bouquet.read_bytes())), 1)

    def test_invalid_request_and_user_modifications_never_replaced(self):
        self.assertFalse(country.request_country('../IT', self.root)['accepted'])
        country.bootstrap(self.root)
        self.bouquet.write_text('#NAME Warder Radio Live\n#COMMENT custom edit\n')
        result = country.bootstrap(self.root)
        self.assertEqual(result['skipped'], 'owner-modified')
        result = country.refresh(self.root, now=NOW, browser=Browser())
        self.assertEqual(result['skipped'], 'owner-modified')
        self.assertIn('custom edit', self.bouquet.read_text())

    def test_existing_custom_country_survives_browse_failure_and_other_bouquets(self):
        country.bootstrap(self.root)
        country.request_country('DE', self.root)
        country.refresh(self.root, now=NOW, browser=Browser())
        expected = self.bouquet.read_bytes()
        other = self.index.read_bytes()
        country.request_country('CZ', self.root)
        country.refresh(self.root, now=NOW + 1, browser=Browser(offline=True))
        self.assertEqual(self.bouquet.read_bytes(), expected)
        self.assertEqual(country.active_country(self.root), 'DE')
        self.assertEqual(self.index.read_bytes(), other)

    def test_context_action_only_for_managed_live_services(self):
        country.bootstrap(self.root)
        first = next(line for line in self.bouquet.read_text().splitlines()
                     if line.startswith('#SERVICE 4097:'))
        ref = first[9:]
        with patch.object(country, 'DIRECTORY', self.root):
            self.assertTrue(country.is_live_service(SimpleNamespace(toString=lambda: ref)))
            self.assertFalse(country.is_live_service(SimpleNamespace(
                toString=lambda: '4097:0:2:999:1:AB:1:0:0:0:https%3A//unrelated')))
        script = (RUNTIME / 'Plugins/Extensions/setupGlass17/plugin.py').read_text()
        self.assertIn('WHERE_CHANNEL_CONTEXT_MENU', script)
        self.assertIn('serviceFilter=warderRadioCountry.is_live_service', script)

    def test_country_menu_on_selected_live_bouquet_folder_only(self):
        """The bouquet-root MENU retains native actions and adds our picker."""
        channel_mod = ModuleType('Screens.ChannelSelection')
        screens_mod = ModuleType('Screens')
        screens_mod.__path__ = []
        choices_mod = ModuleType('Components.ChoiceList')
        components_mod = ModuleType('Components')
        components_mod.__path__ = []
        ui_mod = ModuleType('Plugins.Extensions.setupGlass17.warderUiText')
        ui_mod.ui_text = lambda text: 'Choose country (Warder Radio Live)'
        choices_mod.ChoiceEntryComponent = lambda key=None, text=None: [text]

        class Widget:
            def __init__(self):
                self.items = [[('Settings', lambda: None)],
                              [('Add Bouquet', lambda: None)],
                              [('Rename Entry', lambda: None)]]
            def getList(self):
                return self.items
            def setList(self, entries):
                self.items = entries

        class FakeMenu:
            def __init__(self, session, csel):
                self.widget = Widget()
                self.closed = False
            def __getitem__(self, name):
                return self.widget
            def close(self, *args):
                self.closed = True

        def csel(bouquet, root='bouquets.radio'):
            ref = lambda name: SimpleNamespace(
                getPath=lambda: 'FROM BOUQUET "' + name + '" ORDER BY bouquet')
            return SimpleNamespace(getRoot=lambda: ref(root),
                                   getCurrentSelection=lambda: ref(bouquet))

        channel_mod.ChannelContextMenu = FakeMenu
        installed = [
            ('Screens', screens_mod), ('Screens.ChannelSelection', channel_mod),
            ('Components', components_mod), ('Components.ChoiceList', choices_mod),
            ('Plugins.Extensions.setupGlass17.warderUiText', ui_mod),
        ]
        with patch.dict(sys.modules, dict(installed)):
            self.assertTrue(country.install_root_country_menu())
            self.assertFalse(country.install_root_country_menu())
            session = SimpleNamespace()
            selected = csel(live.FILE)
            self.assertTrue(country._is_live_bouquet_selected(selected))
            actions = []
            with patch.object(country, 'open_country_selector', lambda x: actions.append(x)):
                screen = FakeMenu(session, selected)
                rows = screen['menu'].getList()
                self.assertEqual([x[0][0] for x in rows],
                                 ['Settings', 'Choose country (Warder Radio Live)',
                                  'Add Bouquet', 'Rename Entry'])
                rows[1][0][1]()
                self.assertEqual(actions, [session])
                self.assertTrue(screen.closed)
            other = FakeMenu(session, csel('userbouquet.another.radio'))
            self.assertEqual(len(other['menu'].getList()), 3)
            tv = FakeMenu(session, csel(live.FILE, root='bouquets.tv'))
            self.assertEqual(len(tv['menu'].getList()), 3)

    def test_bouquet_root_menu_hook_source_is_scoped_to_fullhdglass(self):
        plugin_source = (RUNTIME / 'Plugins/Extensions/setupGlass17/plugin.py').read_text()
        self.assertIn('install_root_country_menu()', plugin_source)
        self.assertIn('if reason == 0 and config.skin.primary_skin.value', plugin_source)

    def test_system_language_translates_native_menu_and_country_picker(self):
        """The receiver language drives the native MENU text, not Slovak literals."""
        import importlib.util
        components = ModuleType('Components')
        components.__path__ = []
        config_module = ModuleType('Components.config')
        osd_language = SimpleNamespace(value='en_GB')
        config_module.config = SimpleNamespace(osd=SimpleNamespace(language=osd_language))
        locale_module = ModuleType('Plugins.Extensions.setupGlass17.warderLocale')
        locale_module.language_code = lambda value: value.replace('-', '_').split('_', 1)[0].lower()
        locale_module.get_translator = lambda *args, **kwargs: (lambda value: value)
        module_name = 'Plugins.Extensions.setupGlass17.warderUiText'
        source = RUNTIME / 'Plugins/Extensions/setupGlass17/warderUiText.py'
        spec = importlib.util.spec_from_file_location(module_name, source)
        ui = importlib.util.module_from_spec(spec)
        with patch.dict(sys.modules, {
                'Components': components, 'Components.config': config_module,
                'Plugins.Extensions.setupGlass17.warderLocale': locale_module,
                module_name: ui}):
            spec.loader.exec_module(ui)
            self.assertEqual(ui.ui_text('Select country (Warder Radio Live)'),
                             'Select country (Warder Radio Live)')
            osd_language.value = 'sk_SK'
            self.assertEqual(ui.ui_text('Select country (Warder Radio Live)'),
                             'Vybrať krajinu (Warder Radio Live)')
            osd_language.value = 'cs_CZ'
            self.assertEqual(ui.ui_text('Select country (Warder Radio Live)'),
                             'Vybrat zemi (Warder Radio Live)')
            osd_language.value = 'de_DE'
            self.assertEqual(ui.ui_text('Select country (Warder Radio Live)'),
                             'Land auswählen (Warder Radio Live)')
            for lang, translations in ui._RADIO_COUNTRY_TRANSLATIONS.items():
                with self.subTest(lang=lang):
                    self.assertEqual(len(translations), len(ui._RADIO_COUNTRY_KEYS))
                    osd_language.value = lang + '_XX'
                    for key in ui._RADIO_COUNTRY_KEYS:
                        self.assertTrue(ui.ui_text(key))
                    self.assertIn('Warder Radio Live',
                                  ui.ui_text('Select country (Warder Radio Live)'))
            self.assertEqual(len(ui._RADIO_COUNTRY_TRANSLATIONS), 21)
        plugin_source = (RUNTIME / 'Plugins/Extensions/setupGlass17/plugin.py').read_text()
        picker_source = (RUNTIME / 'Plugins/Extensions/setupGlass17/warderRadioCountry.py').read_text()
        self.assertIn('name=ui_text("Select country (Warder Radio Live)")', plugin_source)
        self.assertIn('title=ui_text("Select country (Warder Radio Live)")', picker_source)
        self.assertIn("ui_text('(current)')", picker_source)
        self.assertNotIn('name="Vybrať krajinu (Warder Radio Live)"', plugin_source)

    def test_country_picker_list_available_offline(self):
        choices = country.country_options()
        self.assertTrue(len(choices) >= 4)
        self.assertIn('SK', [code for label, code in choices])
        self.assertIn('CZ', [code for label, code in choices])
        self.assertIn('DE', [code for label, code in choices])

    def test_first_success_retires_only_owned_legacy_radio_file(self):
        country.bootstrap(self.root)
        self.assertTrue(self.legacy.exists())
        original = self.legacy.read_bytes()
        country.refresh(self.root, now=NOW, browser=Browser())
        self.assertFalse(self.legacy.exists())
        self.assertNotIn(live.LEGACY_FILE.encode(), self.index.read_bytes())
        self.assertIn(b'userbouquet.personal.radio', self.index.read_bytes())
        self.assertNotIn(b'Zeta SK', self.bouquet.read_bytes()) # new online catalogue replaced legacy
        self.assertIn('Áčko'.encode('utf-8'), self.bouquet.read_bytes())

    def test_no_successful_network_preserves_legacy_fallback(self):
        country.bootstrap(self.root)
        country.refresh(self.root, now=NOW, browser=Browser(offline=True))
        self.assertTrue(self.legacy.exists())
        self.assertIn(b'Zeta SK', self.bouquet.read_bytes())


if __name__ == '__main__':
    unittest.main()
