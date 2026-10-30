#!/usr/bin/env python3
"""Owner-authorized removal of relocated preview release copies after activation."""
import hashlib
import importlib.util
import json
import os
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('publisher',ROOT/'tools/publish-settings-update.py')
p=importlib.util.module_from_spec(spec);spec.loader.exec_module(p)
client=p.GitHub(os.environ['GH_TOKEN'])
def delete(path):
    request=p.Request(p.API+path,method='DELETE',headers={
        'Authorization':'Bearer '+client.token,
        'Accept':'application/vnd.github+json',
        'User-Agent':'FullHDGlass-auxiliary-consolidation'})
    with p.urlopen(request,timeout=60) as response:
        if response.status!=204:raise ValueError('Unexpected deletion response')

expected=json.loads((ROOT/'source/package-root/usr/lib/enigma2/python/Plugins/Extensions/setupGlass17/preview-assets.json').read_text())
feed=json.loads(p.content(client,'update-production.json','main'))
assert tuple(map(int,feed['version'].split('.'))) >= (1,0,42)
p.verify_public(client,feed['package_url'],int(json.loads(p.content(client,'docs/PRODUCTION.json','main'))['release']['bytes']),feed['sha256'])
remote=json.loads(p.content(client,'source/package-root/usr/lib/enigma2/python/Plugins/Extensions/setupGlass17/preview-assets.json','main'))
assert remote==expected
for entry in expected.values():p.verify_public(client,entry['url'],entry['size'],entry['sha256'])
record={'date':'2026-10-30','authorization':'tie subory mimo struktury presun k nam kam treba a potom ich na povodnych miestach zmaz','canonical_assets':expected,'production_feed':feed,'archive_bytes_unchanged':True,'removed_release_copies':[],'removed_development_path':'design'+'/preview-assets/warder-infobar-types.zip','older_installations':'Update to 1.0.42 to receive canonical URLs; verified local caches continue working.'}
releases=client.request('GET','/releases?per_page=100')
for release in releases:
    tag=release['tag_name']
    if tag in ('v1.0.23','settings-ui-1.0.16-test263'):
        allowed={'g17_setup_pict.zip':(expected['help']['size'],expected['help']['sha256']),
                 'warder-infobar-types.zip':(expected['types']['size'],expected['types']['sha256']),
                 'warder-help-previews.zip':(24621325,'ba0eb66e2877c368c2a42ddee87e1270c1ea177096bda74f56edbcaef468deed'),
                 'settings-ui-build.json':(506,'59d8564c87a1c057d6bf0baaa72db57e4d3005ba73120aa608e22e6be2c1494e')}
        for asset in release['assets']:
            assert asset['name'] in allowed,(tag,asset['name'])
            size,digest=allowed[asset['name']]
            assert asset['size']==size and asset['digest']=='sha256:'+digest
        delete('/releases/'+str(release['id']))
        record['removed_release_copies'].append({'tag':tag,'release_id':release['id'],'assets':[a['name'] for a in release['assets']]})
    elif tag=='v1.0.41':
        for asset in release['assets']:
            if asset['name']=='g17_setup_pict.zip':
                assert asset['size']==expected['help']['size'] and asset['digest']=='sha256:'+expected['help']['sha256']
                delete('/releases/assets/'+str(asset['id']))
                record['removed_release_copies'].append({'tag':tag,'asset_id':asset['id'],'name':asset['name']})
for entry in expected.values():p.verify_public(client,entry['url'],entry['size'],entry['sha256'])
remaining=client.request('GET','/releases?per_page=100')
assert all(not a['name'].lower().endswith('.zip') for r in remaining for a in r['assets'])
assert not any(r['tag_name'] in ('v1.0.23','settings-ui-1.0.16-test263') for r in remaining)
record['remaining_releases']=[r['tag_name'] for r in remaining]
record['validation']={'workflow_run':int(os.environ['GITHUB_RUN_ID']),'public_archive_hashes_before_and_after':'passed','active_production_package':'verified','release_auxiliary_zip_count':0}
head=p.head(client,'main')
assert p.head(client,p.WORK)==head
commit=p.commit(client,head,{'reports/auxiliary-assets-consolidation-20261030.json':p.encoded(record)},'Record verified auxiliary archive consolidation and obsolete release removal')
p.advance(client,'main',head,commit);p.advance(client,p.WORK,head,commit)
print(json.dumps(record,ensure_ascii=False,indent=2))
