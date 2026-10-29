#!/usr/bin/env python3
"""Bounded anonymous access check; never log lyrics, cookies or credentials."""
from concurrent.futures import ThreadPoolExecutor
import hashlib
from html.parser import HTMLParser
import json
import re
from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit
from urllib.request import HTTPRedirectHandler, Request, build_opener

CASES = (
    ('karaoke', 'search', 'https://www.karaoketexty.sk/search?q=Dozadu'),
    ('karaoke', 'search', 'https://www.karaoketexty.sk/search?q=Mraky'),
    ('karaoke', 'song', 'https://www.karaoketexty.sk/texty-piesni/instinct/dozadu-806696'),
    ('supermusic', 'home', 'https://www.supermusic.sk/'),
    ('supermusic', 'song', 'https://www.supermusic.sk/piesen.php?idpiesne=1007929'),
    ('musixmatch', 'documentation', 'https://developer.musixmatch.com/documentation'),
    ('musixmatch', 'documentation', 'https://docs.musixmatch.com/'),
    ('musixmatch', 'song', 'https://www.musixmatch.com/lyrics/ABBA/Dancing-Queen'),
    ('musixmatch', 'search', 'https://www.musixmatch.com/search/Instinct%20Dozadu'),
    ('musixmatch', 'anonymous-api', 'https://api.musixmatch.com/ws/1.1/track.search?q_artist=Instinct&q_track=Dozadu&format=json'),
)
HOSTS = {
    'karaoke': {'www.karaoketexty.sk', 'www.karaoketexty.cz'},
    'supermusic': {'www.supermusic.sk', 'www.supermusic.cz'},
    'musixmatch': {'developer.musixmatch.com', 'docs.musixmatch.com',
                   'www.musixmatch.com', 'musixmatch.com', 'api.musixmatch.com'},
}


def allowed(source, url):
    p = urlsplit(url)
    return (p.scheme == 'https' and p.hostname in HOSTS[source]
            and p.port in (None, 443) and not p.username and not p.password)


class Redirects(HTTPRedirectHandler):
    def __init__(self, source):
        super().__init__()
        self.source = source

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        if not allowed(self.source, newurl):
            raise URLError('Redirect outside source family')
        return super().redirect_request(req, fp, code, msg, headers, newurl)


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.title = ''
        self.in_title = False
        self.lyric_blocks = 0
        self.song_links = []
        self.scripts = 0
        self.json_script = False
        self.json_parts = []
        self.json_documents = []
        self.lyric_attributes = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == 'title':
            self.in_title = True
        if tag == 'script':
            self.scripts += 1
            self.json_script = (a.get('type') in ('application/json', 'application/ld+json')
                                or a.get('id') == '__NEXT_DATA__')
            self.json_parts = []
        classes = a.get('class', '').split()
        for key in ('class', 'data-testid'):
            value = a.get(key, '')
            if 'lyric' in value.lower() and value not in self.lyric_attributes and len(self.lyric_attributes) < 10:
                self.lyric_attributes.append(value[:150])
        if ('para_1lyrics_col1' in classes or 'lyrics' in classes
                or a.get('data-lyrics-container') == 'true'):
            self.lyric_blocks += 1
        path = a.get('href', '')
        if tag == 'a' and re.fullmatch(r'/texty-p(?:iesni|isni)/[^/]+/[^/]+-\d+', path):
            if path not in self.song_links and len(self.song_links) < 8:
                self.song_links.append(path)

    def handle_endtag(self, tag):
        if tag == 'title':
            self.in_title = False
        if tag == 'script' and self.json_script:
            try:
                self.json_documents.append(json.loads(''.join(self.json_parts)))
            except ValueError:
                pass
            self.json_script = False
            self.json_parts = []

    def handle_data(self, data):
        if self.in_title:
            self.title = (self.title + data)[:150]
        if self.json_script:
            self.json_parts.append(data)


