#!/usr/bin/env python3
"""Validate the settings presentation against the approved 1.0.15 controllers."""
import ast
import hashlib
import importlib.util
import json
from pathlib import Path
import unittest
from types import SimpleNamespace
import xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('setup_style',ROOT/'tools/style-setup-screens.py')
style=importlib.util.module_from_spec(spec);spec.loader.exec_module(style)
BASELINE=json.loads(style.FIXTURE.read_text())
CURRENT=style.PLUGIN.read_text()
LAYOUTS=style.extract(CURRENT)
# The v1.0.76 controller fingerprint includes the approved offline factory-icon
# reset and localized storage menu/help changes from PR #88, in addition to
# the earlier GLES gate and release labels. Keep the historical fixture for
# older releases, and pin the full AST to catch any unreviewed logic edits.
RUNTIME_VERSION=(style.PLUGIN.parent/'version').read_text().strip()
REVIEWED_1076_SHA256='9c2e7e62276c9e3677283c93c6f4849115ec0f8544eb8c1321c5fe8515abbef3'
EXPECTED_SHA=(REVIEWED_1076_SHA256 if RUNTIME_VERSION == '1.0.76' else BASELINE['logic_sha256'])


class SetupStyleTests(unittest.TestCase):
    def test_picon_source_default_cannot_silently_change_to_mini(self):
        changed=CURRENT.replace('par231 = ConfigSelection(default="system"','par231 = ConfigSelection(default="mini"',1)
        self.assertNotEqual(changed,CURRENT)
        self.assertNotEqual(style.normalized(ast.parse(changed)),EXPECTED_SHA)

    def test_modified_channel_picon_hook_is_not_silently_approved(self):
        changed=CURRENT.replace('lambda: config.plugins.setupGlass17.par39.value,','lambda: "/tmp",',1)
        self.assertNotEqual(changed,CURRENT)
        self.assertNotEqual(style.normalized(ast.parse(changed)),EXPECTED_SHA)

    def test_openpli_graph_hook_changes_are_not_silently_approved(self):
        changed=CURRENT.replace('WarderProgramInfo, _warderUiText, report_error=Writelog)', 'None, _warderUiText, report_error=Writelog)',1)
        self.assertNotEqual(changed,CURRENT)
        self.assertNotEqual(style.normalized(ast.parse(changed)),EXPECTED_SHA)

    def test_openpli_hook_changes_are_not_silently_approved(self):
        changed=CURRENT.replace('domScreens as _WarderSkinScreens','screens as _WarderSkinScreens',1)
        self.assertNotEqual(changed,CURRENT)
        self.assertNotEqual(style.normalized(ast.parse(changed)),EXPECTED_SHA)

    def test_openpli_guard_cannot_drop_existing_openatv_protection(self):
        changed=CURRENT.replace('if isATV or _WarderOpenPli:', 'if _WarderOpenPli:',1)
        self.assertNotEqual(changed,CURRENT)
        self.assertNotEqual(style.normalized(ast.parse(changed)),EXPECTED_SHA)

    def test_prime_time_exceptions_are_exact_and_scope_bound(self):
        ledger = json.loads((ROOT / 'design/channelselection-primetime/logic-edits.json').read_text())
        self.assertEqual(len(ledger), 16)
        self.assertTrue(all(record['scope'] and record['after'] and record['before'] == '' for record in ledger))
        self.assertTrue(all('warderEvolutionPrimeTime' in record['after']
                            or 'fieldMargins' in record['after']
                            or 'g17MetrixHDRunningText' in record['after']
                            or 'g17ShowExtraEpg' in record['after']
                            or 'in_default_channel_screen' in record['after']
                            or 'has_clipped_events' in record['after']
                            or ("line.rstrip().endswith('/>')" in record['after'] and record['scope'] == 'changeChF')
                            for record in ledger))
        # Altered new settings/actions must still change the frozen fingerprint.
        for old, new in (
            ('ConfigYesNo(default=False)', 'ConfigYesNo(default=True)'),
            ('warderEvolutionPrimeTime.enabled.save()', 'warderEvolutionPrimeTime.enabled.cancel()'),
            ('warderEvolutionPrimeTime.clock.cancel()', 'warderEvolutionPrimeTime.clock.save()'),
            ('fieldMargins="26"', 'fieldMargins="0"'),
            ('size="685,224"', 'size="685,240"'),
            ('position="1150,695" size="685,226"', 'position="1150,685" size="685,236"'),
            ('render="WarderChannelEpgClip"', 'render="UnknownRenderer"'),
            ("and line.rstrip().endswith('/>'):", "and False:"),
        ):
            changed = CURRENT.replace(old, new, 1)
            self.assertNotEqual(changed, CURRENT)
            self.assertNotEqual(style.normalized(ast.parse(changed)), EXPECTED_SHA)

    def test_each_reviewed_prime_time_ast_node_occurs_once_in_its_scope(self):
        ledger = json.loads((ROOT / 'design/channelselection-primetime/logic-edits.json').read_text())
        expected = [(r['scope'], style.portable(ast.parse(r['after']).body[0])) for r in ledger]
        counts = [0] * len(expected)

        def visit(node, scope='module'):
            if isinstance(node, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
                scope = node.name if scope == 'module' else scope + '.' + node.name
            if isinstance(node, ast.stmt):
                portable_node = style.portable(node)
                for index, (record_scope, reviewed_node) in enumerate(expected):
                    if scope == record_scope and portable_node == reviewed_node:
                        counts[index] += 1
            for child in ast.iter_child_nodes(node):
                visit(child, scope)

        visit(ast.parse(CURRENT))
        # TEST77 changed four legacy Prime Time guards. The old entries
        # remain historical records; verify their approved successor patterns
        # explicitly instead of requiring obsolete AST nodes to still exist.
        evolved = {
            3: "if default_geometry and 'picServiceEventProgressbar=' in line and 'fieldMargins=' not in line:",
            9: "if in_default_channel_screen and 'render=\"g17ShowExtraEpg\"' in line:",
            11: "in_default_channel_screen = default_geometry",
            12: "if in_default_channel_screen and '</screen>' in line:",
        }
        for index, record in enumerate(ledger):
            if index in evolved:
                self.assertEqual(counts[index], 0, record['scope'])
                self.assertEqual(CURRENT.count(evolved[index]), 1, (index, evolved[index]))
            else:
                self.assertEqual(counts[index], 1, (index, record['scope']))
        # A stale ledger record must not silently remove protection.
        for record in ledger:
            self.assertEqual(record['before'], '')

    def test_release_1072_iptv_caid_and_localization_are_fingerprint_guarded(self):
        # All five receiver-approved code paths must remain in the payload.
        # The complete AST fingerprint test below detects any unreviewed edit.
        required = (
            'av.getResolutionX(0)',
            'av.getResolutionY(0)',
            'self.warderCaidScrollTimer.start(220, True)',
            'loop[offset:] + loop[:offset]',
            'manifest.get("changelog_i18n", {})',
        )
        for statement in required:
            self.assertEqual(CURRENT.count(statement), 1, statement)

    def test_pr88_offline_factory_reset_and_storage_labels_remain_guarded(self):
        # Specific contract checks complement the complete controller fingerprint.
        for statement in (
            'def restoreFactoryIcons():',
            'os.path.join(SKINPATH, "icons_factory")',
            'os.replace(tmp, destination)',
            'self._warderFactoryResetPending = True',
            'ui_text("Storage for graphics sets, picons and data")',
            'ui_text("Storage for downloaded graphics sets, picons and other skin data. Saving a changed path creates hdg17_files here.")',
        ):
            self.assertIn(statement, CURRENT, statement)

    def test_configuration_actions_callbacks_and_controller_logic_are_unchanged(self):
        self.assertEqual(style.normalized(ast.parse(CURRENT)),EXPECTED_SHA)

    def test_modified_compatibility_installation_hook_is_not_silently_approved(self):
        changed=CURRENT.replace('_WarderCoolContent.TYPE_TEXT,','_WarderCoolContent.TYPE_PIXMAP,',1)
        self.assertNotEqual(changed,CURRENT)
        self.assertNotEqual(style.normalized(ast.parse(changed)),EXPECTED_SHA)

    def test_modified_approved_bitrate_readiness_limit_still_fails(self):
        changed=CURRENT.replace('self.bitratePrepareAttempts > 20','self.bitratePrepareAttempts > 0',1)
        self.assertNotEqual(changed,CURRENT)
        self.assertNotEqual(style.normalized(ast.parse(changed)),EXPECTED_SHA)

    def test_fingerprint_is_portable_but_still_detects_changed_save_action(self):
        tree=ast.parse(CURRENT);before=style.normalized(tree)
        # Exercise both older and newer grammar shapes on either interpreter.
        for node in ast.walk(tree):
            if isinstance(node,(ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef)) and not getattr(node,'type_params',[]):
                node._fields=tuple(field for field in node._fields if field!='type_params')
        self.assertEqual(style.normalized(tree),before)
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
            if name=='setupGlass17ScreenSetup':
                original.find("widget[@source='Canvas']").set('render','WarderSettingsCanvas')
                original.find("widget[@render='Pig']").set('render','WarderSettingsPig')
                original.remove(original.find("widget[@name='selected_item']"))
            self.assertTrue(set(style.widget_ids(original))<=set(style.widget_ids(current)),name)
            self.assertEqual(current.get('flags'),'wfNoBorder',name)
            self.assertEqual(current.get('backgroundColor'),style.CLEAR,name)

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
                    self.assertEqual(node.get('transparent'),'0' if int(node.get('position').split(',')[1])>=980 else '1')

    def test_native_date_clock_and_seconds_remain_without_section_titles(self):
        for name in LAYOUTS:
            root=ET.fromstring(LAYOUTS[name][1]+('</screen>' if name=='selectIconsDisplayed' else ''))
            self.assertEqual(len(root.findall("widget[@source='global.CurrentTime'][@render='Label']")),4)
            self.assertEqual({x.get('type') for x in root.findall('widget/convert')},{'g17ClockToText'})
        for name in set(LAYOUTS)-{'setupGlass17ScreenSetup','downloadMenu'}:
            root=ET.fromstring(LAYOUTS[name][1]+('</screen>' if name=='selectIconsDisplayed' else ''))
            self.assertEqual(len(root.findall("widget[@source='Title']")),0,name)

    def test_dynamic_download_and_history_coordinates_remain_compatible(self):
        down=ET.fromstring(LAYOUTS['downloadMenu'][1]);dwn=down.find("widget[@name='dwn']")
        self.assertEqual(dwn.get('position'),'50,166');self.assertEqual(dwn.get('size'),'1820,30')
        history=ET.fromstring(LAYOUTS['historyScreen'][1])
        self.assertEqual(history.find("widget[@name='key_red']").get('position'),'135,1006')
        self.assertEqual(history.find("widget[@name='line_red']").get('position'),'135,996')
        main=ET.fromstring(LAYOUTS['setupGlass17ScreenSetup'][1])
        self.assertIsNone(main.find("widget[@name='selected_item']"))
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
        scope={'eSize':lambda *args:args};exec(compile(ast.Module(body=[method],type_ignores=[]),'panels','exec'),scope)
        class Panel:
            visible=False
            def __init__(self):self.instance=self;self.dimensions=None
            def resize(self,size):self.dimensions=size
            def show(self):self.visible=True
            def hide(self):self.visible=False
        class Screen(dict):pass
        screen=Screen()
        root=ET.fromstring(LAYOUTS['setupGlass17ScreenSetup'][1])
        nodes={x.get('name'):x for x in root if x.get('name','').startswith('warder_')}
        self.assertEqual(len(nodes),15)
        for key in nodes:screen[key]=Panel()
        screen["help_txt"]=Panel()
        # Enter short/long groups repeatedly and return to the main menu.
        for main in (True,False,False,True,False,True):
            screen.isMainMenu=main;scope['_warderSetPanelMode'](screen)
            visible=[key for key,panel in screen.items() if panel.visible and key.startswith("warder_")]
            self.assertEqual(len(visible),10 if main else 5)
            self.assertEqual(screen["help_txt"].dimensions,(737,248) if main else (780,350))
            self.assertTrue(all(key.startswith('warder_menu_' if main else 'warder_settings_') for key in visible))
        config=root.find("widget[@name='config']")
        help_text=root.find("widget[@name='help_txt']")
        full=nodes['warder_settings_panel_0']
        self.assertEqual(full.get('position'),'50,232');self.assertEqual(full.get('size'),'1810,728')
        self.assertEqual(config.get('position'),'60,242')
        self.assertEqual(config.get('size'),'1790,320')
        self.assertLessEqual(sum(map(int,(config.get('position').split(',')[0],config.get('size').split(',')[0]))),1850)
        self.assertLess(int(full.get('zPosition')),0)
        self.assertEqual(full.get('backgroundColor'),style.GLASS)
        for node in (config,help_text):self.assertGreater(int(node.get('zPosition')),int(full.get('zPosition'))+1)
        # No anonymous split frame can survive a mode switch.
        self.assertFalse(any(x.tag=='eLabel' and x.get('position') in ('50,200','850,200','808,200','850,958') for x in root))

    def test_download_rows_are_above_the_opaque_panel(self):
        root=ET.fromstring(LAYOUTS['downloadMenu'][1])
        rows=root.find("widget[@name='list']")
        background=next(x for x in root if x.tag=='eLabel' and x.get('position')=='40,197' and x.get('size')=='1840,778')
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
        self.assertNotEqual(style.normalized(ast.parse(changed)),EXPECTED_SHA)

    def test_footer_canvas_is_hidden_until_an_actual_colour_is_selected(self):
        renderer_path=ROOT/'source/package-root/usr/lib/enigma2/python/Components/Renderer/WarderSettingsCanvas.py'
        tree=ast.parse(renderer_path.read_text())
        cls=next(x for x in tree.body if isinstance(x,ast.ClassDef))
        class NativeCanvas:
            def __init__(self):
                self.source=SimpleNamespace();self.visible=True;self.draw_updates=0
            def hide(self):self.visible=False
            def pullUpdates(self):self.draw_updates+=1
        scope={'Canvas':NativeCanvas}
        exec(compile(ast.Module(body=[cls],type_ignores=[]),'renderer','exec'),scope)
        renderer=scope['WarderSettingsCanvas']()
        self.assertFalse(renderer.visible)
        renderer.pullUpdates();self.assertFalse(renderer.visible)
        renderer.source.warder_sample_visible=True
        renderer.pullUpdates();self.assertTrue(renderer.visible)
        renderer.source.warder_sample_visible=False
        renderer.pullUpdates();self.assertFalse(renderer.visible)
        self.assertEqual(renderer.draw_updates,3)  # Native drawing is retained.
        root=ET.fromstring(LAYOUTS['setupGlass17ScreenSetup'][1])
        self.assertEqual(root.find("widget[@source='Canvas']").get('render'),'WarderSettingsCanvas')
        self.assertIsNone(root.find("widget[@name='selected_item']"))

    def test_real_colour_sample_callback_sets_visibility_before_flush(self):
        tree=ast.parse(CURRENT)
        cls=next(x for x in tree.body if isinstance(x,ast.ClassDef) and x.name=='setupGlass17ScreenSetup')
        method=next(x for x in cls.body if isinstance(x,ast.FunctionDef) and x.name=='sampleColor')
        scope={'gFont':lambda *a:a,'_':lambda text:text,'RT_HALIGN_CENTER':0}
        exec(compile(ast.Module(body=[method],type_ignores=[]),'sampleColor','exec'),scope)
        class Source:
            def __init__(self):self.states=[];self.fills=[];self.text=[]
            def fill(self,*args):self.fills.append(args)
            def writeText(self,*args):self.text.append(args)
            def flush(self):self.states.append(self.warder_sample_visible)
        screen=SimpleNamespace(canvas=Source(),isMainMenu=True,isShow=True)
        callback=scope['sampleColor']
        callback(screen,None);self.assertEqual(screen.canvas.states,[False])
        screen.isMainMenu=False
        callback(screen,'#ff0000');self.assertTrue(screen.canvas.states[-1])
        self.assertEqual(screen.canvas.fills[-1][-1],0xff0000)
        self.assertEqual(screen.canvas.text[-1][-2],'Color Sample')
        callback(screen,None);self.assertFalse(screen.canvas.states[-1])
        screen.isMainMenu=True
        callback(screen,'#00ff00');self.assertFalse(screen.canvas.states[-1])

    def test_help_artwork_has_padding_and_preserves_its_aspect_ratio(self):
        root=ET.fromstring(LAYOUTS['setupGlass17ScreenSetup'][1])
        pic=root.find("widget[@name='help_pict']")
        x,y=map(int,pic.get('position').split(','));w,h=map(int,pic.get('size').split(','))
        self.assertGreaterEqual(y,576+16)
        self.assertLessEqual(y+h,958-16)
        self.assertGreaterEqual(x,60);self.assertLessEqual(x+w,1850)
        self.assertAlmostEqual(w/h,882/300,delta=.005)
        self.assertGreater(w,882);self.assertGreater(h,300)
        self.assertLessEqual(abs(x+w/2-960),1)

    def test_duplicate_value_is_removed_and_legacy_date_model_remains_compatible(self):
        cls=next(x for x in ast.parse(CURRENT).body if isinstance(x,ast.ClassDef) and x.name=='setupGlass17ScreenSetup')
        method=next(x for x in cls.body if isinstance(x,ast.FunctionDef) and x.name=='doMyHelpWindow')
        text=ast.unparse(method)
        self.assertNotIn("setText(self.getCurrentValue())",text)
        self.assertIn('strftime(',text)
        self.assertIn('sampleColor(t)',text)
        self.assertIn('_warderLoadHelpPicture(filename)',text)

    def test_every_configuration_group_uses_the_same_bounded_artwork_loader(self):
        cls=next(x for x in ast.parse(CURRENT).body if isinstance(x,ast.ClassDef) and x.name=='setupGlass17ScreenSetup')
        picture=style.portable(ast.parse('self["help_pict"].instance',mode='eval').body)
        loads=[]
        for method in cls.body:
            if not isinstance(method,ast.FunctionDef):continue
            for call in ast.walk(method):
                if isinstance(call,ast.Call) and isinstance(call.func,ast.Attribute) and style.portable(call.func.value)==picture:
                    self.assertNotIn(call.func.attr,('move','resize'))  # No group overrides the shared bounds.
                    if call.func.attr=='setPixmapFromFile':loads.append(method.name)
        self.assertEqual(loads,[])
        loader=next(x for x in cls.body if isinstance(x,ast.FunctionDef) and x.name=='_warderLoadHelpPicture')
        code=ast.unparse(loader)
        self.assertIn('self.onClose.append(self._warderHelpLoader.close)',code)
        self.assertIn('self._warderHelpLoader.request(filename)',code)
        self.assertNotIn('themed_path',code)
        show=next(x for x in cls.body if isinstance(x,ast.FunctionDef) and x.name=='showInfo')
        hook=ast.parse('self["config"].onSelectionChanged.append(self.doMyHelpWindow)').body[0]
        self.assertIn(style.portable(hook),[style.portable(x) for x in ast.walk(show)])
        # Existing static bounds checks also cover all owned popup previews.
        self.assertEqual(len(LAYOUTS),10)

    def test_no_widget_can_draw_a_center_footer_rectangle(self):
        root=ET.fromstring(LAYOUTS['setupGlass17ScreenSetup'][1])
        self.assertIsNone(root.find("widget[@name='selected_item']"))
        for child in root:
            if int(child.get('zPosition','0'))<0:continue
            x,y=map(int,child.get('position').split(','));w,h=map(int,child.get('size').split(','))
            self.assertFalse(x<1360 and x+w>560 and y<1060 and y+h>974,child.attrib)
        cls=next(x for x in ast.parse(CURRENT).body if isinstance(x,ast.ClassDef) and x.name=='setupGlass17ScreenSetup')
        init=next(x for x in cls.body if isinstance(x,ast.FunctionDef) and x.name=='__init__')
        self.assertIn(style.portable(ast.parse(style.VALUE_SOURCE).body[0]),[style.portable(n) for n in init.body])
        setup=next(x for x in cls.body if isinstance(x,ast.FunctionDef) and x.name=='runSetup')
        moved=style.portable(ast.parse(style.GEOMETRY_NEW).body[0])
        self.assertIn(moved,[style.portable(x) for x in ast.walk(setup)])
        self.assertNotIn(style.portable(ast.parse(style.GEOMETRY_OLD).body[0]),[style.portable(x) for x in ast.walk(setup)])

    def test_compact_banner_keeps_the_large_help_preview_and_moves_main_menu_only_one_row(self):
        main=ET.fromstring(LAYOUTS['setupGlass17ScreenSetup'][1])
        expected={'config':('60,242','1790,320'),'list':('860,238','990,720'),
                  'help_pict':('445,592','1029,350'),'white':('60,574','1790,2')}
        for name,(position,size) in expected.items():
            node=main.find("widget[@name='%s']"%name)
            self.assertEqual((node.get('position'),node.get('size')),(position,size))
        for name,(_,xml) in LAYOUTS.items():
            root=ET.fromstring(xml+('</screen>' if name=='selectIconsDisplayed' else ''))
            self.assertEqual(root.get('size'),'1920,1080',name)
            self.assertEqual(len(root.findall("widget[@render='WarderSettingsHeader']")),1,name)
            self.assertFalse(root.findall("ePixmap[@pixmap='%s']"%style.BANNER_IMAGE))
            for node in root:
                if node.tag=='widget' and node.get('name') and node.get('name') not in ('dwn',):
                    if node.get('name').startswith('warder_'):continue
                    self.assertGreaterEqual(int(node.get('position').split(',')[1]),164,(name,node.attrib))

    def test_approved_banner_image_matches_the_pinned_native_full_hd_asset(self):
        import struct
        record=json.loads((ROOT/'design/settings-header-asset.json').read_text())
        path=ROOT/'source/package-root'/record['path'];raw=path.read_bytes()
        self.assertEqual(hashlib.sha256(raw).hexdigest(),record['sha256'])
        self.assertEqual(raw[:8],b'\x89PNG\r\n\x1a\n')
        width,height=struct.unpack('>II',raw[16:24])
        self.assertEqual((width,height),(record['width'],record['height']))
        self.assertAlmostEqual(width/height,16/9,delta=.003)
        self.assertEqual(record['display_header_height'],164)
        for name,(_,skin) in LAYOUTS.items():
            root=ET.fromstring(skin+('</screen>' if name=='selectIconsDisplayed' else ''))
            columns=root.findall("widget[@source='global.CurrentTime'][@render='Label']")
            self.assertEqual([x.find('convert').text for x in columns],['Format:%A','Format:%d. %B %Y','Default','Format::%S'],name)
            self.assertEqual(columns[-1].get('foregroundColor'),style.TEXT)
            self.assertLess(int(columns[-1].get('font').split(';')[1]),int(columns[-2].get('font').split(';')[1]))
            version=next(x for x in root if x.get('text') == (style.PLUGIN.parent/'version').read_text().strip())
            self.assertGreaterEqual(int(version.get('position').split(',')[0]),1680)
            self.assertEqual(version.get('foregroundColor'),style.CYAN)

    def test_dynamic_history_button_remains_centered_after_result_mode_move(self):
        cls=next(x for x in ast.parse(CURRENT).body if isinstance(x,ast.ClassDef) and x.name=='historyScreen')
        method=next(x for x in cls.body if isinstance(x,ast.FunctionDef) and x.name=='readandshow')
        moves=[x for x in ast.walk(method) if isinstance(x,ast.Expr) and isinstance(x.value,ast.Call)
               and isinstance(x.value.func,ast.Attribute) and x.value.func.attr=='move']
        seen=[]
        class Button:
            def move(self,p):seen.append(p)
        scope={'self':{'key_red':Button(),'line_red':Button()},'ePoint':lambda x,y:(x,y)}
        for node in moves:exec(compile(ast.Module(body=[node],type_ignores=[]),'history-moves','exec'),scope)
        self.assertEqual(len(seen),2)
        self.assertAlmostEqual(seen[0][0]+825/2,960,delta=1)
        self.assertGreaterEqual(seen[0][1],134);self.assertLessEqual(seen[0][1]+50,1080)
        self.assertEqual(seen[0][1]-seen[1][1],10)

    def test_all_nine_dynamic_icon_previews_fit_the_shared_header_body(self):
        cls=next(x for x in ast.parse(CURRENT).body if isinstance(x,ast.ClassDef) and x.name=='selectIconsDisplayed')
        init=next(x for x in cls.body if isinstance(x,ast.FunctionDef) and x.name=='__init__')
        append=next(x for x in ast.walk(init) if isinstance(x,ast.AugAssign) and 'str(x)' in ast.unparse(x))
        screen=SimpleNamespace(skin='<screen>')
        for number in range(9):
            scope={'self':screen,'x':number,'off':(number//3)*3,'y':(0,187,375)[number//3]}
            exec(compile(ast.Module(body=[append],type_ignores=[]),'icon-layout','exec'),scope)
        root=ET.fromstring(screen.skin+'</screen>');self.assertEqual(len(root),9)
        for node in root:
            x,y=map(int,node.get('position').split(','));w,h=map(int,node.get('size').split(','))
            self.assertGreaterEqual(x,267);self.assertGreaterEqual(y,134)
            self.assertLessEqual(x+w,1653);self.assertLessEqual(y+h,985)

    def test_styling_is_reproducible_from_the_original_layouts(self):
        for name,(_,skin) in LAYOUTS.items():
            self.assertEqual(skin.strip(),style.themed(name,BASELINE['skins'][name]).strip(),name)


if __name__=='__main__':unittest.main()


