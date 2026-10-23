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

    def test_fingerprint_is_portable_but_still_detects_changed_save_action(self):
        tree=ast.parse(CURRENT);before=style.normalized(tree)
        for node in ast.walk(tree):
            if isinstance(node,(ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef)) and 'type_params' not in node._fields:
                node._fields=node._fields+('type_params',);node.type_params=[]
        self.assertEqual(style.normalized(tree),before)
        changed=CURRENT.replace('"green": self.save','"green": self.exit',1)
        self.assertNotEqual(changed,CURRENT)
        self.assertNotEqual(style.normalized(ast.parse(changed)),before)

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

    def test_split_and_full_panels_are_mutually_exclusive_on_every_transition(self):
        tree=ast.parse(CURRENT)
        cls=next(x for x in tree.body if isinstance(x,ast.ClassDef) and x.name=='setupGlass17ScreenSetup')
        method=next(x for x in cls.body if isinstance(x,ast.FunctionDef) and x.name=='_warderSetPanelMode')
        scope={};exec(compile(ast.Module(body=[method],type_ignores=[]),'panels','exec'),scope)
        class Panel:
            visible=False
            def show(self):self.visible=True
            def hide(self):self.visible=False
        class Screen(dict):pass
        screen=Screen()
        root=ET.fromstring(LAYOUTS['setupGlass17ScreenSetup'][1])
        nodes={x.get('name'):x for x in root if x.get('name','').startswith('warder_')}
        self.assertEqual(len(nodes),15)
        for key in nodes:screen[key]=Panel()
        # Enter short/long groups repeatedly and return to the main menu.
        for main in (True,False,False,True,False,True):
            screen.isMainMenu=main;scope['_warderSetPanelMode'](screen)
            visible=[key for key,panel in screen.items() if panel.visible]
            self.assertEqual(len(visible),10 if main else 5)
            self.assertTrue(all(key.startswith('warder_menu_' if main else 'warder_settings_') for key in visible))
        config=root.find("widget[@name='config']")
        help_text=root.find("widget[@name='help_txt']")
        full=nodes['warder_settings_panel_0']
        self.assertEqual(full.get('position'),'50,200');self.assertEqual(full.get('size'),'1810,760')
        self.assertGreater(int(full.get('zPosition')),int(root.find("widget[@render='Pig']").get('zPosition')))
        for node in (config,help_text):self.assertGreater(int(node.get('zPosition')),int(full.get('zPosition'))+1)
        # No anonymous split frame can survive a mode switch.
        self.assertFalse(any(x.tag=='eLabel' and x.get('position') in ('50,200','850,200','808,200','850,958') for x in root))

    def test_download_rows_are_above_the_opaque_panel(self):
        root=ET.fromstring(LAYOUTS['downloadMenu'][1])
        rows=root.find("widget[@name='list']")
        background=next(x for x in root if x.tag=='eLabel' and x.get('position')=='40,165' and x.get('size')=='1840,810')
        self.assertGreater(int(rows.get('zPosition')),int(background.get('zPosition')))
        self.assertGreater(int(rows.get('zPosition')),1)  # panel borders

    def test_panel_initialization_and_switch_hook_are_wired_without_new_actions(self):
        tree=ast.parse(CURRENT)
        cls=next(x for x in tree.body if isinstance(x,ast.ClassDef) and x.name=='setupGlass17ScreenSetup')
        init=next(x for x in cls.body if isinstance(x,ast.FunctionDef) and x.name=='__init__')
        setup=next(x for x in cls.body if isinstance(x,ast.FunctionDef) and x.name=='runSetup')
        self.assertIn(ast.dump(ast.parse(style.PANEL_INIT).body[0]),[ast.dump(x) for x in init.body])
        self.assertEqual(ast.dump(setup.body[0]),ast.dump(ast.parse(style.PANEL_CALL).body[0]))
        changed=CURRENT.replace('panel.show()', 'panel.hide()',1)
        self.assertNotEqual(style.normalized(ast.parse(changed)),BASELINE['logic_sha256'])

    def test_styling_is_reproducible_from_the_original_layouts(self):
        for name,(_,skin) in LAYOUTS.items():
            self.assertEqual(skin.strip(),style.themed(name,BASELINE['skins'][name]).strip(),name)


if __name__=='__main__':unittest.main()
