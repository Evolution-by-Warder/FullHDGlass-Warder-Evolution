#!/usr/bin/env python3
"""Replay native caption/pixmap sources; only C++ widgets and timers are stubbed."""
import argparse
import ast
from functools import reduce
import json
from pathlib import Path
from types import SimpleNamespace
import unittest
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser()
parser.add_argument('--upstream', required=True, type=Path)
args, rest = parser.parse_known_args()
UPSTREAM = args.upstream


def native(path, name, scope):
    tree = ast.parse((UPSTREAM / path).read_text())
    node = next(n for n in tree.body if isinstance(n, (ast.ClassDef, ast.FunctionDef)) and n.name == name)
    env = dict(scope)
    exec(compile(ast.Module(body=[node], type_ignores=[]), str(UPSTREAM / path), 'exec'), env)
    return env[name]


class Widget:
    def __init__(self, parent=None):
        self.text = ''
        self.visible = True
        self.pixmap = None
        self.animation = None
        self.clicks = []
        self.selected = SimpleNamespace(get=lambda: self.clicks)

    def setText(self, value): self.text = value
    def setPixmap(self, value): self.pixmap = value
    def setDefaultAnimationEnabled(self, value): self.animation = value
    def show(self): self.visible = True
    def hide(self): self.visible = False


class Timer:
    def __init__(self): self.callback = []
    def start(self, *args): pass
    def stop(self): pass


CList = native('Tools/CList.py', 'CList', {})
Element = native('Components/Element.py', 'Element', {'CList': CList, 'reduce': reduce})
cached = native('Components/Element.py', 'cached', {})
GUIComponent = native('Components/GUIComponent.py', 'GUIComponent', {})
VariableText = native('Components/VariableText.py', 'VariableText', {})
Source = native('Components/Sources/Source.py', 'Source', {'Element': Element})
StaticText = native('Components/Sources/StaticText.py', 'StaticText', {'Source': Source})
Boolean = native('Components/Sources/Boolean.py', 'Boolean', {'Source': Source, 'cached': cached, 'eTimer': Timer})
Label = native('Components/Label.py', 'Label', {'GUIComponent': GUIComponent, 'VariableText': VariableText, 'eLabel': Widget})
Button = native('Components/Button.py', 'Button', {'GUIComponent': GUIComponent, 'VariableText': VariableText, 'eButton': Widget})
Pixmap = native('Components/Pixmap.py', 'Pixmap', {'GUIComponent': GUIComponent, 'ePixmap': Widget})
Renderer = native('Components/Renderer/Renderer.py', 'Renderer', {'GUIComponent': GUIComponent, 'Element': Element})
RenderLabel = native('Components/Renderer/Label.py', 'Label', {'Renderer': Renderer, 'VariableText': VariableText, 'eLabel': Widget})
RenderPixmap = native('Components/Renderer/Pixmap.py', 'Pixmap', {'Renderer': Renderer, 'ePixmap': Widget})
Converter = native('Components/Converter/Converter.py', 'Converter', {'Element': Element})
ConditionalShowHide = native('Components/Converter/ConditionalShowHide.py', 'ConditionalShowHide', {'Converter': Converter, 'eTimer': Timer})
EDITS = {e['name']: e for e in json.loads((ROOT / 'design/openatv81-bindings/skin-edits.json').read_text())['edits']}


def fields(path, name):
    cls = next(n for n in ast.parse((UPSTREAM / path).read_text()).body if isinstance(n, ast.ClassDef) and n.name == name)
    init = next(n for n in cls.body if isinstance(n, ast.FunctionDef) and n.name == '__init__')
    scope = {'self': {}, '_': lambda s: s, 'Label': Label, 'StaticText': StaticText,
             'Boolean': Boolean, 'Button': Button, 'Pixmap': Pixmap}
    selected = [n for n in ast.walk(init) if isinstance(n, ast.Assign) and isinstance(n.value, ast.Call)
                and isinstance(n.value.func, ast.Name) and n.value.func.id in scope
                and any(isinstance(t, ast.Subscript) and isinstance(t.value, ast.Name) and t.value.id == 'self' for t in n.targets)]
    exec(compile(ast.Module(body=selected, type_ignores=[]), str(UPSTREAM / path), 'exec'), scope)
    return scope['self']


class BoundScreen:
    def __init__(self, xml, values):
        self.values = values
        self.renderers = {}
        self.missing = []
        for value in values.values():
            if isinstance(value, GUIComponent):
                value.GUIcreate(None)
        for widget in ET.fromstring(xml).findall('widget'):
            conditional = widget.get('conditional')
            if conditional and not any(key in values for key in conditional.split(',')):
                continue
            key = widget.get('name') or widget.get('source')
            if key not in values:
                self.missing.append(key)
                continue
            if widget.get('name'):
                values[key].skinAttributes = list(widget.attrib.items())
                continue
            source = values[key]
            for converter in widget.findall('convert'):
                assert converter.get('type') == 'ConditionalShowHide'
                instance = ConditionalShowHide(converter.text or '')
                instance.connect(source)
                source = instance
            render = {'Label': RenderLabel, 'Pixmap': RenderPixmap}[widget.get('render')]()
            render.connect(source)
            render.GUIcreate(None)
            render.instance.pixmap = widget.get('pixmap')
            self.renderers[key] = render

    def show(self):
        for component in list(self.values.values()) + list(self.renderers.values()):
            if isinstance(component, GUIComponent):
                component.onShow()

    def hide(self):
        for component in list(self.values.values()) + list(self.renderers.values()):
            if isinstance(component, GUIComponent):
                component.onHide()

    def text(self, key):
        value = self.renderers.get(key) or self.values.get(key)
        return value.instance.text if isinstance(value, GUIComponent) and value.instance is not None else None


