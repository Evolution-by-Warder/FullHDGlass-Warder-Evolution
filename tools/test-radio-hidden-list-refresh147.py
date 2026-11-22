#!/usr/bin/env python3
"""GigaBlue regression: reopening RADIO after country switch must not show old UK.

OpenATV keeps InfoBar.instance.servicelist instantiated after the context
selection exits. Reloading eDVBDB does NOT reset this hidden ServiceList.
The worker must invalidate that exact radio bouquet's native C++ root, even
when neither it nor ChannelSelection is visible, without touching TV lists.
"""
import sys
import tempfile
import unittest
from pathlib import Path
from types import ModuleType, SimpleNamespace
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'source/package-root/usr/lib/enigma2/python'))
from Plugins.Extensions.setupGlass17 import warderRadioLive as live

class Call:
    def __init__(self,delay,fn):
        self.delay,self.fn,self.cancelled=delay,fn,False
    def active(self):
        return not self.cancelled
    def cancel(self):
        self.cancelled=True

class Loop:
    def __init__(self):self.calls=[]
    def callLater(self,delay,fn):
        call=Call(delay,fn);self.calls.append(call);return call

class ListWidget:
    def __init__(self,events,old='United Kingdom'):
        self.events=events;self.country=old
        self.instance=object()
    def resetRoot(self):
        self.events.append('resetRoot')
        self.country='United States'  # Native C++ re-queries the changed eDVBDB.
    def goTop(self):
        self.events.append('goTop')

class ChannelSelection:
    def __init__(self,events,mode=1,path=None,shown=False):
        self.events=events;self.mode=mode;self.shown=shown
        self.onShown=[]
        self.path=path or 'FROM BOUQUET "'+live.FILE+'" ORDER BY bouquet'
        self.servicelist=ListWidget(events)
    def getCurrentMode(self):return self.mode
    def getRoot(self):return SimpleNamespace(getPath=lambda:self.path)

class ChannelSelectionRadio:
    def __init__(self,events,shown=False):
        self.shown=shown;self.servicelist=ListWidget(events)
    def getRoot(self):
        return SimpleNamespace(getPath=lambda:'FROM BOUQUET "'+live.FILE+'" ORDER BY bouquet')

class InfoBarModules:
    def __init__(self,servicelist):
        screens=ModuleType('Screens')
        screens.__path__=[]
        info=ModuleType('Screens.InfoBar')
        info.InfoBar=SimpleNamespace(instance=SimpleNamespace(servicelist=servicelist))
        self.patch=patch.dict(sys.modules,{'Screens':screens,'Screens.InfoBar':info})
    def __enter__(self):return self.patch.__enter__()
    def __exit__(self,*args):return self.patch.__exit__(*args)

