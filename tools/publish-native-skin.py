#!/usr/bin/env python3
"""Publish a verified native skin update without replacing the legacy bridge."""
import argparse
import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path
import re
import subprocess
import tarfile

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('skin_publisher',ROOT/'tools/publish-settings-update.py')
p=importlib.util.module_from_spec(spec);spec.loader.exec_module(p)
PACKAGE='enigma2-plugin-skins-fullhdglass-warder-evolution'


def publish(package,info,revision,approval,client,assets):
    raw=package.read_bytes();digest=hashlib.sha256(raw).hexdigest();version=info['version']
    if not re.fullmatch(r'\d+\.\d+\.\d+',version) or not approval.get('enabled') or approval.get('version')!=version:
        raise ValueError('Stable update is not explicitly authorized')
    name=PACKAGE+'_'+version+'_all.ipk'
    if (package.name,info['package'],info['source_commit'],info['bytes'],info['sha256'])!=(name,name,revision,len(raw),digest):
        raise ValueError('Build identity mismatch')
    if not 0<len(raw)<16*1024*1024:raise ValueError('Small package size budget exceeded')
    with tarfile.open(fileobj=io.BytesIO(subprocess.check_output(['ar','p',str(package),'control.tar.gz'])),mode='r:gz') as archive:
        control=archive.extractfile('./control').read().decode()
    if 'Package: '+PACKAGE+'\n' not in control or 'Version: '+version+'-1\n' not in control:
        raise ValueError('Native package control mismatch')
    release=client.request('GET','/releases/tags/v'+version)
    asset=next(a for a in release['assets'] if a['name']==name)
    if release['draft'] or release['prerelease'] or asset['size']!=len(raw) or asset['digest']!='sha256:'+digest:
        raise ValueError('Stable release asset mismatch')
    p.verify_public(client,asset['browser_download_url'],len(raw),digest)
    for entry in assets.values():p.verify_public(client,entry['url'],entry['size'],entry['sha256'])
    previous=json.loads(p.content(client,'update-production.json','main'))
    url=p.RAW+name
    if previous['version']==version:
        if previous['sha256']!=digest or previous['package_url']!=url:raise ValueError('Immutable version collision')
        p.verify_public(client,url,len(raw),digest)
        return p.head(client,'main')
    if release['target_commitish']!=revision:raise ValueError('Release source mismatch')
    main=p.head(client,'main')
    if main!=approval['expected_main_sha'] or p.head(client,p.WORK)!=revision:
        raise ValueError('Branches advanced before publication')
    staged=p.commit(client,revision,{'packages/'+name:raw,'packages/'+name+'.sha256':(digest+'  '+name+'\n').encode()},'Stage verified native FullHDGlass '+version)
    p.advance(client,'main',main,staged)
    p.verify_public(client,url,len(raw),digest)
    if p.head(client,p.WORK)!=revision:raise ValueError('Source advanced; production feed remains unchanged')
    feed={'version':version,'package_url':url,'sha256':digest,'changelog':approval['changelog']}
    record=json.loads(p.content(client,'docs/PRODUCTION.json','main'))
    record.update(source_commit=revision,source_branch=p.WORK,approval=approval['authorization'])
    record['release']=dict(feed,tag='v'+version,bytes=len(raw),url=asset['browser_download_url'])
    record['validation']={'workflow_run':int(os.environ.get('GITHUB_RUN_ID','0')),'build_payloads_and_public_bytes':'verified','receiver_validation':'Native visual confirmation of the new translucent settings is pending.'}
    inventory=json.loads(p.content(client,'design/settings-ui-inventory.json','main'))
    inventory['production_feed_version']=version
    activated=p.commit(client,staged,{'update-production.json':p.encoded(feed),'docs/PRODUCTION.json':p.encoded(record),'docs/LIVE-UPDATE-STATE.json':p.encoded(dict(feed,bytes=len(raw),source_commit=revision,production_status='production-update',production_tag='v'+version,legacy_bridge_version='1.0.18')),'design/settings-ui-inventory.json':p.encoded(inventory)},'Activate verified native FullHDGlass '+version+'; preserve legacy bridge')
    p.advance(client,'main',staged,activated)
    p.advance(client,p.WORK,revision,activated)
    print('Activated stable native skin:',version,len(raw),digest)
    return activated


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--revision',required=True);args=parser.parse_args()
    info=json.loads((ROOT/'packages/test/settings-ui-build.json').read_text())
    approval=json.loads((ROOT/'design/live-update.json').read_text())
    assets=json.loads((ROOT/'source/package-root/usr/lib/enigma2/python/Plugins/Extensions/setupGlass17/preview-assets.json').read_text())
    publish(ROOT/'packages/test'/info['package'],info,args.revision,approval,p.GitHub(os.environ['GH_TOKEN']),assets)


if __name__=='__main__':main()
