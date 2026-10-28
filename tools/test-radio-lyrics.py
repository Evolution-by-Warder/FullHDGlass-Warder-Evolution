#!/usr/bin/env python3
"""Exercise lyrics identity/cache, native scrolling and radio-only layout changes."""
import ast
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import re
import sys
import tempfile
import types
import unittest
from unittest.mock import patch
import xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[1]
P=ROOT/'source/package-root/usr/lib/enigma2/python'
PLUGIN=P/'Plugins/Extensions/setupGlass17'
sys.path.insert(0,str(PLUGIN))
spec=importlib.util.spec_from_file_location('lyrics_provider',PLUGIN/'warderLyrics.py')
provider=importlib.util.module_from_spec(spec);spec.loader.exec_module(provider)


class ProviderTests(unittest.TestCase):
    def setUp(self):
        from functools import partial
        legacy=partial(provider.lookup,site_providers=())
        patcher=patch.object(provider,'lookup',legacy);patcher.start();self.addCleanup(patcher.stop)
    def record(self,**kw):
        return dict(artistName='Žbirka',trackName='Biely kvet',plainLyrics='Original test text',**kw)
    def test_exact_identity_including_accents_and_case(self):
        self.assertEqual(provider.select([self.record()],'ZBIRKA','Biely kvet'),'Original test text')
    def test_first_wrong_result_is_not_used(self):
        bad=self.record();bad['artistName']='Another artist'
        self.assertEqual(provider.select([bad,self.record()],'Žbirka','Biely kvet'),'Original test text')
    def test_different_version_is_not_equated(self):
        row=self.record();row['trackName']='Biely kvet (Live)'
        self.assertEqual(provider.select([row],'Žbirka','Biely kvet'),'')
    def test_artist_or_title_substring_is_not_a_match(self):
        row=self.record();row['artistName']='Žbirka & Someone'
        self.assertEqual(provider.select([row],'Žbirka','Biely kvet'),'')
    def test_instrumental_and_oversized_text_are_ignored(self):
        self.assertEqual(provider.select([self.record(instrumental=True)],'Žbirka','Biely kvet'),'')
        row=self.record();row['plainLyrics']='a'*(provider.MAX_TEXT+1)
        self.assertEqual(provider.select([row],'Žbirka','Biely kvet'),'')
    def test_cache_and_128_record_bound(self):
        with tempfile.TemporaryDirectory() as tmp:
            response=lambda *a,**kw:io.BytesIO(json.dumps([self.record()]).encode())
            folder=Path(tmp)
            found=provider.lookup('Žbirka','Biely kvet',folder,opener=response)
            self.assertEqual(found['status'],'found')
            def no_network(*a,**kw):raise AssertionError('Cache must prevent a second network request')
            self.assertEqual(provider.lookup('Žbirka','Biely kvet',folder,opener=no_network),found)
            for i in range(135):(folder/(str(i)+'.json')).write_text('{}')
            provider.lookup('Žbirka','Biely kvet',folder,opener=response,clock=lambda:time_later())
            self.assertLessEqual(len(list(folder.glob('*.json'))),128)
    def test_offline_is_silent_and_does_not_cache_false_miss(self):
        with tempfile.TemporaryDirectory() as tmp:
            def offline(*a,**kw):raise OSError('offline')
            result=provider.lookup('Artist','Title',Path(tmp),opener=offline)
            self.assertEqual(result['status'],'offline')
            self.assertEqual(result['retry_after'],5)
            self.assertEqual(list(Path(tmp).glob('*.json')),[])
    def test_collaboration_separators_keep_all_performers(self):
        row=dict(artistName='Topic, A7S',trackName='Breaking Me',plainLyrics='Original test text')
        self.assertEqual(provider.select([row],'Topic and A7S','Breaking Me'),'Original test text')
        self.assertEqual(provider.select([row],'Topic','Breaking Me'),'')
        self.assertEqual(provider.select([row],'Topic and Another','Breaking Me'),'')
    def test_reversed_fields_require_both_complete_identities(self):
        row=dict(artistName='Topic, A7S',trackName='Breaking Me',plainLyrics='Original test text')
        self.assertEqual(provider.select([row],'Breaking Me','Topic and A7S'),'Original test text')
        self.assertEqual(provider.select([row],'Breaking Me','Topic'),'')
        self.assertEqual(provider.select([row],'Breaking Me (Live)','Topic and A7S'),'')
    def test_reversed_lookup_searches_titles_without_guessing_first_result(self):
        from urllib.parse import parse_qs,urlsplit
        queries=[]
        def response(request,**kwargs):
            query=parse_qs(urlsplit(request.full_url).query);queries.append(query)
            row=dict(artistName='Topic, A7S',trackName='Breaking Me',plainLyrics='Original test text')
            return io.BytesIO(json.dumps([row] if query.get('track_name')==['Breaking Me'] and 'artist_name' not in query else []).encode())
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(provider.lookup('Breaking Me','Topic and A7S',Path(tmp),opener=response)['text'],'Original test text')
        self.assertTrue(any(q.get('track_name')==['Breaking Me'] and 'artist_name' not in q for q in queries))
    def test_synced_only_record_becomes_plain_text(self):
        row=self.record();row['plainLyrics']=None
        row['syncedLyrics']='[ar:Metadata]\n[00:01.00]Original test line\n[00:03.20][00:04.00]Another line'
        self.assertEqual(provider.select([row],'Žbirka','Biely kvet'),'Original test line\nAnother line')
    def test_404_is_a_miss_and_not_offline(self):
        from urllib.error import HTTPError
        def miss(request,**kwargs):raise HTTPError(request.full_url,404,'missing',{},None)
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(provider.lookup('Artist','Title',Path(tmp),opener=miss)['status'],'not-found')
    def test_fallback_after_lrclib_failure_and_complete_identity_in_url(self):
        from urllib.error import HTTPError
        urls=[]
        def response(request,**kwargs):
            urls.append(request.full_url)
            if request.full_url.startswith(provider.SEARCH):raise HTTPError(request.full_url,503,'busy',{'Retry-After':'120'},None)
            return io.BytesIO(json.dumps({'lyrics':'Original fallback text'}).encode())
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(provider.lookup('Topic and A7S','Breaking Me',Path(tmp),opener=response)['text'],'Original fallback text')
        self.assertEqual(len(urls),2)
        self.assertIn('/Topic%20and%20A7S/Breaking%20Me',urls[-1])
    def test_full_pair_reversal_is_also_available_when_primary_provider_is_offline(self):
        from urllib.error import HTTPError
        urls=[]
        def response(request,**kwargs):
            urls.append(request.full_url)
            if request.full_url.startswith(provider.SEARCH):raise HTTPError(request.full_url,503,'busy',{'Retry-After':'20'},None)
            if request.full_url.endswith('/Topic%20and%20A7S/Breaking%20Me'):
                return io.BytesIO(json.dumps({'lyrics':'Original reversed test text'}).encode())
            raise HTTPError(request.full_url,404,'missing',{},None)
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(provider.lookup('Breaking Me','Topic and A7S',Path(tmp),opener=response)['text'],'Original reversed test text')
        self.assertEqual(len(urls),3)
    def test_rate_limit_survives_between_workers_and_failure_is_not_cached(self):
        from urllib.error import HTTPError
        urls=[]
        def response(request,**kwargs):
            urls.append(request.full_url)
            raise HTTPError(request.full_url,429 if request.full_url.startswith(provider.SEARCH) else 404,'limited',{'Retry-After':'120'},None)
        with tempfile.TemporaryDirectory() as tmp:
            folder=Path(tmp)
            first=provider.lookup('Artist','Title',folder,opener=response,clock=lambda:1000)
            self.assertEqual(first['status'],'offline');self.assertGreaterEqual(first['retry_after'],120)
            self.assertFalse(list(folder.glob('*.json')))
            urls.clear();provider.lookup('Other Artist','Other Title',folder,opener=response,clock=lambda:1001)
            self.assertEqual(len(urls),2);self.assertTrue(all(u.startswith(provider.FALLBACK) for u in urls))
    def test_slow_primary_does_not_block_fallback_and_keeps_ten_second_timeout(self):
        from threading import Event
        import time
        release=Event();calls=[]
        def response(request,**kwargs):
            calls.append((request.full_url,kwargs['timeout']))
            if request.full_url.startswith(provider.SEARCH):
                release.wait(0.5)
                raise TimeoutError('slow')
            return io.BytesIO(json.dumps({'lyrics':'Original backup text'}).encode())
        with tempfile.TemporaryDirectory() as tmp:
            began=time.monotonic()
            try:result=provider.lookup('Artist','Title',Path(tmp),opener=response,hedge_delay=0.01)
            finally:release.set()
            self.assertLess(time.monotonic()-began,0.4)
        self.assertEqual(result['text'],'Original backup text')
        self.assertEqual(calls[0][1],10)
        self.assertEqual(sum(u.startswith(provider.SEARCH) for u,t in calls),1)
        self.assertTrue(any(u.startswith(provider.FALLBACK) for u,t in calls))
    def test_request_budget_returns_without_waiting_for_pending_source(self):
        from threading import Event
        import time
        release=Event();calls=[]
        def response(request,**kwargs):
            calls.append(request.full_url);release.wait(0.4);raise TimeoutError('slow')
        with tempfile.TemporaryDirectory() as tmp:
            began=time.monotonic()
            try:result=provider.lookup('Artist','Title',Path(tmp),opener=response,hedge_delay=0.005,budget=0.05)
            finally:release.set()
        self.assertLess(time.monotonic()-began,0.3)
        self.assertEqual(result['status'],'offline');self.assertLessEqual(len(calls),2)
    def test_retry_after_starts_at_error_receipt_not_request_start(self):
        from urllib.error import HTTPError
        wall=[1000]
        def response(request,**kwargs):
            wall[0]+=8
            raise HTTPError(request.full_url,429 if request.full_url.startswith(provider.SEARCH) else 404,'limited',{'Retry-After':'120'},None)
        with tempfile.TemporaryDirectory() as tmp:
            folder=Path(tmp)
            provider.lookup('Artist','Title',folder,opener=response,clock=lambda:wall[0])
            self.assertEqual(float((folder/'.lrclib-backoff').read_text()),1128)
    def test_retry_after_http_date_is_respected(self):
        from urllib.error import HTTPError
        from email.utils import formatdate
        def response(request,**kwargs):
            raise HTTPError(request.full_url,429 if request.full_url.startswith(provider.SEARCH) else 404,'limited',{'Retry-After':formatdate(1120,usegmt=True)},None)
        with tempfile.TemporaryDirectory() as tmp:
            result=provider.lookup('Artist','Title',Path(tmp),opener=response,clock=lambda:1000)
        self.assertGreaterEqual(result['retry_after'],120)

    def test_optional_failure_does_not_override_confirmed_misses_from_both_sources(self):
        from urllib.error import HTTPError
        def response(request,**kwargs):
            if request.full_url.startswith(provider.FALLBACK):raise HTTPError(request.full_url,404,'missing',{},None)
            if 'artist_name=' in request.full_url:return io.BytesIO(b'[]')
            raise TimeoutError('optional query failed')
        with tempfile.TemporaryDirectory() as tmp:
            folder=Path(tmp);result=provider.lookup('Faraon','Šlapací kolo',folder,opener=response)
            self.assertEqual(result['status'],'not-found');self.assertEqual(len(list(folder.glob('*.json'))),1)
            status=json.loads((folder/'.last-result').read_text())
            self.assertTrue(any(r.get('status')=='request-error' for r in status['requests']))
    def test_optional_request_still_pending_at_deadline_does_not_erase_known_misses(self):
        from threading import Event
        from urllib.error import HTTPError
        release=Event()
        def response(request,**kwargs):
            if request.full_url.startswith(provider.FALLBACK):raise HTTPError(request.full_url,404,'missing',{},None)
            if 'artist_name=' in request.full_url:return io.BytesIO(b'[]')
            release.wait(3)
            raise TimeoutError('optional request still pending')
        with tempfile.TemporaryDirectory() as tmp:
            try:result=provider.lookup('Artist','Title',Path(tmp),opener=response,hedge_delay=0.01,budget=2.05)
            finally:release.set()
            self.assertEqual(result['status'],'not-found')
            data=json.loads((Path(tmp)/'.last-result').read_text())
            self.assertTrue(any(row['status']=='pending' for row in data['requests']))
    def test_partial_miss_cache_expires_sooner_and_successful_later_lookup_replaces_it(self):
        from urllib.error import HTTPError
        def response(request,**kwargs):
            if request.full_url.startswith(provider.FALLBACK):raise HTTPError(request.full_url,404,'missing',{},None)
            if 'artist_name=' in request.full_url:return io.BytesIO(b'[]')
            raise TimeoutError('optional query failed')
        with tempfile.TemporaryDirectory() as tmp:
            folder=Path(tmp);provider.lookup('Žbirka','Biely kvet',folder,opener=response,clock=lambda:1000)
            saved=json.loads((folder/(provider.key('Žbirka','Biely kvet')+'.json')).read_text())
            self.assertEqual(saved['ttl'],300)
            good=lambda *a,**kw:io.BytesIO(json.dumps([self.record()]).encode())
            self.assertEqual(provider.lookup('Žbirka','Biely kvet',folder,opener=good,clock=lambda:1301)['status'],'found')
    def test_one_unreachable_provider_remains_retryable_even_if_other_misses(self):
        from urllib.error import HTTPError
        def response(request,**kwargs):
            if request.full_url.startswith(provider.SEARCH):raise TimeoutError('offline')
            raise HTTPError(request.full_url,404,'missing',{},None)
        with tempfile.TemporaryDirectory() as tmp:
            folder=Path(tmp);result=provider.lookup('Artist','Title',folder,opener=response)
            self.assertEqual(result['status'],'offline');self.assertFalse(list(folder.glob('*.json')))
    def test_retry_uses_earlier_recovering_source_without_bypassing_longer_host_limit(self):
        from urllib.error import HTTPError
        calls=[]
        def response(request,**kwargs):
            calls.append(request.full_url)
            raise HTTPError(request.full_url,429 if request.full_url.startswith(provider.SEARCH) else 503,'busy',{'Retry-After':'120' if request.full_url.startswith(provider.SEARCH) else '20'},None)
        with tempfile.TemporaryDirectory() as tmp:
            folder=Path(tmp);result=provider.lookup('Artist','Title',folder,opener=response,clock=lambda:1000)
            self.assertEqual(result['retry_after'],20)
            calls.clear();provider.lookup('Another','Song',folder,opener=response,clock=lambda:1001)
            self.assertEqual(calls,[])
    def test_swapped_metadata_uses_same_cached_text_without_more_network_requests(self):
        row=dict(artistName='Topic, A7S',trackName='Breaking Me',plainLyrics='Original test text')
        response=lambda *a,**kw:io.BytesIO(json.dumps([row]).encode())
        with tempfile.TemporaryDirectory() as tmp:
            folder=Path(tmp);provider.lookup('Topic and A7S','Breaking Me',folder,opener=response)
            def fail(*a,**kw):raise AssertionError('Swapped fields must use cache')
            self.assertEqual(provider.lookup('Breaking Me','Topic and A7S',folder,opener=fail)['text'],'Original test text')
    def test_diagnostic_record_contains_no_lyrics_and_cache_hit_makes_no_requests(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder=Path(tmp);response=lambda *a,**kw:io.BytesIO(json.dumps([self.record()]).encode())
            provider.lookup('Žbirka','Biely kvet',folder,opener=response)
            data=(folder/'.last-result').read_text();self.assertNotIn('Original test text',data)
            self.assertLessEqual(len(json.loads(data)['requests']),5)
            provider.lookup('Žbirka','Biely kvet',folder,opener=response)
            status=json.loads((folder/'.last-result').read_text())
            self.assertTrue(status['cache_hit']);self.assertEqual(status['requests'],[])
    def test_found_text_survives_cache_write_failure(self):
        with tempfile.TemporaryDirectory() as tmp:
            response=lambda *a,**kw:io.BytesIO(json.dumps([self.record()]).encode())
            with patch.object(provider,'atomic_json',side_effect=OSError('read-only cache')):
                self.assertEqual(provider.lookup('Žbirka','Biely kvet',Path(tmp),opener=response)['text'],'Original test text')
    def test_slovak_and_connector_between_full_names_keeps_entire_credit(self):
        row=dict(artistName='Sima Martausová & Miťo Bodnár',trackName='Slovo chlapa',plainLyrics='Original test text')
        self.assertEqual(provider.select([row],'Sima Martausová a Miťo Bodnár','Slovo chlapa'),'Original test text')
        self.assertEqual(provider.select([row],'Sima Martausová','Slovo chlapa'),'')
        self.assertEqual(provider.select([row],'Sima Martausová a Miťo Bodnár Junior','Slovo chlapa'),'')
        row['artistName']='Not & Band';row['trackName']='Song'
        self.assertEqual(provider.select([row],'Not a Band','Song'),'')

    def test_previous_negative_cache_is_invalidated(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder=Path(tmp);(folder/(provider.key('Žbirka','Biely kvet')+'.json')).write_text(json.dumps({'text':'','status':'not-found','saved':100}))
            response=lambda *a,**kw:io.BytesIO(json.dumps([self.record()]).encode())
            self.assertEqual(provider.lookup('Žbirka','Biely kvet',folder,opener=response,clock=lambda:101)['status'],'found')

    def test_display_announcements_never_reach_the_provider(self):
        self.assertEqual(provider.lookup('','Hudba na maximum')['status'],'no-song')


def time_later():
    import time
    return time.time()+15*86400


class Timer:
    def __init__(self):self.callback=[];self.starts=[]
    def start(self,*args):self.starts.append(args)
    def stop(self):pass


class Label:
    def __init__(self,parent):self.text='';self.position=(0,0);self.dim=(760,530)
    def setTransparent(self,*a):pass
    def setNoWrap(self,*a):pass
    def setFont(self,*a):pass
    def setForegroundColor(self,*a):pass
    def move(self,p):self.position=p
    def resize(self,s):self.dim=s
    def setText(self,t):self.text=t
    def calculateSize(self):return types.SimpleNamespace(height=lambda:max(35,len(self.text.splitlines())*40))


class NativeTests(unittest.TestCase):
    def setUp(self):
        class Renderer:
            def __init__(self):self.instance=None;self.skinAttributes=[]
            def postWidgetCreate(self,instance):self.instance=instance
            def applySkin(self,*a):return True
            def preWidgetRemove(self,*a):pass
        self.navigation=types.SimpleNamespace(instance=types.SimpleNamespace(getCurrentService=lambda:None,getCurrentlyPlayingServiceReference=lambda:None))
        self.metadata=types.SimpleNamespace(current_song=lambda *a:('',''),native_song=lambda *a:('',''),split_song=lambda text:tuple(text.split(' - ',1)) if ' - ' in text else ('',''))
        self.loop=types.SimpleNamespace(spawnProcess=self.spawn)
        self.spawned=[]
        modules={'enigma':types.SimpleNamespace(eLabel=Label,eWidget=object,ePoint=lambda x,y:(x,y),eSize=lambda x,y:(x,y),eTimer=Timer,gFont=lambda *a:a,iRdsDecoder=types.SimpleNamespace(RadioText=1)),
                 'Components.Renderer.Renderer':types.SimpleNamespace(Renderer=Renderer),
                 'Components.Converter.WarderRadioOnly':types.SimpleNamespace(is_radio_reference=lambda ref:ref is not None),
                 'Components.Converter.WarderRadioMetadata':self.metadata,
                 'Components.Language':types.SimpleNamespace(language=types.SimpleNamespace(getLanguage=lambda:'sk_SK')),
                 'NavigationInstance':self.navigation,'skin':types.SimpleNamespace(parseColor=lambda x:x),
                 'Plugins.Extensions.setupGlass17.warderLyrics':provider,
                 'Plugins.Extensions.setupGlass17.warderHelpPreview':types.SimpleNamespace(_NativeLoop=lambda:self.loop)}
        package=types.ModuleType('Plugins.Extensions.setupGlass17');package.__path__=[str(PLUGIN)];package.warderLyrics=provider
        modules['Plugins.Extensions.setupGlass17']=package
        self.modules=patch.dict(sys.modules,modules);self.modules.start();self.addCleanup(self.modules.stop)
        spec=importlib.util.spec_from_file_location('native_lyrics',P/'Components/Renderer/WarderRadioLyrics.py')
        self.m=importlib.util.module_from_spec(spec);spec.loader.exec_module(self.m)
        self.renderer=self.m.WarderRadioLyrics()
        self.instance=types.SimpleNamespace(setTransparent=lambda x:None,size=lambda:types.SimpleNamespace(width=lambda:760,height=lambda:530))
        self.renderer.postWidgetCreate(self.instance)
    def spawn(self,worker,executable,argv,env):
        worker.transport=types.SimpleNamespace(kill=lambda:None)
        self.spawned.append((worker,executable,argv))
    def test_text_is_native_and_short_text_does_not_scroll(self):
        self.renderer._set_text('Short text')
        self.assertIsInstance(self.renderer.label,Label)
        self.assertEqual(self.renderer._overflow,0)
    def test_long_text_scrolls_inside_the_clip_and_restarts_after_end(self):
        r=self.renderer;r._set_text('\n'.join(['Line']*30));r._pause_until=0
        r._tick();self.assertEqual(r.label.position,(0,-1))
        r._offset=r._overflow;r._pause_until=0;r._tick();self.assertEqual(r.label.position,(0,0))
    def song(self,station='one'):
        ref=types.SimpleNamespace(toString=lambda:station)
        self.navigation.instance.getCurrentlyPlayingServiceReference=lambda:ref
        self.m.native_song=lambda *a:('Artist','Title')
    def test_lookup_uses_native_child_argv_and_late_station_result_is_discarded(self):
        r=self.renderer;self.song();r._poll();r._pending_since-=3
        with patch.object(provider,'lookup',side_effect=AssertionError('No provider I/O in GUI')):r._poll()
        self.assertEqual(len(self.spawned),1)
        worker,exe,argv=self.spawned[0];self.assertEqual(exe,'/usr/bin/python3');self.assertEqual(argv[-2:],['Artist','Title'])
        self.song('two');r._poll()
        worker.outReceived(b'{"text":"Old station lyrics"}');worker.complete(0)
        self.assertNotIn('Old station lyrics',r.label.text)
    def test_native_announcement_clears_song_without_stale_icy_lookup(self):
        self.song();r=self.renderer;r._poll()
        self.m.native_song=lambda *a:('','Hudba na maximum')
        self.m.current_song=lambda *a:(_ for _ in ()).throw(AssertionError('Must not reuse ICY song'))
        r._poll();self.assertIsNone(r._key)
    def test_transient_failure_retries_but_stops_after_three_attempts(self):
        r=self.renderer;self.song();r._poll();r._pending_since-=3;r._poll()
        for attempt in range(3):
            worker=self.spawned[-1][0];worker.outReceived(b'{"text":"","status":"offline"}');worker.complete(0)
            self.assertEqual(r._attempts,attempt+1)
            if attempt<2:
                self.assertGreater(r._retry_at,0);r._retry_at=1;r._poll()
        self.assertEqual(r._retry_at,0);r._poll();self.assertEqual(len(self.spawned),3)
    def test_worker_timeout_is_visible_and_late_response_cannot_replace_it(self):
        r=self.renderer;self.song();r._poll();r._pending_since-=3;r._poll()
        worker=self.spawned[-1][0];r._worker_timeout()
        self.assertIn('znova',r.label.text);self.assertGreater(r._retry_at,0)
        worker.outReceived(b'{"text":"Stale text"}');worker.complete(0)
        self.assertNotEqual(r.label.text,'Stale text')
    def test_reversed_same_song_metadata_keeps_display_and_does_not_spawn_again(self):
        r=self.renderer;self.song();r._poll();r._pending_since-=3;r._poll()
        worker=self.spawned[-1][0];worker.outReceived(b'{"text":"Original test text"}');worker.complete(0)
        self.m.native_song=lambda *a:('Title','Artist');r._poll()
        self.assertEqual(r.label.text,'Original test text');self.assertEqual(len(self.spawned),1)
    def test_retry_is_visible_and_host_retry_after_overrides_short_pause(self):
        r=self.renderer;self.song();r._poll();r._pending_since-=3;r._poll()
        worker=self.spawned[-1][0];worker.outReceived(b'{"text":"","status":"offline","retry_after":120}');worker.complete(0)
        import time
        self.assertGreaterEqual(r._retry_at-time.monotonic(),119)
        self.assertIn('znova',r.label.text)

    def test_real_miss_is_not_retried(self):
        r=self.renderer;self.song();r._poll();r._pending_since-=3;r._poll()
        worker=self.spawned[-1][0];worker.outReceived(b'{"text":"","status":"not-found"}');worker.complete(0)
        self.assertEqual(r._retry_at,0);r._poll();self.assertEqual(len(self.spawned),1)

    def test_hiding_cancels_native_timers_and_worker(self):
        r=self.renderer;self.song();r._poll();r._pending_since-=3;r._poll()
        worker=self.spawned[0][0];killed=[];worker.transport.kill=lambda:killed.append(True)
        r.onHide();self.assertFalse(r._shown);self.assertEqual(killed,[True])


class LayoutTests(unittest.TestCase):
    def test_native_contract_and_geometry(self):
        skin=ET.parse(ROOT/'source/package-root/usr/share/enigma2/hd_glass17/skin.xml').getroot()
        for name in ('RdsInfoDisplay','RdsDisplay'):
            screen=skin.find("screen[@name='%s']"%name)
            self.assertEqual({w.get('name') for w in screen.findall('widget') if w.get('name')},{'RadioText','RtpText','RassLogo'})
            artwork=screen.find("widget[@render='WarderRadioCompactArtwork']")
            self.assertEqual(artwork.get('size'),'420,700')
            lyrics=screen.find("widget[@render='WarderRadioLyrics']")
            self.assertEqual(lyrics.get('size'),'760,530')
            for w in screen:
                x,y=map(int,w.get('position').split(','));width,height=map(int,w.get('size').split(','))
                self.assertTrue(x>=0 and y>=0 and x+width<=1920 and y+height<=1080,w.attrib)
    def test_radio_header_removes_middle_title_and_places_seconds_next_to_minutes(self):
        skin=ET.parse(ROOT/'source/package-root/usr/share/enigma2/hd_glass17/skin.xml').getroot()
        from PIL import ImageFont
        for name in ('RdsInfoDisplay','RdsDisplay'):
            screen=skin.find("screen[@name='%s']"%name)
            self.assertFalse(any(c.text=='Radio' for c in screen.findall('widget/convert')))
            date=next(w for w in screen.findall('widget') if w.findtext('convert')=='Date')
            self.assertEqual(date.find('convert').get('type'),'WarderRadioServiceType')
            large=next(w for w in screen.findall('widget') if w.findtext('convert')=='Format:%H:%M')
            small=next(w for w in screen.findall('widget') if w.findtext('convert')=='Format:.%S')
            self.assertEqual(int(small.get('position').split(',')[0]),int(large.get('position').split(',')[0])+int(large.get('size').split(',')[0]))
            bottoms=[]
            for w,text in ((large,'20:52'),(small,'.00')):
                font=ImageFont.truetype(str(ROOT/'source/package-root/usr/share/fonts/prive7.ttf'),int(w.get('font').split(';')[1]))
                self.assertLessEqual(font.getlength(text),int(w.get('size').split(',')[0]))
                y=int(w.get('position').split(',')[1]);height=int(w.get('size').split(',')[1])
                bottoms.append(y+(height-sum(font.getmetrics()))/2+font.getbbox(text)[3])
            self.assertLessEqual(abs(bottoms[0]-bottoms[1]),1)

    def test_tv_and_other_screens_are_byte_identical_to_baseline(self):
        record=json.loads((ROOT/'design/radio-lyrics/implementation.json').read_text())
        text=(ROOT/'source/package-root/usr/share/enigma2/hd_glass17/skin.xml').read_text()
        for name in ('RdsInfoDisplay','RdsDisplay','RadioInfoBar'):
            text=re.sub(r'<screen\b[^>]*name="'+name+r'"[^>]*>.*?</screen>','<RADIO_SCREEN '+name+'/>',text,flags=re.S)
        self.assertEqual(hashlib.sha256(text.encode()).hexdigest(),record['non_radio_xml_sha256'])
    def test_artwork_padding_is_transparent(self):
        source=(P/'Components/Renderer/WarderRadioArtwork.py').read_text()
        self.assertIn('False, 1, "#ff000000"',source)
    def test_provider_and_renderer_syntax_is_python_39_compatible(self):
        for path in [PLUGIN/'warderLyrics.py',P/'Components/Renderer/WarderRadioLyrics.py',P/'Components/Converter/WarderRadioServiceType.py']:
            ast.parse(path.read_text(),feature_version=(3,9))


class RegionalSourceTests(unittest.TestCase):
    def setUp(self):
        import warderLyricsSites
        self.sites=warderLyricsSites
    def hudba(self,artist='Pavol Habera',title='Láska necestuj tým vlakom',text='Original regional test text'):
        return ('<h1>'+artist+'</h1><article class="song-detail"><h2>'+title+'</h2><div class="song-text-full-width">'+text+'</div></article><aside>Advertisement must never appear</aside>').encode()
    def youradio(self,artist='Pavol Habera',title='Láska, necestuj tým vlakom'):
        return ('<p class="title"><a href="/">Texty písní</a><a href="/pavol-habera">'+artist+'</a></p><div class="lyrics-song"><h1>'+title+'</h1><div class="lyrics-orig">Original test line<br>Another line<script>malicious()</script></div><div class="lyrics-translate">Translation must never appear</div></div>').encode()
    def parse(self,name,raw,artist='Pavol Habera',title='Láska, necestuj tým vlakom'):
        return self.sites.parse(name,'https://'+self.sites.HOSTS[name]+'/',raw,artist,title,provider.same_song,provider.clean_text)
    def test_hudba_accepts_comma_difference_and_only_the_lyrics_container(self):
        result=self.parse('hudba',self.hudba(text='First original line<br>Second original line'))
        self.assertEqual(result['text'],'First original line\nSecond original line')
        self.assertNotIn('Advertisement',result['text'])
    def test_youradio_keeps_original_and_rejects_translation_and_scripts(self):
        result=self.parse('youradio',self.youradio())
        self.assertEqual(result['text'],'Original test line\nAnother line')
    def test_wrong_artist_live_version_and_title_substring_are_not_accepted(self):
        for artist,title in [('Other Artist','Láska, necestuj tým vlakom'),('Pavol Habera','Láska, necestuj tým vlakom (Live)'),('Pavol Habera','Láska')]:
            self.assertEqual(self.parse('hudba',self.hudba(artist=artist,title=title))['text'],'')
    def test_youradio_artist_is_verified_in_the_breadcrumb(self):
        self.assertEqual(self.parse('youradio',self.youradio(artist='Another Singer'))['text'],'')
    def test_search_only_accepts_complete_on_site_song_paths(self):
        html='<h1>Výsledky vyhledávání</h1><a href="https://evil.example/pavol-habera/album/laska-necestuj-tym-vlakom">Bad</a><a href="/pavol-habera/album/laska-necestuj-tym-vlakom-live">Wrong version</a><a href="/pavol-habera/album/laska-necestuj-tym-vlakom">Correct</a>'.encode()
        result=self.parse('youradio',html)
        self.assertEqual(result['links'],['https://textypisni.youradio.cz/pavol-habera/album/laska-necestuj-tym-vlakom'])
        self.assertFalse(result['negative'])
    def test_hudba_search_candidates_are_bounded_and_still_need_final_page_identity(self):
        links=''.join('<a href="/pavol-habera/piesen/laska-necestuj-tym-vlakom-%d/">Candidate</a>'%i for i in range(5))
        result=self.parse('hudba',('<h1>Vyhľadávanie</h1>'+links).encode())
        self.assertEqual(len(result['links']),2)
    def test_blocked_login_and_changed_markup_are_not_cached_as_real_misses(self):
        for html in (b'<h1>Access denied</h1>',b'<script>challenge()</script>',b'<h1>Login</h1><form></form>'):
            with self.assertRaises(ValueError):self.parse('hudba',html)
    def test_host_and_redirect_validation_rejects_external_and_local_addresses(self):
        from urllib.request import Request
        for url in ('http://hudba.zoznam.sk/','https://hudba.zoznam.sk.evil.example/','https://127.0.0.1/','https://x@hudba.zoznam.sk/','https://hudba.zoznam.sk:123/','javascript:alert(1)'):
            self.assertFalse(self.sites.safe_url('hudba',url))
        redirect=self.sites.SameHostRedirect('hudba')
        with self.assertRaises(ValueError):redirect.redirect_request(Request('https://hudba.zoznam.sk/'),None,302,'',{},'https://evil.example/')
    def test_malformed_link_does_not_hide_a_valid_result(self):
        html='<h1>Výsledky vyhledávání</h1><a href="https://[invalid/">Broken</a><a href="/pavol-habera/album/laska-necestuj-tym-vlakom#original">Correct</a>'
        result=self.parse('youradio',html.encode())
        self.assertEqual(result['links'],['https://textypisni.youradio.cz/pavol-habera/album/laska-necestuj-tym-vlakom'])
        self.assertFalse(self.sites.safe_url('youradio','https://[invalid/'))
    def test_unclosed_lyrics_container_does_not_absorb_footer_or_advertisements(self):
        html='<h1>Pavol Habera</h1><h2>Láska, necestuj tým vlakom</h2><div class="song-text-full-width">Original test line<footer>Advertisement</footer>'
        with self.assertRaises(ValueError):self.parse('hudba',html.encode())
    def test_cache_upgrade_preserves_found_text_but_invalidates_old_negative_results(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder=Path(tmp);file=folder/(provider.key('Artist','Song')+'.json')
            file.write_text(json.dumps({'version':3,'saved':1000,'status':'found','text':'Original cached text'}))
            def fail(*a,**kw):raise AssertionError('Positive cache should survive upgrade')
            self.assertEqual(provider.lookup('Artist','Song',folder,opener=fail,clock=lambda:1001)['text'],'Original cached text')
            file.write_text(json.dumps({'version':3,'saved':1000,'status':'not-found','text':''}))
            def found(request,**kw):return io.BytesIO(json.dumps([dict(artistName='Artist',trackName='Song',plainLyrics='New original text')]).encode())
            self.assertEqual(provider.lookup('Artist','Song',folder,opener=found,clock=lambda:1001)['text'],'New original text')
    def test_regional_worker_finds_text_when_both_json_apis_fail(self):
        def response(request,**kwargs):
            if request.full_url.startswith('https://hudba.zoznam.sk/'):return io.BytesIO(self.hudba())
            raise TimeoutError('Other source unavailable')
        with tempfile.TemporaryDirectory() as tmp:
            folder=Path(tmp);result=provider.lookup('Pavol Habera','Láska, necestuj tým vlakom',folder,opener=response,hedge_delay=0.005)
            self.assertEqual(result['text'],'Original regional test text')
            status=json.loads((folder/'.last-result').read_text())
            self.assertTrue(any(row['source']=='hudba' and row['status']=='found' for row in status['requests']))
    def test_youradio_search_then_exact_song_finds_text(self):
        from urllib.error import HTTPError
        def response(request,**kwargs):
            if request.full_url.startswith('https://textypisni.youradio.cz/hledej/'):
                return io.BytesIO('<h1>Výsledky vyhledávání</h1><a href="/pavol-habera/album/laska-necestuj-tym-vlakom">Pavol Habera - Láska</a>'.encode())
            if request.full_url.startswith('https://textypisni.youradio.cz/pavol-habera/'):
                return io.BytesIO(self.youradio())
            raise HTTPError(request.full_url,404,'missing',{},None)
        with tempfile.TemporaryDirectory() as tmp:
            result=provider.lookup('Pavol Habera','Láska, necestuj tým vlakom',Path(tmp),opener=response)
            self.assertEqual(result['text'],'Original test line\nAnother line')
    def test_recognized_empty_search_is_a_miss_and_unknown_html_remains_retryable(self):
        from urllib.error import HTTPError
        def response(request,**kwargs):
            if request.full_url.startswith('https://hudba.zoznam.sk/hladaj/'):return io.BytesIO('<h1>Vyhľadávanie</h1>'.encode())
            if request.full_url.startswith('https://textypisni.youradio.cz/'):return io.BytesIO('<h1>Výsledky vyhledávání</h1>'.encode())
            raise HTTPError(request.full_url,404,'missing',{},None)
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(provider.lookup('Artist','Song',Path(tmp),opener=response)['status'],'not-found')
        def blocked(request,**kwargs):return io.BytesIO(b'<h1>Blocked</h1>')
        with tempfile.TemporaryDirectory() as tmp:
            folder=Path(tmp);self.assertEqual(provider.lookup('Artist','Song',folder,opener=blocked)['status'],'offline')
            self.assertEqual(list(folder.glob('*.json')),[])
    def test_oversized_and_deep_html_are_rejected(self):
        with self.assertRaises(ValueError):self.parse('hudba',b'<div>'*130+b'hello'+b'</div>'*130)
        response=lambda *a,**kw:io.BytesIO(b'x'*(provider.MAX_RESPONSE+1))
        with tempfile.TemporaryDirectory() as tmp:
            folder=Path(tmp);self.assertEqual(provider.lookup('Artist','Song',folder,opener=response)['status'],'offline')
            status=json.loads((folder/'.last-result').read_text());self.assertLessEqual(len(status['requests']),12)


class CompactCoverTests(unittest.TestCase):
    def setUp(self):
        class Base:
            FALLBACK_ARTWORK='/approved-fallback.png'
            def __init__(self):self.instance=None;self._decodeToken=0;self._picload=None;self.paths=[];self.skinAttributes=[];self._timer=Timer()
            def postWidgetCreate(self,instance):self.instance=instance
            def applySkin(self,*args):return True
            def _showPath(self,path):self.paths.append(path)
            def _poll(self):pass
            def preWidgetRemove(self,instance):self.instance=None
        class Edge:
            def __init__(self,parent):self.parent=parent
            def setTransparent(self,*args):pass
            def setBackgroundColor(self,*args):pass
            def hide(self):pass
            def show(self):pass
            def move(self,value):self.position=value
            def resize(self,value):self.size=value
        modules={'enigma':types.SimpleNamespace(eLabel=Edge,ePoint=lambda x,y:(x,y),eSize=lambda w,h:(w,h)),
                 'skin':types.SimpleNamespace(parseColor=lambda value:value),
                 'Components.Renderer.WarderRadioArtwork':types.SimpleNamespace(WarderRadioArtwork=Base)}
        with patch.dict(sys.modules,modules):
            spec=importlib.util.spec_from_file_location('compact_cover_test',P/'Components/Renderer/WarderRadioCompactArtwork.py')
            self.m=importlib.util.module_from_spec(spec);spec.loader.exec_module(self.m)
    def test_square_portrait_landscape_and_fallback_stay_centre_aligned_without_stretching(self):
        for width,height in ((600,600),(300,600),(1200,600),(704,640),(100000,1)):
            x,y,w,h=self.m.fitted_cover(width,height)
            self.assertLessEqual(w,420);self.assertLessEqual(h,420)
            self.assertLessEqual(abs(x+w/2-526),0.5)
            self.assertLessEqual(abs(y+h/2-496),0.5)
            if min(width,height)>1:self.assertLess(abs(w/h-width/height),0.01)
        self.assertEqual(self.m.fitted_cover(600,600),(316,286,420,420))
    def test_image_headers_are_parsed_without_a_full_decoder_or_optional_receiver_packages(self):
        from PIL import Image
        with tempfile.TemporaryDirectory() as tmp:
            for kind in ('PNG','JPEG','GIF','BMP'):
                path=Path(tmp)/('cover.'+kind.lower());Image.new('RGB',(360,640)).save(path,format=kind)
                self.assertEqual(self.m.picture_size(path),(360,640),kind)
            bad=Path(tmp)/'bad.jpg';bad.write_bytes(b'not an image'*100000)
            self.assertIsNone(self.m.picture_size(bad))
        fallback=ROOT/'source/package-root/usr/share/enigma2/hd_glass17/warder-radio-no-cover.png'
        self.assertEqual(self.m.picture_size(fallback),self.m.WarderRadioCompactArtwork.FALLBACK_SIZE)
    def test_native_frame_fits_the_actual_image_instead_of_the_full_old_slot(self):
        from unittest.mock import Mock
        r=self.m.WarderRadioCompactArtwork();widget=Mock();r.postWidgetCreate(widget)
        r._showPath(r.FALLBACK_ARTWORK);r._poll()
        widget.move.assert_called_with((316,305));widget.resize.assert_called_with((420,382))
        self.assertEqual(r.paths,[r.FALLBACK_ARTWORK])
        self.assertTrue(all(edge.position[0]>=0 and edge.position[1]>=0 for edge in r._edges))
    def test_late_sizing_result_cannot_replace_a_newer_cover_or_fallback(self):
        from threading import Event
        from unittest.mock import Mock
        entered=Event();release=Event();finished=Event()
        def read(path):entered.set();release.wait(1);finished.set();return (600,600)
        r=self.m.WarderRadioCompactArtwork();widget=Mock();r.postWidgetCreate(widget)
        with patch.object(self.m,'picture_size',side_effect=read):
            r._showPath('/old-cover.jpg');self.assertTrue(entered.wait(0.5))
            r._showPath(r.FALLBACK_ARTWORK);release.set();self.assertTrue(finished.wait(0.5))
            r._poll()
        self.assertEqual(r.paths,[r.FALLBACK_ARTWORK])
    def test_removed_widget_rejects_pending_sizing_and_stale_decoders(self):
        from unittest.mock import Mock
        r=self.m.WarderRadioCompactArtwork();widget=Mock();r.postWidgetCreate(widget)
        r._fitReady=(r._fitGeneration,'/pending-cover.jpg',(600,600));token=r._decodeToken;r.preWidgetRemove(widget);r._poll()
        self.assertEqual(r.paths,[]);self.assertIsNone(r._fitReady);self.assertGreaterEqual(r._decodeToken,token)


class RadioDateTests(unittest.TestCase):
    def test_localized_weekdays_and_full_date_fit_header(self):
        class Converter:
            def __init__(self,*args):pass
        modules={'Components.Converter.Converter':types.SimpleNamespace(Converter=Converter),
                 'Components.Element':types.SimpleNamespace(cached=lambda method:method),
                 'NavigationInstance':types.SimpleNamespace(instance=None)}
        with patch.dict(sys.modules,modules):
            spec=importlib.util.spec_from_file_location('radio_type_test',P/'Components/Converter/WarderRadioServiceType.py')
            module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
        from datetime import datetime,timedelta
        from PIL import ImageFont
        timestamp=datetime(2026,10,28,12).timestamp()
        self.assertEqual(module.radio_date(timestamp,'sk_SK'),'Streda 28.10.2026')
        self.assertEqual(module.radio_date(timestamp,'cs_CZ'),'Středa 28.10.2026')
        self.assertEqual(module.radio_date(timestamp,'fr_FR'),'Mercredi 28.10.2026')
        self.assertEqual(module.radio_date(None,'sk_SK'),'')
        font=ImageFont.truetype(str(ROOT/'source/package-root/usr/share/fonts/prive7.ttf'),32)
        for code in module.WEEKDAYS:
            for day in range(7):
                value=module.radio_date((datetime(2026,10,26,12)+timedelta(days=day)).timestamp(),code)
                self.assertLessEqual(font.getlength(value),520,(code,value))


if __name__=='__main__':unittest.main()
