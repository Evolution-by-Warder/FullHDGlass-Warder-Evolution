"""Bounded public-page adapters. Return original lyrics only after exact identity checks."""
from html.parser import HTMLParser
import re
import unicodedata
from urllib.parse import urlencode,urljoin,urlsplit
from urllib.request import HTTPRedirectHandler,build_opener

HOSTS={'hudba':'hudba.zoznam.sk','youradio':'textypisni.youradio.cz'}
LIMITS={'hudba':4,'youradio':3}
VOID={'area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr'}
SKIP={'script','style','noscript','iframe','template'}


def slug(value):
    value=unicodedata.normalize('NFKD',str(value).casefold())
    value=''.join(c for c in value if not unicodedata.combining(c))
    return re.sub(r'[^a-z0-9]+','-',value).strip('-')


def safe_url(name,url):
    try:
        parsed=urlsplit(url)
        port=parsed.port
    except ValueError:return False
    return parsed.scheme=='https' and parsed.hostname==HOSTS[name] and not parsed.username and not parsed.password and port in (None,443)


class SameHostRedirect(HTTPRedirectHandler):
    max_redirections=2
    max_repeats=2
    def __init__(self,name):self.name=name
    def redirect_request(self,req,fp,code,msg,headers,newurl):
        if not safe_url(self.name,newurl):raise ValueError('Cross-host lyrics redirect rejected')
        return HTTPRedirectHandler.redirect_request(self,req,fp,code,msg,headers,newurl)


def opener(name):return build_opener(SameHostRedirect(name)).open


def initial_urls(name,artist,title):
    base='https://'+HOSTS[name]
    if name=='hudba':
        return [base+'/'+slug(artist)+'/piesen/'+slug(title)+'/',
                base+'/hladaj/?'+urlencode({'q':artist+' '+title})]
    return [base+'/hledej/?'+urlencode({'search':artist+' '+title})]


class Page(HTMLParser):
    def __init__(self,name):
        HTMLParser.__init__(self,convert_charrefs=True)
        self.name=name;self.stack=[];self.headers=[];self.anchors=[];self.blocks=[]
        self.header=None;self.anchor=None;self.body=None
    def ignored(self):return any(node[0] in SKIP for node in self.stack)
    def handle_starttag(self,tag,attrs):
        tag=tag.lower();attributes=dict(attrs);classes=set(attributes.get('class','').split())
        depth=len(self.stack)+1
        if depth>128:raise ValueError('HTML nesting limit')
        if self.ignored():
            if tag not in VOID:self.stack.append((tag,classes))
            return
        if tag=='br' and self.body is not None:self.body['parts'].append('\n')
        if tag in ('p','div','li') and self.body is not None:self.body['parts'].append('\n')
        if tag in ('h1','h2') and len(self.headers)<20:
            self.header={'tag':tag,'depth':depth,'parts':[]};self.headers.append(self.header)
        if tag=='a' and len(self.anchors)<512:
            self.anchor={'href':attributes.get('href',''),'depth':depth,'parts':[],
                         'breadcrumb':any(t=='p' and 'title' in c for t,c in self.stack)}
            self.anchors.append(self.anchor)
        wanted='song-text-full-width' if self.name=='hudba' else 'lyrics-orig'
        if wanted in classes and len(self.blocks)<2:
            self.body={'depth':depth,'parts':[]};self.blocks.append(self.body)
        if tag not in VOID:self.stack.append((tag,classes))
    def handle_startendtag(self,tag,attrs):
        self.handle_starttag(tag,attrs)
        if tag.lower() not in VOID:self.handle_endtag(tag)
    def handle_endtag(self,tag):
        for index in range(len(self.stack)-1,-1,-1):
            if self.stack[index][0]==tag.lower():break
        else:return
        depth=index+1
        if self.body is not None and not self.ignored() and tag in ('p','div','li'):self.body['parts'].append('\n')
        for name in ('header','anchor','body'):
            value=getattr(self,name)
            if value is not None and value['depth']>=depth:setattr(self,name,None)
        del self.stack[index:]
    def handle_data(self,data):
        if self.ignored():return
        for value in (self.header,self.anchor,self.body):
            if value is not None:value['parts'].append(data)
    @staticmethod
    def text(value):return ' '.join(''.join(value['parts']).split())
    def lyrics(self):
        if len(self.blocks)!=1:return ''
        value=''.join(self.blocks[0]['parts']).replace('\r','')
        return re.sub(r'\n{3,}','\n\n','\n'.join(line.strip() for line in value.splitlines())).strip()


def parse(name,url,raw,artist,title,matches,clean):
    if not safe_url(name,url):raise ValueError('Invalid lyrics page host')
    page=Page(name);page.feed(raw.decode('utf-8-sig'));page.close()
    if page.body is not None:raise ValueError('Unclosed lyrics container')
    h1=[Page.text(h) for h in page.headers if h['tag']=='h1']
    h2=[Page.text(h) for h in page.headers if h['tag']=='h2']
    row=None
    if name=='hudba' and h1 and h2:
        row={'artistName':h1[0],'trackName':h2[0]}
    elif name=='youradio' and h1:
        names=[Page.text(a) for a in page.anchors if a['breadcrumb'] and len(urlsplit(a['href']).path.strip('/').split('/'))==1 and urlsplit(a['href']).path.strip('/')]
        if names:row={'artistName':names[0],'trackName':h1[0]}
    if row and matches(row,artist,title):
        text=clean(page.lyrics())
        if text:return {'text':text,'links':[],'negative':False}
    # An expected catalogue/song page is distinguishable from a login,
    # JavaScript challenge, proxy error or unrelated markup.
    is_search=(name=='hudba' and h1 and h1[0]=='Vyhľadávanie') or (name=='youradio' and h1 and h1[0]=='Výsledky vyhledávání')
    recognized=bool((row and page.blocks) or is_search)
    links=[]
    if is_search:
        pairs={(slug(a),slug(t)) for a,t in ((artist,title),(title,artist))}
        for anchor in page.anchors:
            try:target=urljoin(url,anchor['href']).split('#',1)[0]
            except (TypeError,ValueError):continue
            if not safe_url(name,target):continue
            parts=urlsplit(target).path.strip('/').split('/')
            if name=='hudba':
                valid=len(parts)==3 and parts[1]=='piesen' and any(parts[0]==a and (parts[2]==t or re.fullmatch(re.escape(t)+r'-\d+',parts[2])) for a,t in pairs)
            else:valid=len(parts)==3 and any(parts[0]==a and parts[2]==t for a,t in pairs)
            if valid and not urlsplit(target).query and target not in links:
                links.append(target)
                if len(links)==2:break
    if not recognized:raise ValueError('Unrecognized lyrics page')
    return {'text':'','links':links,'negative':not links}
