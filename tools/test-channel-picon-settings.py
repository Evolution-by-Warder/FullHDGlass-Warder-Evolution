#!/usr/bin/env python3
"""Replay the real settings registry, menu branch and save/cancel callbacks."""
import ast
import os
import tempfile
from pathlib import Path
from types import SimpleNamespace as NS
import unittest
from unittest.mock import Mock

ROOT=Path(__file__).resolve().parents[1]
PKG=Path(os.environ.get('WARDER_PICON_PACKAGE_ROOT',str(ROOT/'source/package-root/usr/lib/enigma2/python')))
TEXT=(PKG/'Plugins/Extensions/setupGlass17/plugin.py').read_text()
TREE=ast.parse(TEXT)
OWNER=next(n for n in TREE.body if isinstance(n,ast.ClassDef) and n.name=='setupGlass17ScreenSetup')
REGISTRY=ast.literal_eval(next(n.value for n in TREE.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='ALL_CFG' for t in n.targets)))


class Setting:
    def __init__(self,default,choices=()):
        self.default=self.value=self.saved=default
        self.choices=choices
    def getValue(self):return self.value
    def setValue(self,value):self.value=value
    def save(self):self.saved=self.value
    def cancel(self):self.value=self.saved


class SettingsTests(unittest.TestCase):
    def setUp(self):
        self.values={'par'+str(i):Setting('old-'+str(i)) for i in range(1,232)}
        self.values['par231']=Setting('system')
        self.values['par144'].value='/test-backup/'
        self.section=NS(**self.values)
        self.section.dict=lambda:self.values
        self.config=NS(plugins=NS(setupGlass17=self.section,
                                  warderEpgListScroll=NS(enabled=Setting(True)),
                                  warderPiconExpert=NS(custom_destination=Setting(False),
                                                      destination=Setting('')),
                                  warderUserPicons=NS(enabled=Setting(False),path=Setting(''))))
        self.scope=dict(config=self.config,ALL_CFG=REGISTRY,ui_text=lambda s:s,_=lambda s:s,
            configfile=NS(save=Mock()),_atomicWriteText=Mock(),setPathFiles=Mock(),
            allow_channel_epg_overlay=lambda:True,
            _warderUserNormalize=lambda path:path, os=os,
            _warderEpgListScrollLabel=lambda:"Scroll EPG titles")

    def method(self,name):
        node=next(n for n in OWNER.body if isinstance(n,ast.FunctionDef) and n.name==name)
        exec(compile(ast.Module(body=[node],type_ignores=[]),'packaged-settings.py','exec'),self.scope)
        return self.scope[name]

    def screen(self):
        return NS(_spinnerAtOpen=self.section.par230.value,_weatherCityAtOpen=self.section.par13.value,
                  rst=False,destroyTimers=lambda:True,close=Mock())

    def test_own_picon_folder_is_readonly_and_uses_classic_browser(self):
        self.assertIn('warderUserPicons.path_display = ConfigSelection(', TEXT)
        self.assertIn('self.list.append(getConfigListEntry(S0 % ui_text("Own picon folder"), display))', TEXT)
        self.assertNotIn('self.list.append(getConfigListEntry(S0 % ui_text("Own picon folder"), config.plugins.warderUserPicons.path))', TEXT)
        selection = next(n for n in OWNER.body if isinstance(n,ast.FunctionDef)
                         and n.name == 'ActivateselectedFnc')
        browser = next(n for n in ast.walk(selection) if isinstance(n,ast.If)
                       and ast.unparse(n.test)=='t == config.plugins.warderUserPicons.path_display')
        code = ast.unparse(browser)
        self.assertIn('dirBrowser',code)
        self.assertIn('_warderOwnPiconFolderSelected',code)
        self.assertNotIn('VirtualKeyBoard',code)
        self.assertNotIn('ConfigText',code)

    def test_own_picon_help_is_specific_to_selected_row(self):
        method = next(n for n in OWNER.body if isinstance(n,ast.FunctionDef)
                      and n.name=='doMyHelpWindow')
        branch = next(n for n in ast.walk(method) if isinstance(n,ast.If)
                      and 'config.plugins.warderUserPicons.path_display' in ast.unparse(n.test))
        self.assertIn("self['help_pict'].hide()", ast.unparse(branch))
        self.assertIn("self['help_txt'].setText(message)", ast.unparse(branch))
        self.assertIn('skin only reads PNG files',ast.unparse(branch))
        self.assertIsInstance(branch.body[-1],ast.Return)

    def test_default_is_system_and_choices_are_only_explicit_opt_in(self):
        node=next(n for n in TREE.body if isinstance(n,ast.Assign) and any(ast.unparse(t)=='config.plugins.setupGlass17.par231' for t in n.targets))
        self.scope['ConfigSelection']=Setting
        exec(compile(ast.Module(body=[node],type_ignores=[]),'packaged-config.py','exec'),self.scope)
        self.assertEqual(self.section.par231.default,'system')
        self.assertEqual([v for v,label in self.section.par231.choices],['system','mini'])

    def test_download_menu_offers_current_skin_picon_storage(self):
        menu = next(n for n in TREE.body if isinstance(n, ast.ClassDef) and n.name == 'downloadMenu')
        method = next(n for n in menu.body if isinstance(n, ast.FunctionDef)
                      and n.name == 'openWarderPiconChoice')
        scope = {
            'os': os, '_': lambda value: value,
            'ui_text': lambda value: {'FullHDGlass skin storage': 'Úložisko skinu FullHDGlass'}.get(value, value),
            'warderPiconSync': NS(skin_picon_destination=lambda root, resolution=None: os.path.join(root, {'50x30':'picon_50x30','400x240':'picon_400x240'}.get(resolution, 'picon')),
                                  PICON_DESTINATIONS=(
                ('/usr/share/enigma2/picon', 'Receiver memory'),
                ('/media/hdd/picon', 'Hard disk'))),
            'config': NS(plugins=NS(setupGlass17=NS(par39=Setting('/media/hdd/hdg17_files')))),
            'ChoiceBox': object(),
        }
        exec(compile(ast.Module(body=[method], type_ignores=[]),
                     'packaged-picon-choice.py', 'exec'), scope)
        screen = NS(warderPiconPrefs={'resolution': '220x132', 'style': 'transparent'},
                    session=NS(openWithCallback=Mock()),
                    warderPiconChoiceAnswer=Mock())
        scope['openWarderPiconChoice'](screen, 'wp-dest')
        choices = screen.session.openWithCallback.call_args.kwargs['list']
        self.assertEqual(choices[0], (
            'Úložisko skinu FullHDGlass - /media/hdd/hdg17_files/picon',
            ('destination', '/media/hdd/hdg17_files/picon')))
        self.assertIn(('Hard disk - /media/hdd/picon',
                       ('destination', '/media/hdd/picon')), choices)
        scope['config'].plugins.setupGlass17.par39.value = '/media/usb/hdg17_files'
        scope['openWarderPiconChoice'](screen, 'wp-dest')
        updated = screen.session.openWithCallback.call_args.kwargs['list']
        self.assertEqual(updated[0][1], ('destination', '/media/usb/hdg17_files/picon'))
        screen.warderPiconPrefs['resolution'] = '50x30'
        scope['openWarderPiconChoice'](screen, 'wp-dest')
        size_choices = screen.session.openWithCallback.call_args.kwargs['list']
        self.assertEqual(size_choices[0][1], ('destination', '/media/usb/hdg17_files/picon_50x30'))

    def test_destination_row_indexing_is_contiguous_in_both_modes(self):
        menu = next(n for n in TREE.body if isinstance(n, ast.ClassDef) and n.name == 'downloadMenu')
        constructor = next(n for n in menu.body if isinstance(n, ast.FunctionDef) and n.name == '__init__')
        condition = next(n for n in ast.walk(constructor) if isinstance(n, ast.If)
                         and 'warderPiconExpert.custom_destination.value' in ast.unparse(n.test)
                         and 'self.menuListAll = dict(enumerate(' in ast.unparse(n))
        scope = {'config': self.config}
        apply_filter = compile(ast.Module(body=[condition], type_ignores=[]), 'filtered-rows.py', 'exec')
        original = {index: [name, '', '', '', 'x'] for index, name in enumerate(
            ('wp-pos','wp-res','wp-style','wp-dest','wp-mode','aux-prov','aux-sat','aux-cam'))}
        standard = NS(menuListAll=dict(original))
        scope['self'] = standard
        self.config.plugins.warderPiconExpert.custom_destination.value = False
        exec(apply_filter, scope)
        self.assertEqual(list(standard.menuListAll), list(range(7)))
        self.assertEqual([row[0] for row in standard.menuListAll.values()],
                         ['wp-pos','wp-res','wp-style','wp-mode','aux-prov','aux-sat','aux-cam'])
        expert = NS(menuListAll=dict(original))
        scope['self'] = expert
        self.config.plugins.warderPiconExpert.custom_destination.value = True
        exec(apply_filter, scope)
        self.assertEqual(list(expert.menuListAll), list(range(8)))
        self.assertEqual(expert.menuListAll[3][0], 'wp-dest')

    def test_standard_menu_hides_destination_and_expert_opt_in_restores_it(self):
        source = TEXT
        self.assertIn('config.plugins.warderPiconExpert.custom_destination = ConfigYesNo(default=False)', source)
        self.assertIn('row for row in self.menuListAll.values() if row[0] != "wp-dest"', source)
        self.assertIn('self.menuListAll = dict(enumerate(', source)
        self.assertIn('ui_text("Custom picon location")', source)
        self.assertIn('config.plugins.warderPiconExpert.custom_destination.save()', source)
        self.assertIn('config.plugins.warderPiconExpert.custom_destination.cancel()', source)
        self.assertIn('self.warderPiconPrefs["destination"] = warderPiconSync.skin_picon_destination(', source)
        from types import SimpleNamespace
        directory = '/media/hdd/hdg17_files'
        sync_src = (PKG/'Plugins/Extensions/setupGlass17/warderPiconSync.py').read_text()
        sync_tree = ast.parse(sync_src)
        node = next(n for n in sync_tree.body if isinstance(n, ast.FunctionDef)
                    and n.name == 'skin_picon_destination')
        scope = {'os': os}
        exec(compile(ast.Module(body=[node], type_ignores=[]), 'picon-path.py', 'exec'), scope)
        target = scope['skin_picon_destination']
        self.assertEqual(target(directory, '220x132'), directory + '/picon')
        self.assertEqual(target(directory, '50x30'), directory + '/picon_50x30')
        self.assertEqual(target(directory, '400x240'), directory + '/picon_400x240')
        self.assertEqual(target('/media/usb/hdg17_files'), '/media/usb/hdg17_files/picon')

    def test_registry_preserves_original_parameter_indices(self):
        self.assertEqual(len(REGISTRY),231)
        self.assertEqual(REGISTRY[18],'Channel sel. type')
        self.assertEqual(REGISTRY[229],'Spinner theme')
        self.assertEqual(REGISTRY[230],'Channel-list picon source')

    def test_menu_puts_source_immediately_after_type(self):
        method=next(n for n in OWNER.body if isinstance(n,ast.FunctionDef) and n.name=='runSetup')
        branch=next(n for n in ast.walk(method) if isinstance(n,ast.If) and ast.unparse(n.test)=='tt == 13')
        screen=NS(list=[])
        self.scope.update(self=screen,tt=13,S0='%s:',C1='  %s:',sepCC='Colours',E2OK=False,
                          getConfigListEntry=lambda *args:args)
        # Execute the real branch body without unrelated screen construction.
        exec(compile(ast.Module(body=branch.body,type_ignores=[]),'packaged-menu.py','exec'),self.scope)
        self.assertIs(screen.list[0][1],self.section.par19)
        self.assertIs(screen.list[1][1],self.section.par231)
        self.assertIs(screen.list[2][1],self.section.par132)

    def test_real_save_callback_persists_choice_and_includes_backup(self):
        self.section.par231.value='mini'
        screen=self.screen()
        self.method('saving')(screen)
        self.assertEqual(self.section.par231.saved,'mini')
        self.assertFalse(self.config.plugins.warderPiconExpert.custom_destination.saved)
        self.assertEqual(self.config.plugins.warderPiconExpert.destination.saved, '')
        self.assertFalse(self.config.plugins.warderUserPicons.enabled.saved)
        self.assertEqual(self.config.plugins.warderUserPicons.path.saved, '')
        backup=self.scope['_atomicWriteText'].call_args.args
        self.assertEqual(backup[0],'/test-backup/hdg17.conf')
        self.assertIn('Channel-list picon source: mini\n',backup[1])
        self.assertIn('Icons type: old-1\n',backup[1])
        self.assertEqual(self.section.par1.saved,'old-1')
        self.scope['configfile'].save.assert_called_once()
        screen.close.assert_called_once()

    def test_real_cancel_callback_discards_unsaved_change(self):
        self.section.par231.value='mini'
        self.method('exitNow')(self.screen())
        self.assertEqual(self.section.par231.value,'system')

    def test_real_cancel_callback_keeps_previously_saved_mini_choice(self):
        self.section.par231.value='mini';self.section.par231.save()
        self.section.par231.value='system'
        self.method('exitNow')(self.screen())
        self.assertEqual(self.section.par231.value,'mini')

    def test_real_backup_restore_recognises_the_new_setting(self):
        screen=self.screen()
        screen.session=NS(open=Mock());screen.showInfo=Mock();screen.isNum=lambda text:text.isdigit()
        self.scope.update(os=os,MessageBox=NS(TYPE_INFO=1,TYPE_ERROR=2),ER_F=' failed')
        with tempfile.TemporaryDirectory() as directory:
            path=Path(directory)/'hdg17.conf'
            path.write_text('Channel-list picon source: mini\n')
            self.method('restoreCfgFromFile')(screen,str(path))
        self.assertEqual(self.section.par231.value,'mini')

    def test_all_supported_languages_have_the_new_menu_text(self):
        tree=ast.parse((PKG/'Plugins/Extensions/setupGlass17/warderUiText.py').read_text())
        data=ast.literal_eval(next(n.value for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='TEXT' for t in n.targets)))
        for lang in ('sk','cs','en','de','pl','hu','ru','fr','it','es'):
            for key in ('Channel-list picon source','System setting','Prefer 50x30'):
                self.assertTrue(data[lang][key],(lang,key))

    def test_help_has_a_dedicated_description_and_no_image_lookup(self):
        method=next(n for n in OWNER.body if isinstance(n,ast.FunctionDef) and n.name=='doMyHelpWindow')
        branch=next(n for n in ast.walk(method) if isinstance(n,ast.If) and 'getattr(config.plugins.setupGlass17' in ast.unparse(n.test) and 'par231' in ast.unparse(n.test))
        self.assertIsInstance(branch.body[-1],ast.Return)
        self.assertIn("System setting keeps the image's original picon lookup",ast.unparse(branch))


if __name__=='__main__':unittest.main()
