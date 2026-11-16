#!/usr/bin/env python3
"""Regression check: both weather panels use Enigma2-language WMO labels."""
import ast
import gettext
import os
from pathlib import Path
from types import SimpleNamespace
import unittest

ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "source/package-root/usr/lib/enigma2/python/Plugins/Extensions/setupGlass17"


def isolated_functions():
    source = ast.parse((PLUGIN / "weaUtils.py").read_text(encoding="utf-8"))
    functions = [item for item in source.body
                 if isinstance(item, ast.FunctionDef)
                 and item.name in ("wmoText", "localizedWeatherCondition")]
    assert len(functions) == 2
    config = SimpleNamespace(osd=SimpleNamespace(language=SimpleNamespace(value="sk_SK")))
    runtime = {"config": config, "gettext": gettext, "os": os, "__file__": str(PLUGIN / "weaUtils.py"),
               "language": SimpleNamespace(getLanguage=lambda: "sk_SK")}
    exec(compile(ast.Module(body=functions, type_ignores=[]), "weather-language", "exec"), runtime)
    return runtime, config


class WeatherLanguageTest(unittest.TestCase):
    def test_slovak_open_meteo_conditions_from_compiled_catalogue(self):
        runtime, config = isolated_functions()
        translations = {0: "Jasná obloha", 2: "Čiastočne oblačno",
                        3: "Zamračené", 61: "Slabý dážď", 63: "Dážď"}
        for code, expected in translations.items():
            self.assertEqual(runtime["wmoText"](code), expected, code)
        config.osd.language.value = "en_EN"
        self.assertEqual(runtime["wmoText"](61), "Slight rain")

    def test_enhanced_weather_uses_shared_translator(self):
        source = (PLUGIN / "E_weather.py").read_text(encoding="utf-8")
        self.assertIn("WLANG, wmoText", source)
        self.assertIn("return wmoText(code)", source)
        self.assertNotIn('0: "Clear sky", 1: "Mainly clear"', source)

    def test_unknown_weather_code_falls_back(self):
        runtime, config = isolated_functions()
        config.osd.language.value = "en_EN"
        self.assertEqual(runtime["wmoText"](10000), "Unknown")


if __name__ == "__main__":
    unittest.main()
