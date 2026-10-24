#!/usr/bin/env python3
"""Expose a verified numbered candidate to the existing receiver updater.

Stage the exact tested IPK first. Only after public download verification do
both update feeds advance together. All ref updates are fast-forward only.
"""
import argparse
import base64
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import time
from urllib.error import HTTPError
from urllib.parse import quote
from urllib.request import Request, urlopen, build_opener

ROOT=Path(__file__).resolve().parents[1]
REPO='Evolution-by-Warder/FullHDGlass-Warder-Evolution'
WORK='warder-modernization-work'
RAW='https://raw.githubusercontent.com/'+REPO+'/main/packages/'
API='https://api.github.com/repos/'+REPO


def encoded(value):return (json.dumps(value,indent=2,ensure_ascii=False)+'\n').encode('utf-8')


class GitHub:
    def __init__(self,token):
        if not token:raise ValueError('GitHub Actions token is required')
        self.token=token
    def request(self,method,path,payload=None):
        request=Request(API+path,data=encoded(payload) if payload is not None else None,method=method,headers={
            'Authorization':'Bearer '+self.token,'Accept':'application/vnd.github+json',
            'Content-Type':'application/json','User-Agent':'FullHDGlass-release-publisher'})
        with urlopen(request,timeout=120) as response:return json.load(response)
    def public_bytes(self,url,size):
        for attempt in range(5):
            try:
                request=Request(url,headers={'User-Agent':'FullHDGlass-release-verifier','Cache-Control':'no-cache'})
                if url.startswith('https://github.com/'+REPO+'/releases/download/'):
                    spec=importlib.util.spec_from_file_location('verified_preview_download',ROOT/'source/package-root/usr/lib/enigma2/python/Plugins/Extensions/setupGlass17/warderPreviewAssets.py')
                    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
                    context=build_opener(module._Redirect()).open(request,timeout=60)
                elif url.startswith(RAW):context=urlopen(request,timeout=60)
                else:raise ValueError('Unexpected public package/asset URL')
                with context as response:
                    final=response.geturl()
                    if url.startswith(RAW) and not final.startswith(RAW):raise ValueError('Unsafe raw-package redirect')
                    return response.read(size+1)
            except (HTTPError,OSError):
                if attempt==4:raise
                time.sleep(2)


def head(client,branch):return client.request('GET','/git/ref/heads/'+quote(branch,safe=''))['object']['sha']


def content(client,path,branch):
    result=client.request('GET','/contents/'+path+'?ref='+quote(branch,safe=''))
    return base64.b64decode(result['content'])


def blob(client,data):
    result=client.request('POST','/git/blobs',{'encoding':'base64','content':base64.b64encode(data).decode('ascii')})
    expected=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
    if result['sha']!=expected:raise ValueError('Git blob checksum mismatch')
    return result['sha']


def commit(client,parent,files,message):
    tree=client.request('GET','/git/commits/'+parent)['tree']['sha']
    entries=[{'path':path,'mode':'100644','type':'blob','sha':blob(client,data)} for path,data in files.items()]
    tree=client.request('POST','/git/trees',{'base_tree':tree,'tree':entries})['sha']
    return client.request('POST','/git/commits',{'parents':[parent],'tree':tree,'message':message})['sha']


def advance(client,branch,old,new):
    if head(client,branch)!=old:raise ValueError('Branch advanced before publication: '+branch)
    client.request('PATCH','/git/refs/heads/'+quote(branch,safe=''),{'sha':new,'force':False})


def verify_public(client,url,data_size,digest):
    data=client.public_bytes(url,data_size)
    if len(data)!=data_size or hashlib.sha256(data).hexdigest()!=digest:
        raise ValueError('Published bytes do not match the verified release')


def publish(package,info,revision,expected_main,client,assets):
    if not re.fullmatch(r'[a-f0-9]{40}',revision):raise ValueError('Invalid source revision')
    raw=package.read_bytes();digest=hashlib.sha256(raw).hexdigest();version=info['version']
    if not re.fullmatch(r'\d+\.\d+\.\d+(?:-test\d+)?',version):raise ValueError('Invalid version')
    name='enigma2-skin-fullhdglass-warder-evolution_'+version+'_all.ipk'
    if package.name!=name or info['package']!=name or info['sha256']!=digest or info['bytes']!=len(raw) or info['source_commit']!=revision:
        raise ValueError('Build identity/checksum mismatch')
    if len(raw)>=16*1024*1024:raise ValueError('Small IPK size budget exceeded')
    # Same redirect policy and checksums as the actual receiver downloader.
    for entry in assets.values():verify_public(client,entry['url'],entry['size'],entry['sha256'])
    url=RAW+name
    previous=json.loads(content(client,'update.json','main'))
    current_main=head(client,'main')
    if previous.get('version')==version:
        if previous.get('sha256')!=digest or previous.get('package_url')!=url:raise ValueError('Immutable version collision')
        verify_public(client,url,len(raw),digest)
        if json.loads(content(client,'update-test.json',WORK))!=previous:
            advance(client,WORK,revision,current_main)
        return current_main
    if current_main!=expected_main:raise ValueError('Main branch differs from approved publication base')
    if head(client,WORK)!=revision:raise ValueError('Source branch advanced; refusing a superseded package')
    staged=commit(client,revision,{'packages/'+name:raw,'packages/'+name+'.sha256':(digest+'  '+name+'\n').encode()},
                  'Stage verified small FullHDGlass '+version+' package before updater activation')
    advance(client,'main',current_main,staged)
    verify_public(client,url,len(raw),digest)
    if head(client,WORK)!=revision:raise ValueError('Source branch advanced; feeds remain unchanged')
    manifest={'version':version,'package_url':url,'sha256':digest,
              'changelog':'Kratšie farebné čiary nad tlačidlami v dialógových oknách. Čiary sú vycentrované nad príslušným nápisom a zladené s PiconHub.'}
    payload=encoded(manifest)
    inventory=json.loads(content(client,'design/settings-ui-inventory.json','main'))
    inventory['current_feed_version']=version
    inventory['feeds_sha256']={name:hashlib.sha256(payload).hexdigest() for name in ('update.json','update-test.json')}
    record={'version':version,'package_url':url,'sha256':digest,'bytes':len(raw),'source_commit':revision,
            'authorization':'Explicit owner request to enable the built-in updater, 24 October 2026',
            'receiver_validation':'Not claimed; automated checks and public byte verification passed.'}
    activated=commit(client,staged,{'update.json':payload,'update-test.json':payload,
                     'design/settings-ui-inventory.json':encoded(inventory),'docs/LIVE-UPDATE-STATE.json':encoded(record)},
                     'Activate verified FullHDGlass '+version+' in both receiver update feeds')
    advance(client,'main',staged,activated)
    advance(client,WORK,revision,activated)
    print('Activated updater:',version,len(raw),'bytes, SHA256',digest)
    return activated


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--package',type=Path,required=True);parser.add_argument('--build-info',type=Path,required=True);parser.add_argument('--revision',required=True);args=parser.parse_args()
    approval=json.loads((ROOT/'design/live-update.json').read_text())
    info=json.loads(args.build_info.read_text())
    if not approval.get('enabled') or approval.get('version')!=info['version']:
        print('This version is not enabled for live updater publication');return
    assets=json.loads((ROOT/'source/package-root/usr/lib/enigma2/python/Plugins/Extensions/setupGlass17/preview-assets.json').read_text())
    publish(args.package,info,args.revision,approval['expected_main_sha'],GitHub(os.environ.get('GH_TOKEN')),assets)


if __name__=='__main__':main()
