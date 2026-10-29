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
       'ujdeto':'www.ujdeto.cz','pisnicky':'pisnicky-akordy.cz','roth':'www.pavelroth.cz','tekstowo':'www.tekstowo.pl','karaoke':'www.karaoketexty.sk','kytary':'akordy.kytary.cz','supermusic':'www.supermusic.cz'}
LIMITS={'hudba':4,'youradio':3,'ujdeto':4,'pisnicky':3,'roth':1,'tekstowo':3,'karaoke':4,'kytary':3,'supermusic':4}
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
    return parsed.scheme=='https' and parsed.hostname in ({HOSTS[name],'www.karaoketexty.cz'} if name=='karaoke' else {HOSTS[name],'www.supermusic.sk'} if name=='supermusic' else {HOSTS[name]}) and not parsed.username and not parsed.password and port in (None,443)


class SameHostRedirect(HTTPRedirectHandler):
    max_redirections=2
    max_repeats=2
    def __init__(self,name):self.name=name
    def redirect_request(self,req,fp,code,msg,headers,newurl):
        if not safe_url(self.name,newurl):raise ValueError('Cross-host lyrics redirect rejected')
        return HTTPRedirectHandler.redirect_request(self,req,fp,code,msg,headers,newurl)


def opener(name):
    if name=='supermusic':
        try:from Plugins.Extensions.setupGlass17.warderSuperMusic import Session
        except ImportError:from warderSuperMusic import Session
        return Session().open
    return build_opener(SameHostRedirect(name)).open


