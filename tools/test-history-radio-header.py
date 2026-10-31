"""Four readable history blocks, real font widths and translated radio titles."""
import ast
import importlib.util
import json
from pathlib import Path
from types import SimpleNamespace
import sys
import unittest
from unittest.mock import patch
import xml.etree.ElementTree as ET

from PIL import ImageFont

ROOT = Path(__file__).resolve().parents[1]
PAYLOAD = ROOT / 'source/package-root'
PLUGIN = PAYLOAD / 'usr/lib/enigma2/python/Plugins/Extensions/setupGlass17'


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


history = load('history_test', PLUGIN / 'warderHistory.py')
font_root = PAYLOAD / 'usr/share/fonts'
fonts = {False: ImageFont.truetype(str(font_root / 'prive7.ttf'), 30),
         True: ImageFont.truetype(str(font_root / 'prive7.ttf'), 33)}


def measure(value, heading):
    return fonts[heading].getlength(value)


class HistoryTests(unittest.TestCase):
    def test_full_history_kept_but_only_four_entries_displayed(self):
        text = (PLUGIN / 'history.txtSk').read_text()
        self.assertGreater(len(history.entries(text)), 4)
        rows = history.layout(text, measure, 1552)
        self.assertEqual(len([r for r in rows if r[0] == 'heading']), 4)
        self.assertEqual(len([r for r in rows if r[0] == 'rule']), 3)
        self.assertLessEqual(len(rows), 19)
        self.assertLessEqual(len(rows) * 37, 740)

    def test_visible_history_contains_only_public_change_descriptions(self):
        forbidden = r'(?:/usr/|/etc/|assets/|\.(?:py|cpp|json|xml|ipk|zip)\b|SHA-?256|\bgRC\b|\bCI\b|workflow|unit test|owner.confirm|používateľom|prijímači overené používateľom)'
        for name in ('history.txt', 'history.txtSk'):
            for entry in history.entries((PLUGIN / name).read_text())[:4]:
                for description in entry['paragraphs']:
                    self.assertNotRegex(description, forbidden)

    def test_no_empty_lines_required_between_mixed_legacy_version_formats(self):
        text = 'FullHDGlass Warder Evolution 1.0.47 — 31.10.2026\nLatest change\n1.0.46-test1: Spinner checked\n1.0.45 - Compatibility repaired\n1.0.44: Radio import\n1.0.43: Keyboard'
        entries = history.entries(text)
        self.assertEqual(len(entries), 5)
        self.assertEqual(entries[1]['heading'], 'FullHDGlass 1.0.46-test1')
        self.assertEqual(entries[1]['paragraphs'], ['Spinner checked'])
        self.assertEqual(len([r for r in history.layout(text, measure, 1552) if r[0] == 'heading']), 4)

    def test_long_sentences_and_unsplit_tokens_fit_actual_receiver_font_width(self):
        text = 'FullHDGlass 1.0.47 — 31.10.2026\n' + ('Wide WWW text with Slovak diacritics žľščť and a very long description. ' * 20)
        rows = history.layout(text, measure, 700)
        body = [value for kind, value in rows if kind == 'body']
        self.assertEqual(len(body), 3)
        self.assertTrue(body[-1].endswith('…'))
        for kind, value in rows:
            if kind in ('body', 'heading'):
                self.assertLessEqual(measure(value, kind == 'heading'), 700)
        token = 'https://example.invalid/' + 'W' * 300
        wrapped = history.wrap(token, lambda value: measure(value, False), 700)
        self.assertEqual(''.join(wrapped), token)
        self.assertTrue(all(measure(value, False) <= 700 for value in wrapped))

    def test_result_dialog_bypasses_history_limit_and_keeps_original_actions(self):
        tree = ast.parse((PLUGIN / 'plugin.py').read_text())
        cls = next(n for n in tree.body if isinstance(n, ast.ClassDef) and n.name == 'historyScreen')
        method = next(n for n in cls.body if isinstance(n, ast.FunctionDef) and n.name == 'readandshow')
        guard = next(n for n in method.body if isinstance(n, ast.If) and ast.unparse(n.test) == 'not a')
        self.assertIn('populate(self, f)', ast.unparse(guard))
        rest = ast.unparse(method)
        self.assertIn('MultiContentEntryPixmapAlphaTest', rest)
        self.assertIn("_('SUCCESSFUL')", rest)
        self.assertIn("_('PARTIAL SUCCESS')", rest)


class RadioTitleTests(unittest.TestCase):
    def setUp(self):
        self.config = SimpleNamespace(osd=SimpleNamespace(language=SimpleNamespace(value='sk_SK')))
        with patch.dict(sys.modules, {'Components.config': SimpleNamespace(config=self.config)}):
            self.text = load('radio_title_translations', PLUGIN / 'warderUiText.py')

    def test_active_osd_language_changes_the_caption_without_cached_language(self):
        for locale, expected in [('sk_SK', 'REŽIM RÁDIA'), ('cs_CZ', 'REŽIM RÁDIA'), ('en_GB', 'RADIO MODE'), ('de_DE', 'RADIOMODUS')]:
            self.config.osd.language.value = locale
            self.assertEqual(self.text.ui_text('Radio mode').upper(), expected)

    def test_every_supported_language_has_a_translation_that_fits_the_header(self):
        font = ImageFont.truetype(str(font_root / 'prive7.ttf'), 34)
        for code in ('al','cs','de','en','es','et','fa','fr','hu','it','lt','nl','pl','pt','ro','ru','sk','tr','uk','zh'):
            self.config.osd.language.value = code + '_XX'
            self.assertIn('Radio mode', self.text.TEXT[code])
            self.assertLessEqual(font.getlength(self.text.ui_text('Radio mode').upper()), 320, code)

    def test_one_centered_caption_in_each_radio_header_keeps_date_clock_and_brand(self):
        skin = ET.parse(PAYLOAD / 'usr/share/enigma2/hd_glass17/skin.xml').getroot()
        for name in ('RdsInfoDisplay', 'RdsDisplay'):
            screen = skin.find("screen[@name='%s']" % name)
            labels = [w for w in screen.findall('widget') if w.findtext('convert') == 'RadioMode']
            self.assertEqual(len(labels), 1)
            self.assertEqual(labels[0].get('position'), '800,28')
            self.assertEqual(labels[0].get('size'), '320,58')
            self.assertEqual(labels[0].get('halign'), 'center')
            self.assertEqual(labels[0].get('foregroundColor'), '#003ccfff')
            date = next(w for w in screen.findall('widget') if w.findtext('convert') == 'Date')
            self.assertEqual(date.get('position'), '1120,28')
            self.assertIsNotNone(screen.find("eLabel[@text='FullHDGlass by Warder']"))


if __name__ == '__main__':
    unittest.main()
