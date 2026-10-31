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
sys.path.insert(0,str(PYTHON/'Plugins/Extensions/setupGlass17'))
spec=importlib.util.spec_from_file_location('radio_metadata',PYTHON/'Components/Converter/WarderRadioMetadata.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)

def reference(url='https%3a//radio.example/live',kind='2',engine='4097'):
    return types.SimpleNamespace(toString=lambda:engine+':0:'+kind+':0:0:0:0:0:0:0:'+url)

class Response(io.BytesIO):
    def __init__(self,raw,interval):super().__init__(raw);self.headers={'icy-metaint':str(interval)}

class MetadataTests(unittest.TestCase):
    def test_receiver_reported_compound_name_is_repaired_in_icy_metadata(self):
        self.assertEqual(m.parse_icy(b"StreamTitle='KARMEN PAL - BALAZ-Pustam ta';"),('Karmen Pál-Baláž','Pustam ta'))
    def test_compound_name_repair_is_shared_by_split_native_and_combined_tags(self):
        enum=types.SimpleNamespace(sTagArtist=1,sTagTitle=2)
        for artist,title in [('KARMEN PAL','BALAZ-Pustam ta'),('','KARMEN PAL - BALAZ-Pustam ta')]:
            service=types.SimpleNamespace(info=lambda:types.SimpleNamespace(getInfoString=lambda n:{1:artist,2:title}[n]))
            with patch.dict(sys.modules,{'enigma':types.SimpleNamespace(iServiceInformation=enum)}):
                self.assertEqual(m.native_song(service),('Karmen Pál-Baláž','Pustam ta'))
    def test_numbered_title_artist_stream_is_parsed_without_track_number(self):
        self.assertEqual(m.split_song('08 - Krasnejsi nez ruze (Maliconia) - Pavel Roth'),('Pavel Roth','Krasnejsi nez ruze (Maliconia)'))
    def test_native_tags_split_at_track_number_are_repaired_too(self):
        enum=types.SimpleNamespace(sTagArtist=1,sTagTitle=2)
        service=types.SimpleNamespace(info=lambda:types.SimpleNamespace(getInfoString=lambda n:{1:'08',2:'Krasnejsi nez ruze (Maliconia) - Pavel Roth'}[n]))
        with patch.dict(sys.modules,{'enigma':types.SimpleNamespace(iServiceInformation=enum)}):
            self.assertEqual(m.native_song(service),('Pavel Roth','Krasnejsi nez ruze (Maliconia)'))
    def test_attached_track_number_is_repaired_in_stream_and_native_tags(self):
        self.assertEqual(m.split_song('24_Pavol Habera - Reklama na ticho (remix)'),('Pavol Habera','Reklama na ticho (remix)'))
        enum=types.SimpleNamespace(sTagArtist=1,sTagTitle=2)
        service=types.SimpleNamespace(info=lambda:types.SimpleNamespace(getInfoString=lambda n:{1:'24_Pavol Habera',2:'Reklama na ticho (remix)'}[n]))
        with patch.dict(sys.modules,{'enigma':types.SimpleNamespace(iServiceInformation=enum)}):
            self.assertEqual(m.native_song(service),('Pavol Habera','Reklama na ticho (remix)'))
    def test_missing_hyphen_spaces_do_not_leave_full_song_as_an_announcement(self):
        self.assertEqual(m.split_song('MIROSLAV ZBIRKA-Biely Kvet'),('MIROSLAV ZBIRKA','Biely Kvet'))
        enum=types.SimpleNamespace(sTagArtist=1,sTagTitle=2)
        service=types.SimpleNamespace(info=lambda:types.SimpleNamespace(getInfoString=lambda n:{1:'',2:'MIROSLAV ZBIRKA-Biely Kvet'}[n]))
        with patch.dict(sys.modules,{'enigma':types.SimpleNamespace(iServiceInformation=enum)}):
            self.assertEqual(m.native_song(service),('MIROSLAV ZBIRKA','Biely Kvet'))
        for tag in ('Jay-Z','Jean-Michel Jarre','AC-DC','Hudba na maximum'):
            self.assertEqual(m.split_song(tag),('',''))
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
    def test_icy_announcement_is_preserved_without_becoming_a_song(self):
        self.assertEqual(m.parse_icy(b"StreamTitle='Hudba na maximum';"), ('', 'Hudba na maximum'))
        self.assertEqual(m.split_song('Hudba na maximum'), ('', ''))
    def test_native_announcement_overrides_cached_icy_song(self):
        enum=types.SimpleNamespace(sTagArtist=1,sTagTitle=2)
        values={1:'',2:'Hudba na maximum'}
        service=types.SimpleNamespace(info=lambda:types.SimpleNamespace(getInfoString=lambda key:values[key]))
        with patch.dict(sys.modules,{'enigma':types.SimpleNamespace(iServiceInformation=enum)}),patch.object(m,'monitor') as monitor:
            monitor.song.return_value=('Old artist','Old song')
            self.assertEqual(m.current_song(service,reference()), ('','Hudba na maximum'))
            monitor.song.assert_not_called();monitor.clear.assert_called_once()
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
    def test_artist_only_native_tag_still_allows_icy_song_lookup(self):
        enum=types.SimpleNamespace(sTagArtist=1,sTagTitle=2)
        service=types.SimpleNamespace(info=lambda:types.SimpleNamespace(getInfoString=lambda key:{1:'Station name',2:''}[key]))
        with patch.dict(sys.modules,{'enigma':types.SimpleNamespace(iServiceInformation=enum)}),patch.object(m,'monitor') as monitor:
            monitor.song.return_value=('Artist','Current song')
            self.assertEqual(m.current_song(service,reference()),('Artist','Current song'))
            monitor.song.assert_called_once_with('https://radio.example/live');monitor.clear.assert_not_called()
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

class ArtworkRetryTests(unittest.TestCase):
    def test_failed_song_gets_one_delayed_retry_and_then_stops(self):
        class Renderer:
            def __init__(self):self.instance=Mock()
        timer=Mock();timer.callback=[]
        enum=types.SimpleNamespace(ePicLoad=Mock(),ePixmap=Mock(),eServiceReference=Mock(),eTimer=lambda:timer,iRdsDecoder=Mock(),iServiceInformation=Mock())
        ref=reference();nav=types.SimpleNamespace(instance=types.SimpleNamespace(getCurrentService=lambda:None,getCurrentlyPlayingServiceReference=lambda:ref))
        fake={'enigma':enum,'NavigationInstance':nav,'Components.Renderer.Renderer':types.SimpleNamespace(Renderer=Renderer),'Components.Converter.WarderRadioMetadata':m}
        spec=importlib.util.spec_from_file_location('retry_artwork',PYTHON/'Components/Renderer/WarderRadioArtwork.py');art=importlib.util.module_from_spec(spec)
        with patch.dict(sys.modules,fake):spec.loader.exec_module(art)
        obj=art.WarderRadioArtwork();obj._serviceKey=ref.toString();obj._key='a|b';obj._requestedKey='a|b';obj._attempts=1;obj._result=(0,'a|b','')
        obj._showPath=Mock();obj._showFallback=Mock();obj._radioText=lambda:'A - B';obj._dabSlidePath=lambda:'';obj._request=Mock()
        with patch.object(art.time,'monotonic',return_value=100):obj._poll()
        obj._request.assert_not_called();self.assertEqual(obj._retryAt,115)
        with patch.object(art.time,'monotonic',return_value=116):obj._poll()
        obj._request.assert_called_once_with('A','B','a|b')
        obj._request.reset_mock();obj._attempts=2;obj._result=(0,'a|b','')
        with patch.object(art.time,'monotonic',return_value=200):obj._poll()
        obj._request.assert_not_called()
        obj._radioText=lambda:'C - D'
        with patch.object(art.time,'monotonic',return_value=200):obj._poll()
        obj._request.assert_called_once_with('C','D','c|d');self.assertEqual(obj._attempts,0)

class ArtworkStabilityTests(unittest.TestCase):
    def setUp(self):
        class Renderer:
            def __init__(self):self.instance=Mock()
        self.timer=Mock();self.timer.callback=[]
        enum=types.SimpleNamespace(ePicLoad=Mock(),ePixmap=Mock(),eServiceReference=Mock(),eTimer=lambda:self.timer,iRdsDecoder=Mock(),iServiceInformation=Mock())
        self.ref=reference();self.nav=types.SimpleNamespace(getCurrentService=lambda:None,getCurrentlyPlayingServiceReference=lambda:self.ref)
        fake={'enigma':enum,'NavigationInstance':types.SimpleNamespace(instance=self.nav),'Components.Renderer.Renderer':types.SimpleNamespace(Renderer=Renderer),'Components.Converter.WarderRadioMetadata':m}
        spec=importlib.util.spec_from_file_location('stable_artwork',PYTHON/'Components/Renderer/WarderRadioArtwork.py');self.art=importlib.util.module_from_spec(spec)
        with patch.dict(sys.modules,fake):spec.loader.exec_module(self.art)
        self.obj=self.art.WarderRadioArtwork();self.obj._serviceKey=self.ref.toString();self.obj._key='tiffany aris|vertigo';self.obj._requestedKey=self.obj._key;self.obj._songPair=('tiffany aris','vertigo')
        self.obj._showPath=Mock();self.obj._showFallback=Mock();self.obj._request=Mock();self.obj._dabSlidePath=lambda:''

    def test_metadata_field_order_change_keeps_the_current_cover(self):
        self.obj._radioText=lambda:'Vertigo - Tiffany Aris'
        self.obj._poll()
        self.obj._showFallback.assert_not_called();self.obj._request.assert_not_called()
        self.assertEqual(self.obj._key,'tiffany aris|vertigo')

    def test_short_metadata_gap_keeps_cover_but_long_gap_clears_it(self):
        self.obj._radioText=lambda:''
        with patch.object(self.art,'current_song',return_value=('','')):
            with patch.object(self.art.time,'monotonic',return_value=100):self.obj._poll()
            with patch.object(self.art.time,'monotonic',return_value=104):self.obj._poll()
            self.obj._showFallback.assert_not_called()
            with patch.object(self.art.time,'monotonic',return_value=106):self.obj._poll()
        self.obj._showFallback.assert_called_once()

    def test_standalone_announcement_never_starts_an_artwork_lookup(self):
        self.obj._radioText=lambda:'Hudba na maximum'
        with patch.object(self.art,'current_song',return_value=('','Hudba na maximum')):
            with patch.object(self.art.time,'monotonic',return_value=100):self.obj._poll()
            with patch.object(self.art.time,'monotonic',return_value=106):self.obj._poll()
        self.obj._request.assert_not_called();self.obj._showFallback.assert_called_once()
    def test_new_song_clears_previous_cover_without_grace(self):
        self.obj._radioText=lambda:'Ukitas - Uncovered Paradise';self.obj._poll()
        self.obj._showFallback.assert_called_once();self.obj._request.assert_called_once()

    def test_station_change_never_retains_old_cover_during_metadata_gap(self):
        self.nav.getCurrentlyPlayingServiceReference=lambda:reference(url='https%3a//different.example')
        self.obj._radioText=lambda:''
        with patch.object(self.art,'current_song',return_value=('','')):self.obj._poll()
        self.obj._showFallback.assert_called_once();self.assertEqual(self.obj._key,'')

    def test_late_decoder_callback_cannot_clear_new_decoder_or_pixmap(self):
        new=Mock();self.obj._picload=new;self.obj._decodeToken=2
        self.obj._decoded(token=1)
        self.assertIs(self.obj._picload,new);self.obj.instance.setPixmap.assert_not_called()
        self.obj._decoded(token=2)
        self.obj.instance.setPixmap.assert_called_once_with(new.getData.return_value)
        self.assertIsNone(self.obj._picload)

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
    def test_announcement_and_song_transitions_update_the_same_label(self):
        controller,label,timer=self.load(reference())
        samples=[('Artist','Song'),('','Hudba na maximum'),('Next artist','Next song'),('','')]
        with patch.dict(sys.modules,{'enigma':types.SimpleNamespace(iServiceInformation=types.SimpleNamespace())}),patch.object(m,'monitor') as monitor:
            monitor.song.side_effect=samples
            for expected in ('Artist - Song','Hudba na maximum','Next artist - Next song',''):
                controller.update_song();label.setText.assert_called_with(expected)
        self.assertEqual(label.show.call_count,3)
    def test_dvb_rds_text_is_never_overwritten(self):
        controller,label,timer=self.load(reference(engine='1'))
        with patch.object(m,'monitor'):controller.update()
        label.setText.assert_not_called();timer.start.assert_not_called();timer.stop.assert_called_once()
    def test_tv_transition_stops_metadata_polling(self):
        controller,label,timer=self.load(reference(kind='1'))
        with patch.object(m.monitor,'clear') as clear:controller.update_song();clear.assert_called_once()
        timer.stop.assert_called_once();label.setText.assert_not_called()


class CatalogueArtworkTests(unittest.TestCase):
    def setUp(self):
        fake = {
            'enigma': types.SimpleNamespace(**{name: Mock() for name in
                ('ePicLoad', 'ePixmap', 'eServiceReference', 'eTimer', 'iRdsDecoder', 'iServiceInformation')}),
            'NavigationInstance': types.SimpleNamespace(instance=None),
            'Components.Renderer.Renderer': types.SimpleNamespace(Renderer=object),
            'Components.Converter.WarderRadioMetadata': m,
        }
        spec = importlib.util.spec_from_file_location('catalogue_artwork_test', PYTHON/'Components/Renderer/WarderRadioArtwork.py')
        self.art = importlib.util.module_from_spec(spec)
        with patch.dict(sys.modules, fake):
            spec.loader.exec_module(self.art)
        self.cls = self.art.WarderRadioArtwork
        self.cover = b'\xff\xd8' + b'x' * 2048

    def lookup(self, artist, title, results):
        import json
        from urllib.parse import parse_qs, urlparse
        self.calls = []
        def opener(req, **kwargs):
            self.calls.append(req.full_url)
            if '/search?' not in req.full_url:
                return io.BytesIO(self.cover)
            country = parse_qs(urlparse(req.full_url).query)['country'][0]
            value = results.get(country, [])
            if isinstance(value, Exception):
                raise value
            return io.BytesIO(json.dumps({'results': value}).encode())
        import tempfile
        with tempfile.TemporaryDirectory() as cache, patch.object(self.cls, '_cacheDir', return_value=cache), patch.object(self.art, 'urlopen', side_effect=opener), patch.object(self.cls, '_archiveCover', return_value=''):
            path = self.cls._lookupExact(artist, title, self.cls._norm(artist)+'|'+self.cls._norm(title))
            return bool(path and Path(path).read_bytes() == self.cover)

    @staticmethod
    def item(artist, title):
        return {'artistName': artist, 'trackName': title, 'artworkUrl100': 'https://art.example/100x100bb.jpg'}

    def test_slovak_artist_without_catalogue_accents_matches(self):
        self.assertTrue(self.lookup('Katarína Knechtová', 'Život nás má rád', {'SK': [self.item('Katarina Knechtova', 'Život nás má rád')]}))
        self.assertEqual(len(self.calls), 2)  # one catalogue and its artwork
        self.assertIn('country=SK', self.calls[0])
    def test_receiver_proven_credit_repairs_are_shared_with_lyrics(self):
        cases=[('M. Zbirka, Limit','Biely kvet','Miroslav Žbirka','Biely kvet'),('Necar Vaclav','Svatovitsky chram','Václav Neckář','Svatovítský Chrám (Chrám Sv. Víta)'),('Júlia Hečková','Taliansky muzikál','Júlia a Peter Heckovci','Taliansky muzikál'),('08','Krasnejsi nez ruze (Maliconia) - Pavel Roth','Pavel Roth','Krásnější než růže (Malinconia)')]
        for artist,title,got_artist,got_title in cases:
            with self.subTest(artist=artist):self.assertTrue(self.lookup(artist,title,{'SK':[self.item(got_artist,got_title)]}))
    def test_abbreviated_kroky_credit_accepts_original_band_but_not_solo_or_live(self):
        credit='Michal David, Kroky F. Janecka';title='Kazdy Mi Te Lasko Zavidi'
        self.assertTrue(self.lookup(credit,title,{'SK':[self.item('Michal David & Kroky Františka Janečka','Každý mi tě, lásko, závidí')]}))
        for artist,track in [('Michal David','Každý mi tě, lásko, závidí'),('Michal David & Kroky Františka Janečka','Každý mi tě, lásko, závidí (Live)')]:
            self.assertFalse(self.lookup(credit,title,{'SK':[self.item(artist,track)]}))
    def test_stromy_cover_accepts_verified_original_title_but_not_radio_or_live(self):
        self.assertTrue(self.lookup('Peter Bič Project','Stromy',{'SK':[self.item('Peter Bic Project','Stromy (Original Version)')]}))
        for title in ('Stromy (Radio Edit)','Stromy (naživo - Len sa smej turné 2024)'):
            self.assertFalse(self.lookup('Peter Bič Project','Stromy',{'SK':[self.item('Peter Bic Project',title)]}))
    def test_feature_outside_parentheses_matches_complete_catalogue_credit(self):
        self.assertTrue(self.lookup('Polemic','SPOLU FT. A.M.O.',{'SK':[self.item('AMO & Polemic','Spolu')]}))
        self.assertFalse(self.lookup('Polemic','SPOLU FT. A.M.O.',{'SK':[self.item('Polemic','Spolu')]}))
    def test_helena_known_duet_matches_publisher_credit_without_accepting_other_guests(self):
        self.assertTrue(self.lookup('HELENA VONDRACKOVA','Kazda trampota ma svou mez',{'SK':[self.item('Helena Vondrackova & Jiri Korn','Každá trampota má svou mez')]}))
        self.assertFalse(self.lookup('HELENA VONDRACKOVA','Kazda trampota ma svou mez',{'SK':[self.item('Helena Vondrackova & Jiri Korn & Guest','Každá trampota má svou mez')]}))
    def test_cover_does_not_accept_a_live_recording_or_uncredited_guest(self):
        for got_artist,got_title in [('Miroslav Žbirka','Biely kvet (Live)'),('Miroslav Žbirka & Guest','Biely kvet'),('Another Singer','Biely kvet')]:
            self.assertFalse(self.lookup('M. Zbirka, Limit','Biely kvet',{'SK':[self.item(got_artist,got_title)]}))
        self.assertFalse(self.lookup('Artist','Song',{'SK':[self.item('Artist','Song (Live)')]}))
    def test_title_fallback_finds_hidden_track_but_still_verifies_artist(self):
        import json,tempfile
        from urllib.parse import parse_qs,urlsplit
        terms=[]
        def opener(request,**kwargs):
            if '/search?' not in request.full_url:return io.BytesIO(self.cover)
            q=parse_qs(urlsplit(request.full_url).query);terms.append(q['term'][0])
            rows=[self.item('Wrong Artist','Song'),self.item('Artist','Song')] if q['term']==['Song'] else [self.item('Artist','Another song')]
            return io.BytesIO(json.dumps({'results':rows}).encode())
        with tempfile.TemporaryDirectory() as folder,patch.object(self.cls,'_cacheDir',return_value=folder),patch.object(self.art,'urlopen',side_effect=opener),patch.object(self.cls,'_archiveCover',return_value=''):
            path=self.cls._lookupExact('Artist','Song','title-fallback')
            self.assertEqual(Path(path).read_bytes(),self.cover)
        self.assertEqual(terms,['Artist Song','Artist Song','Artist Song','Song'])

    def test_roth_title_fallback_uses_verified_short_name(self):
        from urllib.parse import parse_qs,urlsplit
        import json
        terms=[]
        def opener(req,**kwargs):
            terms.append(parse_qs(urlsplit(req.full_url).query)['term'][0])
            return io.BytesIO(json.dumps({'results':[]}).encode())
        with patch.object(self.art,'urlopen',side_effect=opener):
            list(self.cls._catalogueResults('Pavel Roth','Krásnější než růže (Malinconia)'))
        self.assertEqual(terms[-1],'Krásnější než růže')
        self.assertEqual(len(terms),4)

    def test_lucie_sen_uses_slovak_catalogue(self):
        self.assertTrue(self.lookup('Lucie', 'Sen', {'SK': [self.item('Lucie', 'Sen')]}))
        self.assertEqual(len(self.calls), 2)

    def test_hdf_example_wrong_song_is_rejected(self):
        wrong = self.item('Olga Lounova, Richard Krajco, Katarina Knechtova', 'Protože to nevzdám (feat. Pavel Callta)')
        self.assertFalse(self.lookup('Katarína Knechtová', 'Život nás má rád', {'SK': [wrong], 'CZ': [wrong], 'US': [wrong]}))
        self.assertEqual(len(self.calls), 4)  # three regions plus bounded title fallback, no image download

    def test_same_title_by_another_artist_is_rejected(self):
        self.assertFalse(self.lookup('Lucie', 'Sen', {'SK': [self.item('Lucie Vondráčková', 'Sen')]}))

    def test_czech_catalogue_is_used_when_slovak_has_no_match(self):
        self.assertTrue(self.lookup('Artist', 'Song', {'CZ': [self.item('Artist', 'Song')]}))
        self.assertIn('country=CZ', self.calls[1])
        self.assertEqual(len(self.calls), 3)

    def test_us_catalogue_remains_available(self):
        self.assertTrue(self.lookup('Artist', 'Song', {'US': [self.item('Artist', 'Song')]}))
        self.assertIn('country=US', self.calls[2])

    def test_catalogue_failure_does_not_prevent_next_region(self):
        self.assertTrue(self.lookup('Artist', 'Song', {'SK': TimeoutError(), 'CZ': [self.item('Artist', 'Song')]}))

    def test_reversed_station_metadata_matches_both_complete_catalogue_fields(self):
        self.assertTrue(self.lookup('Uncovered Paradise', 'Ukitas', {'SK': [self.item('Ukitas', 'Uncovered Paradise')]}))
        self.assertTrue(self.lookup('Ziaris', 'Majk Spirit', {'SK': [self.item('Majk Spirit', 'Žiariš')]}))

    def test_reversed_fields_require_exact_artist_and_title(self):
        self.assertFalse(self.lookup('Uncovered Paradise', 'Ukitas', {'SK': [self.item('Ukitas Orchestra', 'Uncovered Paradise')]}))
        self.assertFalse(self.lookup('Uncovered Paradise', 'Ukitas', {'SK': [self.item('Ukitas', 'Uncovered Paradise Live')]}))

    def test_full_comma_credit_matches_guest_moved_into_catalogue_title(self):
        item = self.item('NERVO & B Jones', 'Wherever You Go (feat. EKe)')
        self.assertTrue(self.lookup('Nervo, B Jones, Eke', 'Wherever You Go', {'SK': [item]}))

    def test_guest_moved_into_radio_title_matches_catalogue_full_credit(self):
        self.assertTrue(self.lookup('Nervo & B Jones', 'Wherever You Go (feat. Eke)', {'SK': [self.item('NERVO, B Jones, EKe', 'Wherever You Go')]}))

    def test_credit_roster_must_keep_every_guest_and_complete_name(self):
        item = self.item('NERVO & B Jones', 'Wherever You Go (feat. EKe)')
        for artist in ('Nervo, B Jones', 'Nervo, B Jones, Other', 'Nervo, B Jones, Eke Junior'):
            with self.subTest(artist=artist):
                self.assertFalse(self.lookup(artist, 'Wherever You Go', {'SK': [item]}))

    def test_full_credit_does_not_allow_another_title_or_remix(self):
        for title in ('Another Song (feat. EKe)', 'Wherever You Go (Remix) (feat. EKe)'):
            with self.subTest(title=title):
                self.assertFalse(self.lookup('Nervo, B Jones, Eke', 'Wherever You Go', {'SK': [self.item('NERVO & B Jones', title)]}))

    def test_reversed_complete_roster_normalizes_and_comma_and_ampersand(self):
        self.assertTrue(self.lookup('All The Time', 'John Summit and The Chainsmokers and Ilsey', {'SK': [self.item('John Summit, The Chainsmokers & Ilsey', 'ALL THE TIME')]}))

    def test_forward_complete_roster_normalizes_separators_and_credit_order(self):
        self.assertTrue(self.lookup('John Summit and The Chainsmokers and Ilsey', 'All The Time', {'SK': [self.item('Ilsey, John Summit & The Chainsmokers', 'ALL THE TIME')]}))

    def test_reversed_roster_rejects_missing_artist_and_another_version(self):
        for artist, title in [('John Summit & The Chainsmokers', 'ALL THE TIME'), ('John Summit, The Chainsmokers & Ilsey Junior', 'ALL THE TIME'), ('Ilsey, John Summit & The Chainsmokers', 'ALL THE TIME (GorillaT Remix)')]:
            with self.subTest(artist=artist, title=title):
                self.assertFalse(self.lookup('All The Time', 'John Summit and The Chainsmokers and Ilsey', {'SK': [self.item(artist, title)]}))

    def test_reversed_title_can_omit_contraction_apostrophe(self):
        self.assertTrue(self.lookup('Cant Deny It', 'Jazzy and Spriitzz', {'SK': [self.item('Jazzy & Spriitzz', "Can't Deny It")]}))

    def test_typographic_apostrophes_have_the_same_complete_title_identity(self):
        for mark in ("'", '’', '‘', 'ʼ'):
            with self.subTest(mark=mark):
                self.assertTrue(self.lookup('Jazzy and Spriitzz', 'Cant Deny It', {'SK': [self.item('Jazzy & Spriitzz', 'Can'+mark+'t Deny It')]}))

    def test_apostrophe_normalization_does_not_drop_artists_or_version_words(self):
        for artist, title in [('Jazzy', "Can't Deny It"), ('Jazzy & Spriitzz', "Can't Deny You"), ('Jazzy, Spriitzz & Spray', "Can't Deny It (Spray VIP)"), ('Jazzy, Spriitzz & Dart', "Can't Deny It (Dart Remix)")]:
            with self.subTest(artist=artist, title=title):
                self.assertFalse(self.lookup('Cant Deny It', 'Jazzy and Spriitzz', {'SK': [self.item(artist, title)]}))

    def test_different_guest_rendition_does_not_replace_band_recording(self):
        self.assertFalse(self.lookup('Robo Grigorov & Midi', 'Po víne', {'SK': [self.item('Kristina', 'Po víne (feat. Robo Grigorov)')]}))

    def test_featured_artist_substring_is_not_a_match(self):
        self.assertFalse(self.lookup('Robo Grigorov & Midi', 'Po víne', {'SK': [self.item('Kristina', 'Po víne (feat. Robo Grigorov Junior)')]}))

    def test_featured_credit_does_not_allow_another_song(self):
        self.assertFalse(self.lookup('Robo Grigorov & Midi', 'Po víne', {'SK': [self.item('Kristina', 'Na vysokej skale (feat. Robo Grigorov)')]}))

    def test_accents_do_not_remove_words_or_version_markers(self):
        self.assertEqual(self.cls._norm('KATARÍNA Knechtová'), self.cls._norm('Katarina Knechtova'))
        self.assertNotEqual(self.cls._norm('Sen'), self.cls._norm('Sen (Live)'))
        self.assertNotEqual(self.cls._norm('Lucie'), self.cls._norm('Lucie Bílá'))


class ArchiveArtworkTests(unittest.TestCase):
    setUp = CatalogueArtworkTests.setUp
    item = staticmethod(CatalogueArtworkTests.item)
    rid = '64ea2902-76ff-489e-9a8d-0b285d5eff1d'
    def fixture(self, **changes):
        recording = {'title': 'Po víne', 'artist-credit': [{'name': 'Robo Grigorov & Midi'}],
                     'releases': [{'id': self.rid, 'status': 'Official'}]}
        recording.update(changes)
        return {'recordings': [recording]}
    def cover_document(self, **changes):
        image = {'approved': True, 'front': True, 'thumbnails': {'500': 'http://coverartarchive.org/release/'+self.rid+'/33849001419-500.jpg'}}
        image.update(changes)
        return {'release': 'https://musicbrainz.org/release/'+self.rid, 'images': [image]}
    def archive(self, data, cover=None):
        import tempfile
        values = [data, cover or self.cover_document()]
        with tempfile.TemporaryDirectory() as cache, patch.object(self.cls, '_cacheDir', return_value=cache), patch.object(self.cls, '_json', side_effect=values) as fetch, patch.object(self.art, 'urlopen', return_value=io.BytesIO(self.cover_bytes)) as download:
            self.cls._archiveNext = 0
            result = self.cls._archiveCover('Robo Grigorov & Midi', 'Po víne', 'archive-key')
            self.fetch_calls = fetch.call_args_list
            self.download_calls = download.call_args_list
            return bool(result)
    @property
    def cover_bytes(self):
        return b'\xff\xd8' + b'x'*2048
    def test_original_recording_finds_approved_front_from_its_release(self):
        self.assertTrue(self.archive(self.fixture()))
        self.assertIn('coverartarchive.org/release/'+self.rid, self.fetch_calls[1].args[0])
        self.assertTrue(self.download_calls[0].args[0].full_url.startswith('https://'))
    def test_duet_with_different_performers_does_not_replace_original(self):
        self.assertFalse(self.archive(self.fixture(**{'artist-credit':[{'name':'Robo Grigorov & Kristina'}]})))
        self.assertEqual(len(self.fetch_calls),1)
    def test_wrong_song_by_same_artist_is_rejected(self):
        self.assertFalse(self.archive(self.fixture(title='Edo')))
    def test_unrequested_live_recording_is_rejected(self):
        self.assertFalse(self.archive(self.fixture(disambiguation='live in Bratislava')))
    def test_back_cover_and_unapproved_image_are_rejected(self):
        for changes in ({'front':False},{'approved':False}):
            with self.subTest(changes=changes):self.assertFalse(self.archive(self.fixture(),self.cover_document(**changes)))
    def test_cover_from_another_release_is_rejected(self):
        cover=self.cover_document();cover['release']='https://musicbrainz.org/release/other'
        self.assertFalse(self.archive(self.fixture(),cover))
    def test_cover_missing_in_first_release_allows_next_release(self):
        data=self.fixture();other='11111111-1111-1111-1111-111111111111'
        data['recordings'][0]['releases'].insert(0,{'id':other,'status':'Official'})
        with patch.object(self.cls,'_json',side_effect=[data,OSError('404'),self.cover_document()]), patch.object(self.cls,'_saveCover',return_value='/tmp/cover.jpg'):
            self.cls._archiveNext=0
            self.assertEqual(self.cls._archiveCover('Robo Grigorov & Midi','Po víne','key'),'/tmp/cover.jpg')
    def test_archive_is_only_consulted_after_store_lookup_fails(self):
        with patch.object(self.cls,'_catalogueResults',return_value=iter(())),patch.object(self.cls,'_archiveCover',return_value='found') as fallback:
            self.assertEqual(self.cls._lookupExact('A','B','key'),'found')
        fallback.assert_called_once_with('A','B','key')
    def test_bad_download_does_not_block_next_catalogue(self):
        first=self.item('A','B');second=self.item('A','B')
        with patch.object(self.cls,'_catalogueResults',return_value=iter((first,second))),patch.object(self.cls,'_saveCover',side_effect=['','good']):
            self.assertEqual(self.cls._lookupExact('A','B','key'),'good')

if __name__=='__main__':unittest.main()
