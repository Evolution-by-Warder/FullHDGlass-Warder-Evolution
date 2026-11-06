from pathlib import Path
import json,hashlib
B=Path('audit-output/approved-repairs');old=json.load(open('manifest.json'));m=json.load(open(B/'manifest.json'));oldspec={x['filename']:x for x in old['parts']};meta={x['filename']:x for x in m['parts']};aliases=[];replacement={}
for p in m['packages']:
 for i,u in enumerate(p['parts']):
  n=u.rsplit('/',1)[-1];expected=p['filename']+f'.part{i:02d}'
  if n==expected:continue
  assert n in oldspec
  raw=(Path('audit-cache')/n).read_bytes();assert hashlib.sha256(raw).hexdigest()==oldspec[n]['sha256'];new={**oldspec[n],'filename':expected};meta[expected]=new;p['parts'][i]=u.rsplit('/',1)[0]+'/'+expected;aliases.append({'path':'assets/warder/downloads/picons/channels/'+expected,'mode':'100644','type':'blob','sha':hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest(),'original_filename':n});replacement[expected]=n
used={u.rsplit('/',1)[-1]for p in m['packages']for u in p['parts']};m['parts']=sorted([meta[n]for n in used],key=lambda x:x['filename']);assert len(m['parts'])==len(used)
raw=(json.dumps(m,ensure_ascii=False,sort_keys=True,indent=2)+'\n').encode();(B/'manifest.json').write_bytes(raw);sums={l.split()[-1]:l.split()[0]for l in Path('fullhd/assets/warder/downloads/picons/channels/SHA256SUMS').read_text().splitlines()if l.strip()};sums.update({x['filename']:x['sha256']for x in m['parts']});sums['manifest.json']=hashlib.sha256(raw).hexdigest();(B/'SHA256SUMS').write_text(''.join(h+'  '+n+'\n'for n,h in sorted(sums.items())));(B/'reused-git-blobs.json').write_text(json.dumps(aliases,indent=2));print('Reused existing Git blob aliases',len(aliases),'new manifest parts',len(m['parts']))
