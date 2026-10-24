#!/usr/bin/env python3
"""Exercise setup entry points, dialog callback contracts and OLED preparation."""
import ast
import importlib.util
import io
from pathlib import Path
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch
import xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parents[1]
P=ROOT/'source/package-root/usr/lib/enigma2/python/Plugins/Extensions/setupGlass17'
TREE=ast.parse((P/'plugin.py').read_text())


def method(cls,name):
    parent=next(n for n in TREE.body if isinstance(n,ast.ClassDef) and n.name==cls)
    return next(n for n in parent.body if isinstance(n,ast.FunctionDef) and n.name==name)


def function(node,scope):
    scope=dict(scope)
    exec(compile(ast.Module(body=[node],type_ignores=[]),'receiver-callback','exec'),scope)
    return scope[node.name]


def load(path,name):
    spec=importlib.util.spec_from_file_location(name,path);mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod);return mod


class Screen(dict):
    def __init__(self,session=None):
        super().__init__();self.session=session;self.onLayoutFinish=[];self.onClose=[];self.returned=()
    def setTitle(self,title):self.title=title
    def close(self,*args):self.returned=args


class Label:
    def __init__(self,text=''):self.text=text;self.visible=True;self.pages=0
    def hide(self):self.visible=False
    def show(self):self.visible=True
    def pageUp(self):self.pages-=1
    def pageDown(self):self.pages+=1


class MenuList:
    def __init__(self,rows,**kw):self.rows=rows;self.index=0
    def getCurrent(self):return self.rows[self.index] if self.rows else None
    def moveToIndex(self,n):self.index=n


class ActionMap:
    def __init__(self,contexts,actions,prio=0):self.actions=actions;self.enabled=True
    def setEnabled(self,value):self.enabled=value


class NativeMessage(Screen):
    TYPE_YESNO=1;TYPE_INFO=2
    def __init__(self,session,text,type=1,default=True,**kwargs):
        super().__init__(session);self.text=text;self.list=[('Yes',True),('No',False)] if type==1 else None
        self['list']=MenuList(self.list or []);self['list'].index=0 if default else 1
        self.timer=SimpleNamespace(stop=lambda:None)
    def cancel(self):self.close(False)
    def select(self):self.close(self['list'].getCurrent()[1] if self.list else True)


class NativeInput(Screen):
    def __init__(self,session,**kwargs):super().__init__(session)
    def cancel(self):self.close(None)
    def go(self):self.close('entered text')


def dialogs():
    classes=[n for n in ast.parse((P/'warderDialogs.py').read_text()).body if isinstance(n,ast.ClassDef)]
    skins=load(P/'warderDialogSkins.py','test_dialog_skins')
    scope={'Screen':Screen,'NativeMessageBox':NativeMessage,'NativeInputBox':NativeInput,'Label':Label,'ScrollLabel':Label,'MenuList':MenuList,'ActionMap':ActionMap,'ui_text':lambda t:t,
           'MESSAGE_SKIN':skins.MESSAGE_SKIN,'CHOICE_SKIN':skins.CHOICE_SKIN,'INPUT_SKIN':skins.INPUT_SKIN}
    exec(compile(ast.Module(body=classes,type_ignores=[]),'owned-dialogs','exec'),scope)
    return scope


