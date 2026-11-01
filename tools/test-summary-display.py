#!/usr/bin/env python3
"""Exercise actual native summary constructors and fallback selection observers."""
import argparse
import ast
from functools import reduce
import importlib.util
from pathlib import Path
import unittest
import xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser();parser.add_argument('--upstream',required=True,type=Path)
args,rest=parser.parse_known_args()
spec=importlib.util.spec_from_file_location('summary_compat',ROOT/'source/package-root/usr/lib/enigma2/python/Plugins/Extensions/setupGlass17/warderSummaryCompat.py')
compat=importlib.util.module_from_spec(spec);spec.loader.exec_module(compat)


def native_class(path,name,scope):
    lines=(args.upstream/path).read_text().splitlines(keepends=True)
    a=next(i for i,line in enumerate(lines) if line.startswith('class '+name+'(') or line.startswith('class '+name+':'))
    b=next((i for i in range(a+1,len(lines)) if lines[i].startswith(('class ','def '))),len(lines))
    env=dict(scope);exec(compile(''.join(lines[a:b]),str(args.upstream/path),'exec'),env);return env[name]
class CList(list):
    def changed(self,*args):
        for obj in self:obj.changed(*args)
class BackendScreen(dict):
    def __init__(self,session,parent=None):
        super().__init__();self.parent=parent;self.onShow=[];self.onHide=[];self.onClose=[]
class Parent(dict):
    skinName='Setup'
    def __init__(self):
        self.onChangedEntry=[];self.onConfigEntryChanged=[];self.entry='Jas';self.value='50'
        self['config']=type('Config',(),{'onSelectionChanged':[]})()
    def getTitle(self):return 'Nastavenie obrazu'
    def getCurrentEntry(self):return self.entry
    def getCurrentValue(self):return self.value


def classes():
    element=native_class('Components/Element.py','Element',{'CList':CList,'reduce':reduce})
    source=native_class('Components/Sources/Source.py','Source',{'Element':element})
    text=native_class('Components/Sources/StaticText.py','StaticText',{'Source':source})
    screen=native_class('Screens/Screen.py','ScreenSummary',{'Screen':BackendScreen,'StaticText':text})
    setup=native_class('Screens/Setup.py','SetupSummary',{'ScreenSummary':screen,'StaticText':text})
    return screen,setup,text


class SummaryTests(unittest.TestCase):
    def test_original_fallback_lacks_reported_fields(self):
        screen,setup,text=classes();summary=screen(None,Parent())
        self.assertIn('SetupSummary',summary.skinName)
        self.assertNotIn('entry',summary);self.assertNotIn('value',summary)
    def test_corrected_fallback_has_native_sources_and_live_values(self):
        screen,setup,text=classes();compat.install(screen,lambda:True,text);parent=Parent();summary=screen(None,parent)
        for key in ('entry','value','SetupTitle','SetupEntry','SetupValue'):
            self.assertIsInstance(summary[key],text)
        self.assertEqual(summary['entry'].text,'Jas');self.assertEqual(summary['value'].text,'50')
        for callback in summary.onShow:callback()
        parent.entry,parent.value='Kontrast','75'
        for callback in parent['config'].onSelectionChanged:callback()
        self.assertEqual(summary['entry'].text,'Kontrast');self.assertEqual(summary['SetupValue'].text,'75')
    def test_show_hide_close_removes_watchers_without_duplicates(self):
        screen,setup,text=classes();compat.install(screen,lambda:True,text);parent=Parent();summary=screen(None,parent)
        for unused in range(3):
            for callback in summary.onShow:callback();callback()
            self.assertEqual(len(parent.onChangedEntry),1)
            self.assertEqual(len(parent['config'].onSelectionChanged),1)
            for callback in summary.onHide:callback()
            self.assertEqual(parent.onChangedEntry,[]);self.assertEqual(parent['config'].onSelectionChanged,[])
        for callback in summary.onShow:callback()
        for callback in summary.onClose:callback()
        self.assertEqual(parent.onConfigEntryChanged,[])
    def test_real_setup_summary_keeps_native_watchers(self):
        screen,setup,text=classes();compat.install(screen,lambda:True,text);parent=Parent();summary=setup(None,parent)
        self.assertEqual(len(summary.onShow),1)
        self.assertEqual(summary.onShow[0].__func__,setup.addWatcher)
        for callback in summary.onShow:callback()
        self.assertEqual(summary['entry'].text,'Jas')
    def test_other_skins_and_nonsetup_summaries_are_untouched(self):
        screen,setup,text=classes();compat.install(screen,lambda:False,text)
        self.assertNotIn('entry',screen(None,Parent()))
        screen,setup,text=classes();compat.install(screen,lambda:True,text);parent=Parent();parent.skinName='Menu'
        self.assertNotIn('entry',screen(None,parent))
    def test_legacy_templates_bind_static_sources_on_both_display_ids(self):
        screen,setup,text=classes();summary=setup(None,Parent())
        skin=ET.parse(ROOT/'source/package-root/usr/share/enigma2/hd_glass17/skin.xml')
        for node in skin.findall("screen[@name='SetupSummary']"):
            for widget in node.findall('widget'):
                key=widget.get('source');self.assertIn(key,summary)
                self.assertIsInstance(summary[key],text)
                self.assertEqual(widget.get('render'),'Label')
    def test_config_fallback_uses_formatted_masked_text(self):
        screen,setup,text=classes();compat.install(screen,lambda:True,text);parent=Parent()
        parent.getCurrentEntry=None;parent.getCurrentValue=None
        parent['config'].getCurrent=lambda:('PIN',type('Masked',(),{'getText':lambda self:'****'})())
        summary=screen(None,parent);self.assertEqual(summary['entry'].text,'PIN');self.assertEqual(summary['value'].text,'****')
    def test_repeated_install_is_idempotent(self):
        screen,setup,text=classes();self.assertTrue(compat.install(screen,lambda:True,text))
        self.assertFalse(compat.install(screen,lambda:True,text))


if __name__=='__main__':unittest.main(argv=[__file__]+rest)
