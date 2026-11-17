"""Regression: FullHDGlass Main menu shortcut must be opt-in, default No."""
import ast
from pathlib import Path
import unittest

PLUGIN=Path(__file__).resolve().parents[1]/'source/package-root/usr/lib/enigma2/python/Plugins/Extensions/setupGlass17/plugin.py'
TRANSLATIONS=PLUGIN.with_name('warderUiText.py')

class Flag:
    def __init__(self,value): self.value=value
    def getText(self): return 'Special info'

class Obj: pass
def fake_cfg():
    cfg=Obj();cfg.skin=Obj();cfg.skin.primary_skin=Flag('hd_glass17/skin.xml')
    cfg.plugins=Obj();cfg.plugins.warderSkinMainMenu=Obj();cfg.plugins.warderSkinMainMenu.enabled=Flag(False)
    cfg.plugins.setupGlass17=Obj();cfg.plugins.setupGlass17.par78=Flag('n')
    cfg.plugins.setupGlass17.par85=Flag(True)
    return cfg

class MainMenuToggleTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source=PLUGIN.read_text()
        cls.tree=ast.parse(cls.source)
        node=next(n for n in cls.tree.body if isinstance(n,ast.FunctionDef) and n.name=='startSetup17')
        cls.fn=ast.get_source_segment(cls.source,node).replace('from .warderSettingsMenuPlacement import target_key', 'pass  # supplied by test')
    def menu(self,config,menuid='mainmenu', target='mainmenu'):
        def main(*args,**kwargs): pass
        def main17(*args,**kwargs): pass
        env=dict(config=config,main=main,main17=main17,target_key=lambda:target)
        exec(self.fn,env)
        return env['startSetup17'](menuid),main,main17
    def test_persistent_config_default_no(self):
        self.assertIn('config.plugins.warderSkinMainMenu.enabled = ConfigYesNo(default=False)',self.source)
        self.assertNotIn('NoSave(ConfigYesNo',self.source.split('config.plugins.warderSkinMainMenu.enabled = ')[1].splitlines()[0])
    def test_default_no_does_not_create_shortcut(self):
        cfg=fake_cfg();items,main,_=self.menu(cfg)
        self.assertEqual(items,[])
    def test_yes_creates_exactly_one_shortcut(self):
        cfg=fake_cfg();cfg.plugins.warderSkinMainMenu.enabled.value=True
        items,main,_=self.menu(cfg)
        self.assertEqual(len(items),1)
        self.assertEqual(items[0][0],'FullHDGlass Warder Evolution')
        self.assertIs(items[0][1],main)
        self.assertEqual(items[0][2],'warder_fullhdglass_settings')
    def test_other_skin_stays_hidden_even_when_enabled(self):
        cfg=fake_cfg();cfg.plugins.warderSkinMainMenu.enabled.value=True
        cfg.skin.primary_skin.value='other/skin.xml'
        self.assertEqual(self.menu(cfg)[0],[])
    def test_existing_special_info_unaffected(self):
        cfg=fake_cfg();cfg.plugins.setupGlass17.par78.value='g'
        items,_,main17=self.menu(cfg)
        self.assertEqual(len(items),1)
        self.assertIs(items[0][1],main17)
        cfg.plugins.warderSkinMainMenu.enabled.value=True
        items,main,main17=self.menu(cfg)
        self.assertEqual(len(items),2)
        self.assertEqual([x[1] for x in items],[main,main17])
    def test_ostatne_is_used_when_image_has_its_own_submenu(self):
        cfg=fake_cfg();cfg.plugins.warderSkinMainMenu.enabled.value=True
        self.assertEqual(self.menu(cfg,'mainmenu',target='others')[0],[])
        items,main,_=self.menu(cfg,'others',target='others')
        self.assertEqual(len(items),1)
        self.assertIs(items[0][1],main)
    def test_not_inserted_into_unrelated_submenu(self):
        cfg=fake_cfg();cfg.plugins.warderSkinMainMenu.enabled.value=True
        self.assertEqual(self.menu(cfg,'setup')[0],[])
    def test_visible_in_skin_menu_settings(self):
        section=self.source.split('elif tt == 28:',1)[1].split('self["config"].list = self.list',1)[0]
        self.assertIn('getConfigListEntry(S0 % ui_text("Show FullHDGlass Warder Evolution in main menu"), config.plugins.warderSkinMainMenu.enabled)',section)
        menu=self.source.split('elif tt == 12:',1)[1].split('elif tt == 13:',1)[0]
        self.assertNotIn('Show FullHDGlass Warder Evolution in main menu',menu)
    def test_save_cancel_restart_and_factory_reset(self):
        self.assertIn('config.plugins.warderSkinMainMenu.enabled.save()',self.source)
        self.assertIn('config.plugins.warderSkinMainMenu.enabled.cancel()',self.source)
        self.assertIn('self._warderMainMenuAtOpen',self.source)
        self.assertIn('if self._warderMainMenuAtOpen != bool(config.plugins.warderSkinMainMenu.enabled.value):',self.source)
        reset=self.source.split('def restoreTofactoryAnswerNow(self,a):',1)[1].split('def restoreCfgFromFile',1)[0]
        self.assertIn('config.plugins.warderSkinMainMenu.enabled.value = False',reset)
    def test_all_locale_names_exist(self):
        data=TRANSLATIONS.read_text()
        key='Show FullHDGlass Warder Evolution in main menu'
        for lang in ('sk','cs','de','en','es','el','fr','hu','it','lt','nl','pl','pt','ro','ru','tr','uk','zh','al','et','fa'):
            self.assertIn('TEXT.setdefault("%s", {})["%s"]' % (lang,key),data)
        self.assertIn('Zobraziť FullHDGlass Warder Evolution v hlavnom menu',data)

if __name__=='__main__': unittest.main()
