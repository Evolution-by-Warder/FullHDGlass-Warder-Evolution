"""Exercise the 13-layout Prime Time EPG converter gate with Enigma2 stubs."""
import importlib.util
import sys
import types
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "source/package-root/usr/lib/enigma2/python/Components/Converter/WarderPrimeTimeGate.py"

class Converter:
    def __init__(self, type):
        self.type = type

def cached(method):
    return method

def install(name, **attrs):
    mod = types.ModuleType(name)
    mod.__dict__.update(attrs)
    sys.modules[name] = mod

enabled = types.SimpleNamespace(value=False)
config = types.SimpleNamespace(plugins=types.SimpleNamespace(
    warderEvolutionPrimeTime=types.SimpleNamespace(enabled=enabled)))
install("Components")
install("Components.Converter")
install("Components.Converter.Converter", Converter=Converter)
install("Components.Element", cached=cached)
install("Components.config", config=config)
spec = importlib.util.spec_from_file_location("warder_gate_under_test", SOURCE)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

class GateTests(unittest.TestCase):
    def setUp(self):
        enabled.value = False
        self.gate = module.WarderPrimeTimeGate("HideWhenEnabled")
        self.gate.source = types.SimpleNamespace(text="Original EPG programme")

    def test_disabled_retains_original_epg_text(self):
        self.assertEqual(self.gate.text, "Original EPG programme")

    def test_enabled_suppresses_original_and_restores_after_disable(self):
        enabled.value = True
        self.assertEqual(self.gate.text, "")
        enabled.value = False
        self.assertEqual(self.gate.text, "Original EPG programme")

    def test_empty_epg_never_becomes_none(self):
        self.gate.source.text = None
        self.assertEqual(self.gate.text, "")
        enabled.value = True
        self.assertEqual(self.gate.text, "")

    def test_missing_optional_config_retains_original(self):
        original = config.plugins.warderEvolutionPrimeTime
        del config.plugins.warderEvolutionPrimeTime
        try:
            self.assertEqual(self.gate.text, "Original EPG programme")
        finally:
            config.plugins.warderEvolutionPrimeTime = original

if __name__ == "__main__":
    unittest.main()
