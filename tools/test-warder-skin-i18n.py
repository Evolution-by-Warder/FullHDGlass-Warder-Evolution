"""Test source-only gettext language resolution without receiver imports."""
import importlib.util
import pathlib
import tempfile
import unittest
from types import SimpleNamespace
from unittest.mock import patch

PATH = pathlib.Path(__file__).resolve().parents[1] / 'source/package-root/usr/lib/enigma2/python/Plugins/Extensions/setupGlass17/warderLocale.py'
spec = importlib.util.spec_from_file_location('warderLocale_test', PATH)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


def settings(lang, enabled=True):
    return SimpleNamespace(
        osd=SimpleNamespace(language=SimpleNamespace(value=lang)),
        plugins=SimpleNamespace(setupGlass17=SimpleNamespace(par49=SimpleNamespace(value=enabled))))


class TestLocale(unittest.TestCase):
    def test_21_languages_and_aliases(self):
        self.assertEqual(len(mod.LANGUAGES), 21)
        for source, expected in [('sk_SK','sk'), ('sq_AL','al'), ('el_GR','el'),
                                 ('gr_GR','el'), ('zh_CN','zh'), ('unknown','en')]:
            self.assertEqual(mod.language_code(source), expected)

    def test_disabled_and_missing_catalogs(self):
        with tempfile.TemporaryDirectory() as directory:
            self.assertEqual(mod.get_translator('setupGlass17', settings('el_GR'), directory)('Sample'), 'Sample')
            self.assertEqual(mod.get_translator('weather', settings('sk_SK', False), directory)('Sample'), 'Sample')

    def test_active_greek_catalog_lookup(self):
        with patch.object(mod.gettext, 'translation') as loader:
            loader.return_value.gettext.return_value = 'Ελληνικά'
            fn = mod.get_translator('setupGlass17', settings('gr_GR'), '/test/plugin')
            self.assertEqual(fn('English'), 'Ελληνικά')
            loader.assert_called_once_with('setupGlass17', localedir='/test/plugin/locale',
                                           languages=['el'], fallback=True)


    def test_greek_catalogs_are_loadable_utf8(self):
        import gettext
        localedir = str(PATH.parent / 'locale')
        examples = {'setupGlass17': ('Save', 'Αποθήκευση'),
                    'helpTxt': ('N/A', 'Μ/Δ'),
                    'weather': ('Sunny', 'Ηλιοφάνεια'),
                    'netatmo': ('Humidity', 'Υγρασία'),
                    'eWeather': ('Rain', 'Βροχή')}
        for domain, (english, expected) in examples.items():
            with self.subTest(domain=domain):
                catalogue = gettext.translation(domain, localedir=localedir,
                                                languages=['el'], fallback=False)
                self.assertEqual(catalogue.gettext(english), expected)

if __name__ == '__main__':
    unittest.main()
