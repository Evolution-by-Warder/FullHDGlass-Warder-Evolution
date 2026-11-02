#!/usr/bin/env python3
"""Check owned resolution helpers, colors and Python geometry without hardware."""
import ast
import importlib.util
from pathlib import Path
import sys
from types import ModuleType, SimpleNamespace
import unittest
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[1]
RUNTIME=ROOT/'source/package-root/usr/lib/enigma2/python/Plugins/Extensions/setupGlass17'
DESKTOP=[1920,1080]
class Size:
    def __init__(self,w,h):self.w,self.h=w,h
    def width(self):return self.w
    def height(self):return self.h
class Listbox:
    orVertical=1
    def __init__(self):self.dim=Size(2080,820);self.row=60
    def size(self):return self.dim
    def resize(self,size):self.dim=size
    def getOrientation(self):return 1
    def getItemHeight(self):return self.row
class Pixmap:
    def setScale(self,value):self.scaled=value
class NativeScreen(dict):
    def __init__(self,*args,**kwargs):dict.__init__(self)
    def applySkin(self):return 'native-result'
    def show(self):return 'shown'

def builder(*args,**kwargs):return (args,kwargs)
pkg=ModuleType('isolated_fullhdglass');pkg.__path__=[str(RUNTIME)]
screen=ModuleType('Screens.Screen');screen.Screen=NativeScreen
engine=ModuleType('enigma');engine.eListbox=Listbox;engine.ePixmap=Pixmap;engine.ePoint=lambda *v:v;engine.eSize=Size;engine.gFont=lambda *v:v;engine.BT_SCALE=1
engine.getDesktop=lambda index:SimpleNamespace(size=lambda:Size(*DESKTOP))
content=ModuleType('Components.MultiContent')
for name in ('MultiContentEntryText','MultiContentEntryPixmap','MultiContentEntryPixmapAlphaTest','MultiContentEntryPixmapAlphaBlend'):setattr(content,name,builder)
components=ModuleType('Components');components.MultiContent=content
with patch.dict(sys.modules,{'isolated_fullhdglass':pkg,'Screens.Screen':screen,'enigma':engine,'Components':components,'Components.MultiContent':content}):
    spec=importlib.util.spec_from_file_location('isolated_fullhdglass.warderResolution',RUNTIME/'warderResolution.py')
    ui=importlib.util.module_from_spec(spec);spec.loader.exec_module(ui)

class ResolutionTests(unittest.TestCase):
    def tearDown(self):DESKTOP[:]=[1920,1080]
    def test_fhd_geometry_fonts_and_entries_keep_the_original_values(self):
        self.assertEqual(ui.ePoint(579,592),(579,592));self.assertEqual(ui.gFont('Prive3',30),('Prive3',30))
        data=dict(pos=(40,2),size=(960,38),font=2,text='Žltý text',color=0xffcc00)
        self.assertEqual(ui.MultiContentEntryText(**data),builder(**data))
    def test_hd_wqhd_uhd_scale_python_geometry_once_and_keep_colors(self):
        for width,height in ((1280,720),(2560,1440),(3840,2160)):
            DESKTOP[:]=[width,height];sx,sy=width/1920,height/1080
            self.assertEqual(ui.ePoint(579,592),(round(579*sx),round(592*sy)))
            self.assertEqual(ui.gFont('Regular',30),('Regular',round(30*sy)))
            args,data=ui.MultiContentEntryText(pos=(40,2),size=(960,38),font=2,text='Žltý text',color=0xffcc00)
            self.assertEqual(data['size'],(round(960*sx),round(38*sy)));self.assertEqual(data['color'],0xffcc00)
            self.assertEqual(data['text'],'Žltý text');self.assertEqual(data['font'],2)
    def test_native_reference_is_added_to_static_partial_and_later_generated_skins(self):
        for value in ('<screen size="1920,1080"></screen>','<screen size="1920,1080">'):
            self.assertIn('resolution="1920,1080"',ui.reference_skin(value))
            self.assertEqual(ui.reference_skin(ui.reference_skin(value)),ui.reference_skin(value))
        class Owned(ui.Screen):skin='<screen size="1920,1080"/>'
        owned=Owned();self.assertIn('resolution="1920,1080"',owned.skin)
        owned.skin='<screen size="1200,770"/>';self.assertIn('resolution="1920,1080"',owned.skin)
    def test_display_and_explicit_reference_are_not_rewritten(self):
        for value in ('<screen id="1" size="132,64"/>','<screen resolution="1280,720"/>'):
            self.assertEqual(ui.reference_skin(value),value)
    def test_pixmaps_scale_to_their_boxes_without_changing_alpha_or_colors(self):
        DESKTOP[:]=[2560,1440]
        _,data=ui.MultiContentEntryPixmapAlphaBlend(pos=(8,8),size=(72,72),png='same-image',flags=8,backcolor=0xff000000)
        self.assertEqual(data['size'],(96,96));self.assertEqual(data['png'],'same-image')
        self.assertEqual(data['flags'],9);self.assertEqual(data['backcolor'],0xff000000)
    def test_fit_preserves_allocation_and_repeated_show_is_stable(self):
        DESKTOP[:]=[2560,1440];owned=ui.Screen();c=SimpleNamespace(instance=Listbox(),skinAttributes=[]);owned['list']=c
        for unused in range(4):self.assertEqual(owned.show(),'shown')
        self.assertEqual(c.instance.size().height(),780)
        c.instance.row=80;owned.show();self.assertEqual(c.instance.size().height(),800)
    def test_native_coordinate_readback_is_converted_back_to_reference_once(self):
        DESKTOP[:]=[2560,1440]
        for value,axis in ((579,0),(592,1)):
            physical=ui.pixel(value,axis)
            self.assertEqual(ui.logical(physical,axis),value)
        for filename in ('plugin.py','screenSaver.py'):
            tree=ast.parse((RUNTIME/filename).read_text())
            imported={alias.asname or alias.name for node in ast.walk(tree) if isinstance(node,ast.ImportFrom) and node.module=='warderResolution' for alias in node.names}
            self.assertIn('logical',imported)

    def test_config_font_installation_uses_the_native_font_factory_once(self):
        self.assertIs(ui.gFont._warder_native_font,engine.gFont)
        DESKTOP[:]=[2560,1440]
        self.assertEqual(ui.gFont._warder_native_font('Regular',34),('Regular',34))

    def test_all_owned_python_sources_compile(self):
        for path in RUNTIME.rglob('*.py'):compile(path.read_text(),str(path),'exec')

if __name__=='__main__':unittest.main()
