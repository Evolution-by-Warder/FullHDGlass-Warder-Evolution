"""Bounded implementation of SuperMusic's public JavaScript visitor handshake."""
from html.parser import HTMLParser
from http.cookiejar import CookieJar
import io
import re
import time
from urllib.parse import urlencode, urljoin, urlsplit
from urllib.request import Request, build_opener, HTTPRedirectHandler, HTTPCookieProcessor

MAX_BYTES = 1024 * 1024


def safe_url(url):
    try:
        p = urlsplit(url)
        return p.scheme == 'https' and p.hostname in ('www.supermusic.cz', 'www.supermusic.sk') and not p.username and not p.password and p.port in (None, 443)
    except ValueError:
        return False


class Redirects(HTTPRedirectHandler):
    max_redirections = 2
    max_repeats = 2
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        if not safe_url(newurl):
            raise ValueError('SuperMusic redirect outside source')
        return super().redirect_request(req, fp, code, msg, headers, newurl)


class Challenge(HTMLParser):
    def __init__(self):
        super().__init__()
        self.data = None
        self.public_client = False
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if a.get('id') == 'msg':
            self.data = a
        if tag == 'script' and urlsplit(a.get('src', '')).path == '/js/smc.js':
            self.public_client = True


def fnv(data, seed=0x811c9dc5):
    for byte in data:
        seed = ((seed ^ byte) * 16777619) & 0xffffffff
    return seed


def answer(nonce, target, seconds=0.4):
    if not re.fullmatch(r'[0-9a-fA-F]{8,64}', nonce) or not 0 < target < 2**32:
        raise ValueError('Invalid public challenge')
    seed = fnv((nonce + ':').encode('ascii'))
    deadline = time.monotonic() + seconds
    for count in range(100000):
        if count % 256 == 0 and time.monotonic() >= deadline:
            break
        if fnv(str(count).encode('ascii'), seed) < target:
            return count
    raise TimeoutError('Public visitor-check CPU budget exhausted')


class PageResponse(io.BytesIO):
    code = 200
    status = 200
    def __init__(self, raw, url):
        super().__init__(raw)
        self.url = url
    def geturl(self):
        return self.url
    def getcode(self):
        return self.code


class Session:
    def __init__(self):
        self.transport = build_opener(Redirects(), HTTPCookieProcessor(CookieJar()))
        self.request_count = 0
        self.validation_count = 0
    def _fetch(self, request, deadline):
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            raise TimeoutError('SuperMusic request budget exhausted')
        self.request_count += 1
        with self.transport.open(request, timeout=remaining) as response:
            raw = response.read(MAX_BYTES + 1)
            final = response.geturl()
        if len(raw) > MAX_BYTES or not safe_url(final):
            raise ValueError('Invalid SuperMusic response')
        return raw, final
    def open(self, request, timeout=10):
        if not safe_url(request.full_url) or request.get_header('Authorization'):
            raise ValueError('Invalid SuperMusic request')
        deadline = time.monotonic() + min(10, timeout)
        raw, final = self._fetch(request, deadline)
        if len(raw) > 4096:
            return PageResponse(raw, final)
        page = Challenge()
        page.feed(raw.decode('utf-8', 'replace'))
        if not page.public_client or not page.data:
            return PageResponse(raw, final)
        attrs = page.data
        nonce, target, token, path = (attrs.get(k, '') for k in ('data-n', 'data-l', 'data-t', 'data-u'))
        if not target.isdecimal() or not re.fullmatch(r'[A-Za-z0-9._-]{1,256}', token):
            raise ValueError('Invalid visitor-check attributes')
        canonical = urljoin(final, path)
        if not safe_url(canonical) or urlsplit(canonical).hostname != urlsplit(final).hostname or urlsplit(canonical).path != '/piesen.php':
            raise ValueError('Invalid visitor-check destination')
        count = answer(nonce, int(target), min(0.4, max(0, deadline - time.monotonic())))
        validated_url = canonical + ('&' if urlsplit(canonical).query else '?') + urlencode({'_smc': token + '.' + str(count)})
        headers = dict(request.header_items())
        headers['Referer'] = final
        self.validation_count += 1
        raw, result_url = self._fetch(Request(validated_url, headers=headers), deadline)
        if len(raw) <= 4096:
            repeated = Challenge()
            repeated.feed(raw.decode('utf-8', 'replace'))
            if repeated.public_client and repeated.data:
                raise ValueError('Public visitor check was not accepted')
        # Keep the canonical URL in parser/diagnostic output, not the visitor token.
        return PageResponse(raw, canonical)
