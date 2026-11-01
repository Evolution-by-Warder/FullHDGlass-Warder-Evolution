#!/usr/bin/env python3
"""Replay native installer status, completion and log events without running opkg."""
import importlib.util
import json
from pathlib import Path
from types import SimpleNamespace
import unittest
import xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('native_animation_fixture',ROOT/'tools/test-openatv81-animation.py')
native=importlib.util.module_from_spec(spec);spec.loader.exec_module(native)
edits=json.loads((ROOT/'design/openatv81-compatibility/skin-edits.json').read_text())['edits']
edit=next(e for e in edits if e['name']=='Opkg')

class SliderWidget(native.Widget):
    def __init__(self,parent=None): super().__init__(parent);self.value=0
    def setRange(self,minimum,maximum): self.range=(minimum,maximum)
    def setValue(self,value): self.value=value

VariableValue=native.native_class('Components/VariableValue.py','VariableValue',{})
Slider=native.native_class('Components/Slider.py','Slider',{'VariableValue':VariableValue,'GUIComponent':native.GUIComponent,'eSlider':SliderWidget})

class ScrollLabel(native.Label):
    def moveTop(self): pass
    def pageUp(self): pass
    def moveUp(self): pass
    def moveDown(self): pass
    def pageDown(self): pass
    def moveBottom(self): pass

class Screen(dict):
    def __init__(self,session): self.session=session;self.queued=[];self.closed=False
    def setTitle(self,title): self.title=title
    def callLater(self,callback): self.queued.append(callback)
    def close(self,*args): self.closed=True

class ProtectedScreen:
    def __init__(self): pass
    def protectedCallback(self,callback): return callback

class Timer:
    def __init__(self): self.callback=[];self.active=False
    def start(self,*args): self.active=True
    def stop(self): self.active=False

class Actions:
    def __init__(self,*args,**kwargs): self.enabled=True
    def setEnabled(self,value): self.enabled=value

class Transport:
    EVENT_DOWNLOAD=1;EVENT_UPGRADE=2;EVENT_INSTALL=3;EVENT_REMOVE=4;EVENT_CONFIGURING=5;EVENT_ERROR=6;EVENT_DONE=7;EVENT_MODIFIED=8
    def __init__(self): self.callbacks=[];self.running=False;self.cache='installation output\n';self.commands=[]
    def addCallback(self,callback): self.callbacks.append(callback)
    def startCmd(self,*args,**kwargs): self.running=True;self.commands.append((args,kwargs))
    def isRunning(self): return self.running
    def write(self,text): self.response=text

scope={'Screen':Screen,'ProtectedScreen':ProtectedScreen,'Label':native.Label,'StaticText':native.StaticText,'Slider':Slider,'ScrollLabel':ScrollLabel,'eTimer':Timer,'OpkgComponent':Transport,'HelpableActionMap':Actions,'_':lambda value:value,'ngettext':lambda single,multiple,n:single if n==1 else multiple}

def create(path='Screens/Opkg.py',xml=None,commands=None):
    cls=native.native_class(path,'Opkg',scope)
    obj=cls(SimpleNamespace(),cmdList=[('install',{})] if commands is None else commands)
    for component in obj.values():
        if isinstance(component,native.GUIComponent): component.GUIcreate(None)
    obj.rendered={}
    for widget in ET.fromstring(xml or edit['updated_screen']).findall('widget'):
        key=widget.get('source')
        if key in obj:
            render=native.RenderLabel();render.connect(obj[key]);render.GUIcreate(None);obj.rendered[key]=render
    for callback in obj.queued: callback()
    return obj

def displayed(obj,key):
    return obj.rendered[key].instance.text if key in obj.rendered else obj[key].instance.text

