from pathlib import Path
import json,hashlib
B=Path('audit-output/approved-repairs');old=json.load(open('manifest.json'));m=json.load(open(B/'manifest.json'));oldspec={x['filename']:x for x in old['parts']};new=[]
for p in m['packages']:
 delta=[u for u in p['parts']if u.rsplit('/',1)[-1]not in oldspec]
 if not delta:continue
 raw=b''.join((B/u.rsplit('/',1)[-1]).read_bytes()for u in delta);urls=[u for u in p['parts']if u.rsplit('/',1)[-1]in oldspec];prefix=delta[0].rsplit('/',1)[0]+'/'
 for offset in range(0,len(raw),300000):
  v=raw[offset:offset+300000];n=p['filename']+f'.part{len(urls):02d}';(B/n).write_bytes(v);urls.append(prefix+n);new.append({'filename':n,'bytes':len(v),'sha256':hashlib.sha256(v).hexdigest()})
 p['parts']=urls
used={u.rsplit('/',1)[-1]for p in m['packages']for u in p['parts']};m['parts']=sorted([s for s in old['parts']+new if s['filename']in used],key=lambda x:x['filename']);assert len(m['parts'])==len(used);raw=(json.dumps(m,ensure_ascii=False,sort_keys=True,indent=2)+'\n').encode();(B/'manifest.json').write_bytes(raw)
sums={l.split()[-1]:l.split()[0]for l in Path('fullhd/assets/warder/downloads/picons/channels/SHA256SUMS').read_text().splitlines()if l.strip()};sums.update({x['filename']:x['sha256']for x in new});sums['manifest.json']=hashlib.sha256(raw).hexdigest();(B/'SHA256SUMS').write_text(''.join(h+'  '+n+'\n'for n,h in sorted(sums.items())))
(B/'new-parts.json').write_text(json.dumps(new,indent=2));print('newparts',len(new),'bytes',sum(x['bytes']for x in new))
