from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from urllib.request import Request,urlopen
from urllib.parse import urljoin
import hashlib,json,re
from lxml import html

R=Path(__file__).resolve().parent
BASE='https://www.satelitnatv.sk'
def fetch(url):
    path=R/'research'/(hashlib.sha256(url.encode()).hexdigest()[:24]+'.html')
    if not path.exists():
        with urlopen(Request(url,headers={'User-Agent':'Mozilla/5.0','Cache-Control':'no-cache'}),timeout=14) as response:
            raw=response.read(6*1024*1024)
        path.write_bytes(raw)
    return path.read_bytes()
def document(url):return html.fromstring(fetch(url))
def text(node):return ' '.join(node.text_content().split())
def safely(url):
    try:return url,document(url),None
    except Exception as e:return url,None,str(e)
def main():
    indices=[BASE+'/vysielace/dvb-t/sk/celoplosne/',BASE+'/vysielace/dvb-t/sk/regionalne/',BASE+'/vysielace/dvb-t/cz/']
    muxes={}
    with ThreadPoolExecutor(max_workers=8) as pool:
        for url,doc,error in pool.map(safely,indices):
            if error:raise RuntimeError(error)
            for a in doc.xpath('//a[@href]'):
                href=urljoin(url,a.get('href'))
                if '/vysielace/dvb-t/' in href and '/multiplex/' in href:
                    muxes[href]={'url':href,'name':text(a),'country':'SK' if '/sk/' in href else 'CZ','scope':'regional' if '/regionalne/' in href or 'regio' in href.lower() else 'national'}
    programmes=[];errors=[]
    with ThreadPoolExecutor(max_workers=8) as pool:
        for url,doc,error in pool.map(safely,muxes):
            if error:errors.append({'url':url,'error':error});continue
            mux=muxes[url]
            for tr in doc.xpath('//tr'):
                cells=tr.xpath('./td');links=tr.xpath('.//a[contains(@href,"/program/")]')
                if len(cells)<3 or not links:continue
                a=links[0];kind=text(cells[-2]);href=urljoin(url,a.get('href'))
                programmes.append(dict(country=mux['country'],scope=mux['scope'],multiplex=mux['name'],multiplex_url=url,name=text(a),programme_url=href,kind=kind,cas=text(cells[-1])))
    print('Multiplexes',len(muxes),'programme rows',len(programmes),flush=True)
    urls=list(dict.fromkeys(p['programme_url'] for p in programmes));details={}
    with ThreadPoolExecutor(max_workers=10) as pool:
        for url,doc,error in pool.map(safely,urls):
            if error:errors.append({'url':url,'error':error});continue
            body=text(doc);m=re.search(r'TSID\s*/\s*ONID\s*/\s*SID\s*:?\s*(\d+)\s*/\s*(\d+)\s*/\s*(\d+)',body)
            details[url]={'tsid':int(m[1]),'onid':int(m[2]),'sid':int(m[3]),'id_number_base':'decimal'} if m else {'id_error':'No measured TSID/ONID/SID tuple'}
            pictures=doc.xpath('//meta[@property="og:image"]/@content')
            details[url]['image_candidates']=pictures
            dates=re.findall(r'Posledn[aá] aktualiz[aá]ci[ae]:?\s*(\d{1,2}\.\d{1,2}\.\d{4}(?:\s+\d\d:\d\d)?)',body)
            if dates:details[url]['measurement_updated']=dates[0]
    for p in programmes:p.update(details.get(p['programme_url'],{'id_error':'Fetch failed'}))
    result={'schema':1,'checked_on':'2026-10-28','measurement_source':'SatelitnaTV live DVB-T/T2 measurements; operator programme lineups take precedence for membership and transmission standard.','multiplexes':list(muxes.values()),'rows':programmes,'errors':errors}
    (R/'catalog/measured-services.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print('Measured',sum('sid' in p for p in programmes),'rows; errors',len(errors),flush=True)
if __name__=='__main__':main()
