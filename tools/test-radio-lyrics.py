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
    def test_missing_text_notice_is_not_lyrics_but_embedded_words_are_preserved(self):
        notice='Táto pieseň momentálne nemá pridaný text.'
        for value in (notice,notice.upper(),'\nTato piesen\u00a0momentalne nema pridany text…\n'):
            self.assertEqual(provider.clean_text(value),'')
            row=self.record();row['plainLyrics']=value
            self.assertEqual(provider.select([row],'Žbirka','Biely kvet'),'')
        row=self.record();row['plainLyrics']='';row['syncedLyrics']='[00:01.00]'+notice
        self.assertEqual(provider.select([row],'Žbirka','Biely kvet'),'')
        real='Original illustrative opening line\n'+notice+'\nOriginal illustrative ending line'
        self.assertEqual(provider.clean_text(real),real)
    def test_old_positive_notice_cache_is_refetched_instead_of_displayed(self):
        for version in (3,provider.CACHE_VERSION):
            with self.subTest(version=version),tempfile.TemporaryDirectory() as tmp:
                folder=Path(tmp);file=folder/(provider.key('Žbirka','Biely kvet')+'.json')
                file.write_text(json.dumps({'version':version,'saved':1000,'status':'found','text':'Táto pieseň momentálne nemá pridaný text.'}))
                calls=[]
                def response(request,**kwargs):
                    calls.append(request.full_url)
                    return io.BytesIO(json.dumps([self.record()]).encode())
                self.assertEqual(provider.lookup('Žbirka','Biely kvet',folder,opener=response,clock=lambda:1001)['text'],'Original test text')
                self.assertTrue(calls)
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
            folder=Path(tmp);result=provider.lookup('Faraon','Šlapací kolo',folder,diagnostics=True,opener=response)
            self.assertEqual(result['status'],'not-found');self.assertTrue(result['partial'])
            self.assertEqual(len(list(folder.glob('*.json'))),0)
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
            try:result=provider.lookup('Artist','Title',Path(tmp),diagnostics=True,opener=response,hedge_delay=0.01,budget=2.05)
            finally:release.set()
            self.assertEqual(result['status'],'not-found')
            data=json.loads((Path(tmp)/'.last-result').read_text())
            self.assertTrue(any(row['status']=='pending' for row in data['requests']))
    def test_partial_miss_is_not_cached_and_recovery_needs_no_station_change(self):
        from urllib.error import HTTPError
        def response(request,**kwargs):
            if request.full_url.startswith(provider.FALLBACK):raise HTTPError(request.full_url,404,'missing',{},None)
            if 'artist_name=' in request.full_url:return io.BytesIO(b'[]')
            raise TimeoutError('optional query failed')
        with tempfile.TemporaryDirectory() as tmp:
            folder=Path(tmp);result=provider.lookup('Žbirka','Biely kvet',folder,opener=response,clock=lambda:1000)
            self.assertTrue(result['partial'])
            self.assertFalse((folder/(provider.key('Žbirka','Biely kvet')+'.json')).exists())
            good=lambda *a,**kw:io.BytesIO(json.dumps([self.record()]).encode())
            self.assertEqual(provider.lookup('Žbirka','Biely kvet',folder,opener=good,clock=lambda:1005)['status'],'found')
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
            provider.lookup('Žbirka','Biely kvet',folder,diagnostics=True,opener=response)
            data=(folder/'.last-result').read_text();self.assertNotIn('Original test text',data)
            self.assertLessEqual(len(json.loads(data)['requests']),5)
            provider.lookup('Žbirka','Biely kvet',folder,diagnostics=True,opener=response)
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
    def test_space_less_metadata_starts_lookup_instead_of_waiting_forever(self):
        import warderSongIdentity as identity
        r=self.renderer;self.song()
        self.m.native_song=lambda *a:identity.split_stream('MIROSLAV ZBIRKA-Biely Kvet')
        r._poll();r._pending_since-=3;r._poll()
        self.assertEqual(len(self.spawned),1)
        self.assertEqual(self.spawned[0][2][-2:],['MIROSLAV ZBIRKA','Biely Kvet'])
        self.assertNotIn('Čakám',r.label.text)
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
    def test_transient_failure_retries_but_stops_after_five_attempts(self):
        r=self.renderer;self.song();r._poll();r._pending_since-=3;r._poll()
        for attempt in range(5):
            worker=self.spawned[-1][0];worker.outReceived(b'{"text":"","status":"offline"}');worker.complete(0)
            self.assertEqual(r._attempts,attempt+1)
            if attempt<4:
                self.assertGreater(r._retry_at,0);r._retry_at=1;r._poll()
        self.assertEqual(r._retry_at,0);r._poll();self.assertEqual(len(self.spawned),5)
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

    def test_regional_station_passes_profile_without_gui_network_io(self):
        r=self.renderer
        ref=types.SimpleNamespace(toString=lambda:'station',getName=lambda:'Rádio KIKS Československo')
        self.navigation.instance.getCurrentlyPlayingServiceReference=lambda:ref
        self.m.native_song=lambda *a:('Artist','Title')
        r._poll();r._pending_since-=3;r._poll()
        self.assertEqual(self.spawned[0][2][-2:],['--profile','skcz'])
    def test_partial_miss_retries_without_zapping_and_later_text_is_displayed(self):
        r=self.renderer;self.song();r._poll();r._pending_since-=3;r._poll()
        worker=self.spawned[-1][0];worker.outReceived(b'{"text":"","status":"not-found","partial":true}');worker.complete(0)
        self.assertGreater(r._retry_at,0);r._retry_at=1;r._poll()
        self.assertEqual(len(self.spawned),2)
        worker=self.spawned[-1][0];worker.outReceived(b'{"text":"Recovered original test text","status":"found"}');worker.complete(0)
        self.assertEqual(r.label.text,'Recovered original test text');r._poll();self.assertEqual(len(self.spawned),2)
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
        # Reverse only the exact reviewed compatibility screens, then the
        # independently verified keyboard repair. Keep the original baseline.
        compatibility=ROOT/'design/openatv-compatibility/skin-edits.json'
        if compatibility.exists():
            for edit in json.loads(compatibility.read_text())['edits']:
                self.assertEqual(text.count(edit['updated_screen']),1)
                text=text.replace(edit['updated_screen'],edit['original_screen'],1)
        keyboard=json.loads((ROOT/'design/virtual-keyboard/compatibility.json').read_text())
        self.assertEqual(hashlib.sha256(text.encode()).hexdigest(),keyboard['updated_skin_sha256'])
        self.assertEqual(text.count(keyboard['updated_screen']),1)
        text=text.replace(keyboard['updated_screen'],keyboard['original_screen'],1)
        self.assertEqual(hashlib.sha256(text.encode()).hexdigest(),keyboard['original_skin_sha256'])
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
    def test_hudba_absence_notice_cannot_win_over_a_later_real_source(self):
        import time
        from urllib.error import HTTPError
        def response(request,**kwargs):
            if request.full_url.startswith('https://hudba.zoznam.sk/'):
                return io.BytesIO(self.hudba(text='Táto pieseň momentálne nemá pridaný text.'))
            if request.full_url.startswith('https://textypisni.youradio.cz/'):
                time.sleep(0.02)
                return io.BytesIO(self.youradio())
            raise HTTPError(request.full_url,404,'missing',{},None)
        with tempfile.TemporaryDirectory() as tmp:
            folder=Path(tmp)
            result=provider.lookup('Pavol Habera','Láska, necestuj tým vlakom',folder,opener=response,hedge_delay=0.005)
            self.assertEqual(result['text'],'Original test line\nAnother line')
            saved=json.loads((folder/(provider.key('Pavol Habera','Láska, necestuj tým vlakom')+'.json')).read_text())
            self.assertNotIn('nemá pridaný text',saved['text'])
    def test_hudba_notice_and_other_source_failures_remain_retryable(self):
        def response(request,**kwargs):
            if request.full_url.startswith('https://hudba.zoznam.sk/'):
                return io.BytesIO(self.hudba(text='Táto pieseň momentálne nemá pridaný text.'))
            raise TimeoutError('Other source unavailable')
        with tempfile.TemporaryDirectory() as tmp:
            folder=Path(tmp)
            result=provider.lookup('Pavol Habera','Láska, necestuj tým vlakom',folder,opener=response,hedge_delay=0.005)
            self.assertEqual(result['status'],'offline')
            self.assertEqual(result['text'],'')
            self.assertFalse(list(folder.glob('*.json')))
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
            folder=Path(tmp);result=provider.lookup('Pavol Habera','Láska, necestuj tým vlakom',folder,diagnostics=True,opener=response,hedge_delay=0.005)
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
            folder=Path(tmp);self.assertEqual(provider.lookup('Artist','Song',folder,diagnostics=True,opener=response)['status'],'offline')
            status=json.loads((folder/'.last-result').read_text());self.assertLessEqual(len(status['requests']),33)


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


