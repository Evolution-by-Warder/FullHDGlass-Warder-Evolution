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
spec=importlib.util.spec_from_file_location('lyrics_provider',PLUGIN/'warderLyrics.py')
provider=importlib.util.module_from_spec(spec);spec.loader.exec_module(provider)


class ProviderTests(unittest.TestCase):
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
            self.assertEqual(result['retry_after'],20)
            self.assertEqual(list(Path(tmp).iterdir()),[])
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
    def test_reversed_lookup_searches_both_fields_without_guessing_first_result(self):
        from urllib.parse import parse_qs,urlsplit
        queries=[]
        def response(request,**kwargs):
            query=parse_qs(urlsplit(request.full_url).query);queries.append(query)
            row=dict(artistName='Topic, A7S',trackName='Breaking Me',plainLyrics='Original test text')
            return io.BytesIO(json.dumps([row] if 'q' in query else []).encode())
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(provider.lookup('Breaking Me','Topic and A7S',Path(tmp),opener=response)['text'],'Original test text')
        self.assertEqual(len(queries),3);self.assertIn('q',queries[2])
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
        self.assertIn('nedostupný',r.label.text);self.assertGreater(r._retry_at,0)
        worker.outReceived(b'{"text":"Stale text"}');worker.complete(0)
        self.assertNotEqual(r.label.text,'Stale text')
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
            artwork=screen.find("widget[@render='WarderRadioArtwork']")
            self.assertEqual(artwork.get('size'),'420,700')
            lyrics=screen.find("widget[@render='WarderRadioLyrics']")
            self.assertEqual(lyrics.get('size'),'760,530')
            for w in screen:
                x,y=map(int,w.get('position').split(','));width,height=map(int,w.get('size').split(','))
                self.assertTrue(x>=0 and y>=0 and x+width<=1920 and y+height<=1080,w.attrib)
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


if __name__=='__main__':unittest.main()
