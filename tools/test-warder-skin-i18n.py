"""Test source-only gettext language resolution without receiver imports."""
import ast
import importlib.util
import pathlib
import tempfile
import shutil
import sys
import unittest
from types import SimpleNamespace
from unittest.mock import patch

PATH = pathlib.Path(__file__).resolve().parents[1] / 'source/package-root/usr/lib/enigma2/python/Plugins/Extensions/setupGlass17/warderLocale.py'
sys.path.insert(0, str(PATH.parent.parent))
from setupGlass17 import warderLocale as mod


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


    def test_existing_translator_loads_downloaded_catalog(self):
        with tempfile.TemporaryDirectory() as directory:
            plugin = pathlib.Path(directory) / "plugin"
            cache = pathlib.Path(directory) / "state"
            target = cache / "el/LC_MESSAGES/setupGlass17.mo"
            active = settings("el_GR")
            with patch.object(mod, "DOWNLOADED_LOCALE", str(cache)), patch.object(
                mod, "request_language"
            ) as request, patch.object(mod.time, "monotonic", side_effect=[1, 4, 7]):
                translate = mod.get_translator("setupGlass17", active, str(plugin))
                self.assertEqual(translate("Save"), "Save")
                target.parent.mkdir(parents=True)
                shutil.copyfile(PATH.parent / "locale/el/LC_MESSAGES/setupGlass17.mo", target)
                self.assertEqual(translate("Save"), "Αποθήκευση")
                active.osd.language.value = "en_GB"
                self.assertEqual(translate("Save"), "Save")
                self.assertEqual([item.args[0] for item in request.call_args_list], ["el", "el"])

    def test_language_notification_requests_only_the_current_language(self):
        callbacks = []
        setting = SimpleNamespace(value="tr_TR")

        def add_notifier(callback, initial_call):
            callbacks.append(callback)
            if initial_call:
                callback(setting)

        setting.addNotifier = add_notifier
        config = SimpleNamespace(osd=SimpleNamespace(language=setting))
        with patch.object(mod, "_watched_language", None), patch.object(mod, "request_language") as request:
            mod.watch_language(config, "/plugin")
            mod.watch_language(config, "/plugin")
            self.assertEqual(len(callbacks), 1)
            setting.value = "sq_AL"
            callbacks[0](setting)
            self.assertEqual([call.args for call in request.call_args_list],
                             [("tr", "/plugin"), ("al", "/plugin")])

    def test_cached_help_weather_and_ui_follow_download_and_language_change(self):
        active = settings("el_GR")
        key = "Press button \"OK\" to activate selected function"
        package = PATH.parent

        def factory(module, name):
            tree = ast.parse((package / (module + ".py")).read_bytes())
            code = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == name)
            scope = {"DG": "°"}
            exec(compile(ast.Module([code], []), module, "exec"), scope)
            return scope[name]

        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            plugin = root / "plugin"
            cache = root / "state"
            tick = [1]
            with patch.object(mod, "DOWNLOADED_LOCALE", str(cache)), patch.object(
                mod.time, "monotonic", side_effect=lambda: tick[0]
            ), patch.object(mod, "request_language"):
                help_text = mod.TranslatedMapping(mod.get_translator("helpTxt", active, plugin),
                                                  factory("txt", "_help_table"))
                weather = mod.TranslatedMapping(mod.get_translator("weather", active, plugin),
                                                factory("weather", "_conditions"))
                ui = mod.get_translator("setupGlass17", active, plugin, always_osd=True)
                self.assertEqual(help_text["ok-1"], key)
                self.assertEqual(weather["Sun"], "Sunny")
                self.assertEqual(ui("Back"), "Back")
                for lang in ("el", "fa"):
                    target = cache / lang / "LC_MESSAGES"
                    target.mkdir(parents=True)
                    for domain in ("helpTxt", "weather", "setupGlass17"):
                        shutil.copyfile(package / "locale" / lang / "LC_MESSAGES" / (domain + ".mo"),
                                        target / (domain + ".mo"))
                tick[0] += 3
                self.assertEqual(ui("Back"), "Πίσω")
                self.assertEqual(weather["Sun"], "Ηλιοφάνεια")
                self.assertNotEqual(help_text.get("ok-1"), key)
                active.osd.language.value = "fa_IR"
                self.assertEqual(ui("Back"), "بازگشت")
                self.assertIn("OK", help_text["ok-1"])
                active.plugins.setupGlass17.par49.value = False
                self.assertEqual(help_text["ok-1"], key)
                self.assertEqual(weather["Sun"], "Sunny")
                self.assertEqual(ui("Back"), "بازگشت")

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

    def test_complete_main_setup_catalogues(self):
        import gettext
        directory = str(PATH.parent / 'locale')
        examples = {'cs': 'Satelitní pozice', 'ru': 'Спутниковые позиции',
                    'lt': 'Palydovinės pozicijos', 'zh': '卫星轨位'}
        for lang, translated in examples.items():
            with self.subTest(language=lang):
                catalog = gettext.translation('setupGlass17',
                                              localedir=directory,
                                              languages=[lang],
                                              fallback=False)
                self.assertEqual(catalog.gettext('Satellite positions'), translated)

    def test_chinese_fuzzy_corrections(self):
        import gettext
        directory = str(PATH.parent / 'locale')
        catalog = gettext.translation('setupGlass17',
                                      localedir=directory,
                                      languages=['zh'], fallback=False)
        self.assertEqual(catalog.gettext('EventView type'), '节目信息类型')
        self.assertEqual(catalog.gettext('Forecast for more days'), '多日天气预报')

if __name__ == '__main__':
    unittest.main()
