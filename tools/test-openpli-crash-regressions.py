#!/usr/bin/env python3
"""Replay reported dialog failures with the actual image MessageBox controller."""
import argparse
import ast
from pathlib import Path
import sys
from types import SimpleNamespace, ModuleType
from unittest.mock import patch
import unittest
import xml.etree.ElementTree as ET

parser=argparse.ArgumentParser()
parser.add_argument('--upstream',type=Path,required=True)
parser.add_argument('--package-root',type=Path)
args,rest=parser.parse_known_args()
ROOT=Path(__file__).resolve().parents[1]
PAYLOAD=args.package_root or ROOT/'source/package-root'
PLUGIN=PAYLOAD/'usr/lib/enigma2/python/Plugins/Extensions/setupGlass17'

class Widget:
    def __init__(self,*args,**kwargs):
        self.text=args[0] if args else '';self.instance=self;self.visible=True;self.index=0
        self.list=args[0] if args and isinstance(args[0],list) else []
    def hide(self):self.visible=False
    def setText(self,text):self.text=text
    def getCurrent(self):return self.list[self.index]
    def moveToIndex(self,index):self.index=index
    def pageUp(self):pass
    def pageDown(self):pass
    def getSize(self):return (800,140)
    def resize(self,size):self.size=size
    def move(self,point):self.point=point

class Screen(dict):
    def __init__(self,session,*args,**kwargs):
        super().__init__();self.session=session;self.execing=False;self.onClose=[];self.onShown=[];self.onExecBegin=[];self.onLayoutFinish=[];self.instance=Widget()
    def setTitle(self,title,**kwargs):self.title=title
    def close(self,result):self.result=result

class Timer:
    def __init__(self):self.callback=[];self.stopped=False
    def stop(self):self.stopped=True
    def start(self,*args):pass

class Actions:
    def __init__(self,*args,**kwargs):self.actions=next(v for v in args if isinstance(v,dict))
    def setEnabled(self,value):self.enabled=value

native_tree=ast.parse((args.upstream/'Screens/MessageBox.py').read_text())
native_class=next(n for n in native_tree.body if isinstance(n,ast.ClassDef) and n.name=='MessageBox')
scope={'Screen':Screen,'Label':Widget,'StaticText':Widget,'MenuList':Widget,'Pixmap':Widget,'MultiPixmap':Widget,'ActionMap':Actions,'HelpableActionMap':Actions,'eTimer':Timer,'_':lambda s:s}
exec(compile(ast.Module(body=[native_class],type_ignores=[]),'native-MessageBox','exec'),scope)
Native=scope['MessageBox']
own_tree=ast.parse((PLUGIN/'warderDialogs.py').read_text())
classes=[n for n in own_tree.body if isinstance(n,ast.ClassDef) and n.name in ('MessageText','MessageBox')]
scope.update(NativeMessageBox=Native,ScrollLabel=Widget,ActionMap=Actions,MESSAGE_SKIN='<screen/>',ui_text=lambda s:s,update_text=lambda *a,**k:'Confirm',config=SimpleNamespace(osd=SimpleNamespace(language=SimpleNamespace(value='sk'))))
exec(compile(ast.Module(body=classes,type_ignores=[]),'warderDialogs','exec'),scope)
Owned=scope['MessageBox']

class CrashRegressions(unittest.TestCase):
    def test_information_confirmation_cancel_and_close_with_optional_timers(self):
        for timeout in (-1,0,5):
            for kind in (Native.TYPE_INFO,Native.TYPE_ERROR):
                box=Owned(None,'Result',kind,timeout)
                box['warderActions'].actions['green']();self.assertIs(box.result,True)
                box['warderActions'].actions['red']();self.assertIs(box.result,False)
                for callback in box.onClose:callback()
                if hasattr(box,'timer'):self.assertTrue(box.timer.stopped)
    def test_yes_no_preserves_selected_result_with_default_false(self):
        for default in (False,True):
            box=Owned(None,'Reset?',Native.TYPE_YESNO,default=default)
            for index in (0,1):
                box['list'].moveToIndex(index)
                expected=box['list'].getCurrent()[1]
                box['warderActions'].actions['green']()
                self.assertIs(box.result,expected)
    def test_disabled_input_and_native_timer_cleanup(self):
        box=Owned(None,'Please wait',Native.TYPE_INFO,timeout=5,enable_input=False)
        self.assertFalse(box['warderActions'].enabled)
        self.assertFalse(box['key_red'].visible)
        # OpenPLi may delete the optional timer in stopTimer before close.
        if hasattr(box,'timer'):del box.timer
        for callback in box.onClose:callback()
    def test_native_timeout_keeps_confirmation_semantics(self):
        box=Owned(None,'Result',Native.TYPE_INFO,timeout=5)
        if hasattr(box,'timeoutCallback'):
            box.timeoutCallback();self.assertIs(box.result,True)
    def test_shipped_message_applet_uses_integer_coordinates(self):
        def coordinates(x,y):
            self.assertIs(type(x),int);self.assertIs(type(y),int);return (x,y)
        module=ModuleType('enigma');module.eSize=coordinates;module.ePoint=coordinates
        module.getDesktop=lambda _:SimpleNamespace(size=lambda:SimpleNamespace(width=lambda:1919,height=lambda:1079))
        tree=ET.parse(PAYLOAD/'usr/share/enigma2/hd_glass17/skin.xml')
        script=tree.find("screen[@name='MessageBox']/applet").text
        for choices in ([],[('Yes',True),('No',False)]):
            box=Screen(None);box.list=choices;box['text']=Widget();box['list']=Widget(choices)
            with patch.dict(sys.modules,{'enigma':module}):exec(compile(script,'shipped-message-applet','exec'),{'self':box})

if __name__=='__main__':unittest.main(argv=[sys.argv[0]]+rest)
