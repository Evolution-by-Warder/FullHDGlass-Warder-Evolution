"""Reject stale TV stills even when an IPK perfectly matches its source files."""
import importlib.util
import io
import json
from pathlib import Path
import unittest
import runpy
import sys
import types
from xml.etree import ElementTree as ET
from unittest.mock import patch
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('radio_video',ROOT/'tools/build-radio-background.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)


class RadioBackgroundTests(unittest.TestCase):
    def test_actual_packaged_video_matches_the_current_scenic_master(self):
        m.verify()
    def test_different_video_scene_is_rejected(self):
        output=io.BytesIO();Image.new('RGB',(1920,1080),'black').save(output,format='PNG')
        with patch.object(m.subprocess,'check_output',return_value=output.getvalue()),self.assertRaisesRegex(ValueError,'differs'):
            m.compare(m.ASSETS/'warder-radio-background.jpg',m.ASSETS/'radio.mvi')
    def test_changed_master_requires_a_matching_rebuilt_video_record(self):
        with patch.object(m,'digest',return_value='changed'),patch.object(m,'compare') as compare,self.assertRaisesRegex(ValueError,'without rebuilding'):
            m.verify()
        compare.assert_not_called()


class InfoPanelBackgroundTests(unittest.TestCase):
    def setUp(self):
        path=ROOT/'source/package-root/usr/lib/enigma2/python/Plugins/Extensions/setupGlass17/warderRadioLayers.py'
        spec=importlib.util.spec_from_file_location('radio_layers_test',path)
        self.layers=importlib.util.module_from_spec(spec);spec.loader.exec_module(self.layers)
    def test_both_modes_keep_the_original_selected_graphic(self):
        original='<screen><ePixmap position="0,0" size="1920,1080" zPosition="-2" pixmap="/media/hdd/extraScreens17/2/infobar-ext3.png" alphatest="off" /><widget name="EPG" position="0,800" size="900,40" /></screen>'
        root=ET.fromstring(self.layers.prepare_radio_layers(original))
        tv,radio=root.findall('widget')[:2]
        self.assertEqual(tv.get('pixmap'),'/media/hdd/extraScreens17/2/infobar-ext3.png')
        self.assertEqual(radio.get('pixmap'),tv.get('pixmap'))
        self.assertEqual(tv.find('convert').get('type'),'WarderTVOnly')
        self.assertEqual(radio.find('convert').get('type'),'WarderRadioOnly')
        self.assertEqual(tv.get('alphatest'),'off')
        self.assertEqual(radio.get('alphatest'),'blend')
        self.assertIsNotNone(root.find("widget[@name='EPG']"))
    def test_small_picons_and_other_widgets_are_unchanged(self):
        original='<screen><ePixmap position="100,800" size="220,132" pixmap="picon.png" alphatest="off" /></screen>'
        self.assertEqual(self.layers.prepare_radio_layers(original),original)
    def test_every_real_full_frame_template_retains_a_radio_graphic(self):
        config=types.SimpleNamespace(plugins=types.SimpleNamespace(setupGlass17=types.SimpleNamespace(par39=types.SimpleNamespace(value='/media/hdd'))))
        with patch.dict(sys.modules,{'Components.config':types.SimpleNamespace(config=config)}):
            templates=runpy.run_path(str(ROOT/'source/package-root/usr/lib/enigma2/python/Screens/G17screens.py'))['g17_extraScreen']
        checked=0
        import re
        for key,template in templates.items():
            patterns=re.findall(r'<ePixmap\b[^<>]*/>',template)
            for pattern in patterns:
                try:node=ET.fromstring(pattern)
                except ET.ParseError:continue
                if node.get('position')=='0,0' and node.get('size')=='1920,1080' and node.get('pixmap','').lower().endswith('.png') and node.get('alphatest','off')=='off':
                    output=self.layers.prepare_radio_layers(pattern)
                    root=ET.fromstring('<screen>'+output+'</screen>')
                    self.assertEqual(len(root.findall("widget/convert[@type='WarderRadioOnly']")),1,key)
                    self.assertEqual(root.findall('widget')[1].get('pixmap'),node.get('pixmap'),key)
                    checked+=1
        self.assertGreater(checked,10)


if __name__=='__main__':unittest.main()
