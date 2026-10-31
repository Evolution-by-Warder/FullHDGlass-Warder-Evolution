#!/usr/bin/env python3
"""Reproduce the reported source-type crash using the matching upstream code."""
import ast
import json
from pathlib import Path
import sys
from types import SimpleNamespace
import unittest
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
DATA = json.loads((ROOT/'tools/fixtures/openatv-numberzap-aaa789a.json').read_text())['files']


class Source:
    CHANGED_ALL, CHANGED_CLEAR, CHANGED_SPECIFIC = 1, 2, 3

    def __init__(self, *args):
        self.connections = []

    def changed(self, what):
        for callback in self.connections:
            callback(what)


class Reference:
    def __init__(self, text):
        self.value = text

    def toString(self):
        return self.value


def upstream_class(path, name, scope):
    node = next(n for n in ast.parse(DATA[path]['source']).body
                if isinstance(n, ast.ClassDef) and n.name == name)
    exec(compile(ast.Module(body=[node], type_ignores=[]), path, 'exec'), scope)
    return scope[name]


def upstream_method(path, cls, method, scope):
    owner = next(n for n in ast.parse(DATA[path]['source']).body
                 if isinstance(n, ast.ClassDef) and n.name == cls)
    node = next(n for n in owner.body if isinstance(n, ast.FunctionDef) and n.name == method)
    exec(compile(ast.Module(body=[node], type_ignores=[]), path, 'exec'), scope)
    return scope[method]


class NumberZapPiconTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if sys.version_info < (3, 10):
            raise unittest.SkipTest('Matching upstream renderer uses Python match syntax; compatibility CI runs Python 3.14')

    def setUp(self):
        self.scope = {
            'Source': Source, 'Converter': Source, 'cached': lambda fn: fn,
            'eServiceReference': Reference, 'iPlayableServicePtr': type('Playable', (), {}),
            'eServiceCenter': SimpleNamespace(getInstance=lambda: SimpleNamespace(info=lambda ref: object())),
            'eEPGCache': SimpleNamespace(getInstance=lambda: SimpleNamespace(lookupEventTime=lambda *a: None)),
            'resolveAlternate': lambda ref: None,
            'iPlayableService': SimpleNamespace(evStart=1, evUpdatedInfo=2),
            'getDABImage': lambda ref: '', 'getPiconName': lambda ref, mode: '/picons/'+ref+'.png',
            'exists': lambda path: bool(path), 'getmtime': lambda path: 123,
            'getsize': lambda path: 456,
            'config': SimpleNamespace(usage=SimpleNamespace(showpicon=SimpleNamespace(value=True))),
        }
        self.event = upstream_class('lib/python/Components/Sources/ServiceEvent.py', 'ServiceEvent', self.scope)()
        self.converter_class = upstream_class('lib/python/Components/Converter/ServiceName.py', 'ServiceName', self.scope)
        changed = upstream_method('lib/python/Components/Renderer/Picon.py', 'Picon', 'changed', self.scope)
        self.show_picon = upstream_method('lib/python/Screens/InfoBarGenerics.py', 'NumberZap', 'showPicon', self.scope)
        self.drawn, self.visible = [], []
        instance = SimpleNamespace(setScale=lambda value: None,
                                   setPixmapFromFile=self.drawn.append,
                                   show=lambda: self.visible.append(True), hide=lambda: self.visible.append(False))
        self.renderer = SimpleNamespace(instance=instance, mode=None, pngname='',
                                        defaultpngname='/default.png', nopicon='/default.png')
        self.render = lambda what: changed(self.renderer, what)
        self.zap = type('Zap', (dict,), {})({'Service': self.event})

    def test_unconverted_actual_source_reproduces_the_reported_exception(self):
        self.renderer.source = self.event
        self.event.connections.append(self.render)
        self.zap.service = Reference('1:0:1:TEST_A:0:0:0:0:0:0:')
        with self.assertRaisesRegex(AttributeError, "has no attribute 'text'"):
            self.show_picon(self.zap)

    def connect_reference_converter(self):
        converter = self.converter_class('Reference')
        converter.source = self.event
        self.event.connections.append(converter.changed)
        converter.connections.append(self.render)
        self.renderer.source = converter

    def test_reference_converter_draws_selected_service_and_updates_after_next_digit(self):
        self.connect_reference_converter()
        for ref in ('1:0:1:TEST_A:0:0:0:0:0:0:', '1:0:1:TEST_B:0:0:0:0:0:0:'):
            self.zap.service = Reference(ref)
            self.show_picon(self.zap)
            self.assertEqual(self.drawn[-1], '/picons/'+ref+'.png')
        self.assertEqual(len(self.drawn), 2)
        self.zap.service = None
        self.show_picon(self.zap)
        self.assertFalse(self.visible[-1])

    def test_missing_icon_keeps_native_default_behavior(self):
        self.connect_reference_converter()
        self.scope['getPiconName'] = lambda ref, mode: ''
        self.zap.service = Reference('1:0:1:MISSING:0:0:0:0:0:0:')
        self.show_picon(self.zap)
        self.assertEqual(self.drawn[-1], '/default.png')

    def test_all_native_service_picon_widgets_supply_a_text_reference(self):
        skin = ET.fromstring((ROOT/'source/package-root/usr/share/enigma2/hd_glass17/skin.xml').read_text())
        widgets = skin.findall("screen/widget[@render='Picon'][@source='Service']")
        self.assertTrue(widgets)
        for widget in widgets:
            converter = widget.find("convert[@type='ServiceName']")
            self.assertIsNotNone(converter)
            self.assertEqual(converter.text.strip(), 'Reference')


if __name__ == '__main__':
    unittest.main()
