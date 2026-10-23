#!/usr/bin/env python3
"""Validate the settings presentation against the approved 1.0.15 controllers."""
import ast
import hashlib
import importlib.util
import json
from pathlib import Path
import unittest
import xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('setup_style',ROOT/'tools/style-setup-screens.py')
style=importlib.util.module_from_spec(spec);spec.loader.exec_module(style)
BASELINE=json.loads(style.FIXTURE.read_text())
CURRENT=style.PLUGIN.read_text()
LAYOUTS=style.extract(CURRENT)


class SetupStyleTests(unittest.TestCase):
    def test_configuration_actions_callbacks_and_controller_logic_are_unchanged(self):
        self.assertEqual(style.normalized(ast.parse(CURRENT)),BASELINE['logic_sha256'])

    def test_all_owned_layouts_retain_original_widget_and_source_contracts(self):
        for name,(_,skin) in LAYOUTS.items():
            close='</screen>' if name=='selectIconsDisplayed' else ''
            original=ET.fromstring(BASELINE['skins'][name]+close)
            current=ET.fromstring(skin+close)
            self.assertTrue(set(style.widget_ids(original))<=set(style.widget_ids(current)),name)
            self.assertEqual(current.get('flags'),'wfNoBorder',name)
            self.assertEqual(current.get('backgroundColor'),style.BASE if name in ('setupGlass17ScreenSetup','downloadMenu') else style.PANEL,name)

    def test_every_static_widget_fits_inside_the_dialog(self):
        for name,(_,skin) in LAYOUTS.items():
            root=ET.fromstring(skin+('</screen>' if name=='selectIconsDisplayed' else ''))
            width,height=map(int,root.get('size').split(','))
            self.assertLessEqual(width,1920);self.assertLessEqual(height,1080)
            for node in root:
                x,y=map(int,node.get('position').split(','));w,h=map(int,node.get('size').split(','))
                self.assertGreaterEqual(x,0,(name,node.attrib));self.assertGreaterEqual(y,0)
                self.assertGreater(w,0);self.assertGreater(h,0)
                self.assertLessEqual(x+w,width,(name,node.attrib));self.assertLessEqual(y+h,height,(name,node.attrib))

    def test_footer_colors_and_centered_captions_match_the_controller_keys(self):
        for name,(_,skin) in LAYOUTS.items():
            root=ET.fromstring(skin+('</screen>' if name=='selectIconsDisplayed' else ''))
            for node in root:
                key=node.get('name') or node.get('source','')
                if key.startswith('key_'):
                    self.assertEqual(node.get('foregroundColor'),style.COLORS[key[4:]],name)
                    self.assertEqual(node.get('halign'),'center');self.assertEqual(node.get('valign'),'center')
                    self.assertEqual(node.get('transparent'),'0')

    def test_native_title_date_clock_and_seconds_sources_are_present(self):
        for name in ('setupGlass17ScreenSetup','downloadMenu'):
            root=ET.fromstring(LAYOUTS[name][1])
            self.assertEqual(len(root.findall("widget[@source='global.CurrentTime']")),3)
            self.assertEqual({x.get('type') for x in root.findall('widget/convert')},{'g17ClockToText'})
        for name in set(LAYOUTS)-{'setupGlass17ScreenSetup','downloadMenu'}:
            root=ET.fromstring(LAYOUTS[name][1]+('</screen>' if name=='selectIconsDisplayed' else ''))
            self.assertEqual(len(root.findall("widget[@source='Title']")),1,name)

    def test_dynamic_download_and_history_coordinates_remain_compatible(self):
        down=ET.fromstring(LAYOUTS['downloadMenu'][1]);dwn=down.find("widget[@name='dwn']")
        self.assertEqual(dwn.get('position'),'0,0');self.assertEqual(dwn.get('size'),'1920,150')
        history=ET.fromstring(LAYOUTS['historyScreen'][1])
        self.assertEqual(history.find("widget[@name='key_red']").get('position'),'0,775')
        self.assertEqual(history.find("widget[@name='line_red']").get('position'),'0,765')
        main=ET.fromstring(LAYOUTS['setupGlass17ScreenSetup'][1])
        self.assertEqual(main.find("widget[@name='selected_item']").get('transparent'),'1')
        self.assertIn('<widget name="config" font="Prive3;34"',LAYOUTS['setupGlass17ScreenSetup'][1])
        # Controller still appends the nine icon previews before </screen>.
        self.assertFalse(LAYOUTS['selectIconsDisplayed'][1].strip().endswith('</screen>'))

    def test_warder_position_picker_still_inherits_the_styled_satellite_layout(self):
        tree=ast.parse(CURRENT);cls=next(x for x in tree.body if isinstance(x,ast.ClassDef) and x.name=='warderPositionSelectorScr')
        node=next(x for x in cls.body if isinstance(x,ast.Assign) and isinstance(x.targets[0],ast.Name) and x.targets[0].id=='skin')
        self.assertEqual(ast.dump(node.value),ast.dump(ast.parse('satSelectorScr.skin',mode='eval').body))

    def test_styling_is_reproducible_from_the_original_layouts(self):
        for name,(_,skin) in LAYOUTS.items():
            self.assertEqual(skin.strip(),style.themed(name,BASELINE['skins'][name]).strip(),name)


if __name__=='__main__':unittest.main()
