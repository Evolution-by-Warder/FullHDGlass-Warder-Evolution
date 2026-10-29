"""Verify normal public visitor loading and report markup shapes, not lyric text."""
from collections import Counter
from html.parser import HTMLParser
import json
import re
from urllib.request import Request
from supermusic_session import Session

class Shape(HTMLParser):
    def __init__(self):
        super().__init__()
        self.headers = []
        self.active = None
        self.blocks = []
        self.classes = Counter()
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        self.classes.update(a.get('class', '').split())
        if tag in ('h1', 'h2', 'title'):
            self.active = tag
            self.headers.append([tag, ''])
        if tag in ('div', 'pre', 'article', 'span') and any(w in (a.get('id', '') + a.get('class', '')).lower() for w in ('lyric', 'song', 'piesen', 'text', 'chord', 'akord')):
            self.blocks.append({'tag': tag, 'id': a.get('id', ''), 'class': a.get('class', '')[:150]})
    def handle_endtag(self, tag):
        if self.active == tag:
            self.active = None
    def handle_data(self, data):
        if self.active:
            self.headers[-1][1] = (self.headers[-1][1] + data)[:200]

session = Session()
for number in (1007929, 62753):
    url = 'https://www.supermusic.cz/piesen.php?idpiesne=' + str(number)
    try:
        with session.open(Request(url, headers={'User-Agent': 'FullHDGlass-Warder-Evolution/source-check'}), timeout=10) as response:
            raw = response.read()
        page = Shape()
        page.feed(raw.decode('utf-8', 'replace'))
        print('SUPERMUSIC_SESSION ' + json.dumps({'url': url, 'bytes': len(raw), 'headers': page.headers[:10], 'blocks': page.blocks[:35], 'classes': page.classes.most_common(15), 'request_count': session.request_count, 'validation_count': session.validation_count}), flush=True)
    except Exception as error:
        print('SUPERMUSIC_SESSION ' + json.dumps({'url': url, 'error': type(error).__name__}), flush=True)

url = 'https://www.supermusic.cz/najdi.php?hladane=Laska+Mraky'
try:
    with session.open(Request(url, headers={'User-Agent': 'FullHDGlass-Warder-Evolution/source-check'}), timeout=10) as response:
        raw = response.read().decode('utf-8', 'replace')
    class SearchShape(HTMLParser):
        def __init__(self):
            super().__init__();self.stack=[];self.links=[];self.anchor=None
        def handle_starttag(self,tag,attrs):
            a=dict(attrs)
            if tag=='a' and any(k in a.get('href','') for k in ('piesen.php','interpret.php')) and len(self.links)<16:
                self.anchor={'href':a.get('href'),'label':'','parents':self.stack[-6:]};self.links.append(self.anchor)
            if tag not in ('br','img','meta','link','input','hr'):
                self.stack.append({'tag':tag,'class':a.get('class',''),'id':a.get('id','')})
        def handle_endtag(self,tag):
            if tag=='a':self.anchor=None
            for index in range(len(self.stack)-1,-1,-1):
                if self.stack[index]['tag']==tag:self.stack=self.stack[:index];break
        def handle_data(self,data):
            if self.anchor is not None:self.anchor['label']=(self.anchor['label']+data)[:150]
    structure=SearchShape();structure.feed(raw)
    links = []
    for match in re.finditer(r'<a\b[^>]*href=["\'][^"\']*piesen\.php[^"\']*["\'][^>]*>', raw, re.I):
        opening = match.group(0)
        before = raw[max(0, match.start()-350):match.start()]
        parents = re.findall(r'<(?:div|tr|td|span)\b[^>]*(?:class|id)=["\'][^"\']*["\'][^>]*>', before, re.I)[-3:]
        links.append({'opening': opening[:250], 'parents': parents})
        if len(links) == 10:
            break
    print('SUPERMUSIC_SEARCH_SHAPE ' + json.dumps({'url': url, 'song_links': links,'structured_links':structure.links}), flush=True)
except Exception as error:
    print('SUPERMUSIC_SEARCH_SHAPE ' + json.dumps({'error': type(error).__name__}), flush=True)
