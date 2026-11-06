import json,urllib.request,pathlib,concurrent.futures,hashlib,re,html,time
B=pathlib.Path('audit-cache');B.mkdir(exist_ok=True)
def get(u,p,digest=None):
 p=pathlib.Path(p)
 if p.exists():
  d=p.read_bytes()
  if not digest or hashlib.sha256(d).hexdigest()==digest:return d
 for i in range(3):
  try:
   req=urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0 WarderAudit/1.0','Referer':'https://www.vhannibal.net/'})
   d=urllib.request.urlopen(req,timeout=75).read()
   if digest:assert hashlib.sha256(d).hexdigest()==digest
   p.write_bytes(d);return d
  except Exception:
   if i==2:raise

def sources():
 pages=['','hot_bird.php','dual_feed.php','motor.php','quadri_trial.php','autosetting.php'];ids=set();evidence=[]
 for page in pages:
  d=get('https://www.vhannibal.net/'+page,B/('page-'+(page or 'home')+'.html')).decode('utf-8','replace')
  found=set(re.findall(r'download_setting\.php\?[^"<>]+',html.unescape(d)));numbers={int(re.search(r'id=(\d+)',x).group(1)) for x in found if re.search(r'id=(\d+)',x)};ids|=numbers;evidence.append({'page':page,'ids':sorted(numbers),'sha256':hashlib.sha256(d.encode()).hexdigest()})
 (pathlib.Path('audit-output')/'source-pages.json').write_text(json.dumps(evidence,indent=2))
 def one(i):
  p=B/f'official-{i}.zip';d=get(f'https://www.vhannibal.net/download_setting.php?action=download&id={i}',p);print('SOURCE',i,len(d),hashlib.sha256(d).hexdigest(),flush=True)
 with concurrent.futures.ThreadPoolExecutor(max_workers=8)as pool:list(pool.map(one,sorted(ids)))

def production():
 m=json.load(open('manifest.json'));spec={x['filename']:x for x in m['parts']};urls={u for p in m['packages'] for u in p['parts']};done=0
 def one(u):
  n=u.rsplit('/',1)[-1];s=spec[n];p=B/n;d=get(u.replace('/main/','/603218ea8fa51176f686f14f303509a4c64dc7e1/'),p,s['sha256']);assert len(d)==s['bytes'];return n
 with concurrent.futures.ThreadPoolExecutor(max_workers=16)as pool:
  for n in pool.map(one,sorted(urls)):
   done+=1
   if done%100==0:print('PARTS',done,len(urls),flush=True)
if __name__=='__main__':
 import sys
 if sys.argv[1]=='sources':sources()
 else:production()