class Tests(unittest.TestCase):
    def controller(self,events,session=None):
        ctrl=live.Controller.__new__(live.Controller)
        ctrl.closed=False
        ctrl.session=session or SimpleNamespace(current_dialog=SimpleNamespace(shown=True))
        ctrl.loop=Loop()
        ctrl.radio_refresh_timer=None
        ctrl.worker=object()
        ctrl.timeout=None
        ctrl.pending=None
        ctrl.icon_timer=None
        ctrl.icon_worker=None
        ctrl.initial_reload=False
        ctrl.local_worker_key=('US','b'*64)
        ctrl.active_local_key=None
        ctrl.reload=lambda:events.append('eDVBDB.reloadBouquets')
        ctrl._load_icon_map=lambda:events.append('load new US picons')
        return ctrl

    def test_hidden_persistent_infobar_radio_root_reloads_us_before_next_open(self):
        events=[]
        radio=ChannelSelection(events,shown=False)
        self.assertEqual(radio.servicelist.country,'United Kingdom')
        ctrl=self.controller(events)
        with InfoBarModules(radio):
            self.assertTrue(ctrl._refresh_visible_radio_list(reset_to_top=True))
        self.assertEqual(events,['resetRoot','goTop'])
        self.assertEqual(radio.servicelist.country,'United States')
        self.assertFalse(radio.shown)  # Do not reopen radio just to refresh.

    def test_hidden_native_radio_reloads_after_worker_success(self):
        events=[]
        radio=ChannelSelection(events,shown=False)
        ctrl=self.controller(events)
        with tempfile.TemporaryDirectory() as t:
            base=Path(t)
            (base/live.FILE).write_text('#NAME Warder Radio Live\n')
            with patch.object(live,'DIRECTORY',base),InfoBarModules(radio):
                ctrl.finished({'changed':True,'country':'US','local':True,'first_page':True})
                self.assertEqual(radio.servicelist.country,'United States')
                self.assertLess(events.index('eDVBDB.reloadBouquets'),events.index('resetRoot'))
                delayed=[c for c in ctrl.loop.calls if c.delay==1]
                self.assertEqual(len(delayed),1)
                delayed[0].fn()
                self.assertEqual(events.count('resetRoot'),2)
                self.assertTrue(any(c.delay==3600 for c in ctrl.loop.calls))

    def test_does_not_touch_tv_list_even_with_same_bouquet_reference(self):
        events=[];tv=ChannelSelection(events,mode=0,shown=False)
        ctrl=self.controller(events)
        with InfoBarModules(tv):
            self.assertFalse(ctrl._refresh_visible_radio_list())
        self.assertEqual(events,[])
        self.assertEqual(tv.servicelist.country,'United Kingdom')

    def test_does_not_touch_personal_radio_bouquet(self):
        events=[];other=ChannelSelection(events,mode=1,
          path='FROM BOUQUET "userbouquet.personal.radio" ORDER BY bouquet')
        ctrl=self.controller(events)
        with InfoBarModules(other):
            self.assertFalse(ctrl._refresh_visible_radio_list())
        self.assertEqual(events,[])

    def test_separate_native_radio_class_even_when_hidden(self):
        events=[];radio=ChannelSelectionRadio(events,shown=False)
        ctrl=self.controller(events)
        with InfoBarModules(radio):
            self.assertTrue(ctrl._refresh_visible_radio_list())
        self.assertEqual(events,['resetRoot','goTop'])

    def test_no_session_but_infobar_radio_is_reusable(self):
        events=[];radio=ChannelSelection(events,shown=False)
        ctrl=self.controller(events)
        ctrl.session=None
        with InfoBarModules(radio):
            self.assertTrue(ctrl._refresh_visible_radio_list())
        self.assertEqual(events,['resetRoot','goTop'])

    def test_hidden_tv_mode_refreshes_only_when_radio_list_is_reopened(self):
        events=[]
        radio=ChannelSelection(events,mode=0,shown=False)
        ctrl=self.controller(events)
        with tempfile.TemporaryDirectory() as t:
            base=Path(t)
            (base/live.FILE).write_text('#NAME Warder Radio Live\\n')
            with patch.object(live,'DIRECTORY',base),InfoBarModules(radio):
                ctrl.finished({'changed':True,'country':'US','local':True,'first_page':True})
                self.assertEqual(events.count('resetRoot'),0)
                self.assertEqual(len(radio.onShown),1)
                # OpenATV's persistent list was kept in TV mode by native
                # cancel(). As soon as Radio is reopened it must reload US.
                radio.mode=1
                radio.shown=True
                for callback in list(radio.onShown):
                    callback()
                self.assertEqual(events.count('resetRoot'),1)
                self.assertEqual(radio.servicelist.country,'United States')
                self.assertEqual(radio.onShown,[])

    def test_tv_onshown_is_ignored_until_radio_mode(self):
        events=[]
        radio=ChannelSelection(events,mode=0,shown=False)
        ctrl=self.controller(events)
        with InfoBarModules(radio):
            self.assertTrue(ctrl._arm_radio_list_refresh_on_show())
            for callback in list(radio.onShown):
                callback()
            self.assertEqual(events,[])
            self.assertEqual(len(radio.onShown),1)
            radio.mode=1
            for callback in list(radio.onShown):
                callback()
            self.assertEqual(events,['resetRoot','goTop'])
            self.assertEqual(radio.onShown,[])

    def test_exit_removes_one_shot_native_radio_hook(self):
        events=[]
        radio=ChannelSelection(events,mode=1,shown=False)
        ctrl=self.controller(events)
        with InfoBarModules(radio):
            self.assertTrue(ctrl._arm_radio_list_refresh_on_show())
            self.assertEqual(len(radio.onShown),1)
            ctrl._disarm_radio_list_refresh_on_show()
            self.assertEqual(radio.onShown,[])

    def test_only_list_in_active_radio_mode_reloaded_deduplicated(self):
        events=[];radio=ChannelSelection(events,shown=False)
        ctrl=self.controller(events,session=SimpleNamespace(current_dialog=radio))
        with InfoBarModules(radio):
            self.assertTrue(ctrl._refresh_visible_radio_list())
        self.assertEqual(events.count('resetRoot'),1)

if __name__=='__main__':unittest.main(verbosity=2)
