"""Regression checks for FullHDGlass GNU gettext catalogues (Python 3.11)."""
import ast
import gettext
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / (
    'source/package-root/usr/lib/enigma2/python/Plugins/Extensions/setupGlass17/locale'
)
LANGS = ('al', 'cs', 'de', 'el', 'es', 'et', 'fa', 'fr', 'hu', 'it',
         'lt', 'nl', 'pl', 'pt', 'ro', 'ru', 'sk', 'tr', 'uk', 'zh')
DOMAINS = ('setupGlass17', 'helpTxt', 'weather', 'netatmo', 'eWeather')
FORMAT = re.compile(r'%(?!%)(?:\([\w]+\))?[-+#0 ]*(?:\d+|\*)?(?:\.(?:\d+|\*))?[diouxXeEfFgGcrs]')


def po_entries(path):
    """Read simple gettext catalogues, including multiline quoted strings."""
    entries = {}
    key = None
    value = ''
    active = None
    for line in path.read_text(encoding='utf-8').splitlines():
        if line.startswith('msgid '):
            if key is not None:
                if key in entries:
                    raise AssertionError('Duplicate msgid in %s: %r' % (path, key))
                entries[key] = value
            key = ast.literal_eval(line[6:])
            value = ''
            active = 'id'
        elif line.startswith('msgstr '):
            if key is None:
                raise AssertionError('msgstr without msgid: %s' % path)
            value = ast.literal_eval(line[7:])
            active = 'str'
        elif line.startswith('"') and active:
            part = ast.literal_eval(line)
            if active == 'id':
                key += part
            else:
                value += part
        elif line.startswith(('msgid_plural ', 'msgstr[', 'msgctxt ')):
            raise AssertionError('Unexpected plural or context in %s' % path)
        elif not line.strip():
            active = None
    if key is not None:
        if key in entries:
            raise AssertionError('Duplicate msgid in %s: %r' % (path, key))
        entries[key] = value
    return entries


