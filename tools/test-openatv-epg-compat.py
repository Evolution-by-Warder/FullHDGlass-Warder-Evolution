"""Execute the real FullHDGlass adapter against both native EPG API contracts."""
from pathlib import Path
from types import SimpleNamespace,ModuleType
import ast,importlib.util,sys,unittest

ROOT=Path(__file__).resolve().parents[1]
RUNTIME=ROOT/'source/package-root/usr/lib/enigma2/python/Plugins/Extensions/setupGlass17'
spec=importlib.util.spec_from_file_location('warder_epg_test',RUNTIME/'warderEpgCompat.py');compat=importlib.util.module_from_spec(spec);spec.loader.exec_module(compat)

class Text:
    def __init__(self,text=''):self.text=text
    def setText(self,text):self.text=text

class Session:
    def __init__(self):self.opens=[];self.raise_on_open=False
    def openWithCallback(self,callback,screen,event,service):
        if self.raise_on_open:raise RuntimeError('dialog unavailable')
        self.opens.append((callback,screen,event,service));return 'opened'

def api(modern=True,skin='GraphicalEPGPIG',refresh=True):
    config=SimpleNamespace(skin=SimpleNamespace(primary_skin=SimpleNamespace(value='hd_glass17/skin.xml')))
    info=SimpleNamespace(instance=SimpleNamespace(LongButtonPressed=False))
    class Base(dict):
        def __init__(self,session=None,*args,**kwargs):
            super().__init__();self.session=session or Session();self.skinName=skin;self.activeList='' if modern else 1
            self.calls=[];self.title=None;self['list'+str(self.activeList)]=SimpleNamespace(getCurrent=lambda:(self.event,self.service));self.event=object();self.service=object()
            for colour in ('red','green','yellow','blue'):self['key_'+colour]=Text('native-'+colour)
            # Native action maps store bound methods during construction. The
            # adapter must patch the concrete controller before this happens.
            self.actions={c:getattr(self,('_btn_'+c) if modern else (c+'ButtonPressed')) for c in ('red','green','yellow','blue')}
            if modern:self._updateButtonText()
            elif refresh:self.RefreshColouredKeys()
        def setTitle(self,title,*args,**kwargs):self.title=title
        def closeEventViewDialog(self):self.calls.append('close-view')
        def RecordTimerQuestion(self,manual=False):self.calls.append(('timer',manual));return 'timer'
        def enterDateTime(self):self.calls.append('date');return 'date'
        def openEPGSearch(self):self.calls.append('search');return 'search'
    def native(colour):
        def action(self):self.calls.append('native-'+colour);return 'native-'+colour
        return action
    if modern:
        class Grid(Base):
            def _updateButtonText(self):
                for c in ('red','green','yellow','blue'):self['key_'+c].setText('updated-native-'+c)
        Grid.__name__='EPGSelectionGrid'
        for c in ('red','green','yellow','blue'):setattr(Grid,'_btn_'+c,native(c))
        # Current OpenATV's compatibility constructor returns the concrete grid.
        class LegacyShim(Base):
            def __new__(cls,*args,**kwargs):return Grid(*args,**kwargs)
        module=SimpleNamespace(EPGSelection=LegacyShim,EPGSelectionGrid=Grid);target=Grid
    else:
        class Legacy(Base):pass
        for c in ('red','green','yellow','blue'):setattr(Legacy,c+'ButtonPressed',native(c))
        if refresh:Legacy.RefreshColouredKeys=lambda self: self['key_red'].setText('native-refresh')
        module=SimpleNamespace(EPGSelection=Legacy);target=Legacy
    errors=[];program=object();installed=compat.install(module,config,Text,lambda s:'translated:'+s,program,errors.append,info)
    return SimpleNamespace(module=module,target=target,config=config,info=info,errors=errors,program=program,installed=installed)

