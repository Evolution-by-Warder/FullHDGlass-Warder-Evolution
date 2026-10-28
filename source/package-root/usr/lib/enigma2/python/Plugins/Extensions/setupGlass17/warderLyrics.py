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
from urllib.parse import urlencode
from urllib.request import Request, urlopen

API = 'https://lrclib.net/api/get'
SEARCH = 'https://lrclib.net/api/search'
CACHE = Path('/tmp/warder-radio-lyrics')
MAX_RESPONSE = 1024 * 1024
MAX_TEXT = 20000


def identity(value):
    value = unicodedata.normalize('NFKD', str(value or '').casefold())
    return ' '.join(''.join(c for c in value if not unicodedata.combining(c) and c not in "'’‘").split())


def key(artist, title):
    return hashlib.sha256((identity(artist)+'\0'+identity(title)).encode()).hexdigest()


def select(records, artist, title):
    """Whole artist/title identity only; never return the first search result."""
    if not isinstance(records, list):
        return ''
    wanted = (identity(artist), identity(title))
    for row in records[:30]:
        if not isinstance(row, dict) or row.get('instrumental'):
            continue
        if (identity(row.get('artistName')), identity(row.get('trackName'))) != wanted:
            continue
        text = row.get('plainLyrics')
        if not isinstance(text, str) or not text.strip():
            continue
        if len(text) > MAX_TEXT or '<html' in text.lower() or '<script' in text.lower():
            continue
        text = ''.join(c for c in text if c in '\n\t' or ord(c) >= 32)
        return text.replace('\r', '').strip()
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
        if 0 <= age < ttl:
            return {'text': saved['text'], 'status': saved['status']}
    except (OSError, ValueError, KeyError, TypeError):
        pass
    text = ''
    reachable = False
    query = urlencode({'artist_name':artist, 'track_name':title})
    for endpoint in (API, SEARCH):
        request = Request(endpoint+'?'+query,
                          headers={'User-Agent':'FullHDGlass-Warder-Evolution/1.0 (https://github.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution)', 'Accept':'application/json'})
        try:
            with opener(request, timeout=8) as response:
                raw = response.read(MAX_RESPONSE+1)
            if len(raw) > MAX_RESPONSE:
                raise ValueError('Oversized lyrics response')
            records = json.loads(raw.decode('utf-8'))
            if not isinstance(records,(list,dict)):raise ValueError('Invalid lyrics result')
            reachable = True
            text = select([records] if isinstance(records,dict) else records, artist, title)
            if text:break
        except Exception:
            continue
    if not reachable:
        return {'text':'', 'status':'offline'}
    result = {'text':text, 'status':'found' if text else 'not-found'}
    with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', dir=str(cache), delete=False) as output:
        json.dump(dict(result,saved=now),output,ensure_ascii=False)
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