class CombinedEngineTests(unittest.TestCase):
    def setUp(self):
        import warderSongIdentity,warderLyricsSites
        self.identity=warderSongIdentity;self.sites=warderLyricsSites
    def row(self,artist,title):
        return dict(artistName=artist,trackName=title,plainLyrics='Illustrative original test text')
    def test_track_number_prefix_is_repaired_but_years_and_numeric_act_names_survive(self):
        self.assertEqual(self.identity.split_stream('08 - Krasnejsi nez ruze (Maliconia) - Pavel Roth'),('Pavel Roth','Krasnejsi nez ruze (Maliconia)'))
        self.assertEqual(self.identity.repair_pair('08','Krasnejsi nez ruze (Maliconia) - Pavel Roth'),('Pavel Roth','Krasnejsi nez ruze (Maliconia)'))
        for raw,expected in [('1970 - Chinaski',('1970','Chinaski')),('070 Shake - Song',('070 Shake','Song')),('08 - Song',('08','Song')),('Artist - Part 1 - Song',('Artist','Part 1 - Song'))]:
            self.assertEqual(self.identity.split_stream(raw),expected)
    def test_zbirka_alias_and_recording_credit_do_not_drop_extra_guests(self):
        row=self.row('Miroslav Žbirka','Biely kvet')
        self.assertTrue(provider.same_song(row,'M. Zbirka, Limit','Biely kvet'))
        for artist,title in [('M. Zbirka, Limit, Guest','Biely kvet'),('M. Zbirka, Limit','Another song'),('M. Zbirka, Limit','Biely kvet (Live)')]:
            self.assertFalse(provider.same_song(row,artist,title))
    def test_neckar_known_spelling_and_exact_title_variants(self):
        row=self.row('Václav Neckář','Svatovítský chrám /Chrám sv. Víta/ (Winchester Cathedral)')
        self.assertTrue(provider.same_song(row,'Necar Vaclav','Svatovitsky chram'))
        self.assertFalse(provider.same_song(row,'Other Vaclav','Svatovitsky chram'))
        self.assertFalse(provider.same_song(row,'Necar Vaclav','Svatovitsky chram (Live)'))
    def test_roth_title_typo_and_alternate_name_are_artist_scoped(self):
        row=self.row('Pavel Roth','Malinconia (Krásnější než růže)')
        self.assertTrue(provider.same_song(row,'08','Krasnejsi nez ruze (Maliconia) - Pavel Roth'))
        self.assertFalse(provider.same_song(row,'Pavel Roth','Krásnější než růže (Remix)'))
        self.assertFalse(provider.same_song(self.row('Another Artist','Malinconia (Krásnější než růže)'),'Another Artist','Krásnější než růže'))
    def test_publisher_verified_band_abbreviation_keeps_every_performer(self):
        row=self.row('Michal David & Kroky Františka Janečka','Každý mi tě, lásko, závidí')
        for credit in ('Michal David, Kroky F. Janecka','Michal David & Kroky F.Janečka'):
            self.assertTrue(provider.same_song(row,credit,'Kazdy Mi Te Lasko Zavidi'))
        for credit in ('Michal David','Kroky F. Janecka','Michal David, Kroky F. Janecka, Guest','Michal David, Kroky F. Novak'):
            self.assertFalse(provider.same_song(row,credit,'Kazdy Mi Te Lasko Zavidi'))
        self.assertFalse(provider.same_song(dict(row,trackName='Každý mi tě, lásko, závidí (Live)'),'Michal David, Kroky F. Janecka','Kazdy Mi Te Lasko Zavidi'))
        self.assertEqual(self.identity.query_pair('Michal David, Kroky F. Janecka','Kazdy Mi Te Lasko Zavidi')[0],'Kroky Františka Janečka & Michal David')
    def test_stromy_original_version_is_scoped_and_other_versions_stay_distinct(self):
        row=self.row('Peter Bic Project','Stromy (Original Version)')
        self.assertTrue(provider.same_song(row,'Peter Bič Project','Stromy'))
        for track in ('Stromy (Radio Edit)','Stromy (Live)','Stromy (Remix)','Stromy (naživo - Len sa smej turné 2024)'):
            self.assertFalse(provider.same_song(dict(row,trackName=track),'Peter Bič Project','Stromy'))
        self.assertFalse(provider.same_song(self.row('Another Artist','Stromy (Original Version)'),'Another Artist','Stromy'))
    def test_inline_feature_title_is_shared_without_omitting_guests(self):
        row=self.row('A.M.O. & Polemic','Spolu')
        for title in ('SPOLU FT. A.M.O.','Spolu feat AMO','Spolu featuring A.M.O.'):
            self.assertTrue(provider.same_song(row,'POLEMIC',title))
        self.assertFalse(provider.same_song(self.row('Polemic','Spolu'),'POLEMIC','SPOLU FT. A.M.O.'))
        self.assertFalse(provider.same_song(self.row('A.M.O. & Polemic & Guest','Spolu'),'POLEMIC','SPOLU FT. A.M.O.'))
        self.assertFalse(provider.same_song(row,'POLEMIC','Spolu (Live) ft. A.M.O.'))
    def test_underscore_file_prefix_is_removed_from_full_artist_but_remix_remains(self):
        self.assertEqual(self.identity.repair_pair('24_Pavol Habera','Reklama na ticho (remix)'),('Pavol Habera','Reklama na ticho (remix)'))
        self.assertEqual(self.identity.split_stream('24_Pavol Habera - Reklama na ticho (remix)'),('Pavol Habera','Reklama na ticho (remix)'))
        for name in ('24kGoldn','070 Shake','1975','24_Band','24_PavolHabera'):
            self.assertEqual(self.identity.repair_pair(name,'Song'),(name,'Song'))
        self.assertFalse(provider.same_song(self.row('Pavol Habera','Reklama na ticho'),'24_Pavol Habera','Reklama na ticho (remix)'))
    def test_documented_helena_song_includes_its_duet_credit_only_for_known_title(self):
        row=self.row('Helena Vondrackova & Jiri Korn','Každá trampota má svou mez (Rest Your Love On Me)')
        self.assertTrue(provider.same_song(row,'HELENA VONDRÁČKOVÁ','Kazda trampota ma svou mez'))
        self.assertFalse(provider.same_song(dict(row,trackName='Other song'),'Helena Vondráčková','Other song'))
        self.assertFalse(provider.same_song(dict(row,artistName='Helena Vondrackova & Jiri Korn & Guest'),'Helena Vondráčková','Kazda trampota ma svou mez'))
        self.assertFalse(provider.same_song(dict(row,trackName='Každá trampota má svou mez (Live)'),'Helena Vondráčková','Kazda trampota ma svou mez'))
    def test_test10_positive_cache_survives_and_its_negative_cache_is_rechecked(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder=Path(tmp);file=folder/(provider.key('Artist','Song')+'.json')
            file.write_text(json.dumps({'version':5,'saved':1000,'status':'found','text':'Original cached test line'}))
            with patch.object(provider,'urlopen',side_effect=AssertionError('Cache hit must not use the network')):
                self.assertEqual(provider.lookup('Artist','Song',folder,clock=lambda:1001)['text'],'Original cached test line')
            file.write_text(json.dumps({'version':5,'saved':1000,'status':'not-found','text':''}))
            response=lambda *a,**kw:io.BytesIO(json.dumps([self.row('Artist','Song')]).encode())
            self.assertEqual(provider.lookup('Artist','Song',folder,opener=response,clock=lambda:1001)['status'],'found')
    def test_receiver_reported_uvitelkou_typo_is_repaired_only_for_darinka(self):
        row=self.row('Darinka Rolincová','Až raz budem učiteľkou')
        self.assertTrue(provider.same_song(row,'DARINKA ROLINCOVA','Az raz budem uvitelkou'))
        self.assertEqual(self.identity.query_pair('DARINKA ROLINCOVA','Az raz budem uvitelkou'),('DARINKA ROLINCOVA','Až raz budem učiteľkou'))
        self.assertFalse(provider.same_song(self.row('Another Artist','Až raz budem učiteľkou'),'Another Artist','Az raz budem uvitelkou'))
        self.assertFalse(provider.same_song(row,'DARINKA ROLINCOVA','Az raz budem uvitelkou (Live)'))
    def test_full_name_slash_credit_matches_without_splitting_acdc(self):
        row=self.row('Vidiek','Hrajte trúbky (feat. Boban Markovic & Marko Markovic)')
        self.assertTrue(provider.same_song(row,'Vidiek','Hrajte trúbky, feat. Boban Markovic / Marko Markovic'))
        self.assertFalse(provider.same_song(self.row('Vidiek','Hrajte trúbky (feat. Boban Markovic)'),'Vidiek','Hrajte trúbky, feat. Boban Markovic / Marko Markovic'))
        self.assertEqual(self.identity.roster('AC/DC'),('ac/dc',))
        self.assertTrue(provider.same_song(self.row('Vidiek','Hrajte trúbky'),'Vidiek','Hrajte trúbky, feat. Boban Markovic / Marko Markovic'))
        self.assertEqual(self.identity.site_artists('Vidiek','Hrajte trúbky, feat. Boban Markovic / Marko Markovic'),['Vidiek'])
    def test_karaoke_reads_only_original_paragraphs_not_translation_or_ads(self):
        url='https://www.karaoketexty.sk/texty-piesni/medial-banana/doba-strieda-dobu-793543'
        raw='<h1 id="song_title">Doba strieda dobu <span>- text</span></h1><div class="navigation_lyrics"><a href="/texty-piesni/medial-banana-51959">Medial Banana</a></div><div class="lyrics_cont"><span class="para_1lyrics_col1">Original line<br>Second line</span><aside>Advertisement</aside><span class="para_1lyrics_col2">Translation</span><span class="para_1lyrics_col1">Third line</span></div>'
        r=self.sites.parse('karaoke',url,raw.encode(),'Medial Banana','Doba strieda dobu',provider.same_song,provider.clean_text)
        self.assertEqual(r['text'],'Original line\nSecond line\n\nThird line')
        translated=raw.replace('- text</span>','- text, preklad</span>')
        self.assertEqual(self.sites.parse('karaoke',url,translated.encode(),'Medial Banana','Doba strieda dobu',provider.same_song,provider.clean_text)['text'],r['text'])
        self.assertEqual(self.sites.parse('karaoke',url,raw.encode(),'Other Artist','Doba strieda dobu',provider.same_song,provider.clean_text)['text'],'')
        self.assertTrue(self.sites.safe_url('karaoke','https://www.karaoketexty.cz/search?q=Song'))
        self.assertFalse(self.sites.safe_url('karaoke','https://www.karaoketexty.cz.evil.example/'))
    def test_karaoke_search_requires_whole_visible_artist_and_song(self):
        url='https://www.karaoketexty.sk/search?q=Song'
        raw='<h1>Hľadanie</h1><a href="/texty-piesni/wrong/song-1">Other Artist - Song</a><a href="/texty-piesni/artist/song-2">Artist - Song</a><a href="https://evil.example/texty-piesni/artist/song-3">Artist - Song</a>'
        r=self.sites.parse('karaoke',url,raw.encode(),'Artist','Song',provider.same_song,provider.clean_text)
        self.assertEqual(r['links'],['https://www.karaoketexty.sk/texty-piesni/artist/song-2'])
    def test_karaoke_follows_verified_result_before_searching_the_mirror(self):
        calls=[]
        def response(request,**kw):
            if request.full_url.startswith('https://www.karaoketexty.sk/search?'):
                calls.append('search')
                return io.BytesIO(b'<h1>Hladanie</h1>'.replace(b'Hladanie','Hľadanie'.encode())+b'<a href="/texty-piesni/artist/song-1">Artist - Song</a>')
            if request.full_url=='https://www.karaoketexty.sk/texty-piesni/artist/song-1':
                calls.append('song')
                return io.BytesIO(b'<h1>Song - text</h1><div class="navigation_lyrics"><a href="/texty-piesni/artist-1">Artist</a></div><span class="para_1lyrics_col1">Original test line</span>')
            if 'karaoketexty.cz' in request.full_url:
                calls.append('mirror');raise AssertionError('Mirror must not delay an already verified candidate')
            raise TimeoutError('Other sources disabled')
        with tempfile.TemporaryDirectory() as tmp:
            result=provider.lookup('Artist','Song',Path(tmp),opener=response,site_providers=('karaoke',),hedge_delay=0)
        self.assertEqual(result['text'],'Original test line');self.assertEqual(calls,['search','song'])
    def test_kytary_uses_complete_sheet_and_discards_chords_and_teaser(self):
        url='https://akordy.kytary.cz/song/song'
        raw='<script type="application/ld+json">{"lyrics":{"text":"Truncated teaser"}}</script><h1>Song</h1><h2>Artist</h2><div class="smartchordsheet"><div><span class="scs-chord"><span class="scs-chord-label">Am</span></span>Original line<br>Second line</div></div><aside>Advertising</aside>'
        r=self.sites.parse('kytary',url,raw.encode(),'Artist','Song',provider.same_song,provider.clean_text)
        self.assertEqual(r['text'],'Original line\nSecond line')
        self.assertEqual(self.sites.parse('kytary',url,raw.encode(),'Other Artist','Song',provider.same_song,provider.clean_text)['text'],'')
    def test_kytary_search_uses_title_and_artist_labels_not_lyric_hits(self):
        url='https://akordy.kytary.cz/songs?query=Song'
        raw='<h1>Písně s akordy a texty</h1><a href="/song/other"><span class="song-card-name">Other song</span><span class="song-card-author">Artist</span><span>Song lyric hit</span></a><a href="/song/song"><span class="song-card-name">Song</span><span class="song-card-author">Artist</span></a>'
        r=self.sites.parse('kytary',url,raw.encode(),'Artist','Song',provider.same_song,provider.clean_text)
        self.assertEqual(r['links'],['https://akordy.kytary.cz/song/song'])
    def test_feature_in_title_and_artist_keep_the_entire_roster(self):
        row=self.row('Bystrík & Fejbs','Káva')
        self.assertTrue(provider.same_song(row,'Bystrik','Káva (feat. Fejbs)'))
        self.assertFalse(provider.same_song(row,'Bystrik','Káva'))
        self.assertFalse(provider.same_song(row,'Bystrik','Káva (feat. Fejbs Junior)'))
    def test_married_name_does_not_turn_a_duet_into_a_solo_recording(self):
        row=self.row('Sima Magušinová (Martausová) & For You','Nenahraditeľná')
        self.assertTrue(provider.same_song(row,'Sima Martausová featuring For You','Nenahraditeľná'))
        self.assertFalse(provider.same_song(row,'Sima Martausová','Nenahraditeľná'))
    def test_recording_specific_heckovci_and_tasler_credits_keep_other_tracks_strict(self):
        for row,artist,title in [(self.row('Júlia a Peter Heckovci','Taliansky muzikál'),'Júlia Hečková','Taliansky muzikál'),(self.row('IMT Smile','Viac'),'Ivan Tásler & IMT Smile','Viac')]:
            self.assertTrue(provider.same_song(row,artist,title))
            self.assertFalse(provider.same_song(dict(row,trackName='Another song'),artist,'Another song'))
    def test_station_formats_select_regional_profile_and_unknown_names_keep_global(self):
        for name in ('Rádio KIKS Československo','Fun Rádio Československé hity','Československé rádio','IPTV SK/CZ'):
            self.assertEqual(self.identity.station_profile(name),'skcz')
        for name in ('Fun Radio','BBC Radio 2','Jazz Prague',''):
            self.assertEqual(self.identity.station_profile(name),'global')
    def test_ujdeto_original_container_and_married_name(self):
        raw='<h1>Sima Magušinová (Martausová) &amp; For You - Nenahraditeľná - text písně</h1><p class="ltext">Original line<br>Second line<script>bad()</script></p><aside>Advertising</aside>'
        r=self.sites.parse('ujdeto','https://www.ujdeto.cz/lyrics/sima-magusinova-martausova/nenahraditelna/',raw.encode(),'Sima Martausová featuring For You','Nenahraditeľná',provider.same_song,provider.clean_text)
        self.assertEqual(r['text'],'Original line\nSecond line')
    def test_pisnicky_uses_song_heading_and_discards_chord_lines(self):
        raw='<h1>Písničky Akordy</h1><div id="songheader"><h1>Ani ty ani já</h1><h2>David Koller</h2></div><div id="songtext"><pre>C G Am F\nOriginal test line\nSecond line</pre></div><aside>Advertising</aside>'
        r=self.sites.parse('pisnicky','https://pisnicky-akordy.cz/david-koller/ani-ty-ani-ja',raw.encode(),'David Koller','Ani ty ani já',provider.same_song,provider.clean_text)
        self.assertEqual(r['text'],'Original test line\nSecond line')
        r=self.sites.parse('pisnicky','https://pisnicky-akordy.cz/david-koller/ani-ty-ani-ja',raw.encode(),'Another Artist','Ani ty ani já',provider.same_song,provider.clean_text)
        self.assertEqual(r['text'],'')
    def test_tekstowo_original_only_never_uses_polish_translation(self):
        url='https://www.tekstowo.pl/dara-rolins/slub'
        raw='<h1>Dara Rolins - Sľub</h1><div id="songText"><h2>Original</h2><div class="inner-text">Original test line<br>Second line</div><aside>Revision links</aside></div><div id="songTranslation"><div class="inner-text">Translation must not appear</div></div>'
        result=self.sites.parse('tekstowo',url,raw.encode(),'Dara Rolins','Sľub',provider.same_song,provider.clean_text)
        self.assertEqual(result['text'],'Original test line\nSecond line')
        result=self.sites.parse('tekstowo',url,raw.encode(),'Other Artist','Sľub',provider.same_song,provider.clean_text)
        self.assertEqual(result['text'],'')
        with self.assertRaises(ValueError):
            self.sites.parse('tekstowo',url,raw.replace('id="songText"','id="other"').encode(),'Dara Rolins','Sľub',provider.same_song,provider.clean_text)
    def test_new_hosts_reject_cross_host_redirects_and_unknown_markup(self):
        for name in ('ujdeto','pisnicky','tekstowo','karaoke','kytary'):
            self.assertFalse(self.sites.safe_url(name,'https://127.0.0.1/'))
            with self.assertRaises(ValueError):
                self.sites.parse(name,'https://'+self.sites.HOSTS[name]+'/',b'<h1>Login required</h1>','Artist','Song',provider.same_song,provider.clean_text)
    def test_regional_profile_starts_both_primary_catalogues_without_waiting(self):
        from threading import Barrier
        import time
        barrier=Barrier(2);calls=[]
        def response(request,**kwargs):
            calls.append(request.full_url)
            if request.full_url.startswith(provider.SEARCH):
                barrier.wait(0.5)
                return io.BytesIO(json.dumps([self.row('Artist','Song')]).encode())
            if request.full_url.startswith('https://hudba.zoznam.sk/'):
                barrier.wait(0.5)
                return io.BytesIO(b'<h1>Artist</h1><h2>Song</h2><div class="song-text-full-width">Original regional text</div>')
            raise AssertionError('Slow alternatives should not be needed')
        with tempfile.TemporaryDirectory() as tmp:
            began=time.monotonic();r=provider.lookup('Artist','Song',Path(tmp),opener=response,profile='skcz',hedge_delay=1)
            self.assertEqual(r['status'],'found');self.assertLess(time.monotonic()-began,0.6)
        self.assertEqual(len(calls),2)
    def test_global_profile_keeps_fast_lrclib_path(self):
        calls=[]
        def response(request,**kwargs):calls.append(request.full_url);return io.BytesIO(json.dumps([self.row('Artist','Song')]).encode())
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(provider.lookup('Artist','Song',Path(tmp),opener=response)['status'],'found')
        self.assertEqual(len(calls),1);self.assertTrue(calls[0].startswith(provider.SEARCH))
    def test_previous_negative_cache_is_invalidated_for_additional_sources(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder=Path(tmp);file=folder/(provider.key('Artist','Song')+'.json')
            file.write_text(json.dumps({'version':4,'saved':1000,'status':'not-found','text':''}))
            response=lambda *a,**kw:io.BytesIO(json.dumps([self.row('Artist','Song')]).encode())
            self.assertEqual(provider.lookup('Artist','Song',folder,opener=response,clock=lambda:1001)['status'],'found')
    def test_official_artist_page_is_recording_scoped_and_requires_its_brand_and_id(self):
        self.assertEqual(self.sites.initial_urls('roth','Pavel Roth','Another song'),[])
        url='https://www.pavelroth.cz/texty.htm?skladba=36'
        raw='<title>Pavel Roth | texty</title><h1>Malinconia (Krásnější než růže)</h1><div class="CDtexty">Original test line<br>Second line</div>'
        r=self.sites.parse('roth',url,raw.encode(),'08','Krasnejsi nez ruze (Maliconia) - Pavel Roth',provider.same_song,provider.clean_text)
        self.assertEqual(r['text'],'Original test line\nSecond line')
        for page,location in [(raw.replace('Pavel Roth | texty','Other site'),url),(raw,url.replace('36','37'))]:
            with self.assertRaises(ValueError):self.sites.parse('roth',location,page.encode(),'Pavel Roth','Krásnější než růže',provider.same_song,provider.clean_text)
    def test_new_sources_respect_host_backoff_between_songs(self):
        from urllib.error import HTTPError
        calls=[]
        def response(request,**kwargs):
            if request.full_url.startswith('https://www.ujdeto.cz/'):
                calls.append(request.full_url)
                raise HTTPError(request.full_url,429,'busy',{'Retry-After':'120'},None)
            raise HTTPError(request.full_url,404,'missing',{},None)
        with tempfile.TemporaryDirectory() as tmp:
            folder=Path(tmp)
            self.assertGreaterEqual(provider.lookup('Artist','Song',folder,opener=response,clock=lambda:1000)['retry_after'],120)
            provider.lookup('Artist','Another song',folder,opener=response,clock=lambda:1001)
        self.assertEqual(len(calls),1)
    def test_all_source_failures_stay_bounded_and_are_not_cached_as_a_miss(self):
        calls=[]
        def response(request,**kwargs):
            calls.append(kwargs['timeout']);raise TimeoutError('all sources unavailable')
        with tempfile.TemporaryDirectory() as tmp:
            folder=Path(tmp);r=provider.lookup('Pavel Roth','Krásnější než růže',folder,opener=response,profile='skcz')
            self.assertEqual(r['status'],'offline');self.assertFalse(list(folder.glob('*.json')))
        self.assertLessEqual(len(calls),34);self.assertTrue(all(0<t<=10 for t in calls))



class SuperMusicTests(unittest.TestCase):
    def setUp(self):
        import warderLyricsSites,warderSuperMusic
        self.sites,self.transport=warderLyricsSites,warderSuperMusic
    def parse(self,raw,artist='Instinct',title='Dozadu',url='https://www.supermusic.cz/piesen.php?id=1'):
        return self.sites.parse('supermusic',url,raw.encode(),artist,title,provider.same_song,provider.clean_text)
    def song(self,artist='Instinct',title='Dozadu'):
        return '<title>'+title+' – '+artist+' | Akordy | SuperMusic.cz</title><div id="chordText">Original <span class="chord">F#</span>first line<br/>Second &amp; original line</div><footer>Advertisement</footer>'
    def test_song_identity_and_chord_removal(self):
        r=self.parse(self.song());self.assertEqual(r['text'],'Original first line\nSecond & original line');self.assertNotIn('Advertisement',r['text'])
    def test_wrong_artist_or_recording_version_rejected(self):
        for artist,title in [('Other Artist','Dozadu'),('Instinct','Dozadu (Live)'),('Instinct','Dozadu (remix)')]:
            self.assertEqual(self.parse(self.song(artist,title))['text'],'')
    def test_verified_imt_subtitle_is_scoped(self):
        self.assertTrue(self.parse(self.song('IMT Smile','Úsmev a čaj {I am tea-smile}'),'IMT Smile','Úsmev a čaj')['text'])
        self.assertEqual(self.parse(self.song('IMT Smile','Úsmev a čaj {Live}'),'IMT Smile','Úsmev a čaj')['text'],'')
    def test_search_pairs_title_with_artist_in_same_row(self):
        raw='<h1>Vyhľadávanie</h1><div class="result-item"><a href="piesen.php?id=2">Dozadu</a>Other Artist</div><div class="result-item"><a href="piesen.php?id=3">Dozadu</a>Instinct</div>'
        r=self.parse(raw,url='https://www.supermusic.cz/najdi.php?hladane=Dozadu');self.assertEqual(r['links'],['https://www.supermusic.cz/piesen.php?idpiesne=3'])
    def test_external_or_non_numeric_search_target_rejected(self):
        for target in ('https://evil.example/piesen.php?id=1','piesen.php?id=abc','piesen.php?id=1&amp;redirect=https://evil.example'):
            raw='<h1>Vyhľadávanie</h1><div class="result-item"><a href="'+target+'">Dozadu</a>Instinct</div>'
            self.assertFalse(self.parse(raw,url='https://www.supermusic.cz/najdi.php?hladane=x')['links'])
    def test_challenge_is_not_a_negative_catalogue_match(self):
        with self.assertRaises(ValueError):self.parse('<p id="msg">Načítavam</p><script src="/js/smc.js"></script>')
    def test_malformed_or_unclosed_body_rejected(self):
        with self.assertRaises(ValueError):self.parse('<title>Dozadu – Instinct | SuperMusic.cz</title><div id="chordText">Original test line')
    def test_fnv_reference_and_public_answer(self):
        self.assertEqual(self.transport.fnv(b'hello'),0x4f9f2cab)
        nonce='4136ba37d50814e7';n=self.transport.answer(nonce,1048576)
        self.assertLess(self.transport.fnv((nonce+':'+str(n)).encode()),1048576)
    def test_malformed_challenge_and_cpu_budget(self):
        for nonce,target in [('bad!',1048576),('4136ba37d50814e7',0),('4136ba37d50814e7',2**32)]:
            with self.assertRaises(ValueError):self.transport.answer(nonce,target)
        with self.assertRaises(TimeoutError):self.transport.answer('4136ba37d50814e7',1,seconds=0)
    def test_transport_public_handshake_is_bounded_and_canonical(self):
        from urllib.request import Request
        challenge=b'<p id="msg" data-n="4136ba37d50814e7" data-l="4294967295" data-t="public.visitor.ticket" data-u="/piesen.php?id=1"></p><script src="/js/smc.js"></script>'
        module=self.transport
        class Response(io.BytesIO):
            def geturl(self):return 'https://www.supermusic.cz/piesen.php?id=1'
        session=module.Session();calls=[]
        def respond(request,**kwargs):
            calls.append((request,kwargs));return Response(challenge if len(calls)==1 else b'<html>Complete public song page</html>')
        with patch.object(session.transport,'open',side_effect=respond):
            with session.open(Request('https://www.supermusic.cz/piesen.php?id=1'),timeout=2) as response:
                self.assertIn(b'Complete public song',response.read());self.assertNotIn('_smc=',response.geturl())
        self.assertEqual(len(calls),2);self.assertEqual(session.validation_count,1)
        self.assertIn('_smc=public.visitor.ticket.',calls[1][0].full_url)
        self.assertTrue(all(0<x[1]['timeout']<=2 for x in calls))
    def test_repeated_visitor_check_stops_after_one_validation(self):
        from urllib.request import Request
        challenge=b'<p id="msg" data-n="4136ba37d50814e7" data-l="4294967295" data-t="public.visitor.ticket" data-u="/piesen.php?idpiesne=1"></p><script src="/js/smc.js"></script>'
        class Response(io.BytesIO):
            def geturl(self):return 'https://www.supermusic.cz/piesen.php?idpiesne=1'
        session=self.transport.Session()
        with patch.object(session.transport,'open',side_effect=lambda *a,**k:Response(challenge)):
            with self.assertRaises(ValueError):session.open(Request('https://www.supermusic.cz/piesen.php?idpiesne=1'))
        self.assertEqual(session.request_count,2);self.assertEqual(session.validation_count,1)
    def test_transport_rejects_credentials_and_external_destination(self):
        from urllib.request import Request
        for u in ('http://www.supermusic.cz/','https://evil.example/','https://u:p@www.supermusic.cz/'):
            with self.assertRaises(ValueError):self.transport.Session().open(Request(u))
        with self.assertRaises(ValueError):self.transport.Session().open(Request('https://www.supermusic.cz/',headers={'Authorization':'Bearer not-used'}))
    def test_positive_cache_from_test12_survives_new_source(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder=Path(tmp);p=folder/(provider.key('Artist','Song')+'.json');p.write_text(json.dumps({'version':7,'saved':1000,'status':'found','text':'Original cached test text'}))
            self.assertEqual(provider.lookup('Artist','Song',folder,opener=lambda *a,**k:(_ for _ in ()).throw(AssertionError()),clock=lambda:1001)['text'],'Original cached test text')

if __name__=='__main__':unittest.main()