class EpgCompatTests(unittest.TestCase):
    def test_all_four_labels_and_real_bound_actions_on_legacy_and_modern(self):
        for modern in (False,True):
            with self.subTest(modern=modern):
                a=api(modern);screen=a.module.EPGSelection(Session());self.assertTrue(a.installed)
                for c in ('red','green','yellow','blue'):self.assertTrue(screen['warder_key_'+c].text.startswith('translated:'))
                self.assertEqual(screen.actions['red'](),'opened');self.assertEqual(len(screen.session.opens),1)
                self.assertIs(screen.session.opens[0][1],a.program);self.assertIs(screen.session.opens[0][2],screen.event);self.assertIs(screen.session.opens[0][3],screen.service)
                self.assertEqual(screen.actions['green'](),'timer');self.assertIn(('timer',True),screen.calls)
                self.assertEqual(screen.actions['yellow'](),'date');self.assertEqual(screen.actions['blue'](),'search')
                self.assertEqual(screen.title,'')
    def test_modern_native_refresh_does_not_replace_or_clear_our_sources(self):
        a=api();s=a.module.EPGSelection();sources=[s['warder_key_'+c] for c in ('red','green','yellow','blue')]
        s._updateButtonText()
        self.assertEqual(sources,[s['warder_key_'+c] for c in ('red','green','yellow','blue')]);self.assertIn('PROGRAM INFO',sources[0].text)
    def test_optional_legacy_refresh_absent_is_not_an_install_failure(self):
        a=api(False,refresh=False);s=a.module.EPGSelection();self.assertEqual(len([k for k in s if k.startswith('warder_key_')]),4);self.assertEqual(s.actions['red'](),'opened')
    def test_duplicate_red_cannot_stack_program_info_and_callback_unlocks(self):
        a=api();s=a.module.EPGSelection();s.actions['red']();s.actions['red']();self.assertEqual(len(s.session.opens),1)
        s.session.opens[0][0]();s.actions['red']();self.assertEqual(len(s.session.opens),2)
    def test_open_failure_unlocks_and_empty_event_does_not_open_foreign_screen(self):
        a=api();s=a.module.EPGSelection();s.session.raise_on_open=True;s.actions['red']();self.assertFalse(s._warderProgramInfoOpen);self.assertEqual(len(a.errors),1)
        s.session.raise_on_open=False;s.event=None;s.actions['red']();self.assertEqual(s.session.opens,[])
    def test_foreign_skins_and_non_pig_screens_keep_native_keys_and_title(self):
        for modern in (False,True):
            for name,primary in (('GraphicalEPG','hd_glass17/skin.xml'),('GraphicalInfoBarEPG','hd_glass17/skin.xml'),('GraphicalEPGPIG','other/skin.xml')):
                a=api(modern,skin=name);a.config.skin.primary_skin.value=primary;s=a.module.EPGSelection();s.setTitle('Original title')
                self.assertEqual(s.title,'Original title');self.assertFalse(any(k.startswith('warder_key_') for k in s))
                for c in ('red','green','yellow','blue'):self.assertEqual(s.actions[c](),'native-'+c)
    def test_modern_long_colour_press_stays_with_native_handler(self):
        a=api();s=a.module.EPGSelection();a.info.instance.LongButtonPressed=True
        for c in ('red','green','yellow','blue'):self.assertEqual(s.actions[c](),'native-'+c)
        self.assertEqual(s.session.opens,[])
    def test_repeated_install_does_not_wrap_twice(self):
        a=api();initial=a.target.__init__;self.assertTrue(compat.install(a.module,a.config,Text,lambda s:s,a.program));self.assertIs(a.target.__init__,initial)
        s=a.module.EPGSelection();s.actions['red']();self.assertEqual(len(s.session.opens),1)
    def test_program_info_colour_callbacks_return_to_selected_epg_action(self):
        a=api();s=a.module.EPGSelection()
        for action,expected in (('green','timer'),('yellow','date'),('blue','search')):self.assertEqual(s.warderProgramInfoClosed(action),expected)
    def test_modern_settings_use_actual_new_action_ids_and_do_not_save(self):
        item=lambda:SimpleNamespace(value='original')
        grid=SimpleNamespace(**{n:item() for n in ('servicetitle_mode','piconwidth','btn_red','btn_green','btn_yellow','btn_blue')})
        c=SimpleNamespace(epgselection=SimpleNamespace(grid=grid));compat.configure_graph(c)
        self.assertEqual(grid.servicetitle_mode.value,'picon');self.assertEqual(grid.piconwidth.value,60)
        self.assertEqual([getattr(grid,'btn_'+x).value for x in ('red','green','yellow','blue')],['openEventView','addEditTimer','enterDateTime','openEPGSearch'])
        compat.configure_graph(SimpleNamespace());compat.configure_graph(SimpleNamespace(epgselection=SimpleNamespace()))
    def test_actual_current_upstream_entry_points_and_factory_match_adapter(self):
        # Optional CLI environment provides pinned/current real source snapshots.
        import os
        for location in filter(None,(os.environ.get('WARDER_OPENATV_BEFORE'),os.environ.get('WARDER_OPENATV_AFTER'))):
            tree=ast.parse((Path(location)/'Screens/EpgSelection.py').read_text());classes={n.name:n for n in tree.body if isinstance(n,ast.ClassDef)}
            if 'EPGSelectionGrid' in classes:
                buttons=classes['EPGStandardButtons'];methods={n.name for n in buttons.body if isinstance(n,ast.FunctionDef)}
                self.assertTrue({'_btn_red','_btn_green','_btn_yellow','_btn_blue','_updateButtonText'}<=methods)
                new=next(n for n in classes['EPGSelection'].body if isinstance(n,ast.FunctionDef) and n.name=='__new__');self.assertIn('createEPGSelection',ast.unparse(new))
            else:
                methods={n.name for n in classes['EPGSelection'].body if isinstance(n,ast.FunctionDef)}
                self.assertTrue({'redButtonPressed','greenButtonPressed','yellowButtonPressed','blueButtonPressed','RefreshColouredKeys'}<=methods)

if __name__=='__main__':unittest.main()
