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
LANGUAGE_TAGS = {
    'al': 'sq_AL', 'cs': 'cs_CZ', 'de': 'de_DE', 'el': 'el_GR',
    'es': 'es_ES', 'et': 'et_EE', 'fa': 'fa_IR', 'fr': 'fr_FR',
    'hu': 'hu_HU', 'it': 'it_IT', 'lt': 'lt_LT', 'nl': 'nl_NL',
    'pl': 'pl_PL', 'pt': 'pt_PT', 'ro': 'ro_RO', 'ru': 'ru_RU',
    'sk': 'sk_SK', 'tr': 'tr_TR', 'uk': 'uk_UA', 'zh': 'zh_CN',
}
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
    def test_main_gettext_language_headers_match_locale(self):
        self.assertEqual(set(LANGUAGE_TAGS), set(LANGS))
        for lang, expected in LANGUAGE_TAGS.items():
            with self.subTest(lang=lang):
                path = ROOT / lang / 'LC_MESSAGES' / 'setupGlass17.po'
                po_header = po_entries(path)['']
                self.assertIn('Language: %s\n' % expected, po_header)
                self.assertIn('charset=UTF-8', po_header)
                with path.with_suffix('.mo').open('rb') as stream:
                    catalog = gettext.GNUTranslations(stream)
                self.assertEqual(catalog.info().get('language'), expected)

    def test_source_literals_are_present_in_each_catalog(self):
        modules = {'setupGlass17': 'plugin', 'helpTxt': 'txt', 'weather': 'weather',
                   'netatmo': 'Netatmo', 'eWeather': 'E_weather'}
        for domain, module in modules.items():
            code = ast.parse((ROOT.parent / (module + '.py')).read_bytes())
            source_keys = {
                call.args[0].value for call in ast.walk(code)
                if isinstance(call, ast.Call) and isinstance(call.func, ast.Name)
                and call.func.id == '_' and call.args and isinstance(call.args[0], ast.Constant)
                and isinstance(call.args[0].value, str)
            }
            reference = po_entries(ROOT / 'sk/LC_MESSAGES' / (domain + '.po'))
            self.assertFalse(source_keys - reference.keys(), (domain, source_keys - reference.keys()))
            for language in LANGS:
                with self.subTest(domain=domain, language=language):
                    path = ROOT / language / 'LC_MESSAGES' / (domain + '.po')
                    values = po_entries(path)
                    for key in source_keys:
                        self.assertTrue(values.get(key, '').strip(), (domain, language, key))

    def test_locale_count_and_complete_main_keys(self):
        self.assertEqual(len(LANGS) + 1, 21)  # en: untranslated msgid source.
        reference = po_entries(ROOT / 'sk' / 'LC_MESSAGES' / 'setupGlass17.po')
        expected = set(reference) - {''}
        self.assertEqual(len(expected), 580)
        for lang in LANGS:
            with self.subTest(lang=lang):
                path = ROOT / lang / 'LC_MESSAGES' / 'setupGlass17.po'
                self.assertTrue(path.is_file(), str(path))
                catalog = po_entries(path)
                actual = set(catalog) - {''}
                self.assertEqual(expected, actual)
                self.assertEqual([], [key for key in expected if not catalog[key]])

    def test_five_new_complete_help_catalogs(self):
        """Verify newly authored help for Ukrainian, Polish, Portuguese, Romanian and Dutch."""
        reference = po_entries(ROOT / 'sk' / 'LC_MESSAGES' / 'helpTxt.po')
        expected_keys = set(reference) - {''}
        self.assertEqual(len(expected_keys), 195)
        samples = {
            'uk': ('Дані EPG недоступні', 'Остання чверть'),
            'pl': ('Brak dostępnych danych EPG', 'Ostatnia kwadra'),
            'pt': ('Não existem dados EPG disponíveis', 'Quarto minguante'),
            'ro': ('Nu sunt disponibile date EPG', 'Ultimul pătrar'),
            'nl': ('Geen EPG-gegevens beschikbaar', 'Laatste kwartier'),
        }
        for lang, (no_epg, last_quarter) in samples.items():
            with self.subTest(lang=lang):
                po = ROOT / lang / 'LC_MESSAGES' / 'helpTxt.po'
                entries = po_entries(po)
                self.assertEqual(set(entries) - {''}, expected_keys)
                self.assertFalse(any(not entries[key].strip() for key in expected_keys))
                self.assertIn('Language: %s\n' % LANGUAGE_TAGS[lang], entries[''])
                self.assertIn('charset=UTF-8', entries[''])
                with po.with_suffix('.mo').open('rb') as stream:
                    compiled = gettext.GNUTranslations(stream)
                self.assertEqual(compiled.info().get('language'), LANGUAGE_TAGS[lang])
                self.assertEqual(set(compiled._catalog), set(entries))
                for key, value in entries.items():
                    if key:
                        self.assertEqual(compiled.gettext(key), value, (lang, key))
                self.assertEqual(compiled.gettext('No EPG data available'), no_epg)
                self.assertEqual(compiled.gettext('Last Quarter'), last_quarter)

    def test_every_help_catalog_is_complete_and_localized(self):
        """All twenty help catalogs must include 195 reference keys and load as GNU gettext."""
        reference = po_entries(ROOT / 'sk/LC_MESSAGES/helpTxt.po')
        expected = set(reference) - {''}
        self.assertEqual(len(expected), 195)
        samples = {
            'al': ('No EPG data available', 'Nuk ka të dhëna EPG'),
            'et': ('Last Quarter', 'Viimane veerand'),
            'fa': ('No EPG data available', 'داده‌های EPG در دسترس نیست'),
            'hu': ('Last Quarter', 'Utolsó negyed'),
            'tr': ('No EPG data available', 'EPG verisi bulunmuyor'),
        }
        for lang in LANGS:
            with self.subTest(lang=lang):
                path = ROOT / lang / 'LC_MESSAGES/helpTxt.po'
                entries = po_entries(path)
                self.assertEqual(set(entries) - {''}, expected)
                self.assertFalse(any(not entries[key].strip() for key in expected))
                valid_tags = (LANGUAGE_TAGS[lang], LANGUAGE_TAGS[lang].split('_')[0])
                self.assertTrue(any('Language: %s\n' % tag in entries['']
                                    for tag in valid_tags), lang)
                with path.with_suffix('.mo').open('rb') as stream:
                    compiled = gettext.GNUTranslations(stream)
                self.assertIn(compiled.info().get('language'), valid_tags)
                self.assertEqual(set(compiled._catalog), set(entries))
                for key in expected:
                    self.assertEqual(compiled.gettext(key), entries[key], (lang, key))
                if lang in samples:
                    key, translation = samples[lang]
                    self.assertEqual(compiled.gettext(key), translation)

    def test_full_five_domain_coverage_in_all_twenty_locales(self):
        """Enforce every reference key in every translated .po and .mo catalog."""
        expected_counts = {'setupGlass17': 580, 'helpTxt': 195,
                           'weather': 108, 'netatmo': 42, 'eWeather': 2119}
        self.assertEqual(set(DOMAINS), set(expected_counts))
        for domain in DOMAINS:
            reference = po_entries(ROOT / 'sk/LC_MESSAGES' / (domain + '.po'))
            keys = set(reference) - {''}
            self.assertEqual(len(keys), expected_counts[domain])
            for lang in LANGS:
                with self.subTest(domain=domain, lang=lang):
                    path = ROOT / lang / 'LC_MESSAGES' / (domain + '.po')
                    values = po_entries(path)
                    missing = {key for key in keys if not values.get(key, '').strip()}
                    self.assertFalse(missing, (domain, lang, sorted(missing)))
                    with path.with_suffix('.mo').open('rb') as stream:
                        binary = gettext.GNUTranslations(stream)
                    for key in keys:
                        self.assertEqual(binary.gettext(key), values[key], (lang, domain, key))

    def test_all_shipped_mo_files_load_and_match_po(self):
        for lang in LANGS:
            for domain in DOMAINS:
                path = ROOT / lang / 'LC_MESSAGES' / (domain + '.po')
                with self.subTest(lang=lang, domain=domain):
                    binary = path.with_suffix('.mo')
                    self.assertTrue(binary.is_file(), str(binary))
                    with binary.open('rb') as stream:
                        translations = gettext.GNUTranslations(stream)
                    catalog = po_entries(path)
                    self.assertEqual(set(translations._catalog), set(catalog))
                    tag = translations.info().get('language')
                    self.assertIn(tag, (LANGUAGE_TAGS[lang], LANGUAGE_TAGS[lang].split('_')[0]))
                    self.assertIn('Language: %s\n' % tag, catalog[''])
                    self.assertEqual(translations.charset().lower(), 'utf-8')
                    for key, value in catalog.items():
                        if key and value:
                            self.assertEqual(translations.gettext(key), value, key)

    def test_printf_placeholders_are_preserved(self):
        for lang in LANGS:
            for domain in DOMAINS:
                path = ROOT / lang / 'LC_MESSAGES' / (domain + '.po')
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

    def test_new_weather_catalogs_complete(self):
        reference = po_entries(ROOT / 'sk' / 'LC_MESSAGES' / 'weather.po')
        keys = set(reference) - {''}
        self.assertEqual(len(keys), 108)
        samples = {
            'es': ('Heavy rain', 'Lluvia intensa', 'Wind direction', 'Dirección del viento'),
            'it': ('Heavy rain', 'Pioggia forte', 'Wind direction', 'Direzione del vento'),
            'pt': ('Heavy rain', 'Chuva forte', 'Wind direction', 'Direção do vento'),
            'al': ('Heavy rain', 'Shi i rrëmbyeshëm', 'Wind direction', 'Drejtimi i erës'),
            'tr': ('Heavy rain', 'Şiddetli yağmur', 'Wind direction', 'Rüzgâr yönü'),
            'fa': ('Heavy rain', 'باران شدید', 'Wind direction', 'جهت باد'),
        }
        for lang, (key1, expected1, key2, expected2) in samples.items():
            with self.subTest(lang=lang):
                path = ROOT / lang / 'LC_MESSAGES' / 'weather.po'
                catalog = po_entries(path)
                self.assertEqual(set(catalog) - {''}, keys)
                self.assertEqual([], [key for key in keys if not catalog[key]])
                with path.with_suffix('.mo').open('rb') as stream:
                    binary = gettext.GNUTranslations(stream)
                self.assertEqual(binary.gettext(key1), expected1)
                self.assertEqual(binary.gettext(key2), expected2)

    def test_every_weather_catalog_is_complete(self):
        reference = po_entries(ROOT / 'sk' / 'LC_MESSAGES' / 'weather.po')
        expected = set(reference) - {''}
        self.assertEqual(len(expected), 108)
        for lang in LANGS:
            with self.subTest(lang=lang):
                path = ROOT / lang / 'LC_MESSAGES' / 'weather.po'
                self.assertTrue(path.is_file())
                values = po_entries(path)
                self.assertEqual(set(values) - {''}, expected)
                self.assertEqual([], [k for k in expected if not values[k]])
                with path.with_suffix('.mo').open('rb') as stream:
                    compiled = gettext.GNUTranslations(stream)
                for key in expected:
                    self.assertEqual(compiled.gettext(key), values[key], (lang, key))

    def test_german_help_translations_complete_and_loadable(self):
        path = ROOT / 'de' / 'LC_MESSAGES' / 'helpTxt.po'
        reference = po_entries(ROOT / 'sk' / 'LC_MESSAGES' / 'helpTxt.po')
        german = po_entries(path)
        self.assertEqual(len(set(reference) - {''}), 195)
        self.assertEqual(set(german), set(reference))
        self.assertEqual([], [key for key, value in german.items() if key and not value])
        self.assertIn('Language: de_DE\n', german[''])
        self.assertIn('charset=UTF-8', german[''])
        samples = {
            'Please wait for the reading and processing of data':
                'Bitte warten, während die Daten gelesen und verarbeitet werden',
            'No plugin Netatmo installed':
                'Das Netatmo-Plugin ist nicht installiert',
            'Press button "OK" to activate selected function':
                'Drücken Sie „OK“, um die ausgewählte Funktion zu aktivieren',
            'Your API-key': 'Ihr API-Schlüssel',
            'Last Quarter': 'Letztes Viertel',
        }
        with path.with_suffix('.mo').open('rb') as stream:
            binary = gettext.GNUTranslations(stream)
        self.assertEqual(binary.info().get('language'), 'de_DE')
        for key in set(reference) - {''}:
            self.assertEqual(binary.gettext(key), german[key], key)
        for key, expected in samples.items():
            self.assertEqual(german[key], expected)
            self.assertEqual(binary.gettext(key), expected)

    def test_french_help_translations_complete_and_loadable(self):
        path = ROOT / 'fr' / 'LC_MESSAGES' / 'helpTxt.po'
        reference = po_entries(ROOT / 'sk' / 'LC_MESSAGES' / 'helpTxt.po')
        french = po_entries(path)
        self.assertEqual(len(set(reference) - {''}), 195)
        self.assertEqual(set(french), set(reference))
        self.assertEqual([], [key for key, value in french.items() if key and not value])
        self.assertIn('Language: fr_FR\n', french[''])
        self.assertIn('charset=UTF-8', french[''])
        samples = {
            'Your API-key': 'Votre clé API',
            'No EPG data available': 'Aucune donnée EPG disponible',
            'Measurement of current network speed is enabled and is displayed in Mb/s':
                'La mesure de la vitesse réseau actuelle est activée et s’affiche en Mb/s',
            'Last Quarter': 'Dernier quartier',
        }
        with path.with_suffix('.mo').open('rb') as stream:
            binary = gettext.GNUTranslations(stream)
        self.assertEqual(binary.info().get('language'), 'fr_FR')
        for key in set(reference) - {''}:
            self.assertEqual(binary.gettext(key), french[key], key)
        for key, expected in samples.items():
            self.assertEqual(french[key], expected)
            self.assertEqual(binary.gettext(key), expected)

    def test_spanish_help_translations_complete_and_loadable(self):
        path = ROOT / 'es' / 'LC_MESSAGES' / 'helpTxt.po'
        reference = po_entries(ROOT / 'sk' / 'LC_MESSAGES' / 'helpTxt.po')
        spanish = po_entries(path)
        self.assertEqual(len(set(reference) - {''}), 195)
        self.assertEqual(set(spanish), set(reference))
        self.assertEqual([], [key for key, value in spanish.items() if key and not value])
        self.assertIn('Language: es_ES\n', spanish[''])
        self.assertIn('charset=UTF-8', spanish[''])
        samples = {
            'No EPG data available': 'No hay datos EPG disponibles',
            'Your API-key': 'Su clave API',
            'Press button "OK" to activate selected function':
                'Pulse «OK» para activar la función seleccionada',
            'Last Quarter': 'Cuarto menguante',
        }
        with path.with_suffix('.mo').open('rb') as stream:
            binary = gettext.GNUTranslations(stream)
        self.assertEqual(binary.info().get('language'), 'es_ES')
        for key in set(reference) - {''}:
            self.assertEqual(binary.gettext(key), spanish[key], key)
        for key, expected in samples.items():
            self.assertEqual(spanish[key], expected)
            self.assertEqual(binary.gettext(key), expected)

    def test_italian_help_is_complete_and_loadable(self):
        path = ROOT / 'it/LC_MESSAGES/helpTxt.po'
        catalog = po_entries(path)
        reference = po_entries(ROOT / 'sk/LC_MESSAGES/helpTxt.po')
        keys = set(catalog) - {''}
        self.assertEqual(len(keys), 195)
        self.assertEqual(keys, set(reference) - {''})
        self.assertTrue(all(catalog[key].strip() for key in keys))
        self.assertEqual(catalog['No EPG data available'], 'Nessun dato EPG disponibile')
        self.assertEqual(catalog['Last Quarter'], 'Ultimo quarto')
        with path.with_suffix('.mo').open('rb') as stream:
            binary = gettext.GNUTranslations(stream)
        self.assertEqual(set(binary._catalog) - {''}, keys)

    def test_translatable_settings_and_weather_labels_are_localized(self):
        for lang in LANGS:
            setup = po_entries(ROOT / lang / 'LC_MESSAGES/setupGlass17.po')
            for key in ('Show recording icon', 'Channel name', 'only Time', 'ECM Labels',
                        'Choose the available satellite picon variant.', 'Configure the FullHDGlass skin'):
                self.assertNotEqual(setup[key].casefold(), key.casefold(), (lang, key))
            weather = po_entries(ROOT / lang / 'LC_MESSAGES/weather.po')
            self.assertNotEqual(weather['Feels like'].casefold(), 'feels like', lang)

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

    def test_estonian_eweather_is_complete(self):
        catalog = po_entries(ROOT / 'et' / 'LC_MESSAGES' / 'eWeather.po')
        reference = po_entries(ROOT / 'sk' / 'LC_MESSAGES' / 'eWeather.po')
        keys = set(catalog) - {''}
        expected_keys = set(reference) - {''}
        self.assertEqual(len(expected_keys), 2119)
        self.assertEqual(keys, expected_keys | {'Select city'})
        self.assertTrue(all(catalog[key].strip() for key in keys))
        expected = {
            'a p.m. snow shower in spots': 'pärastlõunal kohati lumehooge',
            'a severe thunderstorm': 'tugev äikesetorm',
            'windy and frigid': 'tuuline ja pakaseline',
            'rain to snow': 'vihm läheb üle lumeks',
            'a wintry mix late': 'hiljem segasademed',
            'cloudy with snow tapering off': 'Pilves, lumesadu nõrgeneb',
            'a p.m. t-storm': 'Pärastlõunal äikesetorm',
            'partly sunny and warm': 'Osaliselt päikeseline ja soe',
            'Select City': 'Vali linn',
            'a thunderstorm this afternoon': 'Täna pärastlõunal äikesetorm',
            'mostly sunny and comfortable': 'Enamasti päikeseline ja mõnus',
            'strong afternoon t-storms': 'Pärastlõunal tugevad äikesetormid',
            'partly sunny and breezy': 'Osaliselt päikeseline ja tuuline',
            'blowing dust': 'Tuulega lendlev tolm',
            'strong thunderstorms possible': 'Võimalikud tugevad äikesetormid',
            'mostly cloudy and hot': 'Enamasti pilves ja kuum',
            'dense fog': 'Tihe udu',
            'a strong thunderstorm': 'Tugev äikesetorm',
            'fog will lift this morning': 'Udu hajub täna hommikul',
            'cloudy with heavy showers': 'Pilves, tugevad hoovihmad',
            'humid with rain and drizzle': 'Niiske, vihm ja uduvihm',
            'windy in the afternoon': 'Pärastlõunal tuuline',
            'a heavy thunderstorm': 'Tugev äikesetorm',
            'a snow squall in the morning': 'Hommikul tugev lumehoog',
            'a shower this afternoon': 'Täna pärastlõunal hoovihm',
            'a shower late': 'hiljem hoovihm',
            'low clouds and freezing fog': 'madalad pilved ja jäätuv udu',
            'heavy showers this afternoon': 'täna pärastlõunal tugevad hoovihmad',
            'a wintry mix': 'talvised segasademed',
        }
        with (ROOT / 'et' / 'LC_MESSAGES' / 'eWeather.mo').open('rb') as stream:
            binary = gettext.GNUTranslations(stream)
        self.assertEqual(binary.info().get('language'), 'et')
        self.assertEqual(binary.charset().lower(), 'utf-8')
        for key in keys:
            self.assertEqual(binary.gettext(key), catalog[key], key)
        for key, value in expected.items():
            with self.subTest(key=key):
                self.assertEqual(catalog[key], value)
                self.assertEqual(binary.gettext(key), value)

    def test_shared_extended_weather_messages(self):
        expected = set(po_entries(ROOT / 'sk/LC_MESSAGES/eWeather.po')) - {''}
        sun = {'al': 'Diell', 'de': 'Sonne', 'es': 'Sol', 'fa': 'خورشید',
               'fr': 'Soleil', 'hu': 'Nap', 'it': 'Sole', 'nl': 'Zon',
               'pl': 'Słońce', 'pt': 'Sol', 'ro': 'Soare', 'ru': 'Солнце',
               'tr': 'Güneş', 'uk': 'Сонце', 'zh': '太阳'}
        for lang, translation in sun.items():
            with self.subTest(lang=lang):
                path = ROOT / lang / 'LC_MESSAGES' / 'eWeather.po'
                catalog = po_entries(path)
                keys = set(catalog) - {''}
                self.assertEqual(keys, expected)
                self.assertTrue(all(catalog[key].strip() for key in keys))
                self.assertEqual(catalog['sun'], translation)
                with path.with_suffix('.mo').open('rb') as stream:
                    binary = gettext.GNUTranslations(stream)
                self.assertEqual(set(binary._catalog) - {''}, keys)

    def test_extended_greek_weather_batch(self):
        catalog = po_entries(ROOT / 'el' / 'LC_MESSAGES' / 'eWeather.po')
        self.assertEqual(len(catalog) - 1, 2119)
        self.assertEqual(sum(bool(v) for k, v in catalog.items() if k), 2119)
        self.assertEqual([], [k for k, v in catalog.items() if k and not v])
        self.assertEqual(catalog['overcast with late-night rain'], 'συννεφιά με βροχή αργά τη νύχτα')
        self.assertEqual(catalog['heavy showers this afternoon'], 'έντονες μπόρες σήμερα το απόγευμα')
        self.assertEqual(catalog['freezing fog'], 'παγωμένη ομίχλη')
        self.assertEqual(catalog['Heavy rain'], 'Έντονη βροχή')
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