class OpkgTests(unittest.TestCase):
    def variants(self): return ('Screens/Opkg.py','legacy/Screens/Opkg.py')
    def test_original_source_binding_stays_at_preparing_after_download(self):
        obj=create(xml=edit['original_screen']);obj.opkgCallback(Transport.EVENT_DOWNLOAD,None)
        self.assertIn('Preparing',displayed(obj,'status'))
        self.assertEqual(obj.status.getText(),'Downloading')
    def test_download_install_configure_and_remove_update_the_visible_labels(self):
        for path in self.variants():
            obj=create(path)
            for event,text in ((Transport.EVENT_DOWNLOAD,'Downloading'),(Transport.EVENT_INSTALL,'Installing'),(Transport.EVENT_CONFIGURING,'Configuring'),(Transport.EVENT_REMOVE,'Removing')):
                obj.opkgCallback(event,'example.ipk');self.assertEqual(displayed(obj,'status'),text)
                if event!=Transport.EVENT_DOWNLOAD:self.assertEqual(displayed(obj,'package'),'example.ipk')
    def test_native_completion_updates_status_counts_and_both_bars(self):
        for path in self.variants():
            obj=create(path);obj.opkgCallback(Transport.EVENT_INSTALL,'example.ipk');obj.opkgCallback(Transport.EVENT_INSTALL,'example.ipk')
            obj.opkg.running=False;obj.opkgCallback(Transport.EVENT_DONE,None)
            self.assertEqual(obj.packages,1);self.assertIn('Done',displayed(obj,'status'))
            self.assertEqual(displayed(obj,'package'),'');self.assertEqual(obj.slider.instance.value,1);self.assertEqual(obj.activityslider.instance.value,0)
            self.assertEqual(obj['key_red'].text,'Close');self.assertEqual(obj['key_blue'].text,'Log')
    def test_empty_transaction_and_error_completion_are_visible(self):
        for path in self.variants():
            obj=create(path,commands=[]);self.assertIn('Done',displayed(obj,'status'));self.assertIn('0 packages',displayed(obj,'status'))
            obj=create(path);obj.opkg.running=False;obj.opkgCallback(Transport.EVENT_ERROR,None)
            self.assertEqual(obj.error,1);self.assertIn('1 error',displayed(obj,'status'))
    def test_activity_timer_moves_the_native_bar(self):
        obj=create()
        for unused in range(15):obj.doActivityTimer()
        self.assertEqual(obj.activityslider.instance.value,15)
    def test_log_and_status_use_the_same_native_components_and_keep_output(self):
        for path in self.variants():
            obj=create(path);obj.commandOutput='first line\nsecond line\n';obj.keyLog()
            self.assertFalse(obj.status.visible);self.assertFalse(obj.package.visible);self.assertTrue(obj['log'].visible)
            self.assertEqual(obj['log'].text,obj.commandOutput);self.assertEqual(obj['key_blue'].text,'Status')
            obj.keyLog();self.assertTrue(obj.status.visible);self.assertTrue(obj.package.visible);self.assertFalse(obj['log'].visible)
            self.assertEqual(obj['key_blue'].text,'Log');self.assertNotIn('status',obj.rendered);self.assertNotIn('package',obj.rendered)
    def test_native_close_stays_disabled_while_installing(self):
        obj=create();obj.keyCancel();self.assertFalse(obj.closed)
        obj.opkg.running=False;obj.keyCancel();self.assertTrue(obj.closed)
    def test_native_progress_bars_and_selection_lists_fit_the_windows(self):
        skin=ET.parse(ROOT/'source/package-root/usr/share/enigma2/hd_glass17/skin.xml')
        screen=skin.find("screen[@name='Opkg']")
        for name in ('status','package'):
            self.assertIsNotNone(screen.find("widget[@name='%s']"%name));self.assertIsNone(screen.find("widget[@source='%s']"%name))
        for name in ('activityslider','slider'):
            bar=screen.find("widget[@name='%s']"%name);self.assertNotIn('pixmap',bar.attrib);self.assertEqual(bar.get('size'),'1680,16')
        for name in ('Opkg','IpkgInstaller','OpkgInstaller'):
            screen=skin.find("screen[@name='%s']"%name);width,height=map(int,screen.get('size').split(','))
            for w in screen.findall('widget'):
                x,y=map(int,w.get('position').split(','));a,b=map(int,w.get('size').split(','))
                self.assertLessEqual(x+a,width);self.assertLessEqual(y+b,height)

if __name__=='__main__':unittest.main(argv=[__file__]+native.rest)
