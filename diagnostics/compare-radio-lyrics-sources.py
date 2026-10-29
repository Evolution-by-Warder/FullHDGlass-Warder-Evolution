#!/usr/bin/env python3
"""Compare four public lyrics sources on identical recordings; never save lyrics."""
import argparse
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
import hashlib
from html.parser import HTMLParser
import importlib
import json
from pathlib import Path
import re
import sys
import time
from urllib.error import HTTPError, URLError
from urllib.parse import parse_qs, urlencode, urljoin, urlsplit
from urllib.request import HTTPRedirectHandler, Request, build_opener

SOURCES = ('supermusic', 'karaoke_sk', 'karaoke_cz', 'kytary')
HOSTS = {'supermusic': {'www.supermusic.cz', 'www.supermusic.sk'},
         'karaoke_sk': {'www.karaoketexty.sk'}, 'karaoke_cz': {'www.karaoketexty.cz'},
         'kytary': {'akordy.kytary.cz'}}
SONGS = (('IMT Smile', 'Úsmev a čaj'), ('Instinct', 'Dozadu'), ('Kali & Tina', 'Aj keby'),
         ('Láska', 'Mraky'), ('Dara Rolins', 'Sľub'), ('Peter Bič Project', 'Stromy'),
         ('Wanastowi Vjecy', 'Kapky krve'), ('Lucie', 'Chci zas v tobě spát'),
         ('Lucie Vondráčková', 'Hodiny duchů'), ('Hana Horecká', 'Den a noc'),
         ('ABBA', 'Dancing Queen'), ('Queen', 'Bohemian Rhapsody'))


def allowed(source, url):
    try:
        p = urlsplit(url)
        return p.scheme == 'https' and p.hostname in HOSTS[source] and p.port in (None, 443) and not p.username and not p.password
    except ValueError:
        return False


class Redirects(HTTPRedirectHandler):
    max_redirections = 2
    def __init__(self, source):
        self.source = source
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        if not allowed(self.source, newurl):
            raise ValueError('Redirect outside tested source')
        return super().redirect_request(req, fp, code, msg, headers, newurl)


class SuperPage(HTMLParser):
    """Conservative diagnostic parser; unexpected markup remains unverified."""
    VOID = {'br', 'img', 'meta', 'link', 'hr', 'input', 'source', 'wbr'}
    BLOCKS = {'songtext', 'song-text', 'song_text', 'lyrics', 'lyrics-text', 'lyricstext', 'text-piesne'}
    def __init__(self):
        super().__init__()
        self.stack, self.headings, self.anchors, self.blocks, self.shapes = [], [], [], [], []
        self.heading = self.anchor = self.body = None
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        tokens = set(a.get('class', '').split()) | {a.get('id', '')}
        depth = len(self.stack)
        if tag == 'br' and self.body is not None:
            self.body['parts'].append('\n')
        if tag in self.VOID:
            return
        self.stack.append(tag)
        if tag in ('h1', 'h2', 'title'):
            self.heading = {'depth': depth, 'parts': [], 'tag': tag}
        if tag == 'a':
            self.anchor = {'depth': depth, 'parts': [], 'href': a.get('href', '')}
        if tag in ('pre', 'div', 'article') and any(w in (a.get('id', '') + a.get('class', '')).lower() for w in ('song', 'lyric', 'piesen', 'text')):
            if len(self.shapes) < 15:
                self.shapes.append({'tag': tag, 'id': a.get('id', ''), 'class': a.get('class', '')[:150]})
        if self.body is None and (tag == 'pre' or tokens & self.BLOCKS):
            self.body = {'depth': depth, 'parts': []}
    def handle_endtag(self, tag):
        if tag in self.VOID or tag not in self.stack:
            return
        depth = len(self.stack) - 1 - self.stack[::-1].index(tag)
        for name, collection in (('heading', self.headings), ('anchor', self.anchors), ('body', self.blocks)):
            item = getattr(self, name)
            if item is not None and item['depth'] >= depth:
                collection.append(item)
                setattr(self, name, None)
        del self.stack[depth:]
    def handle_data(self, data):
        if any(t in ('script', 'style', 'noscript') for t in self.stack):
            return
        for item in (self.heading, self.anchor, self.body):
            if item is not None:
                item['parts'].append(data)
    @staticmethod
    def text(item):
        return ' '.join(''.join(item['parts']).split())


