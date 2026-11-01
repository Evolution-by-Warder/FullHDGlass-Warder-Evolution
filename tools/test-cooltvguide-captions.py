#!/usr/bin/env python3
"""Replay the event painter extracted from the supplied CoolTVGuide IPK."""
import ast
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
from types import SimpleNamespace, MethodType
import unittest

ROOT=Path(__file__).resolve().parents[1]
PLUGIN=ROOT/'source/package-root/usr/lib/enigma2/python/Plugins/Extensions/setupGlass17'
spec=importlib.util.spec_from_file_location('cool_text',PLUGIN/'warderCoolText.py')
module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
TEXT,WRAP,ELLIPSIS=0,64,128


class GUI:
    def __init__(self):pass
    def applySkin(self,desktop,parent):return True
class HTML:pass
class Content:
    def setBuildFunc(self,callback):self.callback=callback


def text_entry(pos,size,font=0,flags=0,text='',**kwargs):
    return (TEXT,*pos,*size,font,flags,text,tuple(sorted(kwargs.items())))
def pixmap_entry(pos,size,**kwargs):return (1,*pos,*size,tuple(sorted(kwargs.items())))


def create(height=60,center=True,style='No'):
    namespace={'__name__':'Plugins.Extensions.CoolTVGuide.plugin','HTMLComponent':HTML,'GUIComponent':GUI,
        'eListboxPythonMultiContent':Content,'time':lambda:100000,
        'eServiceCenter':SimpleNamespace(getInstance=lambda:None),
        'eEPGCache':SimpleNamespace(getInstance=lambda:None),'ePicLoad':lambda:None,
        'MultiContentEntryText':text_entry,'MultiContentEntryPixmapAlphaTest':pixmap_entry,
        'MultiContentEntryPixmapAlphaBlend':pixmap_entry,'loadPNG':lambda path:path,
        'RT_HALIGN_LEFT':0,'RT_HALIGN_CENTER':2,'RT_VALIGN_CENTER':8,'RT_WRAP':WRAP,
        'config':SimpleNamespace(CTVG=SimpleNamespace(**{
            'C29':SimpleNamespace(value=style),'C37':SimpleNamespace(value=False),'C38':SimpleNamespace(value=False),
            'C44':SimpleNamespace(value=240),'C56':SimpleNamespace(value=center)}))}
    path=ROOT/'design/cooltvguide/reviewed-painter.py'
    exec(compile(path.read_text(),str(path),'exec'),namespace)
    component=namespace['fAzez'](DTkMZWjfksusYP=SimpleNamespace(timer_list=[],processed_timers=[]))
    component.Qqfnb=height
    component.HIUKuTtncR=100000
    component.LeBQcwaTReuWiRb=SimpleNamespace(x=0,y=0,w=100,h=height)
    component.lYvKfeYm=SimpleNamespace(x=100,y=0,w=1600,h=height)
    for name in ('vtOhhFwtL','GmNmJ','yUmvpTyfVpboUQ','khOVCJjlEWtnj','VuJemfthhYALMi','gYwsMLhtIoZLNTn','dwkjjaLTcrvTF','zHGsNjqgOnBifL'):
        setattr(component,name,None)
    return component


class CaptionsTests(unittest.TestCase):
    def events(self):return [(1,'Informácia pre tipujúcich: (305)',100000,180),(2,'Správy\nv slovenskom jazyku',100180,900)]
    def test_original_real_painter_wraps_tall_narrow_event_cells(self):
        component=create()
        entries=component.l.callback('ref','Jednotka',self.events())
        self.assertTrue(any(isinstance(entry,tuple) and entry[0]==TEXT and entry[6]&WRAP for entry in entries if entry))
    def test_adapted_real_painter_uses_complete_single_line_and_ellipsis(self):
        for center in (False,True):
            for style in ('No','Standard','SkinDesign'):
                with self.subTest(center=center,style=style):
                    component=create(center=center,style=style);events=self.events();before=copy.deepcopy(events)
                    original=component.l.callback('ref','Jednotka',events)
                    self.assertTrue(module.adapt(component,lambda:True,TEXT,WRAP,ELLIPSIS))
                    self.assertIsInstance(component.l.callback,MethodType)
                    repaired=component.l.callback('ref','Jednotka',events)
                    self.assertEqual(len(original),len(repaired))
                    for old,new in zip(original,repaired):
                        if old and old[0]==TEXT and old[6]&WRAP:
                            self.assertEqual(old[:6],new[:6]);self.assertEqual(old[8:],new[8:])
                            self.assertFalse(new[6]&WRAP);self.assertTrue(new[6]&ELLIPSIS)
                            self.assertNotIn('\n',new[7])
                        else:self.assertEqual(old,new)
                    self.assertEqual(events,before)
    def test_tiny_guide_existing_single_line_is_unchanged(self):
        component=create(height=30);events=self.events();before=component.l.callback('ref','Jednotka',events)
        module.adapt(component,lambda:True,TEXT,WRAP,ELLIPSIS)
        self.assertEqual(before,component.l.callback('ref','Jednotka',events))
    def test_other_skins_and_unrelated_components_are_unchanged(self):
        component=create();self.assertFalse(module.adapt(component,lambda:False,TEXT,WRAP,ELLIPSIS))
        self.assertFalse(module.adapt(SimpleNamespace(),lambda:True,TEXT,WRAP,ELLIPSIS))
    def test_reapply_is_idempotent_and_switching_skin_restores_original_flags(self):
        active=[True];component=create();module.adapt(component,lambda:active[0],TEXT,WRAP,ELLIPSIS)
        callback=component.l.callback
        self.assertFalse(module.adapt(component,lambda:active[0],TEXT,WRAP,ELLIPSIS))
        self.assertIs(callback,component.l.callback)
        active[0]=False
        self.assertTrue(any(x and x[0]==TEXT and x[6]&WRAP for x in callback('ref','Jednotka',self.events())))
    def test_reviewed_fixture_matches_recorded_upload_extraction(self):
        record=json.loads((ROOT/'design/cooltvguide/source.json').read_text())
        self.assertEqual(hashlib.sha256((ROOT/'design/cooltvguide/reviewed-painter.py').read_bytes()).hexdigest(),record['fixture_sha256'])
        self.assertEqual(record['package_sha256'],'ddd85ffeffdf74a2824d8395edd403aa2116747f4dff7db5a459f74990bb7379')
    def test_actual_plugin_hook_is_scoped_to_fullhdglass(self):
        tree=ast.parse((PLUGIN/'plugin.py').read_text())
        block=next(n for n in tree.body if isinstance(n,ast.Try) and any(isinstance(x,ast.ImportFrom) and x.module=='warderCoolText' for x in n.body))
        self.assertIn("config.skin.primary_skin.value == 'hd_glass17/skin.xml'",ast.unparse(block))


if __name__=='__main__':unittest.main()
