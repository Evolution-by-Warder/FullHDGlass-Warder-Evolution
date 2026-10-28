#!/usr/bin/env python3
"""Verify public lyrics retrieval without printing or publishing any lyrics."""
import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import sys
ROOT=Path(__file__).resolve().parents[1]
path=ROOT/'source/package-root/usr/lib/enigma2/python/Plugins/Extensions/setupGlass17/warderLyrics.py'
sys.path.insert(0,str(path.parent))
spec=importlib.util.spec_from_file_location('provider_check',path)
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
regional='--regional' in sys.argv
artist,title=('Pavol Habera','Láska, necestuj tým vlakom') if regional else ('ABBA','Dancing Queen')
kwargs={}
if regional:
    import warderLyricsSites as sites
    def regional_only(request,**kwargs):
        for name,host in sites.HOSTS.items():
            if request.full_url.startswith('https://'+host+'/'):return sites.opener(name)(request,**kwargs)
        raise TimeoutError('JSON APIs intentionally unavailable during regional-source validation')
    kwargs['opener']=regional_only
with tempfile.TemporaryDirectory() as temp:
    result=m.lookup(artist,title,Path(temp),**kwargs)
    state=json.loads((Path(temp)/'.last-result').read_text())
record={'artist':artist,'title':title,'status':result['status'],
        'characters':len(result['text']),'text_sha256':hashlib.sha256(result['text'].encode()).hexdigest(),
        'elapsed_ms':state['elapsed_ms'],'sources_found':[r['source'] for r in state['requests'] if r.get('status')=='found'],
        'lyrics_published':False,'json_apis_disabled':regional,
        'note':'A known-song availability check is not a coverage measurement.'}
out=ROOT/'packages/test'/('regional-provider-check.json' if regional else 'provider-check.json');out.parent.mkdir(parents=True,exist_ok=True)
out.write_text(json.dumps(record,indent=2,ensure_ascii=False)+'\n')
print(json.dumps(record,ensure_ascii=False))
if result['status']!='found':raise SystemExit('Known-song live provider check did not return an exact match')