class NativeBindingTests(unittest.TestCase):
    def picture(self, variant):
        return BoundScreen(EDITS['picshow'][variant], fields('Plugins/Extensions/PicturePlayer/ui.py', 'picshow'))

    def positioner(self, variant):
        return BoundScreen(EDITS['PositionerSetupLog'][variant], fields('Plugins/SystemPlugins/PositionerSetup/plugin.py', 'PositionerSetupLog'))

    def test_original_picture_captions_are_not_rendered_and_blue_is_absent(self):
        screen = self.picture('original_screen')
        self.assertIn('key_blue', screen.missing)
        for key in ('label', 'key_red', 'key_green', 'key_yellow'):
            self.assertIsInstance(screen.values[key], StaticText)
            self.assertIsNone(screen.text(key))

    def test_picture_captions_follow_native_sources_after_show_hide_and_reopen(self):
        screen = self.picture('updated_screen')
        self.assertNotIn('key_blue', screen.missing)
        for cycle in range(2):
            screen.show()
            for key in ('label', 'key_red', 'key_green', 'key_yellow'):
                value = '%s-%d' % (key, cycle)
                screen.values[key].setText(value)
                self.assertEqual(screen.text(key), value)
            screen.hide()

    def test_original_positioner_buttons_reproduce_animation_failure(self):
        if not hasattr(Renderer, 'updateAnimationPolicy'):
            self.skipTest('Legacy renderer has no animation policy; next/master replay covers the failure')
        screen = self.positioner('original_screen')
        with self.assertRaisesRegex(AttributeError, "Button.*isAnimated"):
            screen.show()

    def test_positioner_buttons_are_native_widgets_and_keep_live_captions(self):
        screen = self.positioner('updated_screen')
        for cycle in range(2):
            screen.show()
            for key in ('key_red', 'key_green', 'key_yellow', 'key_blue'):
                self.assertIsInstance(screen.values[key], Button)
                self.assertNotIn(key, screen.renderers)
                value = '%s-%d' % (key, cycle)
                screen.values[key].setText(value)
                self.assertEqual(screen.text(key), value)
            screen.hide()

    def test_dish_boolean_controls_the_original_pixmap(self):
        old = BoundScreen(EDITS['Dishpip']['original_screen'], fields('Screens/Dish.py', 'Dishpip'))
        self.assertIsInstance(old.values['Dishpixmap'], Boolean)
        self.assertNotIn('Dishpixmap', old.renderers)
        screen = BoundScreen(EDITS['Dishpip']['updated_screen'], fields('Screens/Dish.py', 'Dishpip'))
        screen.show()
        widget = screen.renderers['Dishpixmap'].instance
        self.assertEqual(widget.pixmap, 'hd_glass17/icons/dish.png')
        for enabled in (False, True, False, True):
            screen.values['Dishpixmap'].boolean = enabled
            self.assertEqual(widget.visible, enabled)
        screen.hide()
        screen.show()

    def test_legacy_swap_uses_live_label_widgets_and_modern_swap_keeps_setup(self):
        tree = ast.parse((UPSTREAM / 'Screens/SwapManager.py').read_text())
        cls = next(n for n in tree.body if isinstance(n, ast.ClassDef) and n.name == 'Swap')
        if any(isinstance(n, ast.Name) and n.id == 'Setup' for n in cls.bases):
            aliases = [n.value for n in ast.walk(cls) if isinstance(n, ast.Assign)
                       and any(isinstance(t, ast.Attribute) and t.attr == 'skinName' for t in n.targets)]
            self.assertIn(['SwapManagerSetup', 'Setup'], [ast.literal_eval(n) for n in aliases])
            return
        screen = BoundScreen(EDITS['Swap']['updated_screen'], fields('Screens/SwapManager.py', 'Swap'))
        screen.show()
        for key in ('key_red', 'key_green', 'key_yellow'):
            self.assertIsInstance(screen.values[key], Label)
            self.assertNotIn(key, screen.renderers)
            screen.values[key].setText(key)
            self.assertEqual(screen.text(key), key)

    def test_only_registered_bindings_change_and_all_geometry_is_preserved(self):
        skin = (ROOT / 'source/package-root/usr/share/enigma2/hd_glass17/skin.xml').read_text()
        for name, edit in EDITS.items():
            self.assertEqual(skin.count(edit['updated_screen']), 1, name)
            before, after = ET.fromstring(edit['original_screen']), ET.fromstring(edit['updated_screen'])
            self.assertEqual(before.attrib, after.attrib)
            old, new = before.findall('widget'), after.findall('widget')
            self.assertEqual(len(old), len(new))
            for a, b in zip(old, new):
                geometry = lambda w: {k: v for k, v in w.attrib.items() if k not in ('name', 'source', 'render', 'conditional')}
                self.assertEqual(geometry(a), geometry(b), name)


if __name__ == '__main__':
    unittest.main(argv=[__file__] + rest)
