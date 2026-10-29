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
combined='--combined' in sys.argv
pisnicky='--pisnicky' in sys.argv
allow_unavailable='--allow-unavailable' in sys.argv
official='--official' in sys.argv
tekstowo='--tekstowo' in sys.argv
karaoke='--karaoke' in sys.argv
kytary='--kytary' in sys.argv
regional='--regional' in sys.argv or combined or pisnicky or official or tekstowo or karaoke or kytary
artist,title=(('08','Krasnejsi nez ruze (Maliconia) - Pavel Roth') if official else
              ('Láska','Mraky') if karaoke else
              ('Lucie','Chci zas v tobě spát') if kytary else
              ('Dara Rolins','Sľub') if tekstowo else
              ('Sima Martausová featuring For You','Nenahraditeľná') if combined else
              ('David Koller','Ani ty ani já') if pisnicky else
              ('Pavol Habera','Láska, necestuj tým vlakom') if regional else ('ABBA','Dancing Queen'))
kwargs={}
if regional:
    import warderLyricsSites as sites
    def regional_only(request,**kwargs):
        for name,host in sites.HOSTS.items():
            if official and name!='roth':continue
            if tekstowo and name!='tekstowo':continue
            if karaoke and name!='karaoke':continue
            if kytary and name!='kytary':continue
            if combined and name!='ujdeto':continue
            if pisnicky and name!='pisnicky':continue
            if sites.safe_url(name,request.full_url):return sites.opener(name)(request,**kwargs)
        raise TimeoutError('JSON APIs intentionally unavailable during regional-source validation')
    kwargs['opener']=regional_only
    kwargs['profile']='skcz'
with tempfile.TemporaryDirectory() as temp:
    result=m.lookup(artist,title,Path(temp),**kwargs)
    state=json.loads((Path(temp)/'.last-result').read_text())
record={'artist':artist,'title':title,'status':result['status'],
        'characters':len(result['text']),'text_sha256':hashlib.sha256(result['text'].encode()).hexdigest(),
        'elapsed_ms':state['elapsed_ms'],'sources_found':[r['source'] for r in state['requests'] if r.get('status')=='found'],
        'lyrics_published':False,'json_apis_disabled':regional,
        'isolated_source':'karaoke' if karaoke else 'kytary' if kytary else 'tekstowo' if tekstowo else 'roth' if official else 'ujdeto' if combined else 'pisnicky' if pisnicky else None,
        'note':'A known-song availability check is not a coverage measurement.',
        'requests':state['requests'],
        'availability_check':'unavailable' if result['status']=='offline' else result['status']}
out=ROOT/'packages/test'/('karaoke-provider-check.json' if karaoke else 'kytary-provider-check.json' if kytary else 'tekstowo-provider-check.json' if tekstowo else 'official-provider-check.json' if official else 'ujdeto-provider-check.json' if combined else 'pisnicky-provider-check.json' if pisnicky else 'regional-provider-check.json' if regional else 'provider-check.json');out.parent.mkdir(parents=True,exist_ok=True)
out.write_text(json.dumps(record,indent=2,ensure_ascii=False)+'\n')
print(json.dumps(record,ensure_ascii=False))
if result['status']!='found':
    if allow_unavailable and (pisnicky or karaoke or kytary) and result['status']=='offline':
        print('::warning::Optional public source unavailable from this runner; availability result is recorded as unavailable, not found. Deterministic parser and fallback tests remain required.')
    else:raise SystemExit('Known-song live provider check did not return an exact match')
