#!/usr/bin/env python3
"""Check the owner's public LyricFind links without logging lyrics or credentials."""
import hashlib
from html.parser import HTMLParser
import json
from urllib.error import HTTPError, URLError
from urllib.request import HTTPRedirectHandler, Request, build_opener
from urllib.parse import urlsplit

URLS = (
    'https://lyrics.lyricfind.com/lyrics/i-m-t-smile-usmev-a-caj',
    'https://lyrics.lyricfind.com/lyrics/kali-aj-keby',
)
MAX_BYTES = 1024 * 1024


def allowed(url):
    p = urlsplit(url)
    return (p.scheme == 'https' and p.hostname == 'lyrics.lyricfind.com'
            and p.port in (None, 443) and not p.username and not p.password)


class SameHostRedirects(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        if not allowed(newurl):
            raise URLError('Redirect outside the public source host')
        return super().redirect_request(req, fp, code, msg, headers, newurl)


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.has_next_data = False
        self.in_title = False
        self.title = ''

    def handle_starttag(self, tag, attrs):
        if tag == 'script' and dict(attrs).get('id') == '__NEXT_DATA__':
            self.has_next_data = True
        if tag == 'title':
            self.in_title = True

    def handle_endtag(self, tag):
        if tag == 'title':
            self.in_title = False

    def handle_data(self, data):
        if self.in_title:
            self.title = (self.title + data)[:120]


def check(url):
    if not allowed(url):
        raise ValueError('Unsupported source URL')
    result = {'url': url, 'lyrics_logged': False}
    try:
        request = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        try:
            response = build_opener(SameHostRedirects()).open(request, timeout=15)
        except HTTPError as error:
            response = error
        with response:
            raw = response.read(MAX_BYTES + 1)
            result.update(http=response.code, final_url=response.geturl(), bytes=len(raw))
        if len(raw) > MAX_BYTES:
            result['classification'] = 'response-too-large'
            return result
        page = Page()
        page.feed(raw.decode('utf-8', 'replace'))
        result.update(sha256=hashlib.sha256(raw).hexdigest(),
                      page_title=page.title, has_next_data=page.has_next_data)
        if response.code != 200:
            result['classification'] = 'http-error'
        elif 'site unavailable' in page.title.lower():
            result['classification'] = 'unavailable-placeholder'
        elif page.has_next_data:
            result['classification'] = 'app-page-received-not-yet-lyrics-verified'
        else:
            result['classification'] = 'unverified-html'
    except (OSError, ValueError) as error:
        result.update(classification='request-error', error=type(error).__name__)
    return result


if __name__ == '__main__':
    for url in URLS:
        print('LYRICFIND_ACCESS ' + json.dumps(check(url), ensure_ascii=False), flush=True)
