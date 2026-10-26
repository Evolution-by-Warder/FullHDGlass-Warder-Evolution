#!/usr/bin/env python3
import importlib.util
from pathlib import Path
from types import SimpleNamespace,ModuleType
import sys
import unittest
from unittest.mock import MagicMock,patch
from xml.etree import ElementTree as ET

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('glass_style',ROOT/'tools/style-setup-screens.py')
s=importlib.util.module_from_spec(spec);spec.loader.exec_module(s)


class GlassTests(unittest.TestCase):
    def layouts(self):
        for name,(_,xml) in s.extract(s.PLUGIN.read_text()).items():
            yield name,ET.fromstring(xml+('</screen>' if name=='selectIconsDisplayed' else ''))
        spec=importlib.util.spec_from_file_location('dialog_skins',s.PLUGIN.parent/'warderDialogSkins.py')
        d=importlib.util.module_from_spec(spec);spec.loader.exec_module(d)
        for name in ('MESSAGE_SKIN','CHOICE_SKIN','INPUT_SKIN'):yield name,ET.fromstring(getattr(d,name))

    def test_all_thirteen_owned_screens_have_one_glass_layer_and_clipped_banner(self):
        layouts=list(self.layouts());self.assertEqual(len(layouts),13)
        for name,root in layouts:
            self.assertEqual(root.get('backgroundColor'),s.CLEAR,name)
            self.assertFalse(root.findall("ePixmap[@pixmap='%s']"%s.BANNER_IMAGE),name)
            header=root.findall("widget[@render='WarderSettingsHeader']")
            self.assertEqual(len(header),1,name);self.assertEqual(header[0].get('size'),'1920,164')
            glass=[n for n in root if n.get('backgroundColor')==s.GLASS]
            self.assertEqual(len(glass),1,name)
            self.assertLess(int(glass[0].get('zPosition')),0,name)
            self.assertTrue(root.findall("eLabel[@backgroundColor='%s']"%s.CYAN),name)
            for node in root:
                if node.get('name') in ('config','list','text','Changelog_info'):
                    self.assertEqual(node.get('backgroundColor'),s.CLEAR,(name,node.attrib))
                    self.assertEqual(node.get('transparent'),'1')
                if node.get('backgroundColorSelected'):self.assertEqual(node.get('backgroundColorSelected'),s.SELECT)

    def test_live_menu_panels_and_picture_preview_backing_remain_opaque(self):
        layouts=dict(self.layouts());main=layouts['setupGlass17ScreenSetup']
        for key in ('warder_menu_panel_0','warder_menu_panel_5'):
            self.assertEqual(main.find("widget[@name='%s']"%key).get('backgroundColor'),s.PANEL)
        preview=layouts['selectScreenShowed']
        self.assertTrue(any(n.get('position')=='741,244' and n.get('size')=='960,540' and n.get('backgroundColor')==s.PANEL for n in preview))

    def test_pig_is_hidden_in_settings_and_restored_when_returning_to_main(self):
        scope={'eSize':lambda *x:x};exec(s.PANEL_MODE,scope)
        class Pig:
            def __init__(self):self.instance=MagicMock();self.onShow=MagicMock();self.onHide=MagicMock()
        class Screen(dict):pass
        screen=Screen();screen.renderer=[Pig()]
        for prefix,count in (('warder_menu_panel_',10),('warder_settings_panel_',5)):
            for n in range(count):screen[prefix+str(n)]=MagicMock()
        screen['help_txt']=MagicMock()
        screen.isMainMenu=False;scope['_warderSetPanelMode'](screen)
        screen.renderer[0].onHide.assert_called_once();screen.renderer[0].instance.hide.assert_called_once()
        screen.isMainMenu=True;scope['_warderSetPanelMode'](screen)
        screen.renderer[0].onShow.assert_called_once();screen.renderer[0].instance.show.assert_called_once()

    def test_screen_resume_cannot_reopen_small_tv_while_settings_are_active(self):
        class Pig:
            def __init__(self):self.instance=MagicMock();self.shows=0;self.hides=0
            def applySkin(self,desktop,parent):return True
            def onShow(self):self.shows+=1
            def onHide(self):self.hides+=1
        native=ModuleType('Components.Renderer.Pig');native.Pig=Pig
        with patch.dict(sys.modules,{'Components.Renderer.Pig':native}):
            path=ROOT/'source/package-root/usr/lib/enigma2/python/Components/Renderer/WarderSettingsPig.py'
            spec=importlib.util.spec_from_file_location('pig',path);module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
            item=module.WarderSettingsPig();parent=SimpleNamespace(isMainMenu=False)
            item.applySkin(None,parent);item.onShow();item.onShow()
            self.assertEqual(item.shows,0);self.assertEqual(item.hides,2)
            item.instance.hide.assert_called();item.instance.show.assert_not_called()
            parent.isMainMenu=True;item.onShow()
            self.assertEqual(item.shows,1);item.instance.show.assert_called_once()

    def test_header_decodes_existing_artwork_once_and_never_on_clock_ticks(self):
        class Renderer:
            def __init__(self):pass
        renderer=ModuleType('Components.Renderer.Renderer');renderer.Renderer=Renderer
        native=ModuleType('enigma');native.eWidget=object;native.eSize=lambda *x:x;native.ePixmap=MagicMock()
        with patch.dict(sys.modules,{'Components.Renderer.Renderer':renderer,'enigma':native}):
            path=ROOT/'source/package-root/usr/lib/enigma2/python/Components/Renderer/WarderSettingsHeader.py'
            spec=importlib.util.spec_from_file_location('header',path);module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
            h=module.WarderSettingsHeader();parent=object();h.postWidgetCreate(parent)
            h.changed((0,));h.changed((1,))
            native.ePixmap.assert_called_once_with(parent)
            native.ePixmap.return_value.resize.assert_called_once_with((1920,1080))
            native.ePixmap.return_value.setPixmapFromFile.assert_called_once_with(s.BANNER_IMAGE)
            h.preWidgetRemove(parent);self.assertIsNone(h.picture)


if __name__=='__main__':unittest.main()
