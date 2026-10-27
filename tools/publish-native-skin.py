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
import zipfile

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('skin_publisher',ROOT/'tools/publish-settings-update.py')
p=importlib.util.module_from_spec(spec);spec.loader.exec_module(p)
PACKAGE='enigma2-plugin-skins-fullhdglass-warder-evolution'


def canonical_files(directory,catalogue):
    report=json.loads((directory/'catalogue.json').read_text())
    expected={kind+'/'+style for kind in ('provider','satellite') for style in ('transparent','black','white')}
    if set(report['variants'])!=expected or report['resolution']!=[220,132]:raise ValueError('Incomplete canonical picon packages')
    files={};entries=[]
    for key,entry in report['variants'].items():
        kind,style=key.split('/');root='piconProv' if kind=='provider' else 'piconSat'
        path='assets/warder/downloads/picons/'+('providers' if kind=='provider' else 'satellites')+'/'+style+'/'+root+'.zip'
        if entry['path']!=path or entry['root']!=root or entry['filename']!=root+'.zip' or entry.get('url')!='https://raw.githubusercontent.com/'+p.REPO+'/main/'+path:raise ValueError('Noncanonical picon path')
        raw=(directory/path).read_bytes()
        if len(raw)!=entry['size'] or hashlib.sha256(raw).hexdigest()!=entry['sha256']:raise ValueError('Picon package hash mismatch')
        with zipfile.ZipFile(io.BytesIO(raw)) as archive:
            if len(archive.namelist())!=entry['png_count'] or archive.testzip() is not None:raise ValueError('Picon package count/CRC mismatch')
            for name in archive.namelist():
                if len(name.split('/'))!=2 or not name.startswith(root+'/') or not name.endswith('.png'):raise ValueError('Wrong picon package root')
        files[path]=raw;entries.append(entry)
    for key in list(catalogue['assets']):
        if key.startswith(('piconProv','piconSat')):del catalogue['assets'][key]
    catalogue.pop('auxiliary_hybrid',None)
    for key,entry in report['variants'].items():
        kind,style=key.split('/');root='piconProv' if kind=='provider' else 'piconSat';suffix={'transparent':'220','black':'b','white':'w'}[style]
        catalogue['assets'][root+'-'+suffix]={k:v for k,v in entry.items() if k not in ('path','legacy_images_normalized')}
    allowed_removals={
        'assets/warder/downloads/picons/providers/220x132/piconProv_220x132.zip',
        'assets/warder/downloads/picons/satellites/220x132/piconSat_220x132.zip',
        'assets/warder/downloads/picons/providers/transparent-legacy/provider-transparent-canalplus.zip',
        'assets/warder/downloads/picons/providers/white/parts/piconProv-white.zip.chunk00.part',
        'assets/warder/downloads/picons/providers/white/parts/piconProv-white.zip.chunk01.part'}
    if set(report['remove_paths'])!=allowed_removals:raise ValueError('Unexpected picon removal plan')
    files.update({path:None for path in allowed_removals})
    files['assets/warder/downloads.json']=p.encoded(catalogue)
    files['docs/PICON-PACKAGES-1.0.24.json']=p.encoded(report)
    return files,entries


def publish(package,info,revision,approval,client,assets,help_bundle=None,canonical_dir=None):
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
    staged_files={'packages/'+name:raw,'packages/'+name+'.sha256':(digest+'  '+name+'\n').encode()}
    help_entry=assets.get('help',{})
    help_raw_url='https://raw.githubusercontent.com/'+p.REPO+'/main/assets/warder/downloads/ui/help/g17_setup_pict.zip'
    if help_entry.get('filename')=='g17_setup_pict.zip':
        if help_bundle is None:raise ValueError('Canonical Help bundle missing')
        help_raw=help_bundle.read_bytes()
        if len(help_raw)!=help_entry['size'] or hashlib.sha256(help_raw).hexdigest()!=help_entry['sha256']:
            raise ValueError('Canonical Help bundle mismatch')
        catalogue=json.loads(p.content(client,'assets/warder/downloads.json','main'))
        catalogue['assets']['help']={'filename':'g17_setup_pict.zip','root':'g17_setup_pict','size':len(help_raw),'sha256':help_entry['sha256'],'url':help_raw_url}
        staged_files['assets/warder/downloads/ui/help/g17_setup_pict.zip']=help_raw
        staged_files['assets/warder/downloads.json']=p.encoded(catalogue)
    canonical=[]
    if canonical_dir is not None:
        catalogue=json.loads(staged_files.get('assets/warder/downloads.json') or p.content(client,'assets/warder/downloads.json','main'))
        extra,canonical=canonical_files(canonical_dir,catalogue);staged_files.update(extra)
    staged=p.commit(client,revision,staged_files,'Stage verified native FullHDGlass '+version)
    p.advance(client,'main',main,staged)
    p.verify_public(client,url,len(raw),digest)
    if help_entry.get('filename')=='g17_setup_pict.zip':p.verify_public(client,help_raw_url,help_entry['size'],help_entry['sha256'])
    for entry in canonical:p.verify_public(client,entry['url'],entry['size'],entry['sha256'])
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
    publish(ROOT/'packages/test'/info['package'],info,args.revision,approval,p.GitHub(os.environ['GH_TOKEN']),assets,Path('/tmp/g17_setup_pict.zip'),Path('/tmp/warder-canonical-picons'))


if __name__=='__main__':main()