def parse_super(url, raw, artist, title, lyrics):
    page = SuperPage()
    page.feed(raw.decode('utf-8', 'replace'))
    headings = [page.text(h) for h in page.headings]
    matched = False
    for heading in headings:
        heading = re.sub(r'\s*\|\s*SuperMusic\.(?:cz|sk).*$', '', heading).strip()
        heading = re.sub(r'\s*\[(?:akordy a text|text)\]\s*$', '', heading).strip()
        for separator in (' - ', ' – '):
            if separator in heading:
                a, t = heading.split(separator, 1)
                matched |= lyrics.same_song({'artistName': a.strip(' +'), 'trackName': t}, artist, title)
    if matched and len(page.blocks) == 1:
        text = lyrics.clean_text(''.join(page.blocks[0]['parts']))
        if text:
            return {'text': text, 'links': [], 'negative': False}
    links = []
    if urlsplit(url).path == '/najdi.php':
        for anchor in page.anchors:
            label = page.text(anchor)
            if lyrics.identity(title) not in lyrics.identity(label):
                continue
            target = urljoin(url, anchor['href']).split('#', 1)[0]
            q = parse_qs(urlsplit(target).query)
            if allowed('supermusic', target) and urlsplit(target).path == '/piesen.php' and any(k in q for k in ('id', 'idpiesne')):
                if target not in links:
                    links.append(target)
                if len(links) == 2:
                    break
    return {'text': '', 'links': links, 'negative': False,
            'diagnostic': {'headers': headings[:4], 'candidate_blocks': len(page.blocks), 'block_shapes': page.shapes}}


def check(source, artist, title, sites, lyrics, timeout, budget):
    started = time.monotonic()
    if source == 'supermusic':
        urls = ['https://www.supermusic.cz/najdi.php?' + urlencode({'hladane': artist + ' ' + title})]
    elif source.startswith('karaoke_'):
        host = next(iter(HOSTS[source]))
        urls = ['https://' + host + '/search?' + urlencode({'q': sites.song_identity.query_pair(artist, title)[1]})]
    else:
        urls = sites.initial_urls('kytary', artist, title)
    result = {'source': source, 'artist': artist, 'title': title, 'status': 'unverified_page',
              'characters': 0, 'lyrics_logged': False, 'requests': []}
    seen = set()
    index = 0
    while index < len(urls) and len(seen) < 4:
        url = urls[index]
        index += 1
        if url in seen or not allowed(source, url):
            continue
        remaining = budget - (time.monotonic() - started)
        if remaining <= 0:
            result['status'] = 'budget_exhausted'
            break
        seen.add(url)
        trace = {'url': url}
        stamp = time.monotonic()
        try:
            try:
                response = build_opener(Redirects(source)).open(Request(url, headers={'User-Agent': 'FullHDGlass-Warder-Evolution/source-comparison'}), timeout=min(timeout, remaining))
            except HTTPError as error:
                response = error
            with response:
                raw = response.read(1024 * 1024 + 1)
                status, final = response.code, response.geturl()
            trace.update(http=status, bytes=len(raw), final_url=final)
            low = raw[:20000].decode('utf-8', 'replace').lower()
            if len(raw) > 1024 * 1024:
                state = 'response_too_large'
            elif 'site unavailable' in low[:500]:
                state = 'environment_placeholder'
            elif status == 403:
                state = 'blocked'
            elif status == 429:
                state = 'rate_limited'
            elif status == 503 and ('robot' in low or 'captcha' in low):
                state = 'access_challenge'
            elif status == 404:
                state = 'http_not_found'
            elif status != 200:
                state = 'http_error'
            elif len(raw) < 1500 and b'<script' in raw.lower():
                state = 'script_intermediate'
            else:
                try:
                    parsed = parse_super(final, raw, artist, title, lyrics) if source == 'supermusic' else sites.parse('karaoke' if source.startswith('karaoke_') else 'kytary', final, raw, artist, title, lyrics.same_song, lyrics.clean_text)
                    if parsed.get('text'):
                        body = parsed['text']
                        result.update(status='found', characters=len(body), text_sha256=hashlib.sha256(body.encode()).hexdigest(), matched_url=final)
                        state = 'found'
                    else:
                        linked = [u for u in parsed.get('links', []) if u not in seen and allowed(source, u)]
                        urls[index:index] = linked
                        state = 'candidate_links' if linked else 'not_found' if parsed.get('negative') else 'unverified_page'
                        if parsed.get('diagnostic'):
                            trace['parser_diagnostic'] = parsed['diagnostic']
                except (ValueError, KeyError, UnicodeError):
                    state = 'unrecognized_page'
            trace['status'] = state
            if state != 'found':
                result['status'] = state
        except (OSError, ValueError) as error:
            trace.update(status='connection_error', error=type(error).__name__)
            result['status'] = 'connection_error'
        trace['elapsed_ms'] = round(1000 * (time.monotonic() - stamp))
        result['requests'].append(trace)
        if result['status'] == 'found':
            break
    result['elapsed_ms'] = round(1000 * (time.monotonic() - started))
    return result