def lyric_schema(documents):
    """Only shapes, sizes and hashes of public structured fields; no text values."""
    found = []
    def visit(value, path, depth):
        if depth > 14 or len(found) >= 25:
            return
        if isinstance(value, dict):
            for key, child in list(value.items())[:200]:
                if any(word in key.lower() for word in ('token', 'secret', 'password', 'cookie', 'apikey')):
                    continue
                if 'lyric' in key.lower():
                    item = {'path': path + '.' + key, 'type': type(child).__name__}
                    if isinstance(child, (str, list, dict)):
                        item['length'] = len(child)
                    if isinstance(child, dict):
                        item['keys'] = list(child)[:20]
                    found.append(item)
                visit(child, path + '.' + key, depth + 1)
        elif isinstance(value, list):
            for index, child in enumerate(value[:3]):
                visit(child, path + '[%d]' % index, depth + 1)
    for index, value in enumerate(documents[:5]):
        visit(value, 'script[%d]' % index, 0)
    return found


def check(case):
    source, role, url = case
    out = {'source': source, 'role': role, 'url': url, 'lyrics_logged': False}
    try:
        if not allowed(source, url):
            raise ValueError('Unsupported URL')
        try:
            response = build_opener(Redirects(source)).open(
                Request(url, headers={'User-Agent': 'Mozilla/5.0'}), timeout=12)
        except HTTPError as error:
            response = error
        with response:
            raw = response.read(1024 * 1024 + 1)
            out.update(http=response.code, final_url=response.geturl(), bytes=len(raw))
        if len(raw) > 1024 * 1024:
            out['classification'] = 'response-too-large'
            return out
        text = raw.decode('utf-8', 'replace')
        page = Page()
        page.feed(text)
        out.update(sha256=hashlib.sha256(raw).hexdigest(), page_title=page.title,
                   lyric_blocks=page.lyric_blocks, song_links=page.song_links,
                   script_count=page.scripts, lyric_attributes=page.lyric_attributes,
                   structured_lyrics_fields=lyric_schema(page.json_documents))
        if source == 'musixmatch':
            for document in page.json_documents:
                if not isinstance(document, dict):
                    continue
                props = document.get('props', {}).get('pageProps', {})
                data = props.get('data', {})
                if not isinstance(data, dict):
                    continue
                out['page_data_keys'] = list(data)[:25]
                track_info = data.get('trackInfo', {}).get('data', {})
                if not isinstance(track_info, dict):
                    continue
                out['track_info_keys'] = list(track_info)[:25]
                track = track_info.get('track', {})
                out['track_keys'] = list(track)[:60] if isinstance(track, dict) else []
                if isinstance(track, dict):
                    out['track_identity'] = {k: track[k] for k in ('name', 'artistName', 'title', 'trackName') if isinstance(track.get(k), str)}
                body = track_info.get('lyrics', {}).get('body')
                if isinstance(body, str):
                    out['lyrics_body'] = {'characters': len(body), 'lines': len(body.splitlines()),
                                          'sha256': hashlib.sha256(body.encode()).hexdigest(),
                                          'has_preview_notice': 'not for commercial use' in body.lower()
                                          or 'lyrics preview' in body.lower()}
        lowered = text.lower()
        if out['http'] >= 400:
            kind = 'http-error'
        elif 'site unavailable' in page.title.lower():
            kind = 'unavailable-placeholder'
        elif ('ověř, že nejsi robot' in lowered or 'verify you are human' in lowered
              or 'just a moment' in page.title.lower()):
            kind = 'access-challenge'
        elif len(raw) < 1500 and page.scripts:
            kind = 'script-intermediate-not-lyrics'
        else:
            kind = 'response-received-content-not-yet-verified'
        out['classification'] = kind
        if role == 'documentation':
            out['mentions'] = {label: term in lowered for label, term in (
                ('api_key', 'api key'), ('apikey', 'apikey'),
                ('access_token', 'access token'), ('authentication', 'authentication'),
                ('lyrics_endpoint', 'track.lyrics.get'))}
        if role == 'anonymous-api':
            try:
                data = json.loads(text)
                out['api_status'] = data.get('meta', {}).get('status')
                out['api_message_status'] = data.get('message', {}).get('header', {}).get('status_code')
                if out['api_status'] == 401 or out['api_message_status'] == 401:
                    out['classification'] = 'authentication-required'
            except (ValueError, AttributeError):
                pass
    except (OSError, ValueError) as error:
        out.update(classification='request-error', error=type(error).__name__)
    return out


if __name__ == '__main__':
    with ThreadPoolExecutor(max_workers=4) as pool:
        for row in pool.map(check, CASES):
            print('RADIO_SOURCE_ACCESS ' + json.dumps(row, ensure_ascii=False), flush=True)