class CatalogIntegrity(unittest.TestCase):
    def test_locale_count_and_complete_main_keys(self):
        self.assertEqual(len(LANGS) + 1, 21)  # en: untranslated msgid source.
        reference = po_entries(ROOT / 'sk' / 'LC_MESSAGES' / 'setupGlass17.po')
        expected = set(reference) - {''}
        self.assertEqual(len(expected), 517)
        for lang in LANGS:
            with self.subTest(lang=lang):
                path = ROOT / lang / 'LC_MESSAGES' / 'setupGlass17.po'
                self.assertTrue(path.is_file(), str(path))
                catalog = po_entries(path)
                actual = set(catalog) - {''}
                self.assertEqual(expected, actual)
                self.assertEqual([], [key for key in expected if not catalog[key]])

    def test_all_shipped_mo_files_load_and_match_po(self):
        for lang in LANGS:
            for domain in DOMAINS:
                path = ROOT / lang / 'LC_MESSAGES' / (domain + '.po')
                if not path.is_file():
                    continue  # Missing auxiliary catalogs are tracked in the audit.
                with self.subTest(lang=lang, domain=domain):
                    binary = path.with_suffix('.mo')
                    self.assertTrue(binary.is_file(), str(binary))
                    with binary.open('rb') as stream:
                        translations = gettext.GNUTranslations(stream)
                    for key, value in po_entries(path).items():
                        if key and value:
                            self.assertEqual(translations.gettext(key), value, key)

    def test_printf_placeholders_are_preserved(self):
        for lang in LANGS:
            for domain in DOMAINS:
                path = ROOT / lang / 'LC_MESSAGES' / (domain + '.po')
                if not path.exists():
                    continue
                with self.subTest(lang=lang, domain=domain):
                    for key, value in po_entries(path).items():
                        if key and value:
                            self.assertEqual(sorted(FORMAT.findall(key)),
                                             sorted(FORMAT.findall(value)), key)

    def test_known_localized_messages(self):
        samples = {
            ('de', 'setupGlass17'): ('Standard Infobar type', 'Typ der Standard-Infobar'),
            ('fr', 'setupGlass17'): ('Root picon directory', 'Répertoire racine des picons'),
            ('nl', 'setupGlass17'): ('Root picon directory', 'Hoofdmap voor picons'),
            ('el', 'setupGlass17'): ('Satellite positions', 'Δορυφορικές θέσεις'),
            ('el', 'weather'): ('Heavy rain', 'Ισχυρή βροχή'),
            ('el', 'netatmo'): ('Wind Strength', 'Ένταση ανέμου'),
            ('el', 'helpTxt'): ('Temperature will be displayed in Celsius',
                                 'Η θερμοκρασία εμφανίζεται σε βαθμούς Κελσίου'),
            ('el', 'eWeather'): ('Add City', 'Προσθήκη πόλης'),
        }
        for (lang, domain), (key, expected) in samples.items():
            with self.subTest(lang=lang, domain=domain):
                with (ROOT / lang / 'LC_MESSAGES' / (domain + '.mo')).open('rb') as stream:
                    catalog = gettext.GNUTranslations(stream)
                self.assertEqual(catalog.gettext(key), expected)

    def test_greek_help_is_complete(self):
        greek = po_entries(ROOT / 'el' / 'LC_MESSAGES' / 'helpTxt.po')
        slovak = po_entries(ROOT / 'sk' / 'LC_MESSAGES' / 'helpTxt.po')
        self.assertEqual(set(greek), set(slovak))
        self.assertEqual([], [key for key, value in greek.items() if key and not value])


    def test_new_netatmo_catalogs_complete(self):
        reference = po_entries(ROOT / 'sk' / 'LC_MESSAGES' / 'netatmo.po')
        keys = set(reference) - {''}
        self.assertEqual(len(keys), 42)
        samples = {
            'it': ('Wind Strength', 'Velocità del vento'),
            'nl': ('Dew Point', 'Dauwpunt'),
            'pl': ('Pressure', 'Ciśnienie atmosferyczne'),
            'pt': ('Rainfall', 'Precipitação'),
            'ro': ('Wind Angle', 'Direcția vântului'),
            'hu': ('Humidity', 'Páratartalom'),
            'ru': ('Wind Strength', 'Скорость ветра'),
            'uk': ('Gust Angle', 'Напрям поривів'),
            'tr': ('Wind Angle', 'Rüzgâr yönü'),
            'zh': ('Dew Point', '露点'),
            'al': ('Humidity', 'Lagështia'),
            'et': ('Dew Point', 'Kastepunkt'),
            'lt': ('Wind Strength', 'Vėjo greitis'),
            'fa': ('Humidity', 'رطوبت'),
        }
        for lang, (key, expected) in samples.items():
            with self.subTest(lang=lang):
                catalog = po_entries(ROOT / lang / 'LC_MESSAGES' / 'netatmo.po')
                self.assertEqual(set(catalog) - {''}, keys)
                self.assertEqual([], [k for k in keys if not catalog[k]])
                with (ROOT / lang / 'LC_MESSAGES' / 'netatmo.mo').open('rb') as stream:
                    compiled = gettext.GNUTranslations(stream)
                self.assertEqual(compiled.gettext(key), expected)

    def test_estonian_historical_weather_terminology(self):
        catalog = po_entries(ROOT / 'et' / 'LC_MESSAGES' / 'eWeather.po')
        expected = {
            'warm': 'soe',
            'then t-storms': 'seejärel äikesetormid',
            'ENE': 'ida-kirde',
            'WNW': 'lääne-loode',
            'WSW': 'lääne-edela',
            'Change city': 'Muuda linna',
            'then showers': 'seejärel hoovihmad',
        }
        for key, translation in expected.items():
            with self.subTest(key=key):
                self.assertEqual(catalog[key], translation)
        with (ROOT / 'et' / 'LC_MESSAGES' / 'eWeather.mo').open('rb') as stream:
            binary = gettext.GNUTranslations(stream)
        for key, translation in expected.items():
            self.assertEqual(binary.gettext(key), translation)

    def test_extended_greek_weather_batch(self):
        catalog = po_entries(ROOT / 'el' / 'LC_MESSAGES' / 'eWeather.po')
        self.assertEqual(len(catalog) - 1, 2117)
        self.assertEqual(sum(bool(v) for k, v in catalog.items() if k), 1674)
        self.assertEqual(catalog['cloudy with a heavy shower'], 'Συννεφιά με ισχυρή μπόρα')
        self.assertEqual(catalog['early showers'], 'Πρωινές μπόρες')
        self.assertEqual(catalog['drizzle'], 'Ψιχάλα')
        self.assertEqual(catalog['a thunderstorm'], 'Καταιγίδα')
        self.assertEqual(catalog['abundant sunshine and breezy'], 'Άφθονη ηλιοφάνεια με αεράκι')
        self.assertEqual(catalog['late-night rain'], 'βροχή αργά τη νύχτα')
        self.assertEqual(catalog['heavy evening thunderstorms'], 'ισχυρές καταιγίδες το βράδυ')
        self.assertEqual(catalog['clear and unseasonably cold'], 'αίθριος καιρός με ασυνήθιστο κρύο για την εποχή')
        self.assertEqual(catalog['snow'], 'χιόνι')
        self.assertEqual(catalog['fog in the morning'], 'ομίχλη το πρωί')

    def test_chinese_catalog_headers_and_enabled_speed_hint(self):
        weather = po_entries(ROOT / 'zh' / 'LC_MESSAGES' / 'weather.po')
        help_data = po_entries(ROOT / 'zh' / 'LC_MESSAGES' / 'helpTxt.po')
        self.assertIn('nplurals=1; plural=0;', weather[''])
        self.assertIn('Language: zh_CN', help_data[''])
        self.assertIn('nplurals=1; plural=0;', help_data[''])
        self.assertEqual(help_data['Measurement of current network speed is enabled and is displayed in kb/s'],
                         '已启用当前网络速度测量，并以 kb/s 显示')
        self.assertEqual([], [k for k, v in help_data.items() if k and not v])

if __name__ == '__main__':
    unittest.main()