def main():
    args = argparse.ArgumentParser(description=__doc__)
    args.add_argument('--engine-dir', type=Path, default=Path(__file__).resolve().parents[1] / 'source/package-root/usr/lib/enigma2/python/Plugins/Extensions/setupGlass17')
    args.add_argument('--report', type=Path, default=Path('/tmp/warder-radio-source-comparison.json'))
    args.add_argument('--timeout', type=float, default=5)
    args.add_argument('--budget', type=float, default=15)
    args.add_argument('--workers', type=int, default=4, choices=range(1, 5))
    options = args.parse_args()
    if not 0 < options.timeout <= 20 or not 0 < options.budget <= 30:
        args.error('timeout/budget outside diagnostic bounds')
    sys.path.insert(0, str(options.engine_dir))
    sites = importlib.import_module('warderLyricsSites')
    lyrics = importlib.import_module('warderLyrics')
    cases = [(s, a, t) for a, t in SONGS for s in SOURCES]
    results = []
    def run(case):
        return check(*case, sites, lyrics, options.timeout, options.budget)
    with ThreadPoolExecutor(max_workers=options.workers) as pool:
        for row in pool.map(run, cases):
            results.append(row)
            print('SOURCE_COMPARISON ' + json.dumps(row, ensure_ascii=False), flush=True)
    summary = {source: dict(Counter(r['status'] for r in results if r['source'] == source)) for source in SOURCES}
    report = {'schema': 1, 'sources': list(SOURCES), 'recordings': len(SONGS), 'cases': len(cases),
              'timeout': options.timeout, 'case_budget': options.budget, 'summary': summary,
              'results': results, 'coverage_measurement': False, 'lyrics_saved': False,
              'notes': ['Identical small sample, not overall catalogue coverage.',
                        'SK/CZ domains isolated; cross-domain fallback is not counted as success.',
                        'SuperMusic parser is diagnostic and conservative; unverified_page is not a catalogue miss.',
                        'Live access failures are not proof that a song has no lyrics.']}
    options.report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print('SOURCE_COMPARISON_SUMMARY ' + json.dumps({'summary': summary, 'report': str(options.report)}, ensure_ascii=False), flush=True)


if __name__ == '__main__':
    main()
