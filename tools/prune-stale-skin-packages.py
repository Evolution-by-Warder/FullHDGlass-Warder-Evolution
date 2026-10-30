"""Keep only current, previous and active migration skin packages after activation."""
import importlib.util,json,os,re
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('skin_publisher',ROOT/'tools/publish-settings-update.py')
p=importlib.util.module_from_spec(spec);spec.loader.exec_module(p)
PACKAGE=re.compile(r'^packages/(?:test/)?enigma2-(?:plugin-skins|skin)-fullhdglass(?:17)?(?:-warder-evolution)?_(\d+\.\d+\.\d+(?:-test\d+)?)_all\.ipk(?:\.sha256)?$')

def retention(paths,feeds,current,previous):
    versions={current,previous}|{feed['version'] for feed in feeds}
    active=set()
    for feed in feeds:
        assert feed['package_url'].startswith(p.RAW)
        relative='packages/'+feed['package_url'][len(p.RAW):]
        assert PACKAGE.fullmatch(relative) and relative in paths,relative
        active.update((relative,relative+'.sha256'))
    removed=[]
    for path in paths:
        match=PACKAGE.fullmatch(path)
        if not match:continue
        if path in active:continue
        if '/test/' not in path and match.group(1) in versions:continue
        removed.append(path)
    assert not active.intersection(removed)
    return sorted(removed),versions

def obsolete_releases(releases,versions,current):
    result=[]
    for release in releases:
        tag=release['tag_name'];match=re.fullmatch(r'v(\d+\.\d+\.\d+)',tag)
        if not match or match.group(1) in versions:continue
        if tuple(map(int,match.group(1).split('.'))) >= tuple(map(int,current.split('.'))):continue
        assets=release['assets']
        if assets and all(PACKAGE.fullmatch('packages/'+a['name']) for a in assets):result.append(release)
    return result

def main():
    approval=json.loads((ROOT/'docs/PRODUCTION-APPROVAL.json').read_text())
    client=p.GitHub(os.environ['GH_TOKEN']);head=p.head(client,'main')
    assert p.head(client,p.WORK)==head
    feeds=[json.loads(p.content(client,path,'main')) for path in ('update-production.json','update-test.json','update.json')]
    current=feeds[0]['version'];previous=approval['previous_production']['version']
    assert current==approval['production_version'] and current==feeds[1]['version'] and current!=previous
    record=json.loads(p.content(client,'docs/PRODUCTION.json','main'))
    p.verify_public(client,feeds[0]['package_url'],record['release']['bytes'],feeds[0]['sha256'])
    listing=client.request('GET','/git/trees/'+head+'?recursive=1');assert not listing.get('truncated')
    entries={x['path']:x for x in listing['tree'] if x['type']=='blob'}
    removed,versions=retention(set(entries),feeds,current,previous)
    releases=obsolete_releases(client.request('GET','/releases?per_page=100'),versions,current)
    for release in releases:
        assert p.head(client,'main')==head
        request=p.Request(p.API+'/releases/'+str(release['id']),method='DELETE',headers={'Authorization':'Bearer '+client.token,'Accept':'application/vnd.github+json','User-Agent':'FullHDGlass-package-retention'})
        with p.urlopen(request,timeout=60) as response:assert response.status==204
    assert p.head(client,'main')==head and p.head(client,p.WORK)==head
    result={'status':'VERIFIED','current':current,'previous':previous,'retained_versions':sorted(versions),'removed_paths':removed,'removed_ipks':sum(x.endswith('.ipk') for x in removed),'removed_bytes':sum(entries[x]['size'] for x in removed),'removed_releases':[r['tag_name'] for r in releases],'active_feeds_preserved':True,'trezor_accessed':False,'workflow_run':int(os.environ.get('GITHUB_RUN_ID','0'))}
    files={path:None for path in removed}
    files['reports/package-retention-'+current+'.json']=p.encoded(result)
    files['packages/README.md']=('# Update packages\n\nCurrent production: **'+current+'**. Previous production: **'+previous+'**. Active migration versions are retained according to update.json.\n\nOnly these versions and matching compatibility filenames/checksums are retained. Unreferenced TEST IPKs are removed; packages/test remains ignored build output. Shared auxiliary archives belong in assets/warder/downloads/.\n\nRetention runs only after verified production activation and preserves every active feed target. Trezor is excluded.\n').encode()
    commit=p.commit(client,head,files,'Retain current, previous and active migration packages after '+current)
    p.advance(client,'main',head,commit);p.advance(client,p.WORK,head,commit)
    for feed in feeds:assert json.loads(p.content(client,'update-production.json' if feed is feeds[0] else 'update-test.json' if feed is feeds[1] else 'update.json','main'))==feed
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
