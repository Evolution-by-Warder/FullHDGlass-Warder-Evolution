#!/usr/bin/env python3
"""Exercise inherited/explicit plugin fonts through the shared applySkin path."""
import importlib.util
from pathlib import Path
from types import SimpleNamespace
import unittest

ROOT=Path(__file__).resolve().parents[1]
PATH=ROOT/'source/package-root/usr/lib/enigma2/python/Plugins/Extensions/setupGlass17/warderConfigFonts.py'
spec=importlib.util.spec_from_file_location('config_font_compat',PATH)
module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)

class Font:
    def __init__(self,family,size): self.family=family;self.pointSize=size

def parse_font(value,scale):
    family,size=value.split(';')
    return Font(family,int(size)*scale[1][0]//scale[1][1])

class Widget:
    def __init__(self,height=25): self.height=height;self.fonts={};self.calls=[]
    def getItemHeight(self): return self.height
    def setEntryFont(self,font): self.fonts['entry']=font;self.calls.append(('entry',font.pointSize))
    def setValueFont(self,font): self.fonts['value']=font;self.calls.append(('value',font.pointSize))

class FontTests(unittest.TestCase):
    def create(self,height=25,attributes=(),active=True,scale=((1,1),(1,1))):
        class ConfigList:
            def __init__(self):
                self.instance=Widget(height);self.skinAttributes=list(attributes);self.original_calls=0
                self.values=['unchanged',32,True]
            def applySkin(self,desktop,parent):
                self.original_calls+=1
                for name,text in self.skinAttributes:
                    role='entry' if name in ('font','entryFont') else 'value' if name in ('valueFont','secondFont','secondfont') else None
                    if role:self.instance.fonts[role]=parse_font(text,parent.scale)
                return 'original-result'
        self.assertTrue(module.install(ConfigList,lambda:active,Font,parse_font))
        return ConfigList(),SimpleNamespace(scale=scale),ConfigList
    def apply(self,widget,parent): return widget.applySkin(None,parent)
    def test_lcd4linux_and_cacheflush_default_25px_rows_fit(self):
        for name,width in [('LCDdisplayConfig',910),('CacheFlushSetupMenu',480),('UnlistedFuturePlugin',620)]:
            with self.subTest(plugin=name,width=width):
                obj,parent,_=self.create(attributes=[('size',str(width)+',200')]);before=list(obj.values)
                self.assertEqual(self.apply(obj,parent),'original-result')
                self.assertEqual({k:f.pointSize for k,f in obj.instance.fonts.items()},{'entry':20,'value':18})
                self.assertEqual(obj.values,before);self.assertEqual(obj.original_calls,1)
    def test_existing_fhd_40_and_45px_rows_keep_their_fonts(self):
        for height in (40,45,50):
            obj,parent,_=self.create(height=height,attributes=[('font','Prive3;33')]);self.apply(obj,parent)
            self.assertEqual(obj.instance.fonts['entry'].pointSize,33)
            self.assertEqual(obj.instance.calls,[])
    def test_explicit_small_fonts_and_families_are_preserved(self):
        obj,parent,_=self.create(attributes=[('entryFont','Regular;18'),('valueFont','Custom;16')]);self.apply(obj,parent)
        self.assertEqual(obj.instance.calls,[]);self.assertEqual(obj.instance.fonts['value'].family,'Custom')
    def test_oversized_explicit_fonts_are_fitted_without_resizing_rows(self):
        obj,parent,_=self.create(attributes=[('entryFont','Custom;48'),('valueFont','Regular;40')]);self.apply(obj,parent)
        self.assertEqual(obj.instance.height,25);self.assertEqual(obj.instance.fonts['entry'].family,'Custom')
        self.assertEqual(obj.instance.fonts['entry'].pointSize,20)
    def test_legacy_value_font_aliases_are_respected(self):
        for name in ('secondFont','secondfont'):
            obj,parent,_=self.create(attributes=[(name,'Regular;15')]);self.apply(obj,parent)
            self.assertEqual(obj.instance.fonts['value'].pointSize,15)
    def test_scaled_native_font_sizes_are_compared_with_actual_pixel_rows(self):
        obj,parent,_=self.create(height=37,attributes=[('font','Regular;20')],scale=((3,2),(3,2)));self.apply(obj,parent)
        self.assertEqual(obj.instance.fonts['entry'].pointSize,30)
    def test_other_skins_are_delegated_without_font_changes(self):
        obj,parent,_=self.create(active=False);self.apply(obj,parent)
        self.assertEqual(obj.instance.calls,[]);self.assertEqual(obj.original_calls,1)
    def test_repeated_install_does_not_stack_wrappers(self):
        obj,parent,cls=self.create();self.assertFalse(module.install(cls,lambda:True,Font,parse_font))
        self.apply(obj,parent);self.assertEqual(obj.original_calls,1)
    def test_reskin_to_taller_rows_restores_previous_inherited_fonts(self):
        obj,parent,_=self.create();self.apply(obj,parent);obj.instance.height=45;self.apply(obj,parent)
        self.assertEqual({k:f.pointSize for k,f in obj.instance.fonts.items()},{'entry':33,'value':30})
    def test_missing_optional_native_apis_do_not_break_apply_skin(self):
        obj,parent,_=self.create();obj.instance=SimpleNamespace();self.assertEqual(self.apply(obj,parent),'original-result')
    def test_local_subclass_uses_the_same_policy(self):
        obj,parent,cls=self.create()
        class PluginSpecificConfigList(cls): pass
        derived=PluginSpecificConfigList();self.apply(derived,parent)
        self.assertEqual(derived.instance.fonts['entry'].pointSize,20)
    def test_skin_default_fonts_match_the_shared_policy(self):
        import xml.etree.ElementTree as ET
        skin=ET.parse(ROOT/'source/package-root/usr/share/enigma2/hd_glass17/skin.xml')
        node=skin.find("windowstyle[@id='0']/configList")
        self.assertEqual(node.get('entryFont'),module.DEFAULTS['entry']);self.assertEqual(node.get('valueFont'),module.DEFAULTS['value'])
    def test_actual_plugin_hook_installs_once_and_checks_the_active_skin(self):
        import ast,sys
        from types import ModuleType
        from unittest.mock import patch
        path=PATH.with_name('plugin.py');tree=ast.parse(path.read_text())
        block=next(n for n in tree.body if isinstance(n,ast.Try) and any(isinstance(x,ast.ImportFrom) and x.module=='warderConfigFonts' for x in n.body))
        obj,parent,cls=self.create();cls.applySkin=cls.applySkin.__wrapped__
        components=ModuleType('Components');components.__path__=[]
        configlist=ModuleType('Components.ConfigList');configlist.ConfigList=cls
        skin=ModuleType('skin');skin.parseFont=parse_font
        package=ModuleType('font_install_fixture');package.__path__=[]
        config=SimpleNamespace(skin=SimpleNamespace(primary_skin=SimpleNamespace(value='hd_glass17/skin.xml')))
        modules={'Components':components,'Components.ConfigList':configlist,'skin':skin,'font_install_fixture':package,'font_install_fixture.warderConfigFonts':module}
        env={'__package__':'font_install_fixture','config':config,'gFont':Font}
        with patch.dict(sys.modules,modules):
            for unused in range(2):exec(compile(ast.Module(body=[block],type_ignores=[]),'actual-font-hook','exec'),env)
        self.apply(obj,parent);self.assertEqual(obj.original_calls,1);self.assertEqual(obj.instance.fonts['entry'].pointSize,20)
        config.skin.primary_skin.value='MetrixHD/skin.xml';other=cls();self.apply(other,parent);self.assertEqual(other.instance.calls,[])

if __name__=='__main__':unittest.main()
