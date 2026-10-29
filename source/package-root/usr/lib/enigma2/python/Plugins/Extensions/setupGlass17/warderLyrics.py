"""Bounded, exact-identity plain-lyrics lookup; executable outside Enigma2."""
import hashlib
import json
import os
from pathlib import Path
from queue import Queue, Empty
from threading import Event, Thread, Lock
import re
import sys
import tempfile
import time
import unicodedata
from email.utils import parsedate_to_datetime
from urllib.error import HTTPError
from urllib.parse import urlencode, quote
from urllib.request import Request, urlopen

SEARCH = 'https://lrclib.net/api/search'
FALLBACK = 'https://api.lyrics.ovh/v1/'
CACHE_VERSION = 7
CACHE = Path('/tmp/warder-radio-lyrics')
MAX_RESPONSE = 1024 * 1024
MAX_TEXT = 20000

try:
    from Plugins.Extensions.setupGlass17 import warderSongIdentity as song_identity
except ImportError:
    import warderSongIdentity as song_identity


def identity(value):
    value = unicodedata.normalize('NFKD', str(value or '').casefold())
    return ' '.join(''.join(c for c in value if not unicodedata.combining(c) and c not in "'’‘").split())


def artist_identity(value):
    # Keep every credited performer; only normalize common credit separators.
    return tuple(sorted(part.strip() for part in
        re.split(r'\s+(?:feat\.?|ft\.?|featuring|and)\s+|\s*[&,;]\s*', identity(value))
        if part.strip()))



def artist_options(value):
    options = {artist_identity(value)}
    # Slovak/Czech "a" joins full personal names. Keep band names such as
    # "Not a Band" intact, and never omit either credited performer.
    parts = re.split(r'\s+a\s+', identity(value))
    if len(parts) > 1 and all(len(part.split()) >= 2 for part in parts):
        options.add(tuple(sorted(parts)))
    return options


def title_identity(value):
    # RDS commonly omits commas; preserve every word and version suffix.
    return identity(value).replace(',','')


def same_song(row, artist, title):
    return song_identity.same_recording(row,artist,title)

def clean_text(text):
    if not isinstance(text, str) or not text.strip() or len(text) > MAX_TEXT:
        return ''
    if any(tag in text.lower() for tag in ('<html', '<script', '<!doctype')):
        return ''
    text = ''.join(c for c in text if c in '\n\t' or ord(c) >= 32).replace('\r', '').strip()
    # Hudba.sk uses its lyrics container for this absence notice too. Reject
    # the complete notice (also in an old positive cache), not arbitrary
    # substrings that might occur inside an actual song. Let other sources run.
    if identity(text).rstrip(' .!?…') == 'tato piesen momentalne nema pridany text':
        return ''
    return text


def plain_text(row):
    text = clean_text(row.get('plainLyrics'))
    if text:
        return text
    # LRC is another representation of the same verified record, not karaoke.
    synced = clean_text(row.get('syncedLyrics'))
    lines = []
    for line in synced.splitlines():
        if not re.match(r'^\[\d{1,3}:\d{2}(?:[.:]\d+)?\]', line):
            continue
        lines.append(re.sub(r'^(?:\[\d{1,3}:\d{2}(?:[.:]\d+)?\])+', '', line).strip())
    return clean_text('\n'.join(lines))


def key(artist, title):
    return hashlib.sha256('\0'.join(sorted((identity(artist),identity(title)))).encode()).hexdigest()


def select(records, artist, title):
    """Whole artist/title identity only; never return the first search result."""
    if not isinstance(records, list):
        return ''
    for row in records[:30]:
        if not isinstance(row, dict) or row.get('instrumental'):
            continue
        if not same_song(row,artist,title):
            continue
        text = plain_text(row)
        if text:
            return text
    return ''



def atomic_json(path, value):
    with tempfile.NamedTemporaryFile(mode='w',encoding='utf-8',dir=str(path.parent),delete=False) as output:
        tmp = Path(output.name)
        json.dump(value,output,ensure_ascii=False)
    try:os.replace(str(tmp),str(path))
    finally:
        try:tmp.unlink()
        except OSError:pass


def retry_delay(error, now):
    value = error.headers.get('Retry-After','20') if error.headers else '20'
    try:return max(1,int(value))
    except (TypeError,ValueError):
        try:return max(1,int(parsedate_to_datetime(value).timestamp()-now)+1)
        except (TypeError,ValueError,OverflowError):return 20


