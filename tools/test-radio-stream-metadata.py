#!/usr/bin/env python3
"""Internet radio parsing, bounded background I/O and stale station ownership."""
import importlib.util
import io
from pathlib import Path
import sys
import threading
import time
import types
import unittest
from unittest.mock import Mock, patch

ROOT=Path(__file__).resolve().parents[1]
PYTHON=ROOT/'source/package-root/usr/lib/enigma2/python'
spec=importlib.util.spec_from_file_location('radio_metadata',PYTHON/'Components/Converter/WarderRadioMetadata.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)

def reference(url='https%3a//radio.example/live',kind='2',engine='4097'):
    return types.SimpleNamespace(toString=lambda:engine+':0:'+kind+':0:0:0:0:0:0:0:'+url)

class Response(io.BytesIO):
    def __init__(self,raw,interval):super().__init__(raw);self.headers={'icy-metaint':str(interval)}

class MetadataTests(unittest.TestCase):
    def test_unicode_artist_and_full_title_are_kept(self):
        self.assertEqual(m.split_song('  Žbirka – Biely kvet (Live)  '),('Žbirka','Biely kvet (Live)'))
    def test_station_slogan_without_artist_separator_is_not_a_song(self):
        self.assertEqual(m.split_song('Radio PSR LIVE'),('',''))
    def test_controls_and_html_entities_are_normalized(self):
        self.assertEqual(m.split_song('A &amp; B\x00 - Song'),('A & B','Song'))
    def test_icy_apostrophe_and_metadata_suffix(self):
        self.assertEqual(m.parse_icy(b"StreamTitle='Guns N' Roses - Don't Cry';StreamUrl='https://x';\0"),("Guns N' Roses","Don't Cry"))
    def test_icy_cp1252_encoding(self):
        self.assertEqual(m.parse_icy("StreamTitle='Beyoncé - Halo';".encode('cp1252')),('Beyoncé','Halo'))
    def test_icy_empty_payload_does_not_reuse_a_previous_song(self):
        self.assertEqual(m.parse_icy(b"StreamTitle='';"),('',''))
    def test_explicit_radio_url_is_decoded(self):
        self.assertEqual(m.stream_url(reference()),'https://radio.example/live')
    def test_tv_stream_never_starts_metadata_fetch(self):
        self.assertEqual(m.stream_url(reference(kind='1')),'')
    def test_dvb_reference_and_local_file_are_not_web_radio(self):
        self.assertEqual(m.stream_url(reference(engine='1')),'')
        self.assertEqual(m.stream_url(reference(url='/tmp/audio.mp3')),'')
    def test_decoded_getpath_preserves_encoded_query(self):
        ref=reference();ref.getPath=lambda:'https://radio.example/live?token=a%2Fb'
        self.assertEqual(m.stream_url(ref),'https://radio.example/live?token=a%2Fb')
    def test_native_artist_and_title_take_priority(self):
        enum=types.SimpleNamespace(sTagArtist=1,sTagTitle=2)
        service=types.SimpleNamespace(info=lambda:types.SimpleNamespace(getInfoString=lambda key:{1:'ABBA',2:'Dancing Queen'}[key]))
        with patch.dict(sys.modules,{'enigma':types.SimpleNamespace(iServiceInformation=enum)}),patch.object(m,'monitor') as monitor:
            self.assertEqual(m.current_song(service,reference()),('ABBA','Dancing Queen'));monitor.song.assert_not_called();monitor.clear.assert_called_once()
    def test_native_combined_title_is_split(self):
        enum=types.SimpleNamespace(sTagArtist=1,sTagTitle=2)
        service=types.SimpleNamespace(info=lambda:types.SimpleNamespace(getInfoString=lambda key:{1:'',2:'ABBA - Dancing Queen'}[key]))
        with patch.dict(sys.modules,{'enigma':types.SimpleNamespace(iServiceInformation=enum)}):self.assertEqual(m.native_song(service),('ABBA','Dancing Queen'))
    def test_fetch_reads_only_the_first_metadata_block(self):
        text=b"StreamTitle='ABBA - Dancing Queen';";size=(len(text)+15)//16
        response=Response(b'x'*32+bytes([size])+text.ljust(size*16,b'\0')+b'audio-not-read',32)
        response.close=lambda:None
        opener=Mock(return_value=response)
        self.assertEqual(m.fetch_icy('https://radio.example',opener=opener),('ABBA','Dancing Queen'))
        self.assertEqual(response.read(),b'audio-not-read')
        self.assertEqual(opener.call_args.kwargs['timeout'],3.0)
        self.assertEqual(opener.call_args.args[0].get_header('Icy-metadata'),'1')
    def test_unbounded_or_missing_interval_is_rejected_without_reading(self):
        for value in (0,-1,256*1024+1,'invalid'):
            response=Response(b'audio',value);response.read=Mock(side_effect=AssertionError('Unbounded read'))
            self.assertEqual(m.fetch_icy('https://radio.example',opener=lambda *a,**kw:response),('',''))
    def test_truncated_icy_payload_is_rejected(self):
        with self.assertRaises(EOFError):m.fetch_icy('https://radio.example',opener=lambda *a,**kw:Response(b'x',32))
    def test_read_deadline_stops_slow_stream(self):
        clock=iter((0,7))
        with self.assertRaises(TimeoutError):m.fetch_icy('https://radio.example',opener=lambda *a,**kw:Response(b'x'*32,32),clock=lambda:next(clock))
    def test_fetch_runs_off_calling_thread_and_station_change_discards_old_result(self):
        started=threading.Event();release=threading.Event();done=threading.Event();caller=threading.get_ident();threads=[]
        def fetch(url):
            threads.append(threading.get_ident());started.set();release.wait(2);done.set();return 'Old artist','Old title'
        monitor=m.IcyMonitor(fetch=fetch)
        self.assertEqual(monitor.song('https://old.example'),('',''));self.assertTrue(started.wait(1))
        self.assertEqual(monitor.song('https://new.example'),('',''));release.set();self.assertTrue(done.wait(1))
        for _ in range(100):
            with monitor.lock:
                if not monitor.busy:break
            time.sleep(.001)
        self.assertEqual(monitor.result,('',''));self.assertNotEqual(threads[0],caller)
    def test_repeated_consumers_share_one_inflight_worker(self):
        release=threading.Event();started=threading.Event();calls=[]
        def fetch(url):calls.append(url);started.set();release.wait(2);return 'A','B'
        monitor=m.IcyMonitor(fetch=fetch);monitor.song('https://radio.example');self.assertTrue(started.wait(1))
        for _ in range(20):monitor.song('https://radio.example')
        self.assertEqual(len(calls),1);monitor.clear();release.set()

class ArtworkOwnershipTests(unittest.TestCase):
    def test_old_station_result_is_discarded_before_it_can_be_painted(self):
        class Renderer:
            def __init__(self):self.instance=Mock()
        enum=types.SimpleNamespace(ePicLoad=Mock(),ePixmap=Mock(),eServiceReference=Mock(),eTimer=Mock(),iRdsDecoder=Mock(),iServiceInformation=Mock())
        nav=types.SimpleNamespace(instance=types.SimpleNamespace(getCurrentService=lambda:None,getCurrentlyPlayingServiceReference=lambda:reference(url='https%3a//new.example')))
        fake={'enigma':enum,'NavigationInstance':nav,'Components.Renderer.Renderer':types.SimpleNamespace(Renderer=Renderer),'Components.Converter.WarderRadioMetadata':m}
        path=PYTHON/'Components/Renderer/WarderRadioArtwork.py';spec=importlib.util.spec_from_file_location('radio_artwork_test',path);art=importlib.util.module_from_spec(spec)
        with patch.dict(sys.modules,fake):spec.loader.exec_module(art)
        obj=art.WarderRadioArtwork();obj._serviceKey='old';obj._generation=3;obj._key='old-song';obj._result=(3,'old-song','/tmp/old-cover.jpg')
        obj._showFallback=Mock();obj._showPath=Mock();obj._radioText=lambda:'';obj._dabSlidePath=lambda:''
        with patch.object(art,'current_song',return_value=('','')):obj._poll()
        obj._showPath.assert_not_called();obj._showFallback.assert_called_once();self.assertEqual(obj._generation,4)

class NativeTextIntegrationTests(unittest.TestCase):
    def load(self,ref):
        timer=Mock();timer.callback=[]
        label=Mock();nav=types.SimpleNamespace(getCurrentlyPlayingServiceReference=lambda:ref,getCurrentService=lambda:None)
        bar=types.SimpleNamespace(session=types.SimpleNamespace(nav=nav),rds_display={"RadioText":label},onClose=[],instance=None)
        fake={'enigma':types.SimpleNamespace(eTimer=lambda:timer),'Components.Converter.WarderRadioMetadata':m,'Components.Converter.WarderRadioOnly':types.SimpleNamespace(is_radio_reference=lambda ref:True)}
        path=PYTHON/'Plugins/Extensions/setupGlass17/warderRadioWindows.py';spec=importlib.util.spec_from_file_location('radio_windows_test',path);windows=importlib.util.module_from_spec(spec)
        with patch.dict(sys.modules,fake):spec.loader.exec_module(windows)
        return windows.RadioWindowTransparency(bar),label,timer
    def test_stream_text_uses_the_existing_native_radio_label(self):
        controller,label,timer=self.load(reference())
        with patch.dict(sys.modules,{'enigma':types.SimpleNamespace(iServiceInformation=types.SimpleNamespace())}),patch.object(m,'monitor') as monitor:
            monitor.song.return_value=('Artist','Song')
            controller.update()
        label.setText.assert_called_with('Artist - Song');label.show.assert_called_once();timer.start.assert_called_once_with(1000)
    def test_dvb_rds_text_is_never_overwritten(self):
        controller,label,timer=self.load(reference(engine='1'))
        with patch.object(m,'monitor'):controller.update()
        label.setText.assert_not_called();timer.start.assert_not_called();timer.stop.assert_called_once()
    def test_tv_transition_stops_metadata_polling(self):
        controller,label,timer=self.load(reference(kind='1'))
        with patch.object(m.monitor,'clear') as clear:controller.update_song();clear.assert_called_once()
        timer.stop.assert_called_once();label.setText.assert_not_called()

if __name__=='__main__':unittest.main()
