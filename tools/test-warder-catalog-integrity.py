"""Ensure all shipped FullHDGlass core language catalogues load under Python 3."""
import gettext
import re
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1] / 'source/package-root/usr/lib/enigma2/python/Plugins/Extensions/setupGlass17/locale'
LANGS = ('al', 'cs', 'de', 'el', 'es', 'et', 'fa', 'fr', 'hu', 'it',
         'lt', 'nl', 'pl', 'pt', 'ro', 'ru', 'sk', 'tr', 'uk', 'zh')
COMPLETE_MAIN = ('cs', 'de', 'el', 'es', 'et', 'fr', 'it', 'lt', 'nl', 'pl', 'ru', 'sk', 'zh')


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


    def test_completed_main_po_files_contain_no_empty_translations(self):
        # Count only real messages, not the multi-line gettext metadata header.
        pattern = re.compile(r'^msgid "((?:\\.|[^"\\])*)"\nmsgstr ""$', re.MULTILINE)
        for lang in COMPLETE_MAIN:
            with self.subTest(language=lang):
                path = ROOT / lang / 'LC_MESSAGES' / 'setupGlass17.po'
                source = path.read_text(encoding='utf-8')
                # Empty msgid is the gettext metadata header, not a real message.
                untranslated = [msgid for msgid in pattern.findall(source) if msgid]
                self.assertEqual([], untranslated,
                                 'Untranslated entries in %s: %r' % (lang, untranslated[:5]))

    def test_completed_new_language_messages_load_correctly(self):
        samples = {
            'de': ('Standard Infobar type', 'Typ der Standard-Infobar'),
            'fr': ('Root picon directory', 'Répertoire racine des picons'),
            'nl': ('Root picon directory', 'Hoofdmap voor picons'),
            'es': ('Root picon directory', 'Directorio raíz de picons'),
            'it': ('Root picon directory', 'Cartella principale dei picon'),
            'et': ('Root picon directory', 'Pikonite juurkataloog'),
        }
        for lang, (source, expected) in samples.items():
            with self.subTest(language=lang):
                path = ROOT / lang / 'LC_MESSAGES' / 'setupGlass17.mo'
                with path.open('rb') as f:
                    catalog = gettext.GNUTranslations(f)
                self.assertEqual(catalog.gettext(source), expected)

    def test_greek_all_five_domains_and_known_messages(self):
        samples = {
            'setupGlass17': ('Satellite positions', 'Δορυφορικές θέσεις'),
            'weather': ('Heavy rain', 'Ισχυρή βροχή'),
            'netatmo': ('Wind Strength', 'Ένταση ανέμου'),
            'helpTxt': ('Temperature will be displayed in Celsius',
                        'Η θερμοκρασία εμφανίζεται σε βαθμούς Κελσίου'),
            'eWeather': ('Add City', 'Προσθήκη πόλης'),
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
