"""Bounded public-page adapters. Return original lyrics only after exact identity checks."""
from html.parser import HTMLParser
import re
import unicodedata
from urllib.parse import urlencode,urljoin,urlsplit,parse_qs
from urllib.request import HTTPRedirectHandler,build_opener
try:
    from Plugins.Extensions.setupGlass17 import warderSongIdentity as song_identity
except ImportError:
    import warderSongIdentity as song_identity

HOSTS={'hudba':'hudba.zoznam.sk','youradio':'textypisni.youradio.cz',
       'ujdeto':'www.ujdeto.cz','pisnicky':'pisnicky-akordy.cz','roth':'www.pavelroth.cz','tekstowo':'www.tekstowo.pl'}
LIMITS={'hudba':4,'youradio':3,'ujdeto':4,'pisnicky':3,'roth':1,'tekstowo':3}
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
    if name=='roth':
        known={'artistName':'Pavel Roth','trackName':'Malinconia (Krásnější než růže)'}
        return [base+'/texty.htm?skladba=36'] if song_identity.same_recording(known,artist,title) else []
    query_artist,query_title=song_identity.query_pair(artist,title)
    names=song_identity.site_artists(artist,title)
    titles=song_identity.site_titles(artist,title)
    if name=='hudba':
        # Preserve the established first URL when no normalization is needed.
        return [base+'/'+slug(n)+'/piesen/'+slug(titles[0])+'/' for n in names[:2]]+[
                base+'/hladaj/?'+urlencode({'q':names[0]+' '+query_title})]
    if name=='youradio':
        return [base+'/hledej/?'+urlencode({'search':names[0]+' '+query_title})]
    if name=='ujdeto':
        candidates=[(n,t) for t in titles for n in names][:3]
        return [base+'/lyrics/'+slug(n)+'/'+slug(t)+'/' for n,t in candidates]+[
            base+'/hledej.php?'+urlencode({'hledat':names[0]+' '+query_title})]
    return [base+'/'+slug(n)+'/'+slug(t) for t in titles for n in names][:3]


class Page(HTMLParser):
    def __init__(self,name):
        HTMLParser.__init__(self,convert_charrefs=True)
        self.name=name;self.stack=[];self.headers=[];self.anchors=[];self.blocks=[]
        self.header=None;self.anchor=None;self.body=None
    def ignored(self):
        return any(t in SKIP or (self.name=='pisnicky' and ('chord' in c or 'akord' in c)) for t,c in self.stack)
    def handle_starttag(self,tag,attrs):
        tag=tag.lower();attributes=dict(attrs);classes=set(attributes.get('class','').split())
        if attributes.get('id'):classes.add('#'+attributes['id'])
        depth=len(self.stack)+1
        if depth>128:raise ValueError('HTML nesting limit')
        if self.ignored():
            if tag not in VOID:self.stack.append((tag,classes))
            return
        if tag=='br' and self.body is not None:self.body['parts'].append('\n')
        if tag in ('p','div','li') and self.body is not None:self.body['parts'].append('\n')
        if (tag in ('h1','h2') or (self.name=='roth' and tag=='title')) and len(self.headers)<20:
            self.header={'tag':tag,'depth':depth,'parts':[],
                         'song_scope':any('#songheader' in c for t,c in self.stack)};self.headers.append(self.header)
        if tag=='a' and len(self.anchors)<512:
            self.anchor={'href':attributes.get('href',''),'depth':depth,'parts':[],
                         'breadcrumb':any(t=='p' and 'title' in c for t,c in self.stack)}
            self.anchors.append(self.anchor)
        wanted={'hudba':'song-text-full-width','youradio':'lyrics-orig',
                'ujdeto':'ltext','pisnicky':'#songtext','roth':'CDtexty','tekstowo':'inner-text'}[self.name]
        if wanted in classes and len(self.blocks)<2 and (self.name!='tekstowo' or any('#songText' in c for t,c in self.stack)):
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
        lines=[line.strip() for line in value.splitlines()]
        if self.name=='pisnicky':
            chord=r'[A-H](?:#|b)?(?:m|mi|maj|min|dim|sus|aug)?\d*(?:/[A-H](?:#|b)?)?'
            lines=[line for line in lines if not re.fullmatch(chord+r'(?:\s+'+chord+r'){1,}',line)]
        return re.sub(r'\n{3,}','\n\n','\n'.join(lines)).strip()


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
    elif name=='ujdeto' and h1:
        heading=h1[0]
        suffix=' - text písně'
        if heading.endswith(suffix) and ' - ' in heading[:-len(suffix)]:
            artist_name,track_name=heading[:-len(suffix)].split(' - ',1)
            row={'artistName':artist_name,'trackName':track_name}
    elif name=='tekstowo' and h1 and ' - ' in h1[0]:
        artist_name,track_name=h1[0].split(' - ',1)
        row={'artistName':artist_name,'trackName':track_name}
    elif name=='pisnicky':
        titles=[Page.text(h) for h in page.headers if h['song_scope'] and h['tag']=='h1']
        artists=[Page.text(h) for h in page.headers if h['song_scope'] and h['tag']=='h2']
        if titles and artists:row={'artistName':artists[0],'trackName':titles[0]}
    elif name=='roth' and h1:
        branded=any(h['tag']=='title' and Page.text(h)=='Pavel Roth | texty' for h in page.headers)
        location=urlsplit(url)
        if branded and location.path=='/texty.htm' and parse_qs(location.query)=={'skladba':['36']}:
            row={'artistName':'Pavel Roth','trackName':h1[0]}
    if row and matches(row,artist,title):
        text=clean(page.lyrics())
        if text:return {'text':text,'links':[],'negative':False}
    # An expected catalogue/song page is distinguishable from a login,
    # JavaScript challenge, proxy error or unrelated markup.
    is_search=(name=='hudba' and h1 and h1[0]=='Vyhľadávanie') or (name=='youradio' and h1 and h1[0]=='Výsledky vyhledávání') or (name=='ujdeto' and urlsplit(url).path=='/hledej.php' and any(v.startswith('Výsledky vyhledávání') for v in h1))
    missing_page=name=='ujdeto' and h1 and h1[0]=='Text písně nenalezen'
    recognized=bool((row and page.blocks) or is_search or missing_page)
    links=[]
    if is_search:
        pairs=set()
        for a,t in ((artist,title),(title,artist)):
            qa,qt=song_identity.query_pair(a,t)
            pairs.update((slug(n),slug(st)) for n in song_identity.site_artists(a,t) for st in song_identity.site_titles(a,t))
            pairs.add((slug(qa),slug(qt)))
        for anchor in page.anchors:
            try:target=urljoin(url,anchor['href']).split('#',1)[0]
            except (TypeError,ValueError):continue
            if not safe_url(name,target):continue
            parts=urlsplit(target).path.strip('/').split('/')
            if name=='hudba':
                valid=len(parts)==3 and parts[1]=='piesen' and any(parts[0]==a and (parts[2]==t or re.fullmatch(re.escape(t)+r'-\d+',parts[2])) for a,t in pairs)
            elif name=='ujdeto':valid=len(parts)==3 and parts[0]=='lyrics' and any(parts[1]==a and parts[2]==t for a,t in pairs)
            else:valid=len(parts)==3 and any(parts[0]==a and parts[2]==t for a,t in pairs)
            if valid and not urlsplit(target).query and target not in links:
                links.append(target)
                if len(links)==2:break
    if not recognized:raise ValueError('Unrecognized lyrics page')
    return {'text':'','links':links,'negative':not links}
