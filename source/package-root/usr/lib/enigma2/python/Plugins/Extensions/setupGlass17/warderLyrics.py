"""Bounded, exact-identity plain-lyrics lookup; executable outside Enigma2."""
import hashlib
import json
import os
from pathlib import Path
import re
import sys
import tempfile
import time
import unicodedata
from urllib.error import HTTPError
from urllib.parse import urlencode, quote
from urllib.request import Request, urlopen

API = 'https://lrclib.net/api/get'
SEARCH = 'https://lrclib.net/api/search'
FALLBACK = 'https://api.lyrics.ovh/v1/'
CACHE_VERSION = 2
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
    return hashlib.sha256((identity(artist)+'\0'+identity(title)).encode()).hexdigest()


def select(records, artist, title):
    """Whole artist/title identity only; never return the first search result."""
    if not isinstance(records, list):
        return ''
    wanted = {(artist_identity(artist), identity(title)),
              (artist_identity(title), identity(artist))}
    for row in records[:30]:
        if not isinstance(row, dict) or row.get('instrumental'):
            continue
        if (artist_identity(row.get('artistName')), identity(row.get('trackName'))) not in wanted:
            continue
        text = plain_text(row)
        if text:
            return text
    return ''


def lookup(artist, title, cache=CACHE, opener=urlopen, clock=time.time):
    artist, title = str(artist).strip(), str(title).strip()
    if not artist or not title or max(len(artist), len(title)) > 250:
        return {'text': '', 'status': 'no-song'}
    cache.mkdir(parents=True, exist_ok=True)
    filename = cache/(key(artist, title)+'.json')
    now = clock()
    try:
        saved = json.loads(filename.read_text())
        ttl = 14*86400 if saved.get('text') else 6*3600
        age = now-float(saved['saved'])
        if saved.get('version') == CACHE_VERSION and 0 <= age < ttl:
            return {'text': saved['text'], 'status': saved['status']}
    except (OSError, ValueError, KeyError, TypeError):
        pass
    text = ''
    failures = False
    retry_after = 20
    backoff_file = cache/'.lrclib-backoff'
    try:
        backoff_until = float(backoff_file.read_text())
    except (OSError, ValueError):
        backoff_until = 0
    query = urlencode({'artist_name':artist, 'track_name':title})
    # Search reads the database directly. /get can trigger slow upstream work.
    urls = [SEARCH+'?'+query, SEARCH+'?'+urlencode({'q':artist+' '+title})]
    normalized = urlencode({'artist_name':identity(artist), 'track_name':identity(title)})
    if normalized != query:
        urls.append(SEARCH+'?'+normalized)
    # Exact title plus all credited artists are checked locally in select().
    urls.append(SEARCH+'?'+urlencode({'track_name':title}))
    urls = list(dict.fromkeys(urls))[:4]
    urls.append(FALLBACK+quote(artist,safe='')+'/'+quote(title,safe=''))
    for url in urls:
        lrclib = url.startswith(SEARCH)
        if lrclib and backoff_until > now:
            failures = True
            retry_after = max(retry_after,int(backoff_until-now)+1)
            continue
        request = Request(url, headers={
            'User-Agent':'FullHDGlass-Warder-Evolution/1.0 (https://github.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution)',
            'Accept':'application/json'})
        try:
            with opener(request, timeout=6) as response:
                raw = response.read(MAX_RESPONSE+1)
            if len(raw) > MAX_RESPONSE:
                raise ValueError('Oversized lyrics response')
            records = json.loads(raw.decode('utf-8'))
            if lrclib:
                if not isinstance(records,list):raise ValueError('Invalid lyrics result')
                text = select(records, artist, title)
            else:
                # This documented endpoint is keyed by the complete artist/title.
                if not isinstance(records,dict):raise ValueError('Invalid fallback result')
                text = clean_text(records.get('lyrics'))
            if text:break
        except HTTPError as error:
            if error.code == 404:
                continue  # A real miss, never an internet failure.
            failures = True
            if lrclib and error.code in (429,503):
                try:delay = max(1,int(error.headers.get('Retry-After','20')))
                except (TypeError,ValueError):delay = 20
                backoff_until = now+delay
                retry_after = max(retry_after,delay)
                try:backoff_file.write_text(str(backoff_until))
                except OSError:pass
        except Exception:
            failures = True
    if not text and failures:
        # Failed requests must not become a six-hour cached "not found" result.
        return {'text':'', 'status':'offline', 'retry_after':retry_after}
    result = {'text':text, 'status':'found' if text else 'not-found'}
    with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', dir=str(cache), delete=False) as output:
        json.dump(dict(result,saved=now,version=CACHE_VERSION),output,ensure_ascii=False)
        tmp = output.name
    os.replace(tmp,str(filename))
    files = sorted(cache.glob('*.json'),key=lambda p:p.stat().st_mtime)
    for old in files[:-128]:
        try:old.unlink()
        except OSError:pass
    return result


if __name__ == '__main__':
    if len(sys.argv) != 3:sys.exit(2)
    try:
        os.nice(8)
        print(json.dumps(lookup(sys.argv[1], sys.argv[2]),ensure_ascii=False))
    except Exception:
        print(json.dumps({'text':'', 'status':'offline'}))