class BatchTests(unittest.TestCase):
    def test_setup_moves_to_plugins_exclusively_and_keeps_session_start(self):
        start=next(n for n in TREE.body if isinstance(n,ast.FunctionDef) and n.name=='startSetup17')
        plugins=next(n for n in TREE.body if isinstance(n,ast.FunctionDef) and n.name=='Plugins')
        class Descriptor:
            WHERE_MENU=1;WHERE_SESSIONSTART=2;WHERE_EXTENSIONSMENU=3;WHERE_PLUGINMENU=4
            def __init__(self,**kw):self.__dict__.update(kw)
        setup=SimpleNamespace(par78=SimpleNamespace(value='n'),par85=SimpleNamespace(value=False))
        cfg=SimpleNamespace(skin=SimpleNamespace(primary_skin=SimpleNamespace(value='hd_glass17/skin.xml')),plugins=SimpleNamespace(setupGlass17=setup))
        scope={'config':cfg,'PluginDescriptor':Descriptor,'main':object(),'main17':object(),'startHdg17':object(),'ui_text':lambda t:t,'_':lambda t:t}
        scope['startSetup17']=function(start,scope)
        self.assertEqual(scope['startSetup17']('setup'),[])
        entries=function(plugins,scope)('path')
        configs=[d for d in entries if d.fnc is scope['main']]
        self.assertEqual(len(configs),1);self.assertEqual(configs[0].where,Descriptor.WHERE_PLUGINMENU)
        self.assertTrue((P/configs[0].icon).is_file())
        cfg.skin.primary_skin.value='other/skin.xml';self.assertEqual(function(plugins,scope)('path'),[])

    def test_reviewed_batch_does_not_hide_changes_to_the_new_destructive_paths(self):
        mod=load(ROOT/'tools/style-setup-screens.py','test_batch_guard')
        current=(P/'plugin.py').read_text()
        expected=mod.normalized(ast.parse(current))
        changed=current.replace('tool_row[4] = "d"','tool_row[4] = "x"',1)
        self.assertNotEqual(current,changed)
        self.assertNotEqual(mod.normalized(ast.parse(changed)),expected)

    def test_choice_returns_the_original_tuple_and_cancel_returns_none(self):
        cls=dialogs()['ChoiceBox'];choices=[('50x30',('resolution','50x30')),('220x132',('resolution','220x132'))]
        for key in ('ok','green'):
            screen=cls(None,title='Select',list=choices,selection=1)
            for callback in screen.onLayoutFinish:callback()
            screen['actions'].actions[key]()
            self.assertIs(screen.returned[0],choices[1])
        for key in ('cancel','red'):
            screen=cls(None,list=choices);screen['actions'].actions[key]();self.assertEqual(screen.returned,(None,))
        screen=cls(None,list=[]);screen.choose();self.assertEqual(screen.returned,())

    def test_message_preserves_safe_no_default_and_noninteractive_progress(self):
        cls=dialogs()['MessageBox']
        box=cls(None,'Reset?',default=False);box['warderActions'].actions['green']();self.assertEqual(box.returned,(False,))
        box=cls(None,'Reset?',default=False);box['list'].index=0;box['warderActions'].actions['green']();self.assertEqual(box.returned,(True,))
        box=cls(None,'Reset?');box['warderActions'].actions['red']();self.assertEqual(box.returned,(False,))
        box=cls(None,'Updating...',type=2,enable_input=False)
        self.assertFalse(box['warderActions'].enabled);self.assertFalse(box['warderScroll'].enabled);self.assertFalse(box['key_red'].visible)
        box=cls(None,'Long result',type=2);box['warderScroll'].actions['down']();self.assertEqual(box['text'].pages,1)

    def test_native_text_input_keeps_cancel_and_confirmation_values(self):
        cls=dialogs()['InputBox'];box=cls(None);box['warderActions'].actions['red']();self.assertEqual(box.returned,(None,))
        box=cls(None);box['warderActions'].actions['green']();self.assertEqual(box.returned,('entered text',))

    def test_oled_choice_does_not_require_an_extraction_tool(self):
        calls=[]
        screen=Screen(SimpleNamespace(openWithCallback=lambda *args:calls.append(args)))
        screen.ena=True;screen['list']=SimpleNamespace(getSelectedIndex=lambda:9)
        screen.menuListAll={9:['oa','***Select*** OLED',8,'','x']};screen.warderPiconRows=();screen.warderAuxRows=()
        screen.satSelcallback=lambda *a:None
        callback=function(method('downloadMenu','doSelection'),{'satSelectorScr':'sat-selector'})
        callback(screen)
        self.assertEqual(calls[0][1:3],('sat-selector',8))

    def test_missing_helper_is_prepared_before_any_picon_archive(self):
        calls=[];screen=Screen();screen.dwnTimer=SimpleNamespace(isActive=lambda:False)
        screen.clrSelectsat=False;screen.menuListAll={9:['oa','OLED',8,[], 'd'],17:['7z','7zip','7zip-m','', 'd']}
        screen.warderFailedRows=set();screen.setWdir=lambda:'/tmp/';screen.downAnswerNow=lambda:calls.append(screen.type_download)
        function(method('downloadMenu','dwnLoop'),{'find_sevenzip':lambda p:None,'SEVENZIP':'private'})(screen)
        self.assertEqual(calls,['7zip-m']);self.assertEqual(screen.menuListAll[9][4],'d');self.assertEqual(screen.menuListAll[17][4],'x')

    def test_tool_resolver_rejects_nonexecutable_private_file_and_finds_system_tool(self):
        mod=load(P/'warderTools.py','test_warder_tools')
        with tempfile.TemporaryDirectory() as folder:
            private=Path(folder)/'private';system=Path(folder)/'7z';private.write_text('x');system.write_text('x');system.chmod(0o755)
            with patch.object(mod.shutil,'which',side_effect=lambda n:str(system) if n=='7z' else None):
                self.assertEqual(mod.find_sevenzip(str(private)),str(system))
                private.chmod(0o755);self.assertEqual(mod.find_sevenzip(str(private)),str(private))

    def test_all_owned_dialogs_are_opaque_and_have_a_single_shared_header(self):
        module=load(P/'warderDialogSkins.py','test_dialog_xml')
        for key in ('MESSAGE_SKIN','CHOICE_SKIN','INPUT_SKIN'):
            root=ET.fromstring(getattr(module,key));self.assertEqual(root.get('size'),'1920,1080');self.assertEqual(root.get('backgroundColor'),'#00071627')
            self.assertEqual(len(root.findall("widget[@source='global.CurrentTime']")),4)
            self.assertEqual(len(root.findall('ePixmap')),1)
            for node in root:
                x,y=map(int,node.get('position').split(','));w,h=map(int,node.get('size').split(','))
                self.assertTrue(0<=x<x+w<=1920 and 0<=y<y+h<=1080,node.attrib)
            for name in ('key_red','key_green'):
                node=root.find("widget[@name='%s']"%name);self.assertEqual(node.get('halign'),'center');self.assertGreaterEqual(int(node.get('position').split(',')[1]),960)

    def test_prepared_thumbnails_cover_the_stock_types_without_decoding_full_screenshots(self):
        import zipfile
        from PIL import Image
        mod=load(P/'warderTypePreviews.py','test_type_previews')
        with zipfile.ZipFile(P/'warder-infobar-types.zip') as archive:
            self.assertEqual(len(archive.namelist()),78)
            for name in archive.namelist():
                with Image.open(io.BytesIO(archive.read(name))) as image:
                    self.assertEqual(image.size,(174,98));self.assertEqual(image.getchannel('A').getextrema(),(255,255))
        with tempfile.TemporaryDirectory() as folder,patch.object(mod.tempfile,'gettempdir',return_value=folder):
            path=mod.thumbnail_path(1);self.assertTrue(Path(path).is_file())
            with patch.object(mod.zipfile,'ZipFile',side_effect=AssertionError('Warm list must not unpack again')):
                self.assertEqual(mod.thumbnail_path(1),path)
            self.assertEqual(mod.thumbnail_path('../escape'),'')

    def test_png_compression_preserves_all_rgba_pixels_palette_and_metadata(self):
        from PIL import Image
        mod=load(ROOT/'tools/optimize-png.py','test_png_optimizer')
        for mode in ('RGB','RGBA','P'):
            image=Image.new(mode,(200,100));stream=io.BytesIO();image.save(stream,format='PNG',compress_level=0)
            original=stream.getvalue();packed=mod.optimize(original)
            self.assertLess(len(packed),len(original))
            self.assertEqual(Image.open(io.BytesIO(packed)).convert('RGBA').tobytes(),image.convert('RGBA').tobytes())
            self.assertEqual([(k,v) for k,v in mod.chunks(original) if k!=b'IDAT'],[(k,v) for k,v in mod.chunks(packed) if k!=b'IDAT'])

    def test_extra_infobar_samples_cannot_masquerade_as_type_previews(self):
        text=ast.unparse(method('selectScreenShowed','mainFnc'))
        self.assertNotIn('"Title"',text);self.assertNotIn("'Title'",text)
        self.assertIn('thumbnail_path(x)',text)
        self.assertNotIn('b_tl.png',text)
        self.assertIn("ui_text('Type')",text)


if __name__=='__main__':unittest.main()
