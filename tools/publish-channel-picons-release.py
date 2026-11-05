#!/usr/bin/env python3
"""Publish the verified picon fix, then activate both installed updater paths."""
import argparse
import base64
import hashlib
import importlib.util
import json
import os
from pathlib import Path
from urllib.parse import quote

ROOT=Path.cwd()
ENCODE=lambda value:(json.dumps(value,ensure_ascii=False,indent=2)+'\n').encode()
SHA=lambda value:hashlib.sha256(value).hexdigest()


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--verified-source')
    parser.add_argument('--verified-run',type=int)
    args=parser.parse_args()
    config=json.loads((ROOT/'docs/CHANNEL-PICONS-RELEASE.json').read_text())
    repo=os.environ['GITHUB_REPOSITORY']; tools_revision=os.environ['GITHUB_SHA']
    revision=args.verified_source or tools_revision
    assert repo==config['repository']
    assert os.environ['GITHUB_REF_NAME']==(config['release_branch'].replace('-20261105','-recovery-20261105') if args.verified_source else config['release_branch'])
    module_path=ROOT/'.piconhub-source/plugin/tools/publish_plugin_release.py'
    spec=importlib.util.spec_from_file_location('picon_release_core',module_path)
    core=importlib.util.module_from_spec(spec); spec.loader.exec_module(core)
    core.REPO=repo; core.API='https://api.github.com/repos/'+repo
    client=core.GitHub(os.environ['GITHUB_TOKEN'])
    if args.verified_source:
        assert args.verified_run
        run=client.request('GET','/actions/runs/'+str(args.verified_run))
        assert run['head_sha']==revision and run['head_branch']==config['release_branch'] and run['status']=='completed'
        jobs=client.request('GET','/actions/runs/'+str(args.verified_run)+'/jobs?per_page=100')['jobs']
        required={'build','openatv / OpenATV 8.0','openatv / OpenATV 8.0-next','openatv / OpenATV master','openpli / native (release-9.2)','openpli / native (develop)','openpli / regression'}
        assert {j['name'] for j in jobs if j['conclusion']=='success'}>=required
    version=config['version']; tag='v'+version
    package=ROOT/config['package']; raw=package.read_bytes(); digest=SHA(raw)
    proof=json.loads((ROOT/'reports/channel-picons-1.0.69/ipk-verification.json').read_text())
    assert (proof['version'],proof['source_commit'],proof['sha256'],proof['bytes'])==(version,revision,digest,len(raw))
    assert proof['all_other_payload_bytes_preserved'] and proof['added_payload_files']==[]

    def head(branch):
        return client.request('GET','/git/ref/heads/'+quote(branch,safe=''))['object']['sha']
    def read(path,branch='main'):
        value=client.request('GET','/contents/'+path+'?ref='+quote(branch,safe=''))
        return base64.b64decode(value['content'])
    def root_entries(commit):
        commit_tree=client.request('GET','/git/commits/'+commit)['tree']['sha']
        return commit_tree,{e['path']:e for e in client.request('GET','/git/trees/'+commit_tree)['tree']}
    def blob(data):
        result=client.request('POST','/git/blobs',dict(encoding='base64',content=base64.b64encode(data).decode()))
        assert result['sha']==hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
        return result['sha']
    def commit(branch,expected,files,message,entries=None):
        assert head(branch)==expected,'Branch advanced; preserve concurrent changes'
        parent_tree,_=root_entries(expected)
        updates=list(entries or [])
        updates.extend(dict(path=p,mode='100644',type='blob',sha=blob(data)) for p,data in files.items())
        tree=client.request('POST','/git/trees',dict(base_tree=parent_tree,tree=updates))
        made=client.request('POST','/git/commits',dict(tree=tree['sha'],parents=[expected],message=message))
        assert head(branch)==expected,'Branch advanced; preserve concurrent changes'
        client.request('PATCH','/git/refs/heads/'+quote(branch,safe=''),dict(sha=made['sha'],force=False))
        return made['sha']
    def verify_public(url):
        downloaded=client.public_package(url,len(raw))
        assert len(downloaded)==len(raw) and SHA(downloaded)==digest

    feeds=('update-production.json','update-test.json')
    current_main=head('main'); _,main_entries=root_entries(current_main)
    assert main_entries['source']['sha']==config['source_base_tree'],'Runtime source advanced before release'
    assert head(config['compatibility_branch'])==config['compatibility_head'],'Updater branch advanced'
    bridge=SHA(read('update.json'))
    for branch in ('main',config['compatibility_branch']):
        for name in feeds:
            assert json.loads(read(name,branch))['version']==config['previous_version']

    release=client.request('GET','/releases/tags/'+tag,allow_missing=True)
    if release is None:
        release=client.request('POST','/releases',dict(tag_name=tag,target_commitish=revision,
            name='FullHDGlass '+version,body=config['notes_i18n']['sk'],draft=True,prerelease=False,make_latest='false'))
    assert release['target_commitish']==revision,'Immutable release source collision'
    assets={a['name']:a for a in release.get('assets',[])}
    for name,data in ((package.name,raw),(package.name+'.sha256',(digest+'  '+package.name+'\n').encode())):
        asset=assets.get(name)
        if asset is None:
            assert release['draft']
            asset=client.request('POST','/releases/'+str(release['id'])+'/assets?name='+quote(name),binary=data)
        assert asset['size']==len(data) and asset['digest']=='sha256:'+SHA(data)
    if release['draft']:
        client.request('PATCH','/releases/'+str(release['id']),dict(draft=False,prerelease=False,make_latest='false'))
    public_url='https://github.com/'+repo+'/releases/download/'+tag+'/'+package.name
    verify_public(public_url)

    _,revision_entries=root_entries(revision)
    _,tool_entries=root_entries(tools_revision)
    assert tool_entries['source']['sha']==revision_entries['source']['sha'],'Recovery must preserve the verified runtime source'
    tree_cache={}
    def exact_entry(path):
        entries=tool_entries
        parts=path.split('/')
        for index,part in enumerate(parts):
            item=entries[part]
            if index==len(parts)-1:return item
            assert item['type']=='tree'
            if item['sha'] not in tree_cache:
                tree_cache[item['sha']]={e['path']:e for e in client.request('GET','/git/trees/'+item['sha'])['tree']}
            entries=tree_cache[item['sha']]
    entries=[dict(path='source',mode='040000',type='tree',sha=revision_entries['source']['sha'])]
    for path in config['release_paths']:
        item=exact_entry(path)
        entries.append(dict(path=path,mode=item['mode'],type=item['type'],sha=item['sha']))
    package_path='packages/'+package.name
    staged=commit('main',current_main,{package_path:raw,package_path+'.sha256':(digest+'  '+package.name+'\n').encode()},
        'Stage FullHDGlass '+version+' verified picon fix and package [skip ci]',entries)
    package_url='https://raw.githubusercontent.com/'+repo+'/main/'+package_path
    verify_public(package_url)
    assert head(config['compatibility_branch'])==config['compatibility_head']
    assert SHA(read('update.json'))==bridge

    feed=dict(version=version,package_url=package_url,sha256=digest,changelog=config['notes_i18n']['sk'])
    release_record=dict(feed,tag=tag,url=public_url,bytes=len(raw),notes_i18n=config['notes_i18n'],
        release_url='https://github.com/'+repo+'/releases/tag/'+tag)
    production=json.loads(read('docs/PRODUCTION.json'))
    production['previous_release']=production.get('release')
    if production.get('receiver_confirmation'):
        production['previous_receiver_confirmation']=production.pop('receiver_confirmation')
    production.update(status='production-update-active',approved_on='2026-11-05',approval=config['approval'],
        source_branch=config['release_branch'],source_commit=revision,package_source_commit=revision,release=release_record)
    production['validation']=dict(ci='passed',workflow_run=int(os.environ['GITHUB_RUN_ID']),
        public_ipk_verified=True,channel_picon_lookup_verified=True,channel_picon_default_system_verified=True,all_other_payload_bytes_preserved=True,
        physical_receiver_tested=False)
    production['receiver_validation']='Owner authorized normal publication for receiver feedback; physical confirmation of the picon change is pending.'
    production['version_policy']='1.0.69 restores the original image picon lookup by default and adds an explicit 50x30 option; previous packages and the legacy migration bridge remain immutable.'
    inventory=json.loads(read('design/settings-ui-inventory.json'))
    inventory.update(production_feed_version=version,test_feed_version=version)
    inventory.setdefault('feeds_sha256',{}).update({name:SHA(ENCODE(feed)) for name in feeds})
    readme=read('README.md').decode(); end=readme.find('\n## Project status')
    if end>=0:readme=readme[:end].replace(config['previous_version'],version)+readme[end:]
    readme+='\n## FullHDGlass '+version+' — picony v zozname staníc\n\n'+feed['changelog']+'\n'
    current='# FullHDGlass '+version+'\n\n'+feed['changelog']+'\n\n[Stiahnuť IPK]('+public_url+')\n\nSHA256: '+digest+'\n\nAutomatické kontroly OpenATV a OpenPLi a overenie skutočného balíka prešli. Čakáme na spätnú väzbu z prijímača.\n'
    checkpoint='## FullHDGlass 1.0.69 — 5 November 2026\n\nOwner authorized immediate publication of the channel-list picon source selector. System setting restores the original image lookup by default; Prefer 50x30 is explicit opt-in. OpenATV/OpenPLi automated checks and public package verification passed. Physical receiver feedback is pending. The legacy bridge is preserved.\n\n'
    changes={name:ENCODE(feed) for name in feeds}
    changes.update({'docs/PRODUCTION.json':ENCODE(production),'design/settings-ui-inventory.json':ENCODE(inventory),
        'docs/LIVE-UPDATE-STATE.json':ENCODE(dict(feed,bytes=len(raw),source_commit=revision,production_status='production-update-active',physical_receiver_tested=False)),
        'README.md':readme.encode(),'docs/CURRENT-RELEASE.md':current.encode(),
        'PROJECT-CONTINUITY.md':checkpoint.encode()+read('PROJECT-CONTINUITY.md'),
        'reports/channel-picons-1.0.69/ipk-verification.json':ENCODE(proof)})
    active=commit('main',staged,changes,'Activate FullHDGlass '+version+' channel picon fix [skip ci]')
    compatibility=commit(config['compatibility_branch'],config['compatibility_head'],{name:ENCODE(feed) for name in feeds},
        'Activate FullHDGlass '+version+' installed updater feeds [skip ci]')
    for branch in ('main',config['compatibility_branch']):
        for name in feeds:assert json.loads(read(name,branch))==feed
    assert SHA(read('update.json'))==bridge
    verify_public(public_url); verify_public(package_url)
    client.request('PATCH','/releases/'+str(release['id']),dict(draft=False,prerelease=False,make_latest='true'))
    report=dict(status='PRODUCTION_VERIFIED',release=release_record,source_commit=revision,
        publication_tool_commit=tools_revision,verified_source_workflow_run=args.verified_run or int(os.environ['GITHUB_RUN_ID']),
        main_activation_commit=active,compatibility_activation_commit=compatibility,
        workflow_run=int(os.environ['GITHUB_RUN_ID']),physical_receiver_tested=False)
    output=ROOT/'reports/channel-picons-1.0.69/production.json'
    output.parent.mkdir(parents=True,exist_ok=True); output.write_bytes(ENCODE(report))
    print(json.dumps(report),flush=True)


if __name__=='__main__':main()

