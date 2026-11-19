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
        if self.with_pages and offset < 300:
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

    def _alt_file(self, filename, mapped_station):
        """Write an Enigma2-managed alternatives group referencing the same station."""
        (self.root / filename).write_bytes(
            b'#NAME Stored alternatives\\n'.replace(b'\\n', b'\n') +
            live._service(mapped_station).encode('utf-8'))

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
        self.assertEqual(browser.calls, [('GB', 0), ('GB', 60), ('GB', 120), ('GB', 180), ('GB', 240), ('GB', 300)])
        self.assertEqual(len(live._sections(self.bouquet.read_bytes())), 1)

    def test_enigma_alternative_edit_is_backed_up_and_czech_switch_recovers(self):
        """Mimic real receiver: 2 mapped stations, one normal, one 1:134:2."""
        country.bootstrap(self.root)
        country.refresh(self.root, now=NOW, browser=Browser())
        mapping = json.loads((self.root / live.DATA_FILE).read_text())['stations']
        self.assertEqual(len(mapping), 2)
        self._alt_file('alternatives.test_897.radio', mapping[0])
        previous = self.bouquet.read_bytes()
        original_service = live._service(mapping[0]).encode('utf-8')
        self.assertIn(original_service, previous)
        reference = (
            b'#SERVICE 1:134:2:0:0:0:0:0:0:0:FROM BOUQUET '
            b'"alternatives.test_897.radio" ORDER BY bouquet\n'
            + ('#DESCRIPTION ' + mapping[0]['name'] + '\n').encode('utf-8'))
        modified = previous.replace(original_service, reference, 1)
        self.assertNotEqual(previous, modified)
        self.bouquet.write_bytes(modified)
        state = json.loads(self.prefs.read_text())
        self.assertEqual(state['active'], 'SK')
        self.assertFalse(country._owner_valid(self.root, modified, state))
        diagnostic = country.diagnose(self.root)
        self.assertTrue(diagnostic['enigma_alternative_recovery_possible'])
        self.assertFalse((self.root / (live.FILE + '.enigma-alternatives.bak')).exists())
        country.request_country('CZ', self.root)
        result = country.refresh(self.root, now=NOW + country.RETRY, browser=Browser())
        self.assertTrue(result['changed'])
        self.assertEqual(result['country'], 'CZ')
        self.assertEqual(country.active_country(self.root), 'CZ')
        self.assertEqual(list(live._sections(self.bouquet.read_bytes())),
                         [country.country_name('CZ')])
        backup = self.root / (live.FILE + '.enigma-alternatives.bak')
        self.assertEqual(backup.read_bytes(), modified)
        self.assertTrue(country._choice(self.root)['recovered_alternative_edit'])
        self.assertEqual(len(json.loads((self.root / live.DATA_FILE).read_text())['stations']), 2)

    def test_crlf_enigma_alternative_is_verified_backed_up_then_switches_country(self):
        """Reproduce receiver: recognizable first line, strict raw header fails."""
        country.bootstrap(self.root)
        country.refresh(self.root, now=NOW, browser=Browser())
        rows = json.loads((self.root / live.DATA_FILE).read_text())['stations']
        original = self.bouquet.read_bytes()
        self.assertEqual(len(rows), 2)
        self._alt_file('alternatives.live_radio.radio', rows[0])
        edited = original.replace(
            live._service(rows[0]).encode('utf-8'),
            (b'#SERVICE 1:134:2:0:0:0:0:0:0:0:FROM BOUQUET '
             b'"alternatives.live_radio.radio" ORDER BY bouquet\n' +
             ('#DESCRIPTION ' + rows[0]['name'] + '\n').encode('utf-8')), 1
        ).replace(b'\n', b'\r\n')
        self.assertFalse(edited.startswith(live.HEADER))
        self.assertEqual(edited.splitlines()[0], b'#NAME Warder Radio Live')
        self.bouquet.write_bytes(edited)
        report = country.diagnose(self.root)
        self.assertEqual(report['bouquet_line_endings'], 'crlf')
        self.assertTrue(report['bouquet_format_normalizable'])
        self.assertEqual(report['visible_country_sections'], ['Slovensko'])
        self.assertFalse(report['bouquet_owned_checksum_valid'])
        self.assertTrue(report['enigma_alternative_recovery_possible'])
        country.request_country('CZ', self.root)
        switched = country.refresh(self.root, now=NOW + country.RETRY, browser=Browser())
        self.assertTrue(switched['changed'])
        self.assertEqual(switched['country'], 'CZ')
        self.assertEqual(country.active_country(self.root), 'CZ')
        self.assertEqual(
            (self.root / (live.FILE + '.enigma-alternatives.bak')).read_bytes(), edited)
        self.assertEqual(list(live._sections(self.bouquet.read_bytes())),
                         [country.country_name('CZ')])

    def test_receiver_scale_123_mapped_122_streams_one_alternative_crlf(self):
        """Actual Enigma2 flushChanges: 248 rows, no alt DESCRIPTION, 0 raw refs."""

        def e2_encoded(value):
            data = value.encode('utf-8')
            return b''.join(('%02x' % byte).encode('ascii').join((b'%', b''))
                            if byte in (37, 58) or byte < 32 else bytes([byte])
                            for byte in data)

        def e2_service(row):
            service = row['stem'].replace('_', ':').encode('ascii')
            return (
                b'#SERVICE ' + service + b':' + e2_encoded(row['url']) +
                b':' + e2_encoded(row['name']) + b'\r\n' +
                ('#DESCRIPTION ' + row['name'] + '\r\n').encode('utf-8'))

        class LargeCountryBrowser:
            def page(self, country='', offset=0):
                if country == 'SK':
                    prefix = '12345678-1234-1234-1234-'
                    rows = [
                        {'stationuuid': prefix + ('%012x' % i),
                         'name': 'Radio %03d' % i,
                         'url': 'https://radio.example.org/live/%d?key=abc%%25xyz' % i,
                         'favicon': ''}
                        for i in range(123)
                    ]
                else:
                    rows = [
                        {'stationuuid': '22345678-1234-1234-1234-123456789abc',
                         'name': 'České rádio',
                         'url': 'https://radio.example.org/czech',
                         'favicon': ''}
                    ]
                return SimpleNamespace(rows=rows, more=False, offline=False)

        browser = LargeCountryBrowser()
        country.bootstrap(self.root)
        previous = country.refresh(self.root, now=NOW, browser=browser)
        self.assertEqual(previous['stations'], 123)
        rows = json.loads((self.root / live.DATA_FILE).read_text())['stations']
        original = self.bouquet.read_bytes()
        self._alt_file('alternatives.radio_007.radio', rows[7])
        items = [live.HEADER.replace(b'\n', b'\r\n'),
                 b'#SERVICE 1:64:2:0:0:0:0:0:0:0:\r\n',
                 '#DESCRIPTION Slovensko\r\n'.encode('utf-8')]
        for index, row in enumerate(rows):
            if index == 7:
                items.append(b'#SERVICE 1:134:2:0:0:0:0:0:0:0:FROM BOUQUET '
                             b'"alternatives.radio_007.radio" ORDER BY bouquet\r\n')
            else:
                items.append(e2_service(row))
        modified = b''.join(items)
        self.assertEqual(len(modified.splitlines()), 248)
        self.assertEqual(sum(x.startswith(b'#DESCRIPTION ') for x in modified.splitlines()), 123)
        canonical = {live._service(row).encode('utf-8').splitlines()[0] for row in rows}
        self.assertFalse(canonical.intersection(modified.splitlines()))
        self.assertNotEqual(original, modified)
        self.bouquet.write_bytes(modified)
        report = country.diagnose(self.root)
        self.assertEqual(report['mapped_stations'], 123)
        self.assertEqual(report['bouquet_stream_entries'], 122)
        self.assertEqual(report['bouquet_group_markers'], 1)
        self.assertTrue(report['enigma_alternative_recovery_possible'])
        country.request_country('CZ', self.root)
        result = country.refresh(self.root, now=NOW + country.RETRY, browser=browser)
        self.assertTrue(result['changed'])
        self.assertEqual(country.active_country(self.root), 'CZ')
        self.assertEqual((self.root / (live.FILE + '.enigma-alternatives.bak')).read_bytes(),
                         modified)
        self.assertEqual(list(live._sections(self.bouquet.read_bytes())),
                         [country.country_name('CZ')])

    def test_alternative_group_without_matching_station_is_not_adopted(self):
        country.bootstrap(self.root)
        country.refresh(self.root, now=NOW, browser=Browser())
        rows = json.loads((self.root / live.DATA_FILE).read_text())['stations']
        original = self.bouquet.read_bytes()
        deleted = live._service(rows[0]).encode('utf-8')
        modified = original.replace(
            deleted,
            b'#SERVICE 1:134:2:0:0:0:0:0:0:0:FROM BOUQUET '
            b'"alternatives.other.radio" ORDER BY bouquet\n', 1)
        self.bouquet.write_bytes(modified)
        self._alt_file('alternatives.other.radio', rows[1])
        self.assertFalse(country.diagnose(self.root)['enigma_alternative_recovery_possible'])
        self.assertEqual(country.refresh(self.root, now=NOW, browser=Browser())['skipped'],
                         'owner-modified')
        self.assertEqual(self.bouquet.read_bytes(), modified)

    def test_only_crlf_or_bom_format_differences_keep_trusted_ownership(self):
        country.bootstrap(self.root)
        country.refresh(self.root, now=NOW, browser=Browser())
        published = self.bouquet.read_bytes()
        state = country._choice(self.root)
        for variant in (published.replace(b'\n', b'\r\n'),
                        b'\xef\xbb\xbf' + published,
                        published.replace(b'#NAME Warder Radio Live\n',
                                          b'#NAME Warder Radio Live   \r\n', 1)):
            with self.subTest(kind=variant[:42]):
                self.bouquet.write_bytes(variant)
                self.assertTrue(country._owner_valid(self.root, variant, state))
                self.assertTrue(country.diagnose(self.root)['bouquet_owned_checksum_valid'])
        self.bouquet.write_bytes(published)

    def test_enigma_header_formatting_does_not_authorize_modified_stream(self):
        country.bootstrap(self.root)
        country.refresh(self.root, now=NOW, browser=Browser())
        published = self.bouquet.read_bytes().replace(b'\n', b'\r\n')
        malicious = published.replace(b'radio.example.org', b'untrusted.example.org', 1)
        self.bouquet.write_bytes(malicious)
        self.assertFalse(country._owner_valid(
            self.root, malicious, country._choice(self.root)))
        self.assertFalse(country.diagnose(self.root)['enigma_alternative_recovery_possible'])
        country.request_country('CZ', self.root)
        result = country.refresh(self.root, now=NOW + country.RETRY, browser=Browser())
        self.assertEqual(result['skipped'], 'owner-modified')
        self.assertEqual(self.bouquet.read_bytes(), malicious)
        self.assertFalse(
            (self.root / (live.FILE + '.enigma-alternatives.bak')).exists())

    def test_explicit_czech_switch_replaces_native_edited_managed_bouquet_after_backup(self):
        """No saved ref URLs match, alt has no description or matching alt file.

        This matches the actual receiver report while ensuring the previous
        active-country catalogue is signed and all 122 normal numeric IDs match.
        """
        country.bootstrap(self.root)
        result = country.refresh(self.root, now=NOW, browser=Browser())
        self.assertEqual(result['stations'], 2)
        rows = json.loads((self.root / live.DATA_FILE).read_text())['stations']
        original = self.bouquet.read_bytes()
        live_header = live.HEADER.replace(b'\n', b'\r\n')
        active_marker = (
            b'#SERVICE 1:64:2:0:0:0:0:0:0:0:\r\n' +
            '#DESCRIPTION Slovensko\r\n'.encode('utf-8'))
        rewritten = (
            b'#SERVICE ' + rows[1]['stem'].replace('_', ':').encode('ascii') +
            b':https%3a//radio.example.org/other:' +
            rows[1]['name'].encode('utf-8') + b'\r\n' +
            ('#DESCRIPTION ' + rows[1]['name'] + '\r\n').encode('utf-8'))
        alternative = (
            b'#SERVICE 1:134:2:0:0:0:0:0:0:0:FROM BOUQUET '
            b'"alternatives.radio_001.radio" ORDER BY bouquet\r\n')
        edited = live_header + active_marker + alternative + rewritten
        self.assertEqual(edited.count(b'#SERVICE 4097:'), 1)
        self.bouquet.write_bytes(edited)
        state = country._choice(self.root)
        self.assertFalse(country._owner_valid(self.root, edited, state))
        self.assertFalse(country._recover_enigma_alternative(
            self.root, edited, state, inspect_only=True))
        self.assertFalse(country._pending_country_switch_backup_allowed(
            self.root, edited, state)) # no explicit pending country yet
        self.assertEqual(country.refresh(
            self.root, now=NOW + country.RETRY, browser=Browser())['skipped'],
            'owner-modified')
        self.assertEqual(self.bouquet.read_bytes(), edited)
        country.request_country('CZ', self.root)
        report = country.diagnose(self.root)
        self.assertTrue(report['pending_country_switch_safe'])
        self.assertFalse(report['enigma_alternative_recovery_possible'])
        self.assertFalse((self.root / (live.FILE + '.before-country-switch.bak')).exists())
        result = country.refresh(self.root, now=NOW + country.RETRY, browser=Browser())
        self.assertTrue(result['changed'])
        self.assertEqual(result['country'], 'CZ')
        self.assertEqual(country.active_country(self.root), 'CZ')
        backup = self.root / (live.FILE + '.before-country-switch.bak')
        self.assertEqual(backup.read_bytes(), edited)
        self.assertEqual(list(live._sections(self.bouquet.read_bytes())),
                         [country.country_name('CZ')])

    def test_pending_country_does_not_authorize_unknown_numeric_service_edit(self):
        country.bootstrap(self.root)
        country.refresh(self.root, now=NOW, browser=Browser())
        row = json.loads((self.root / live.DATA_FILE).read_text())['stations'][0]
        orig = self.bouquet.read_bytes()
        edit = orig.replace(row['stem'].replace('_', ':').encode('ascii'),
                            b'4097:0:2:FFFF:FFFF:FFFF:FFFFFFFF:0:0:0', 1)
        self.bouquet.write_bytes(edit)
        country.request_country('CZ', self.root)
        self.assertFalse(country.diagnose(self.root)['pending_country_switch_safe'])
        self.assertEqual(country.refresh(
            self.root, now=NOW + country.RETRY, browser=Browser())['skipped'],
            'owner-modified')
        self.assertEqual(self.bouquet.read_bytes(), edit)
        self.assertFalse((self.root / (live.FILE + '.before-country-switch.bak')).exists())

    def test_explicit_pending_switch_rejects_tampered_catalogue_and_backup_collision(self):
        country.bootstrap(self.root)
        country.refresh(self.root, now=NOW, browser=Browser())
        rows = json.loads((self.root / live.DATA_FILE).read_text())['stations']
        previous = self.bouquet.read_bytes()
        # Reordering the two known stations creates a checksum mismatch but
        # does not introduce an unknown identity or change any station.
        pairs = [live._service(row).encode('utf-8') for row in rows]
        edited = previous.replace(pairs[0] + pairs[1], pairs[1] + pairs[0])
        self.assertNotEqual(edited, previous)
        self.bouquet.write_bytes(edited)
        country.request_country('CZ', self.root)
        self.assertTrue(country.diagnose(self.root)['pending_country_switch_safe'])
        backup = self.root / (live.FILE + '.before-country-switch.bak')
        backup.write_bytes(b'user backup must not be overwritten')
        self.assertFalse(country.diagnose(self.root)['pending_country_switch_safe'])
        self.assertEqual(country.refresh(
            self.root, now=NOW + country.RETRY, browser=Browser())['skipped'],
            'owner-modified')
        self.assertEqual(backup.read_bytes(), b'user backup must not be overwritten')
        backup.unlink()
        mapping = json.loads((self.root / live.DATA_FILE).read_text())
        mapping['stations'][0]['name'] = 'unauthorized new title'
        (self.root / live.DATA_FILE).write_text(json.dumps(mapping))
        self.assertFalse(country.diagnose(self.root)['pending_country_switch_safe'])
        self.assertEqual(self.bouquet.read_bytes(), edited)

    def test_unknown_user_edits_are_not_adopted_even_if_alternative_present(self):
        country.bootstrap(self.root)
        country.refresh(self.root, now=NOW, browser=Browser())
        mapping = json.loads((self.root / live.DATA_FILE).read_text())['stations']
        previous = self.bouquet.read_bytes()
        self._alt_file('alternatives.test.radio', mapping[0])
        alt = (b'#SERVICE 1:134:2:0:0:0:0:0:0:0:FROM BOUQUET '
               b'"alternatives.test.radio" ORDER BY bouquet\n'
               + ('#DESCRIPTION ' + mapping[0]['name'] + '\n').encode('utf-8'))
        first = live._service(mapping[0]).encode('utf-8')
        self.assertIn(first, previous)
        self.bouquet.write_bytes(previous.replace(first, alt, 1))
        altered = self.bouquet.read_bytes()
        variants = [
            altered.replace(b'alternatives.test.radio', b'other.userbouquet.radio'),
            altered.replace(('#DESCRIPTION ' + mapping[0]['name']).encode('utf-8'),
                            b'#DESCRIPTION unrelated owner edit'),
            altered.replace(('https%3A//radio.example.org/live').encode('utf-8'),
                            b'https%3A//changed.example.org/stream'),
        ]
        for original in variants:
            with self.subTest(kind=original[-90:]):
                self.bouquet.write_bytes(original)
                self.assertFalse(country._recover_enigma_alternative(
                    self.root, original, country._choice(self.root)))
                self.assertEqual(self.bouquet.read_bytes(), original)
                self.assertFalse((self.root / (live.FILE + '.enigma-alternatives.bak')).exists())

    def test_do_not_overwrite_previous_alternative_recovery_backup(self):
        country.bootstrap(self.root)
        country.refresh(self.root, now=NOW, browser=Browser())
        mapping = json.loads((self.root / live.DATA_FILE).read_text())['stations']
        original = self.bouquet.read_bytes()
        self._alt_file('alternatives.protected.radio', mapping[0])
        modified = original.replace(
            live._service(mapping[0]).encode('utf-8'),
            b'#SERVICE 1:134:2:0:0:0:0:0:0:0:FROM BOUQUET '
            b'"alternatives.protected.radio" ORDER BY bouquet\n' +
            ('#DESCRIPTION ' + mapping[0]['name'] + '\n').encode('utf-8'), 1)
        self.bouquet.write_bytes(modified)
        backup = self.root / (live.FILE + '.enigma-alternatives.bak')
        backup.write_bytes(b'original user backup')
        country.request_country('CZ', self.root)
        result = country.refresh(self.root, now=NOW + country.RETRY, browser=Browser())
        self.assertEqual(result['skipped'], 'owner-modified')
        self.assertEqual(self.bouquet.read_bytes(), modified)
        self.assertEqual(backup.read_bytes(), b'original user backup')

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
            self.assertEqual(len(ui._RADIO_COUNTRY_START_ERROR_TRANSLATIONS), 21)
            osd_language.value = 'sk_SK'
            self.assertEqual(
                ui.ui_text('Country saved, but background radio update did not start.'),
                'Krajina bola uložená, ale aktualizácia rádia sa nespustila.')
        plugin_source = (RUNTIME / 'Plugins/Extensions/setupGlass17/plugin.py').read_text()
        picker_source = (RUNTIME / 'Plugins/Extensions/setupGlass17/warderRadioCountry.py').read_text()
        self.assertIn('name=ui_text("Select country (Warder Radio Live)")', plugin_source)
        self.assertIn('title=ui_text("Select country (Warder Radio Live)")', picker_source)
        self.assertIn("ui_text('(current)')", picker_source)
        self.assertNotIn('name="Vybrať krajinu (Warder Radio Live)"', plugin_source)

    def test_diagnostic_shows_czech_pending_and_progress_without_stream_urls(self):
        country.bootstrap(self.root)
        country.request_country('CZ', self.root)
        first = country.diagnose(self.root)
        self.assertEqual(first['active'], 'SK')
        self.assertEqual(first['pending'], 'CZ')
        self.assertEqual(first['last_error'], None)
        self.assertEqual(first['visible_country_sections'], ['Slovensko'])
        self.assertNotIn('https:', str(first))
        country.refresh(self.root, now=NOW, browser=Browser(offline=True))
        offline = country.diagnose(self.root)
        self.assertEqual(offline['active'], 'SK')
        self.assertEqual(offline['pending'], 'CZ')
        self.assertEqual(offline['last_error'], 'radio-browser-unavailable')
        country.refresh(self.root, now=NOW + country.RETRY, browser=Browser())
        ready = country.diagnose(self.root)
        self.assertEqual(ready['active'], 'CZ')
        self.assertIsNone(ready['pending'])
        self.assertIsNone(ready['last_error'])
        self.assertEqual(ready['visible_country_sections'], [country.country_name('CZ')])
        self.assertEqual(ready['mapped_stations'], 2)

    def test_paged_czech_download_reports_progress_then_switches(self):
        country.bootstrap(self.root)
        country.request_country('CZ', self.root)
        browser = Browser(with_pages=True)
        pending = country.refresh(self.root, now=NOW, browser=browser)
        self.assertTrue(pending['incomplete'])
        info = country.diagnose(self.root)
        self.assertEqual(info['active'], 'SK')
        self.assertEqual(info['pending'], 'CZ')
        self.assertEqual(info['pending_pages'], country.MAX_PAGES_PER_JOB)
        self.assertEqual(info['downloaded'], 2)
        result = country.refresh(self.root, now=NOW + country.STEP, browser=browser)
        self.assertTrue(result['changed'])
        info = country.diagnose(self.root)
        self.assertEqual(info['active'], 'CZ')
        self.assertIsNone(info['pending'])

    def test_selection_starts_missing_gui_controller_instead_of_silent_queue(self):
        session = SimpleNamespace()
        started = []
        class Controller:
            closed = False
            def request_refresh(self):
                started.append('scheduled')
        def start(reason, session=None):
            self.assertEqual(reason, 0)
            started.append(session)
            live._controller = Controller()
        with patch.object(live, '_controller', None), patch.object(live, 'start', start):
            self.assertTrue(country._start_selected_country_refresh(session))
        self.assertEqual(started, [session, 'scheduled'])

    def test_missing_gui_controller_reports_failed_update_start(self):
        with patch.object(live, '_controller', None), patch.object(live, 'start', lambda *args, **kwargs: None):
            self.assertFalse(country._start_selected_country_refresh(SimpleNamespace()))

    def test_diagnostic_detects_unowned_country_file_without_stream_urls(self):
        country.bootstrap(self.root)
        good = country.diagnose(self.root)
        self.assertTrue(good['bouquet_owned_checksum_valid'])
        self.assertTrue(good['bouquet_header_valid'])
        self.assertEqual(good['bouquet_group_markers'], 1)
        content = live.HEADER + b'#COMMENT user modified group headers\n'
        self.bouquet.write_bytes(content)
        bad = country.diagnose(self.root)
        self.assertTrue(bad['bouquet_exists'])
        self.assertEqual(bad['bouquet_group_markers'], 0)
        self.assertFalse(bad['bouquet_owned_checksum_valid'])
        self.assertFalse(bad['enigma_alternative_recovery_possible'])
        self.assertEqual(bad['visible_country_sections'], [])
        self.assertEqual(country.refresh(self.root, now=NOW, browser=Browser())['skipped'], 'owner-modified')
        self.assertIsNone(country.diagnose(self.root)['last_attempt'])  # no worker attempt reached
        self.assertNotIn('http', str(bad))

    def test_country_picker_list_available_offline(self):
        choices = country.country_options()
        self.assertTrue(len(choices) >= 4)
        self.assertIn('SK', [code for label, code in choices])
        self.assertIn('CZ', [code for label, code in choices])
        self.assertIn('DE', [code for label, code in choices])

    def test_country_switch_refreshes_visible_native_radio_list(self):
        """GUI must not keep showing Slovensko after Czech data was published."""
        country.bootstrap(self.root)
        country.request_country('CZ', self.root)
        result = country.refresh(self.root, now=NOW, browser=Browser())
        self.assertTrue(result['changed'])
        self.assertEqual(result['country'], 'CZ')

        class FakeCall:
            def __init__(self, callback=None):
                self.callback, self.cancelled = callback, False
            def active(self):
                return not self.cancelled
            def cancel(self):
                self.cancelled = True

        class FakeLoop:
            def __init__(self):
                self.calls = []
            def callLater(self, delay, callback):
                self.calls.append((delay, callback))
                return FakeCall(callback)

        view = []
        class ChannelSelectionRadio:
            shown = True
            def __init__(self):
                self.servicelist = SimpleNamespace(
                    instance=object(),
                    resetRoot=lambda: view.append('reset'),
                    goTop=lambda: view.append('top'))
            def getRoot(self):
                return SimpleNamespace(
                    getPath=lambda: 'FROM BOUQUET "' + live.FILE + '" ORDER BY bouquet')

        radio = ChannelSelectionRadio()
        session = SimpleNamespace(current_dialog=radio)
        controller = live.Controller.__new__(live.Controller)
        loop = FakeLoop()
        controller.loop = loop
        controller.session = session
        controller.reload = lambda: view.append('reload')
        controller.worker = object()
        controller.pending = FakeCall()
        controller.timeout = None
        controller.radio_refresh_timer = None
        controller.closed = False
        controller.initial_reload = False
        with patch.object(live, 'DIRECTORY', self.root):
            controller.finished(result)
        self.assertEqual(view[:3], ['reload', 'reset', 'top'])
        self.assertTrue(any(delay == 5 for delay, _ in loop.calls))
        self.assertTrue(any(delay == 3600 for delay, _ in loop.calls))

    def test_pending_country_is_retried_not_silently_delayed_for_an_hour(self):
        country.bootstrap(self.root)
        country.request_country('CZ', self.root)
        class Call:
            def active(self): return True
            def cancel(self): pass
        class Loop:
            def __init__(self): self.calls = []
            def callLater(self, seconds, callback):
                self.calls.append(seconds)
                return Call()
        loop = Loop()
        controller = live.Controller.__new__(live.Controller)
        controller.loop = loop
        controller.session = None
        controller.reload = lambda: None
        controller.worker = None
        controller.pending = None
        controller.timeout = None
        controller.radio_refresh_timer = None
        controller.closed = False
        controller.initial_reload = False
        with patch.object(live, 'DIRECTORY', self.root):
            controller.finished({'changed': False, 'skipped': 'radio-browser-unavailable'})
            self.assertIn(60, loop.calls)
            controller.finished({'changed': False, 'incomplete': True, 'country': 'CZ'})
            self.assertIn(3, loop.calls)
        self.assertNotIn(3600, loop.calls)

    def test_radio_list_redraw_resumes_after_country_confirmation_dialog(self):
        class FakeCall:
            def active(self): return True
            def cancel(self): pass
        class Loop:
            def __init__(self): self.calls = []
            def callLater(self, seconds, callback):
                self.calls.append((seconds, callback))
                return FakeCall()
        class ChannelSelectionRadio:
            shown = True
            def __init__(self):
                self.count = 0
                self.servicelist = SimpleNamespace(
                    instance=object(), resetRoot=self.count_up, goTop=lambda: None)
            def count_up(self): self.count += 1
            def getRoot(self):
                return SimpleNamespace(getPath=lambda: 'FROM BOUQUET "' + live.FILE + '"')
        radio = ChannelSelectionRadio()
        session = SimpleNamespace(current_dialog=SimpleNamespace(shown=True))
        ctrl = live.Controller.__new__(live.Controller)
        ctrl.session = session
        ctrl.loop = Loop()
        ctrl.closed = False
        ctrl.radio_refresh_timer = None
        self.assertFalse(ctrl._refresh_visible_radio_list())
        self.assertEqual(radio.count, 0)
        session.current_dialog = radio
        self.assertTrue(ctrl._refresh_visible_radio_list())
        self.assertEqual(radio.count, 1)

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
