#!/usr/bin/env python3
"""Read-only Genius API/page check with hidden token entry and redacted results."""
from concurrent.futures import ThreadPoolExecutor
import getpass
import hashlib
from html.parser import HTMLParser
import json
import re
import unicodedata
from urllib.error import HTTPError
from urllib.parse import urlencode, urlsplit
from urllib.request import HTTPRedirectHandler, Request, build_opener

MAX_BYTES = 1024 * 1024
SONGS = (('ABBA', 'Dancing Queen'), ('Instinct', 'Dozadu'), ('IMT Smile', 'Úsmev a čaj'))


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, *args, **kwargs):
        # A credential must never be forwarded to a redirect destination.
        return None


def identity(value):
    return ''.join(c for c in unicodedata.normalize('NFKD', value).casefold() if c.isalnum())


def fetch(url, token=None):
    parsed = urlsplit(url)
    expected = 'api.genius.com' if token is not None else 'genius.com'
    if (parsed.scheme != 'https' or parsed.hostname != expected
            or parsed.username or parsed.password or parsed.port not in (None, 443)):
        raise ValueError('Unsupported destination')
    headers = {'User-Agent': 'FullHDGlass-Warder-Evolution/source-check'}
    if token is not None:
        headers['Authorization'] = 'Bearer ' + token
    result = {}
    try:
        try:
            response = build_opener(NoRedirect()).open(Request(url, headers=headers), timeout=12)
        except HTTPError as error:
            response = error
        with response:
            raw = response.read(MAX_BYTES + 1)
            result.update(http=response.code, bytes=len(raw))
        if len(raw) > MAX_BYTES:
            return dict(result, classification='response-too-large'), None
        text = raw.decode('utf-8', 'replace')
        if 'site unavailable' in text.lower()[:500]:
            return dict(result, classification='unavailable-placeholder'), None
        if result['http'] != 200:
            return dict(result, classification='http-error'), None
        return dict(result, classification='response-received'), text
    except (OSError, ValueError) as error:
        return dict(result, classification='request-error', error=type(error).__name__), None


class LyricsPage(HTMLParser):
    """Count public lyric containers without logging text or interpreting scripts."""
    def __init__(self):
        super().__init__()
        self.depth = 0
        self.active_depth = None
        self.parts = []
        self.containers = 0

    def handle_starttag(self, tag, attrs):
        if tag == 'br' and self.active_depth is not None:
            self.parts.append('\n')
        if tag in ('area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'param', 'source', 'track', 'wbr'):
            return
        self.depth += 1
        if self.active_depth is None and dict(attrs).get('data-lyrics-container') == 'true':
            self.active_depth = self.depth
            self.containers += 1

    def handle_endtag(self, tag):
        if tag in ('area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'param', 'source', 'track', 'wbr'):
            return
        if self.active_depth == self.depth:
            self.parts.append('\n')
            self.active_depth = None
        self.depth = max(0, self.depth - 1)

    def handle_data(self, data):
        if self.active_depth is not None:
            self.parts.append(data)


def check(song, token):
    artist, title = song
    result = {'artist': artist, 'title': title, 'token_supplied': True, 'token_logged': False}
    result['api'], text = fetch('https://api.genius.com/search?' + urlencode({'q': artist + ' ' + title}), token)
    if text is None:
        return result
    try:
        data = json.loads(text)
        result['api_status'] = data.get('meta', {}).get('status')
        hits = data.get('response', {}).get('hits', [])
        matches = []
        for hit in hits[:10]:
            row = hit.get('result', {})
            found_artist = row.get('primary_artist', {}).get('name', '')
            found_title = row.get('title', '')
            if identity(found_artist) == identity(artist) and identity(found_title) == identity(title):
                matches.append({'artist': found_artist, 'title': found_title, 'url': row.get('url', '')})
        result['exact_matches'] = matches[:3]
        if matches:
            result['song_page'], page = fetch(matches[0]['url'])  # No token on web requests.
            if page is not None:
                parser = LyricsPage()
                parser.feed(page)
                body = ''.join(parser.parts).strip()
                result['public_lyric_containers'] = parser.containers
                result['text_characters'] = len(body)
                result['text_sha256'] = hashlib.sha256(body.encode()).hexdigest() if body else None
                result['lyrics_logged'] = False
                result['note'] = 'No containers does not establish catalogue absence; embedded page-state parsing is not tested here.'
    except (ValueError, AttributeError, TypeError) as error:
        result['parse_error'] = type(error).__name__
    return result


if __name__ == '__main__':
    token = getpass.getpass('Genius token (vstup sa nezobrazuje): ').strip()
    if not token or re.search(r'[\r\n]', token):
        raise SystemExit('Token nebol zadaný správne.')
    with ThreadPoolExecutor(max_workers=3) as pool:
        for row in pool.map(lambda song: check(song, token), SONGS):
            print('GENIUS_AUTH_CHECK ' + json.dumps(row, ensure_ascii=False), flush=True)
    token = ''
