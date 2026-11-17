"""Ensure all shipped FullHDGlass core language catalogues load under Python 3."""
import gettext
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1] / 'source/package-root/usr/lib/enigma2/python/Plugins/Extensions/setupGlass17/locale'
LANGS = ('al', 'cs', 'de', 'el', 'es', 'et', 'fa', 'fr', 'hu', 'it',
         'lt', 'nl', 'pl', 'pt', 'ro', 'ru', 'sk', 'tr', 'uk', 'zh')
COMPLETE_MAIN = ('cs', 'el', 'lt', 'ru', 'sk', 'zh')


class CatalogIntegrity(unittest.TestCase):
    def test_all_locales_have_loadable_compiled_main_catalog(self):
        self.assertEqual(len(LANGS) + 1, 21)  # English is the msgid source.
        for lang in LANGS:
            with self.subTest(language=lang):
                path = ROOT / lang / 'LC_MESSAGES' / 'setupGlass17.mo'
                self.assertTrue(path.is_file(), str(path))
                with path.open('rb') as stream:
                    catalog = gettext.GNUTranslations(stream)
                self.assertTrue(callable(catalog.gettext))

    def test_greek_all_five_domains_and_known_messages(self):
        samples = {
            'setupGlass17': ('Satellite positions', 'Δορυφορικές θέσεις'),
            'weather': ('Heavy rain', 'Ισχυρή βροχή'),
            'netatmo': ('Wind Strength', 'Ένταση ανέμου'),
            'helpTxt': ('Temperature will be displayed in Celsius',
                        'Η θερμοκρασία εμφανίζεται σε βαθμούς Κελσίου'),
            'eWeather': ('Rain', 'Βροχή'),
        }
        for domain, (source, translated) in samples.items():
            with self.subTest(domain=domain):
                with (ROOT / 'el' / 'LC_MESSAGES' / (domain + '.mo')).open('rb') as f:
                    catalog = gettext.GNUTranslations(f)
                self.assertEqual(catalog.gettext(source), translated)

    def test_recent_translations_survive_rebuild(self):
        examples = {
            'cs': ('Satellite positions', 'Satelitní pozice'),
            'ru': ('Satellite positions', 'Спутниковые позиции'),
            'lt': ('Satellite positions', 'Palydovinės pozicijos'),
            'zh': ('Satellite positions', '卫星轨位'),
            'de': ('Satellite positions', 'Satellitenpositionen'),
            'fr': ('Satellite positions', 'Positions satellites'),
            'al': ('Satellite positions', 'Pozicionet satelitore'),
            'tr': ('Satellite positions', 'Uydu konumları'),
            'uk': ('Satellite positions', 'Супутникові позиції'),
        }
        for lang, (source, translated) in examples.items():
            with self.subTest(language=lang):
                with (ROOT / lang / 'LC_MESSAGES' / 'setupGlass17.mo').open('rb') as f:
                    catalog = gettext.GNUTranslations(f)
                self.assertEqual(catalog.gettext(source), translated)


if __name__ == '__main__':
    unittest.main()
