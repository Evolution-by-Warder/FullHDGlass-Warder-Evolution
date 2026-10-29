#!/usr/bin/env python3
"""Standalone OpenATV Genius diagnostic. No token or lyrics are written to the log."""
import argparse
import getpass
import hashlib
from html.parser import HTMLParser
import importlib
import inspect
import json
import logging
from pathlib import Path
import signal
import socket
import sys
import time
import unicodedata
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode, urlsplit
from urllib.request import HTTPRedirectHandler, Request, build_opener

LOG = Path('/tmp/warder-genius-test.log')


class Deadline(BaseException):
    pass


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, *args, **kwargs):
        return None


def emit(stage, **fields):
    line = json.dumps(dict(stage=stage, **fields), ensure_ascii=False)
    with LOG.open('a', encoding='utf-8') as handle:
        handle.write(line + '\n')
    print(line, flush=True)


def normalized(value):
    return ''.join(c for c in unicodedata.normalize('NFKD', value).casefold() if c.isalnum())


def fetch(url, timeout, retries, token=None):
    parsed = urlsplit(url)
    expected_host = 'api.genius.com' if token is not None else 'genius.com'
    if (parsed.scheme != 'https' or parsed.hostname != expected_host
            or parsed.username or parsed.password or parsed.port not in (None, 443)):
        emit('destination_rejected')
        return None
    headers = {'User-Agent': 'Warder-Genius-Test/1.0'}
    if token is not None:
        headers['Authorization'] = 'Bearer ' + token
    for attempt in range(retries + 1):
        started = time.monotonic()
        emit('request_start', host=expected_host, path=parsed.path,
             attempt=attempt + 1, timeout=timeout, authorization_present=token is not None)
        try:
            try:
                response = build_opener(NoRedirect()).open(Request(url, headers=headers), timeout=timeout)
            except HTTPError as error:
                response = error
            with response:
                raw = response.read(1024 * 1024 + 1)
                status = response.code
            placeholder = b'Site Unavailable' in raw[:500]
            emit('http_response', host=expected_host, http=status, bytes=len(raw),
                 elapsed_ms=round(1000 * (time.monotonic() - started)),
                 unavailable_placeholder=placeholder)
            if len(raw) > 1024 * 1024 or status != 200 or placeholder:
                return None
            return raw.decode('utf-8', 'replace')
        except (URLError, OSError) as error:
            emit('request_error', host=expected_host, attempt=attempt + 1,
                 error=type(error).__name__, reason_type=type(getattr(error, 'reason', None)).__name__,
                 elapsed_ms=round(1000 * (time.monotonic() - started)))
    return None


class LyricsPage(HTMLParser):
    VOID = {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'param', 'source', 'track', 'wbr'}

    def __init__(self):
        super().__init__()
        self.stack, self.parts = [], []
        self.active = None
        self.containers = 0

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        excluded = bool(self.stack and self.stack[-1][1]) or tag in ('script', 'style') or attrs.get('data-exclude-from-selection') == 'true' or 'LyricsHeader' in attrs.get('class', '')
        if tag == 'br' and self.active is not None and not excluded:
            self.parts.append('\n')
        if tag in self.VOID:
            return
        self.stack.append((tag, excluded))
        if self.active is None and attrs.get('data-lyrics-container') == 'true' and not excluded:
            self.active = len(self.stack) - 1
            self.containers += 1

    def handle_endtag(self, tag):
        if tag in self.VOID:
            return
        indices = [i for i, frame in enumerate(self.stack) if frame[0] == tag]
        if not indices:
            return
        index = indices[-1]
        if self.active is not None and self.active >= index:
            self.parts.append('\n')
            self.active = None
        del self.stack[index:]

    def handle_data(self, data):
        if self.active is not None and self.stack and not self.stack[-1][1]:
            self.parts.append(data)


def standard_check(options, token):
    text = fetch('https://api.genius.com/search?' + urlencode({'q': options.artist + ' ' + options.title}), options.timeout, options.retries, token)
    if text is None:
        emit('standard_api', status='no_usable_response')
        return
    try:
        data = json.loads(text)
        hits = data.get('response', {}).get('hits', [])
        exact = []
        for hit in hits[:20]:
            row = hit.get('result', {})
            artist = row.get('primary_artist', {}).get('name', '')
            title = row.get('title', '')
            if normalized(artist) == normalized(options.artist) and normalized(title) == normalized(options.title):
                exact.append({'artist': artist, 'title': title, 'url': row.get('url', '')})
        emit('standard_api', status='json_received', api_status=data.get('meta', {}).get('status'),
             hits=len(hits), exact_matches=exact[:3])
        if not exact:
            return
        page = fetch(exact[0]['url'], options.timeout, options.retries)
        if page is not None:
            parser = LyricsPage()
            parser.feed(page)
            body = ''.join(parser.parts).strip()
            emit('standard_lyrics', containers=parser.containers, characters=len(body),
                 sha256=hashlib.sha256(body.encode()).hexdigest() if body else None,
                 lyrics_logged=False,
                 note='Embedded song-state parsing is not tested; no containers does not prove catalogue absence.')
    except (ValueError, AttributeError, TypeError) as error:
        emit('standard_api', status='parse_error', error=type(error).__name__)