def initial_urls(name,artist,title):
    base='https://'+HOSTS[name]
    if name=='roth':
        known={'artistName':'Pavel Roth','trackName':'Malinconia (Krásnější než růže)'}
        return [base+'/texty.htm?skladba=36'] if song_identity.same_recording(known,artist,title) else []
    query_artist,query_title=song_identity.query_pair(artist,title)
    names=song_identity.site_artists(artist,title)
    titles=song_identity.site_titles(artist,title)
    if name=='karaoke':
        return [base+'/search?'+urlencode({'q':query_title}),'https://www.karaoketexty.cz/search?'+urlencode({'q':query_title})]
    if name=='kytary':
        return [base+'/song/'+slug(query_title),base+'/songs?'+urlencode({'query':query_title})]
    if name=='supermusic':
        return [base+'/najdi.php?'+urlencode({'hladane':names[0]+' '+query_title}),base+'/najdi.php?'+urlencode({'hladane':query_title})]
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
        self.header=None;self.anchor=None;self.body=None;self.super_row=None
    def ignored(self):
        return any(t in SKIP or (self.name=='pisnicky' and ('chord' in c or 'akord' in c)) or (self.name=='kytary' and ('scs-chord' in c or 'scs-chord-label' in c)) or (self.name=='supermusic' and ('chord' in c or 'chord-name' in c)) for t,c in self.stack)
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
        if self.name=='supermusic' and tag=='div' and 'result-item' in classes:
            self.super_row={'depth':depth,'parts':[]}
        if (tag in ('h1','h2') or (self.name in ('roth','supermusic') and tag=='title')) and len(self.headers)<20:
            self.header={'tag':tag,'depth':depth,'parts':[],
                         'song_scope':any('#songheader' in c for t,c in self.stack)};self.headers.append(self.header)
        if tag=='a' and len(self.anchors)<512:
            self.anchor={'href':attributes.get('href',''),'depth':depth,'parts':[],
                         'breadcrumb':any(t=='p' and 'title' in c for t,c in self.stack),
                         'karaoke_artist':any('navigation_lyrics' in c for t,c in self.stack),
                         'song_title_parts':[],'song_artist_parts':[],
                         'supermusic_row':self.super_row}
            self.anchors.append(self.anchor)
        wanted={'hudba':'song-text-full-width','youradio':'lyrics-orig',
                'ujdeto':'ltext','pisnicky':'#songtext','roth':'CDtexty','tekstowo':'inner-text','karaoke':'para_1lyrics_col1','kytary':'smartchordsheet','supermusic':'#chordText'}[self.name]
        if wanted in classes and len(self.blocks)<(128 if self.name=='karaoke' else 2) and (self.name!='tekstowo' or any('#songText' in c for t,c in self.stack)):
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
        for name in ('header','anchor','body','super_row'):
            value=getattr(self,name)
            if value is not None and value['depth']>=depth:setattr(self,name,None)
        del self.stack[index:]
    def handle_data(self,data):
        if self.ignored():return
        if self.name=='kytary' and self.anchor is not None:
            if any('song-card-name' in c for t,c in self.stack):self.anchor['song_title_parts'].append(data)
            if any('song-card-author' in c for t,c in self.stack):self.anchor['song_artist_parts'].append(data)
        for value in (self.header,self.anchor,self.body,self.super_row):
            if value is not None:value['parts'].append(data)
    @staticmethod
    def text(value):return ' '.join(''.join(value['parts']).split())
    def lyrics(self):
        if not self.blocks or (self.name!='karaoke' and len(self.blocks)!=1):return ''
        value='\n\n'.join(''.join(b['parts']) for b in self.blocks).replace('\r','')
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
    elif name=='karaoke' and h1:
        artists=[Page.text(a) for a in page.anchors if a['karaoke_artist'] and re.fullmatch(r'/texty-p(?:iesni|isni)/[^/]+-\d+',urlsplit(a['href']).path)]
        suffix=re.search(r'\s+-\s+text(?:,\s*(?:preklad|překlad))?$',h1[0])
        if artists and suffix:
            row={'artistName':artists[0],'trackName':h1[0][:suffix.start()].strip()}
    elif name=='kytary' and h1 and h2:
        row={'artistName':h2[0],'trackName':h1[0]}
    elif name=='supermusic':
        branded=[Page.text(h) for h in page.headers if h['tag']=='title' and re.search(r'\|\s*SuperMusic\.(?:cz|sk)$',Page.text(h))]
        if branded:
            heading=branded[0].split(' | ',1)[0]
            if ' – ' in heading:
                track_name,artist_name=heading.rsplit(' – ',1)
                # Verified site subtitle for this recording, not a generic
                # removal of version/live/remix information.
                if slug(artist_name)=='imt-smile' and slug(track_name)=='usmev-a-caj-i-am-tea-smile':
                    track_name='Úsmev a čaj'
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
    is_search=is_search or (name=='karaoke' and urlsplit(url).path=='/search' and h1 and h1[0] in ('Hľadanie','Hledání')) or (name=='kytary' and urlsplit(url).path=='/songs' and h1 and h1[0]=='Písně s akordy a texty')
    is_search=is_search or (name=='supermusic' and urlsplit(url).path=='/najdi.php' and h1 and 'Vyhľadávanie' in h1)
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
            if name=='karaoke':
                label=Page.text(anchor)
                candidate=None
                if ' - ' in label:
                    aa,tt=label.split(' - ',1);candidate={'artistName':aa,'trackName':tt}
                valid=len(parts)==3 and parts[0] in ('texty-piesni','texty-pisni') and re.fullmatch(r'.+-\d+',parts[2]) and candidate is not None and matches(candidate,artist,title)
            elif name=='kytary':
                candidate={'artistName':' '.join(''.join(anchor['song_artist_parts']).split()),'trackName':' '.join(''.join(anchor['song_title_parts']).split())}
                valid=len(parts)==2 and parts[0]=='song' and matches(candidate,artist,title)
            elif name=='supermusic':
                label=Page.text(anchor)
                q=parse_qs(urlsplit(target).query)
                row_words=set(slug(' '.join(anchor['supermusic_row']['parts'])).split('-')) if anchor.get('supermusic_row') else set()
                artist_in_row=any(set(slug(n).split('-'))<=row_words for n in song_identity.site_artists(artist,title))
                valid=urlsplit(target).path=='/piesen.php' and len(q)==1 and any(len(v)==1 and re.fullmatch(r'\d{1,12}',v[0]) for k,v in q.items() if k in ('id','idpiesne')) and artist_in_row and any(slug(st)==slug(label) or slug(label).startswith(slug(st)+'-') for st in song_identity.site_titles(artist,title))
                if valid:
                    # Search still emits the legacy id= form. Use the site's
                    # observed canonical idpiesne= destination before opening
                    # its visitor-check flow.
                    number=q.get('idpiesne',q.get('id'))[0]
                    target=urljoin(target,'/piesen.php')+'?'+urlencode({'idpiesne':number})
            elif name=='hudba':
                valid=len(parts)==3 and parts[1]=='piesen' and any(parts[0]==a and (parts[2]==t or re.fullmatch(re.escape(t)+r'-\d+',parts[2])) for a,t in pairs)
            elif name=='ujdeto':valid=len(parts)==3 and parts[0]=='lyrics' and any(parts[1]==a and parts[2]==t for a,t in pairs)
            else:valid=len(parts)==3 and any(parts[0]==a and parts[2]==t for a,t in pairs)
            if valid and (name=='supermusic' or not urlsplit(target).query) and target not in links:
                links.append(target)
                if len(links)==2:break
    if not recognized:raise ValueError('Unrecognized lyrics page')
    return {'text':'','links':links,'negative':not links}
