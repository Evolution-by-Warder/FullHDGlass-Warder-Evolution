#!/usr/bin/env python3
"""Choosing a radio country closes the old native Radio list, not playback/TV.

The model's 224 signed country ZIPs are loaded only after the user's choice
is safely saved. Closing ChannelSelectionRadio is UI-only; the worker must
already be scheduled and may continue while the native list is closed.
"""
import sys
import unittest
from pathlib import Path
from types import ModuleType, SimpleNamespace
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'source/package-root/usr/lib/enigma2/python'))
from Plugins.Extensions.setupGlass17 import warderRadioCountry as country

class ChannelSelectionRadio:
    def __init__(self,events,shown=True):
        self.shown=shown
        self.events=events
    def cancel(self):
        self.events.append('native-radio-cancel')

class ChannelSelection:
    def __init__(self,events):
        self.shown=True
        self.events=events
    def cancel(self):
        self.events.append('TV-WRONG-CANCEL')

class ScreensHarness:
    def __enter__(self):
        screens=ModuleType('Screens');screens.__path__=[]
        choice=ModuleType('Screens.ChoiceBox')
        choice.ChoiceBox=type('ChoiceBox',(),{})
        message=ModuleType('Screens.MessageBox')
        message.MessageBox=type('MessageBox',(),{'TYPE_INFO':0})
        ui=ModuleType('Plugins.Extensions.setupGlass17.warderUiText')
        ui.ui_text=lambda text:text
        self.patch=patch.dict(sys.modules,{'Screens':screens,
              'Screens.ChoiceBox':choice,'Screens.MessageBox':message,
              'Plugins.Extensions.setupGlass17.warderUiText':ui})
        return self.patch.__enter__()
    def __exit__(self,*args):
        self.patch.__exit__(*args)

class Session:
    def __init__(self,current=None):
        self.current_dialog=current
        self.callback=None
        self.open_calls=[]
    def openWithCallback(self,callback,widget,**kwargs):
        self.callback=callback
        self.open_calls.append(('chooser',kwargs))
    def open(self,widget,*args,**kwargs):
        self.open_calls.append(('message',args,kwargs))
    def select(self,code):
        self.callback(('Germany',code))

class Tests(unittest.TestCase):
    def picker(self,session,request,schedule,radio=None):
        with ScreensHarness(),patch.object(country,'country_options',
                  return_value=[('Germany','DE'),('Slovakia','SK')]),\
            patch.object(country,'active_country',return_value='SK'),\
            patch.object(country,'_choice',return_value={}),\
            patch.object(country,'_queued_country',return_value=None),\
            patch.object(country,'request_country',side_effect=request),\
            patch.object(country,'_start_selected_country_refresh',
                         side_effect=schedule):
            country.open_country_selector(session,channel_selection=radio)
            yield session

    def test_success_closes_native_radio_after_worker_schedule(self):
        events=[]
        radio=ChannelSelectionRadio(events)
        session=Session(radio)
        def request(code):
            events.append('saved-'+code)
            return {'accepted':True,'already_active':False}
        def schedule(_):
            events.append('scheduled-background-worker')
            return True
        for session in self.picker(session,request,schedule,radio):
            session.select('DE')
        self.assertEqual(events,
          ['saved-DE','scheduled-background-worker','native-radio-cancel'])
        self.assertEqual(session.open_calls[0][0],'chooser')
        self.assertEqual(len(session.open_calls),1)

    def test_cancel_or_invalid_request_does_not_close(self):
        events=[]
        radio=ChannelSelectionRadio(events)
        session=Session(radio)
        for session in self.picker(session,lambda cc:{'accepted':False},
                                   lambda ss:True,radio):
            session.callback(None)
            self.assertEqual(events,[])
            session.select('DE')
        self.assertEqual(events,[])
        self.assertEqual(session.open_calls[-1][0],'message')

    def test_no_worker_scheduled_does_not_hide_problem(self):
        events=[]
        radio=ChannelSelectionRadio(events)
        session=Session(radio)
        for session in self.picker(session,lambda cc:{'accepted':True},
                                   lambda ss:False,radio):
            session.select('DE')
        self.assertEqual(events,[])
        self.assertEqual(session.open_calls[-1][0],'message')

    def test_already_selected_country_may_close_radio_without_new_worker(self):
        events=[]
        radio=ChannelSelectionRadio(events)
        session=Session(radio)
        def unexpected(_):self.fail("No worker for already active country")
        for session in self.picker(session,lambda cc:{
            'accepted':True,'already_active':True},unexpected,radio):
            session.select('SK')
        self.assertEqual(events,['native-radio-cancel'])

    def test_only_native_radio_list_may_close_not_tv_or_player(self):
        events=[]
        tv=ChannelSelection(events)
        session=Session(tv)
        self.assertFalse(country._close_radio_list_after_country_choice(session,tv))
        self.assertEqual(events,[])
        # Can still find an underlying native radio dialog.
        radio=ChannelSelectionRadio(events)
        session.current_dialog=radio
        self.assertTrue(country._close_radio_list_after_country_choice(session))
        self.assertEqual(events,['native-radio-cancel'])

    def test_hidden_or_missing_radio_is_not_force_closed(self):
        events=[]
        radio=ChannelSelectionRadio(events,shown=False)
        session=Session(radio)
        self.assertFalse(country._close_radio_list_after_country_choice(session,radio))
        self.assertFalse(country._close_radio_list_after_country_choice(Session()))
        self.assertEqual(events,[])

if __name__=='__main__':
    unittest.main(verbosity=2)
