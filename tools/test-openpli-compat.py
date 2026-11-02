#!/usr/bin/env python3
"""Exercise the OpenPLi adapter against real native Python components/controllers."""
import argparse
import ast
from copy import deepcopy
import json
from pathlib import Path
import runpy
import tempfile
from types import SimpleNamespace
import unittest
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser()
parser.add_argument('--upstream', required=True, type=Path)
parser.add_argument('--report', type=Path)
args, rest = parser.parse_known_args()
UPSTREAM = args.upstream
MODULE = ROOT/'source/package-root/usr/lib/enigma2/python/Plugins/Extensions/setupGlass17/warderOpenPli.py'
ADAPTER = runpy.run_path(str(MODULE))
AUDIT = runpy.run_path(str(ROOT/'tools/audit-openatv-skin-bindings.py'))
NATIVE = runpy.run_path(str(ROOT/'tools/test-native-screen-bindings.py'))
SKIN = ROOT/'source/package-root/usr/share/enigma2/hd_glass17/skin.xml'
ORIGINAL = ET.parse(SKIN).getroot()
SCREENS = {s.get('name'): s for s in ORIGINAL.findall('screen')}

class OpenPliTests(unittest.TestCase):
    def test_native_audit_reproduces_original_and_checks_every_adapted_binding(self):
        before = AUDIT['audit'](UPSTREAM, SKIN)
        self.assertEqual(len(before['binding_errors']), 29)
        registry={s.get('name'):(s,'/usr/share/enigma2/hd_glass17/') for s in ORIGINAL.findall('screen')}
        ADAPTER['install'](registry,'hd_glass17/skin.xml','OpenPLi')
        adapted = deepcopy(ORIGINAL)
        for i, child in enumerate(list(adapted)):
            if child.tag == 'screen': adapted[i] = registry[child.get('name')][0]
        with tempfile.TemporaryDirectory() as folder:
            target = Path(folder)/'skin.xml'
            ET.ElementTree(adapted).write(target)
            after = AUDIT['audit'](UPSTREAM, target)
        self.assertEqual(after['binding_errors'], [])
        self.assertEqual(after['parse_errors'], [])
        # Keep unresolved/dynamic fields visible; they are not hardware proof.
        if args.report:
            args.report.parent.mkdir(parents=True,exist_ok=True)
            args.report.write_text(json.dumps({'before':before,'after':after,
                'physical_receiver_verified':False},indent=2)+'\n')

    def test_native_button_failure_and_repaired_binding_updates(self):
        values = {'key_red': NATIVE['Button']('All'), 'key_green': NATIVE['Button']('Satellites')}
        original = ET.tostring(SCREENS['SimpleChannelSelection'], encoding='unicode')
        broken = NATIVE['BoundScreen'](original, values)
        broken.show()
        values['key_red'].setText('Changed natively')
        self.assertNotEqual(broken.text('key_red'), 'Changed natively')
        broken.hide()
        xml = ET.tostring(ADAPTER['adapt_screen'](SCREENS['SimpleChannelSelection']),encoding='unicode')
        for cycle in range(2):
            screen = NATIVE['BoundScreen'](xml, values)
            self.assertEqual(screen.missing, [])
            screen.show()
            values['key_red'].setText('All-%d' % cycle)
            self.assertEqual(screen.text('key_red'), 'All-%d' % cycle)
            screen.hide()

    def test_native_sources_receive_caption_changes(self):
        fields = NATIVE['fields']('Screens/Hotkey.py', 'HotkeySetupSelect')
        xml = ET.tostring(ADAPTER['adapt_screen'](SCREENS['HotkeySetupSelect']),encoding='unicode')
        screen = NATIVE['BoundScreen'](xml, fields)
        for key in ('key_red','key_green','key_yellow'):
            self.assertIsInstance(fields[key],NATIVE['StaticText'])
            fields[key].setText('Updated '+key)
            self.assertEqual(screen.text(key),'Updated '+key)

    def test_openpli_keyboard_retains_prompt_input_locale_and_all_buttons(self):
        registry={name:(screen,'/usr/share/enigma2/hd_glass17/') for name,screen in SCREENS.items()}
        ADAPTER['install'](registry,'hd_glass17/skin.xml','OpenPLi')
        keyboard=registry['VirtualKeyBoard'][0]
        index=AUDIT['NativeIndex'](UPSTREAM)
        fields=index.fields('Screens.VirtualKeyBoard.VirtualKeyBoard')
        widgets={w.get('name') or w.get('source'):w for w in keyboard.findall('widget')}
        for key in ('prompt','text','list','mode','locale','key_red','key_green','key_yellow','key_blue','key_text','key_info','key_help'):
            self.assertIn(key,fields)
            self.assertIn(key,widgets)
        self.assertEqual(keyboard.get('size'),'1500,900')
        self.assertEqual(widgets['list'].get('size'),'938,335')
        fonts=ORIGINAL.find('fonts')
        self.assertEqual(fonts.find("alias[@name='VirtualKeyBoard']").get('height'),'67')
        self.assertEqual(SCREENS['VirtualKeyBoard'].get('size'),'970,600')

    def test_openatv_other_skins_and_user_overlays_are_unchanged(self):
        own = '/usr/share/enigma2/hd_glass17/'
        for distro,primary in [('openatv','hd_glass17/skin.xml'),('OpenPLi','Other/skin.xml'),(None,'hd_glass17/skin.xml')]:
            registry={'SimpleChannelSelection':(SCREENS['SimpleChannelSelection'],own)}
            self.assertEqual(ADAPTER['install'](registry,primary,distro),0)
            self.assertIs(registry['SimpleChannelSelection'][0],SCREENS['SimpleChannelSelection'])
        registry={'owned':(SCREENS['SimpleChannelSelection'],own),
                  'user':(SCREENS['SimpleChannelSelection'],'/etc/enigma2/'),
                  'other':(SCREENS['SimpleChannelSelection'],'/usr/share/enigma2/hd_glass17-other/')}
        self.assertEqual(ADAPTER['install'](registry,'hd_glass17/skin.xml','OpenPLi'),1)
        self.assertIsNot(registry['owned'][0],SCREENS['SimpleChannelSelection'])
        self.assertIs(registry['user'][0],SCREENS['SimpleChannelSelection'])
        self.assertIs(registry['other'][0],SCREENS['SimpleChannelSelection'])
        once=ET.tostring(registry['owned'][0])
        ADAPTER['install'](registry,'hd_glass17/skin.xml','openpli')
        self.assertEqual(ET.tostring(registry['owned'][0]),once)

    def test_openpli_legacy_options_cannot_write_image_files(self):
        plugin=ast.parse((MODULE.parent/'plugin.py').read_text())
        saved=[]
        item=SimpleNamespace(value=True,save=lambda:saved.append('setting'))
        scope={'isATV':False,'_WarderOpenPli':True,
               'setCFGoff':lambda n:saved.append(n),
               'config':SimpleNamespace(plugins=SimpleNamespace(setupGlass17=SimpleNamespace(par67=item))),
               'configfile':SimpleNamespace(save=lambda:saved.append('config'))}
        names=('setMenuPyo','chnlSelPatch','setEncodingUser','chckFifo')
        functions=[n for n in plugin.body if isinstance(n,ast.FunctionDef) and n.name in names]
        self.assertEqual(len(functions),4)
        exec(compile(ast.Module(body=functions,type_ignores=[]),'legacy-guards','exec'),scope)
        for name in names:self.assertIs(scope[name](),False)
        self.assertIn(62,saved)
        self.assertIn(59,saved)
        self.assertFalse(item.value)

    def test_populated_native_plugin_browser_is_bound_and_launches_selection(self):
        # Execute the native list class, row factory, population and launch
        # methods. Only C++ content/drawing and the plugin catalogue are fakes.
        class Content:
            def __init__(self):self.values=[];self.fonts={};self.height=0;self.index=0
            def setList(self,values):self.values=values
            def setFont(self,index,font):self.fonts[index]=font
            def setItemHeight(self,height):self.height=height
            def getCurrentSelection(self):return self.values[self.index]
        menu=NATIVE['native']('Components/MenuList.py','MenuList',{
            'GUIComponent':NATIVE['GUIComponent'],'eListbox':object,
            'eListboxPythonStringContent':Content})
        fonts={a.get('name'):(a.get('font'),int(a.get('size')),int(a.get('height',a.get('size'))))
               for a in ORIGINAL.find('fonts').findall('alias')}
        old_height=fonts['PluginBrowser0'][2]
        registry={name:(screen,'/usr/share/enigma2/hd_glass17/') for name,screen in SCREENS.items()}
        ADAPTER['install'](registry,'hd_glass17/skin.xml','openpli',font_registry=fonts)
        listing=NATIVE['native']('Components/PluginList.py','PluginList',{
            'MenuList':menu,'eListboxPythonMultiContent':Content,'fonts':fonts,
            'applySkinFactor':lambda *values:values,'gFont':lambda name,size:(name,size)})
        component=listing([])
        parameters={p.get('name'):tuple(map(int,p.get('value').split(',')))
                    for p in ORIGINAL.find('parameters') if p.get('name','').startswith('PluginBrowser')}
        def text(**values):return dict(kind='text',**values)
        def icon(**values):return dict(kind='icon',**values)
        entry=NATIVE['native']('Components/PluginList.py','PluginEntryComponent',{
            'parameters':parameters,'applySkinFactor':lambda *values:values,
            'MultiContentEntryText':text,'MultiContentEntryPixmapAlphaBlend':icon,
            'BT_SCALE':4,'BT_KEEP_ASPECT_RATIO':8,'BT_HALIGN_CENTER':16,'BT_VALIGN_CENTER':32})
        launched=[]
        class Plugin:
            def __init__(self,name):self.name=name;self.description=name+' description';self.path='/usr/lib/enigma2/python/Plugins/Extensions/'+name;self.icon=name+'.png'
            def __call__(self,session):launched.append((self.name,session))
        catalogue=[Plugin('CSFD.cz'),Plugin('PiconHub'),Plugin('GT IPTV Player Pro')]
        session=object()
        class Browser(dict):pass
        browser=Browser(list=component);browser.listWidth=1620;browser.session=session
        tree=ast.parse((UPSTREAM/'Screens/PluginBrowser.py').read_text())
        native=next(n for n in tree.body if isinstance(n,ast.ClassDef) and n.name=='PluginBrowser')
        functions=[n for n in native.body if isinstance(n,ast.FunctionDef) and n.name in ('updateList','run')]
        scope={'plugins':SimpleNamespace(getPlugins=lambda where:catalogue[:]),
               'PluginDescriptor':SimpleNamespace(WHERE_PLUGINMENU=1),'PluginEntryComponent':entry,
               'config':SimpleNamespace(misc=SimpleNamespace(pluginbrowser=SimpleNamespace(plugin_order=SimpleNamespace(value=''))),usage=SimpleNamespace(menu_show_numbers=SimpleNamespace(value='none')))}
        exec(compile(ast.Module(body=functions,type_ignores=[]),'native-plugin-browser','exec'),scope)
        scope['updateList'](browser)
        self.assertEqual([row[0].name for row in component.l.values],[p.name for p in catalogue])
        self.assertEqual(component.l.values[0][1]['text'],'CSFD.cz')
        self.assertEqual(component.l.values[0][2]['text'],'CSFD.cz description')
        self.assertEqual(component.l.values[0][3]['png'],'CSFD.cz.png')
        self.assertGreater(parameters['PluginBrowserDescr'][1]+parameters['PluginBrowserDescr'][2],old_height)
        self.assertEqual(component.l.height,90)
        for row in component.l.values:
            for cell in row[1:]:self.assertLessEqual(cell['pos'][1]+cell['size'][1],component.l.height)
        # Replay OpenPLi's actual conditional template processor: the old skin
        # selects no list at all, while the repaired skin binds this exact GUI.
        skin=ast.parse((UPSTREAM/'skin.py').read_text())
        read=next(n for n in skin.body if isinstance(n,ast.FunctionDef) and n.name=='readSkin')
        process=next(n for n in read.body if isinstance(n,ast.FunctionDef) and n.name=='processScreen')
        seen=[]
        def widget(w,c):
            if (w.get('name') or w.get('source'))=='list':seen.append(browser[w.get('name')])
        env={'screen':browser,'processors':{'widget':widget},'processNone':lambda w,c:None,'SkinError':ValueError}
        exec(compile(ast.Module(body=[process],type_ignores=[]),'native-processScreen','exec'),env)
        env['processScreen'](SCREENS['PluginBrowser'],None)
        self.assertEqual(seen,[])
        env['processScreen'](registry['PluginBrowser'][0],None)
        self.assertEqual(seen,[component])
        component.instance=SimpleNamespace(moveSelectionTo=lambda index:setattr(component.l,'index',index))
        component.moveToIndex(1)
        scope['run'](browser)
        self.assertEqual(launched,[('PiconHub',session)])
        for name in ('PluginBrowser','PluginBrowserList','PluginBrowserGrid','PluginDownloadBrowser'):
            xml=registry[name][0]
            self.assertIsNotNone(xml.find("widget[@name='list']"),name)
            self.assertEqual(xml.find("widget[@name='list']").get('itemHeight'),'90')

    def test_startup_hook_updates_the_native_shared_font_registry(self):
        import sys
        from types import ModuleType
        from unittest.mock import patch
        native_skin=ModuleType('skin');native_skin.fonts={'PluginBrowser0':('Prive4',32,60,32)}
        with patch.dict(sys.modules,{'skin':native_skin}):
            ADAPTER['install']({},'hd_glass17/skin.xml','OpenPLi')
        self.assertEqual(native_skin.fonts['PluginBrowser0'],('Prive4',32,90,32))

    def test_plugin_fonts_remain_scoped_and_preserve_larger_user_rows(self):
        for distro,primary in [('openatv','hd_glass17/skin.xml'),('openpli','Other/skin.xml')]:
            fonts={'PluginBrowser0':('Custom',32,60,32)}
            ADAPTER['install']({},primary,distro,font_registry=fonts)
            self.assertEqual(fonts['PluginBrowser0'],('Custom',32,60,32))
        fonts={'PluginBrowser0':('Custom',34,120,40)}
        ADAPTER['install']({},'hd_glass17/skin.xml','openpli',font_registry=fonts)
        self.assertEqual(fonts['PluginBrowser0'],('Custom',34,120,40))

    def test_geometry_artwork_and_visibility_rules_are_preserved(self):
        for original in SCREENS.values():
            before=ET.tostring(original)
            adapted=ADAPTER['adapt_screen'](original)
            self.assertEqual(ET.tostring(original),before)
            self.assertEqual(original.attrib,adapted.attrib)
            before_tree=deepcopy(original);after_tree=deepcopy(adapted)
            if original.get('name') in ('PluginBrowser','PluginBrowserList','PluginBrowserGrid','PluginDownloadBrowser'):
                for tree in (before_tree,after_tree):
                    for child in list(tree):
                        if child.tag=='widget' and (child.get('name') or child.get('source')) in ('list','pluginList','pluginGrid'):tree.remove(child)
            self.assertEqual(len(list(before_tree.iter())),len(list(after_tree.iter())))
            for old,new in zip(before_tree.iter(),after_tree.iter()):
                attrs=lambda e:{k:v for k,v in e.attrib.items() if k not in ('name','source','render','conditional')}
                self.assertEqual(attrs(old),attrs(new))
                self.assertEqual(old.text,new.text)
                if old.get('conditional'):self.assertEqual(old.get('conditional'),new.get('conditional'))

    def test_native_conditional_processor_skips_absent_fields(self):
        tree=ast.parse((UPSTREAM/'skin.py').read_text())
        read=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='readSkin')
        process=next(n for n in read.body if isinstance(n,ast.FunctionDef) and n.name=='processScreen')
        seen=[];scope={'screen':{},'processors':{'widget':lambda w,c:seen.append(w)},'processNone':lambda w,c:None,'SkinError':ValueError}
        exec(compile(ast.Module(body=[process],type_ignores=[]),'native-skin-processScreen','exec'),scope)
        xml=ET.fromstring('<screen><widget source="missing" render="Label"/></screen>')
        scope['processScreen'](ADAPTER['adapt_screen'](xml),None)
        self.assertEqual(seen,[])
        scope['screen']['missing']=object()
        scope['processScreen'](ADAPTER['adapt_screen'](xml),None)
        self.assertEqual(len(seen),1)

if __name__=='__main__':unittest.main(argv=[__file__]+rest)