def library_check(options, token):
    try:
        module = importlib.import_module('lyricsgenius')
    except ImportError:
        emit('lyricsgenius', status='not_installed', note='Standard-library API test still ran; no packages were installed.')
        return
    logging.disable(logging.CRITICAL)
    try:
        from importlib.metadata import version
        emit('lyricsgenius', version=version('lyricsgenius'))
        kwargs = dict(remove_section_headers=True, timeout=options.timeout, retries=options.retries, sleep_time=0)
        if 'verbose' in inspect.signature(module.Genius).parameters:
            kwargs['verbose'] = False
        bot = module.Genius(token, **kwargs)
        original = bot._session.send

        def tracked(request, **kw):
            parsed = urlsplit(request.url)
            authenticated = bool(request.headers.get('Authorization'))
            if parsed.scheme != 'https' or parsed.hostname not in ('api.genius.com', 'genius.com') or (authenticated and parsed.hostname != 'api.genius.com'):
                raise ValueError('Unsupported library destination')
            # Keep each redirect visible to this guard instead of following it inside requests.
            kw['allow_redirects'] = False
            response = original(request, **kw)
            emit('library_http', host=parsed.hostname, path=parsed.path, http=response.status_code,
                 authorization_present=authenticated, bytes=len(response.content),
                 unavailable_placeholder='Site Unavailable' in response.text[:500])
            return response

        bot._session.send = tracked
        for step in ('authenticated_search', 'search_song'):
            emit('library_start', step=step)
            try:
                if step == 'authenticated_search':
                    result = bot.search_songs(options.artist + ' ' + options.title)
                    emit('library_result', step=step, status='json_received', hits=len(result.get('hits', [])))
                else:
                    song = bot.search_song(options.title, options.artist)
                    emit('library_result', step=step, status='song_returned' if song else 'no_result',
                         characters=len(song.lyrics or '') if song else 0, lyrics_logged=False)
            except Exception as error:
                emit('library_result', step=step, status='error', error=type(error).__name__)
    except Exception as error:
        emit('lyricsgenius', status='configuration_error', error=type(error).__name__)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--artist', default='IMT Smile')
    parser.add_argument('--title', default='Úsmev a čaj')
    parser.add_argument('--timeout', type=int, default=20, choices=range(1, 31))
    parser.add_argument('--retries', type=int, default=3, choices=range(4))
    options = parser.parse_args()
    if not sys.stdin.isatty():
        raise SystemExit('Spusti skript v interaktivnom SSH terminali; token sa zadava skryto.')
    token = getpass.getpass('Genius token (vstup sa nezobrazuje): ').strip()
    if not token or '\r' in token or '\n' in token:
        raise SystemExit('Token nebol zadany spravne.')
    LOG.write_text('', encoding='utf-8')
    emit('start', python=sys.version.split()[0], artist=options.artist, title=options.title,
         timeout=options.timeout, retries=options.retries, overall_limit_seconds=120,
         token_supplied=True, token_logged=False)

    def deadline(*args):
        raise Deadline()
    signal.signal(signal.SIGALRM, deadline)
    signal.alarm(120)
    try:
        started = time.monotonic()
        try:
            addresses = socket.getaddrinfo('api.genius.com', 443, type=socket.SOCK_STREAM)
            emit('dns', status='resolved', address_count=len(addresses), elapsed_ms=round(1000 * (time.monotonic() - started)))
        except OSError as error:
            emit('dns', status='error', error=type(error).__name__)
        standard_check(options, token)
        library_check(options, token)
    except Deadline:
        emit('deadline', status='overall_time_limit_reached')
    except Exception as error:
        emit('diagnostic_error', error=type(error).__name__)
    finally:
        signal.alarm(0)
        token = ''
        emit('finished', log=str(LOG), note='Diagnostic finished; source availability is described by the individual stages.')
        print('\nHotovo. Posli subor: ' + str(LOG), flush=True)


if __name__ == '__main__':
    main()
