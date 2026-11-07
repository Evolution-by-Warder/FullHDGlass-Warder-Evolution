"""Behavioral renderer checks using Enigma2 module stubs (no receiver required)."""
import importlib.util
import sys
import types
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "source/package-root/usr/lib/enigma2/python/Components/Renderer/WarderPrimeTime.py"


def install_stub(name, **attrs):
    module = types.ModuleType(name)
    module.__dict__.update(attrs)
    sys.modules[name] = module
    return module


class Renderer:
    CHANGED_CLEAR = 1
    CHANGED_DEFAULT = 0

    def __init__(self):
        self.instance = None


class VariableText:
    def __init__(self):
        self.text = ""


class Label:
    def __init__(self):
        self.visible = True

    def show(self):
        self.visible = True

    def hide(self):
        self.visible = False


class ServiceRef:
    isMarker = 1
    flagDirectory = 2

    def __init__(self, flags=0):
        self.flags = flags


enabled = types.SimpleNamespace(value=False)
clock = types.SimpleNamespace(value=[20, 25])
config = types.SimpleNamespace(
    plugins=types.SimpleNamespace(
        warderEvolutionPrimeTime=types.SimpleNamespace(enabled=enabled, clock=clock)
    )
)
install_stub("Components")
install_stub("Components.Renderer")
install_stub("Components.Renderer.Renderer", Renderer=Renderer)
install_stub("Components.VariableText", VariableText=VariableText)
install_stub("Components.config", config=config)
install_stub("enigma", eLabel=Label,
             eEPGCache=types.SimpleNamespace(getInstance=lambda: object()),
             eServiceReference=ServiceRef)
install_stub("Plugins")
install_stub("Plugins.Extensions")
install_stub("Plugins.Extensions.setupGlass17")
install_stub("Plugins.Extensions.setupGlass17.warderPrimeTime",
             prime_time_event=lambda *args: None)

spec = importlib.util.spec_from_file_location("WarderPrimeTime_under_test", SOURCE)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class PrimeTimeRendererTests(unittest.TestCase):
    def setUp(self):
        enabled.value = False
        clock.value = [20, 25]
        self.renderer = module.WarderPrimeTime()
        self.renderer.instance = Label()
        self.service = ServiceRef()
        self.renderer.source = types.SimpleNamespace(service=self.service)

    def test_opt_in_is_off_and_hide_on_clear(self):
        self.renderer.changed((Renderer.CHANGED_DEFAULT,))
        self.assertFalse(self.renderer.instance.visible)
        self.assertEqual(self.renderer.text, "")
        enabled.value = True
        self.renderer.changed((Renderer.CHANGED_CLEAR,))
        self.assertFalse(self.renderer.instance.visible)
        self.assertEqual(self.renderer.text, "")

    def test_service_switch_and_missing_epg(self):
        enabled.value = True
        with patch.object(module, "prime_time_event", side_effect=[
            (1, "Film A"), (1, "Film B"), None
        ]) as lookup:
            self.renderer.changed((Renderer.CHANGED_DEFAULT,))
            self.assertIn("Film A", self.renderer.text)
            self.assertTrue(self.renderer.instance.visible)
            new_service = ServiceRef()
            self.renderer.source.service = new_service
            self.renderer.changed((Renderer.CHANGED_DEFAULT,))
            self.assertIn("Film B", self.renderer.text)
            self.renderer.changed((Renderer.CHANGED_DEFAULT,))
            self.assertIn("EPG unavailable", self.renderer.text)
            self.assertEqual(lookup.call_count, 3)
            self.assertIs(lookup.call_args.args[1], new_service)

    def test_folders_markers_and_missing_source_are_hidden(self):
        enabled.value = True
        with patch.object(module, "prime_time_event") as lookup:
            for service in (None, ServiceRef(ServiceRef.isMarker),
                            ServiceRef(ServiceRef.flagDirectory)):
                self.renderer.source.service = service
                self.renderer.changed((Renderer.CHANGED_DEFAULT,))
                self.assertFalse(self.renderer.instance.visible)
                self.assertEqual(self.renderer.text, "")
            lookup.assert_not_called()

    def test_source_failure_hides_label(self):
        enabled.value = True
        self.renderer.source = object()
        self.renderer.changed((Renderer.CHANGED_DEFAULT,))
        self.assertFalse(self.renderer.instance.visible)
        self.assertEqual(self.renderer.text, "")

    def test_invalid_clock_falls_back_to_disabled(self):
        enabled.value = True
        for invalid in (["bad", 25], [24, 0], [-1, 0], [20, 60], [20]):
            clock.value = invalid
            self.renderer.changed((Renderer.CHANGED_DEFAULT,))
            self.assertFalse(self.renderer.instance.visible)
            self.assertEqual(self.renderer.text, "")



if __name__ == "__main__":
    unittest.main()