def lookup(artist, title, cache=CACHE, opener=urlopen, clock=time.time,
           monotonic=time.monotonic, hedge_delay=0.75, budget=32,
           site_providers=('hudba','youradio','ujdeto','pisnicky','tekstowo','karaoke','kytary','roth'), profile='global'):
    if profile not in ('global','skcz'):raise ValueError('Unknown radio profile')
    artist,title=song_identity.repair_pair(artist,title)
    artist, title = str(artist).strip(), str(title).strip()
    if not artist or not title or max(len(artist), len(title)) > 250:
        return {'text':'','status':'no-song'}
    site_providers=tuple(dict.fromkeys(site_providers))
    if any(name not in ('hudba','youradio','ujdeto','pisnicky','tekstowo','karaoke','kytary','roth') for name in site_providers):raise ValueError('Unknown lyrics provider')
    sites=None
    if site_providers:
        try:from Plugins.Extensions.setupGlass17 import warderLyricsSites as sites
        except ImportError:import warderLyricsSites as sites
        site_providers=tuple(name for name in site_providers if sites.initial_urls(name,artist,title))
    source_names=('lrclib','ovh')+site_providers
    max_requests=5+sum(sites.LIMITS[name] for name in site_providers)
    cache.mkdir(parents=True,exist_ok=True)
    filename = cache/(key(artist,title)+'.json')
    started = monotonic()
    def finish(result, traces=None, cached=False):
        # One bounded diagnostic record; never store lyrics or full responses.
        diagnostic = {'artist':artist,'title':title,'status':result['status'],
                      'cache_hit':cached,'elapsed_ms':int(max(0,monotonic()-started)*1000),
                      'requests':(traces or [])[:max_requests]}
        try:atomic_json(cache/'.last-result',diagnostic)
        except OSError:pass
        return result
    try:
        saved = json.loads(filename.read_text())
        text = clean_text(saved.get('text'))
        valid = saved.get('version') == CACHE_VERSION or (saved.get('version') in (3,4,5,6) and bool(text))
        age = clock()-float(saved['saved'])
        ttl = 14*86400 if text else min(1800,max(60,int(saved.get('ttl',1800))))
        if valid and 0 <= age < ttl and saved.get('status') == ('found' if text else 'not-found'):
            return finish({'text':text,'status':saved['status']},cached=True)
    except (OSError,ValueError,KeyError,TypeError):pass

    deadline = started+max(0.01,min(32,budget))
    cancel = Event()
    events = Queue()
    trace_rows = []
    trace_lock = Lock()
    query_artist,query_title=song_identity.query_pair(artist,title)
    primary = list(dict.fromkeys((
        SEARCH+'?'+urlencode({'artist_name':query_artist,'track_name':query_title}),
        SEARCH+'?'+urlencode({'track_name':query_title}),
        SEARCH+'?'+urlencode({'track_name':artist}))))
    backup = [FALLBACK+quote(query_artist,safe='')+'/'+quote(query_title,safe=''),
              FALLBACK+quote(title,safe='')+'/'+quote(artist,safe='')]

    def run_source(name, urls):
        trace = []
        negative = False
        failed = False
        after = 5
        backoff = cache/('.'+name+'-backoff')
        try:until = float(backoff.read_text())
        except (OSError,ValueError):until = 0
        if until > clock():
            events.put(('done',name,{'negative':False,'failed':True,
                'retry_after':max(1,int(until-clock())+1),'trace':[]}))
            return
        for index,url in enumerate(urls):
            if sites is not None and name in site_providers and index>=sites.LIMITS[name]:break
            if cancel.is_set():return
            remaining = deadline-monotonic()
            # Do not launch a predictably doomed optional request at the end.
            if remaining <= 0 or (index > 0 and remaining < 2):
                failed = True
                break
            began = monotonic()
            item = {'source':name,'variant':index+1}
            pending = dict(item,status='pending')
            with trace_lock:trace_rows.append(pending)
            text = ''
            try:
                request = Request(url,headers={
                    'User-Agent':'FullHDGlass-Warder-Evolution/1.0 (https://github.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution)',
                    'Accept':'text/html' if name in site_providers else 'application/json'})
                fetch = sites.opener(name) if name in site_providers and opener is urlopen else opener
                with fetch(request,timeout=min(10,remaining)) as response:
                    raw = response.read(MAX_RESPONSE+1)
                    final_url=response.geturl() if name in site_providers and hasattr(response,'geturl') else url
                if len(raw) > MAX_RESPONSE:raise ValueError('Oversized response')
                if name in site_providers:
                    page=sites.parse(name,final_url,raw,artist,title,same_song,clean_text)
                    text=page['text'];negative=negative or page['negative']
                    linked=[link for link in page['links'] if link not in urls][:max(0,sites.LIMITS[name]-len(urls))]
                    # Follow verified search candidates before trying another
                    # search/mirror, avoiding an unnecessary network round trip.
                    urls[index+1:index+1]=linked
                    item['status']='found' if text else 'links' if page['links'] else 'not-found'
                else:
                    records = json.loads(raw.decode('utf-8'))
                    if name == 'lrclib':
                        if not isinstance(records,list):raise ValueError('Invalid result')
                        text = select(records,artist,title)
                    else:
                        if not isinstance(records,dict):raise ValueError('Invalid result')
                        text = clean_text(records.get('lyrics'))
                    negative = negative or not text
                if name not in site_providers:item['status'] = 'found' if text else 'not-found'
            except HTTPError as error:
                item['http'] = error.code
                if error.code == 404:
                    negative = True;item['status'] = 'not-found'
                else:
                    failed = True;item['status'] = 'http-error'
                    if error.code in (429,503):
                        received = clock();after = retry_delay(error,received)
                        try:
                            # Retain a longer limit already set by another worker.
                            try:previous = float(backoff.read_text())
                            except (OSError,ValueError):previous = 0
                            backoff.write_text(str(max(previous,received+after)))
                        except OSError:pass
                        item['retry_after'] = after
            except Exception as error:
                failed = True;item['status'] = 'request-error'
                item['error'] = type(error).__name__
            item['elapsed_ms'] = int(max(0,monotonic()-began)*1000)
            trace.append(item)
            with trace_lock:pending.update(item)
            if cancel.is_set():return
            if text:
                events.put(('found',name,{'text':text,'trace':trace}))
                return
            if item.get('http') in (429,503):break
        events.put(('done',name,{'negative':negative,'failed':failed,
                    'retry_after':after,'trace':trace}))

    def start_source(name,urls):
        # These threads live only in the existing helper process, never Enigma.
        Thread(target=run_source,args=(name,urls),name='lyrics-'+name,daemon=True).start()

    plans={'lrclib':primary,'ovh':backup}
    for site_name in site_providers:
        plans[site_name]=sites.initial_urls(site_name,artist,title)
    first=('hudba','lrclib') if profile=='skcz' and 'hudba' in site_providers else ('lrclib',)
    for name in first:start_source(name,plans[name])
    backup_started = False
    summaries = {}
    traces = []
    result = None
    try:
        while monotonic() < deadline:
            elapsed = monotonic()-started
            if not backup_started and (elapsed >= hedge_delay or any(name in summaries for name in first)):
                for name in source_names:
                    if name not in first:start_source(name,plans[name])
                backup_started = True
            remaining = deadline-monotonic()
            wait = remaining if backup_started else min(remaining,max(0.001,hedge_delay-elapsed))
            try:kind,name,data = events.get(timeout=max(0.001,wait))
            except Empty:continue
            traces.extend(data['trace'])
            if kind == 'found':
                result = {'text':data['text'],'status':'found'}
                break
            summaries[name] = data
            if len(summaries) == len(source_names):break
    finally:cancel.set()
    with trace_lock:traces = [dict(row) for row in trace_rows]

    if result is None:
        # A late optional failure does not erase valid misses from both sources.
        missing = all(any(row['source']==name and row.get('status')=='not-found'
                          for row in traces) for name in source_names)
        if missing:result = {'text':'','status':'not-found'}
        else:
            waits = [s['retry_after'] for s in summaries.values() if not s['negative']]
            return finish({'text':'','status':'offline','retry_after':min(waits or [5])},traces)
    try:
        partial = any(row.get('status') in ('pending','http-error','request-error') for row in traces)
        if partial and not result.get('text'):
            # A source failure must not pin an apparent miss for five minutes.
            # The renderer retries this case without a manual station change.
            result['partial']=True
            result['retry_after']=min([s.get('retry_after',5) for s in summaries.values() if s.get('failed')] or [5])
        else:
            atomic_json(filename,dict(result,saved=clock(),version=CACHE_VERSION,ttl=1800))
        files = sorted(cache.glob('*.json'),key=lambda p:p.stat().st_mtime)
        for old in files[:-128]:
            try:old.unlink()
            except OSError:pass
    except OSError:pass  # A cache write failure must not discard a found text.
    return finish(result,traces)


if __name__ == '__main__':
    if len(sys.argv) not in (3,5):sys.exit(2)
    profile='global'
    if len(sys.argv)==5:
        if sys.argv[3]!='--profile' or sys.argv[4] not in ('global','skcz'):sys.exit(2)
        profile=sys.argv[4]
    try:
        os.nice(8)
        print(json.dumps(lookup(sys.argv[1],sys.argv[2],profile=profile),ensure_ascii=False))
    except Exception:
        print(json.dumps({'text':'','status':'offline'}))
