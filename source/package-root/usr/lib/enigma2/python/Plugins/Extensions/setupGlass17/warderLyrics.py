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
CACHE_VERSION = 3
CACHE = Path('/tmp/warder-radio-lyrics')
MAX_RESPONSE = 1024 * 1024
MAX_TEXT = 20000


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


def same_song(row, artist, title):
    got_title = identity(row.get('trackName'))
    got_artists = artist_options(row.get('artistName'))
    return any(got_title == identity(t) and got_artists.intersection(artist_options(a))
               for a,t in ((artist,title),(title,artist)))

def clean_text(text):
    if not isinstance(text, str) or not text.strip() or len(text) > MAX_TEXT:
        return ''
    if any(tag in text.lower() for tag in ('<html', '<script', '<!doctype')):
        return ''
    return ''.join(c for c in text if c in '\n\t' or ord(c) >= 32).replace('\r', '').strip()


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
           monotonic=time.monotonic, hedge_delay=0.75, budget=32):
    artist, title = str(artist).strip(), str(title).strip()
    if not artist or not title or max(len(artist), len(title)) > 250:
        return {'text':'','status':'no-song'}
    cache.mkdir(parents=True,exist_ok=True)
    filename = cache/(key(artist,title)+'.json')
    started = monotonic()
    def finish(result, traces=None, cached=False):
        # One bounded diagnostic record; never store lyrics or full responses.
        diagnostic = {'artist':artist,'title':title,'status':result['status'],
                      'cache_hit':cached,'elapsed_ms':int(max(0,monotonic()-started)*1000),
                      'requests':(traces or [])[:5]}
        try:atomic_json(cache/'.last-result',diagnostic)
        except OSError:pass
        return result
    try:
        saved = json.loads(filename.read_text())
        text = clean_text(saved.get('text'))
        valid = saved.get('version') == CACHE_VERSION
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
    primary = list(dict.fromkeys((
        SEARCH+'?'+urlencode({'artist_name':artist,'track_name':title}),
        SEARCH+'?'+urlencode({'track_name':title}),
        SEARCH+'?'+urlencode({'track_name':artist}))))
    backup = [FALLBACK+quote(artist,safe='')+'/'+quote(title,safe=''),
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
                    'Accept':'application/json'})
                with opener(request,timeout=min(10,remaining)) as response:
                    raw = response.read(MAX_RESPONSE+1)
                if len(raw) > MAX_RESPONSE:raise ValueError('Oversized response')
                records = json.loads(raw.decode('utf-8'))
                if name == 'lrclib':
                    if not isinstance(records,list):raise ValueError('Invalid result')
                    text = select(records,artist,title)
                else:
                    if not isinstance(records,dict):raise ValueError('Invalid result')
                    text = clean_text(records.get('lyrics'))
                negative = negative or not text
                item['status'] = 'found' if text else 'not-found'
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

    start_source('lrclib',primary)
    backup_started = False
    summaries = {}
    traces = []
    result = None
    try:
        while monotonic() < deadline:
            elapsed = monotonic()-started
            if not backup_started and (elapsed >= hedge_delay or 'lrclib' in summaries):
                start_source('ovh',backup);backup_started = True
            remaining = deadline-monotonic()
            wait = remaining if backup_started else min(remaining,max(0.001,hedge_delay-elapsed))
            try:kind,name,data = events.get(timeout=max(0.001,wait))
            except Empty:continue
            traces.extend(data['trace'])
            if kind == 'found':
                result = {'text':data['text'],'status':'found'}
                break
            summaries[name] = data
            if len(summaries) == 2:break
    finally:cancel.set()
    with trace_lock:traces = [dict(row) for row in trace_rows]

    if result is None:
        # A late optional failure does not erase valid misses from both sources.
        missing = all(any(row['source']==name and row.get('status')=='not-found'
                          for row in traces) for name in ('lrclib','ovh'))
        if missing:result = {'text':'','status':'not-found'}
        else:
            waits = [s['retry_after'] for s in summaries.values() if not s['negative']]
            return finish({'text':'','status':'offline','retry_after':min(waits or [5])},traces)
    try:
        partial = any(row.get('status') in ('pending','http-error','request-error') for row in traces)
        atomic_json(filename,dict(result,saved=clock(),version=CACHE_VERSION,ttl=300 if partial else 1800))
        files = sorted(cache.glob('*.json'),key=lambda p:p.stat().st_mtime)
        for old in files[:-128]:
            try:old.unlink()
            except OSError:pass
    except OSError:pass  # A cache write failure must not discard a found text.
    return finish(result,traces)


if __name__ == '__main__':
    if len(sys.argv) != 3:sys.exit(2)
    try:
        os.nice(8)
        print(json.dumps(lookup(sys.argv[1],sys.argv[2]),ensure_ascii=False))
    except Exception:
        print(json.dumps({'text':'','status':'offline'}))
