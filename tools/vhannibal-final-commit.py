from pathlib import Path
import subprocess,json,os,hashlib
run=lambda *a,**kw:subprocess.check_output(a,**kw).decode().strip()
root=Path('.');data=root/'assets/warder/downloads/picons/channels';inputs=Path('.completion-input');proof=json.load(open(inputs/'part-git-shas.json'));existing={line.split()[2] for line in run('git','ls-tree','-r','HEAD','--','assets/warder/downloads/picons/channels').splitlines()};index=str(Path('.completion-index').resolve());env=dict(os.environ,GIT_INDEX_FILE=index);subprocess.check_call(['git','read-tree','HEAD'],env=env);entries=[]
def add(path,expected=None):
 p=Path(path)
 if p.exists():
  oid=run('git','hash-object','-w',str(p));assert expected is None or oid==expected
 else:
  assert expected in existing,('Missing old Git blob',path,expected);oid=expected
 entries.append(f'100644 {oid}\t{path}\n')
for n,oid in proof.items():add(str(data/n),oid)
for n in ('manifest.json','SHA256SUMS'):add(str(data/n))
report=Path('reports/vhannibal-final-20261105');report.mkdir(parents=True,exist_ok=True)
for n in ('live-verification.json','receiver-checks.json','part-git-shas.json','live-config.json'):
 p=report/n;p.write_bytes((inputs/n).read_bytes());add(str(p))
for p in (inputs/'guard').glob('*'):
 if p.is_file():
  target=report/'guard'/p.name;target.parent.mkdir(exist_ok=True);target.write_bytes(p.read_bytes());add(str(target))
subprocess.run(['git','update-index','--index-info'],input=''.join(entries).encode(),env=env,check=True);tree=run('git','write-tree','--missing-ok',env=env);parent=run('git','rev-parse','HEAD');commit=run('git','commit-tree',tree,'-p',parent,input=b'Complete all usable Vhannibal source references in every satellite size and family\n');branch=os.environ['GITHUB_REF_NAME'];subprocess.check_call(['git','push','origin',f'{commit}:refs/heads/{branch}']);(inputs/'publish-result.json').write_text(json.dumps({'commit':commit,'tree':tree,'manifest_sha256':hashlib.sha256((data/'manifest.json').read_bytes()).hexdigest()},indent=2)+'\n');print('PUBLISHED',commit,flush=True)
