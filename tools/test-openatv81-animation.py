#!/usr/bin/env python3
"""Replay the real 8.1 Renderer/Element/Screen classes with native widgets stubbed."""
import argparse
import ast
from functools import reduce
import json
from pathlib import Path
import unittest
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser()
parser.add_argument('--upstream', required=True, type=Path)
args, rest = parser.parse_known_args()
UPSTREAM = args.upstream

class CList(list):
    def changed(self, *args):
        for item in self:
            item.changed(*args)

class Widget:
    def __init__(self, parent=None):
        self.text = ''; self.animation = None
    def setText(self, value): self.text = value
    def setDefaultAnimationEnabled(self, value): self.animation = value
    def show(self): pass
    def hide(self): pass

def native_class(path, name, scope):
    node = next(n for n in ast.parse((UPSTREAM/path).read_text()).body if isinstance(n, ast.ClassDef) and n.name == name)
    env = dict(scope)
    exec(compile(ast.Module(body=[node], type_ignores=[]), str(UPSTREAM/path), 'exec'), env)
    return env[name]

Element = native_class('Components/Element.py', 'Element', {'CList':CList, 'reduce':reduce})
GUIComponent = native_class('Components/GUIComponent.py', 'GUIComponent', {})
VariableText = native_class('Components/VariableText.py', 'VariableText', {})
Source = native_class('Components/Sources/Source.py', 'Source', {'Element':Element})
StaticText = native_class('Components/Sources/StaticText.py', 'StaticText', {'Source':Source})
Label = native_class('Components/Label.py', 'Label', {'GUIComponent':GUIComponent, 'VariableText':VariableText, 'eLabel':Widget})
Renderer = native_class('Components/Renderer/Renderer.py', 'Renderer', {'GUIComponent':GUIComponent, 'Element':Element})
RenderLabel = native_class('Components/Renderer/Label.py', 'Label', {'Renderer':Renderer, 'VariableText':VariableText, 'eLabel':Widget})
ScreenNode = next(n for n in ast.parse((UPSTREAM/'Screens/Screen.py').read_text()).body if isinstance(n,ast.ClassDef) and n.name == 'Screen')
scope = {'GUIComponent':GUIComponent,'Source':Source,'eStack':Widget}
exec(compile(ast.Module(body=[n for n in ScreenNode.body if isinstance(n,ast.FunctionDef) and n.name in ('show','hide')],type_ignores=[]),'native-Screen-visibility','exec'),scope)
record = json.loads((ROOT/'design/openatv81-compatibility/skin-edits.json').read_text())['edits'][0]

class Screen(dict):
    show = scope['show']; hide = scope['hide']
    def __init__(self, xml):
        self.instance=Widget();self.shown=False;self.alreadyShown=False;self.onShow=[];self.onHide=[];self.renderer=[];self.stacks=[]
        video = ast.parse((UPSTREAM/'Plugins/SystemPlugins/VideoEnhancement/plugin.py').read_text())
        cls = next(n for n in video.body if isinstance(n,ast.ClassDef) and n.name == 'VideoEnhancementSetup')
        init = next(n for n in cls.body if isinstance(n,ast.FunctionDef) and n.name == '__init__')
        fields = [n for n in init.body if isinstance(n,ast.Assign) and isinstance(n.value,ast.Call) and isinstance(n.value.func,ast.Name) and n.value.func.id in ('Label','StaticText') and any(isinstance(t,ast.Subscript) for t in n.targets)]
        exec(compile(ast.Module(body=fields,type_ignores=[]),'native-VideoEnhancement-fields','exec'),{'self':self,'Label':Label,'StaticText':StaticText,'_':lambda text:text})
        for item in self.values():
            if isinstance(item,GUIComponent):item.GUIcreate(None)
        for widget in ET.fromstring(xml).findall('widget'):
            key=widget.get('source')
            if key in self:
                self.assert_source(key,widget)
    def assert_source(self,key,widget):
        assert widget.get('render')=='Label'
        render=RenderLabel();render.connect(self[key]);render.GUIcreate(None);self.renderer.append(render)

class AnimationTests(unittest.TestCase):
    def test_original_binding_reproduces_exact_crash_on_native_screen_show(self):
        screen=Screen(record['original_screen'])
        with self.assertRaisesRegex(AttributeError,"'Label' object has no attribute 'isAnimated'"):
            screen.show()
    def test_repaired_binding_opens_hides_and_reopens(self):
        screen=Screen(record['updated_screen'])
        screen.show();screen.hide();screen.show()
        self.assertTrue(screen.shown)
    def test_description_changes_update_the_visible_native_widget(self):
        screen=Screen(record['updated_screen']);screen.show()
        for text in ('Kontrast','Jas','Ostrosť obrazu'):
            screen['description'].setText(text)
            self.assertEqual(screen['description'].instance.text,text)
        self.assertFalse(hasattr(screen['description'],'isAnimated'))
    def test_real_sources_keep_the_native_animation_policy(self):
        screen=Screen(record['updated_screen']);screen.show()
        source=screen['key_green'];render=next(r for r in screen.renderer if r.source is source)
        self.assertTrue(render.instance.animation)
        source.isAnimated=False
        self.assertFalse(render.instance.animation)
        source.setText('Uložiť');self.assertEqual(render.instance.text,'Uložiť')
    def test_only_binding_changes_and_geometry_is_preserved(self):
        old=ET.fromstring(record['original_screen']);new=ET.fromstring(record['updated_screen'])
        before=old.find("widget[@source='description']");after=new.find("widget[@name='description']")
        self.assertIsNotNone(before);self.assertIsNotNone(after)
        expected=dict(before.attrib);del expected['source'];del expected['render'];expected['name']='description'
        self.assertEqual(after.attrib,expected)
        skin=(ROOT/'source/package-root/usr/share/enigma2/hd_glass17/skin.xml').read_text()
        self.assertEqual(skin.count(record['updated_screen']),1)
    def test_real_controller_declares_description_as_label(self):
        screen=Screen(record['updated_screen'])
        self.assertIsInstance(screen['description'],Label)
        self.assertIsInstance(screen['introduction'],StaticText)

if __name__=='__main__':unittest.main(argv=[__file__]+rest)
