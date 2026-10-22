"""Publish bounded archive batches on staging, then commit the verified live catalogue."""
from pathlib import Path
import subprocess
R=Path(__file__).resolve().parents[1];branch='release/original-satellite-sizes-20261022'
def git(*args):return subprocess.check_output(['git',*args],cwd=R).decode().strip()
new=git('ls-files','--others','--exclude-standard','-z','assets/warder/downloads/picons/channels').split('\0');groups={}
for name in new:
 if '.zip.part' in name:groups.setdefault(Path(name).name,[]).append(name)
batches=[];batch=[];size=0
for basename,paths in sorted(groups.items()):
 length=(R/paths[0]).stat().st_size
 if batch and size+length>300*1024*1024:batches.append(batch);batch=[];size=0
 batch.extend(paths);size+=length
if batch:batches.append(batch)
for i,paths in enumerate(batches,1):
 git('add','--sparse','--',*paths);git('commit','-m','Store supplied satellite archive data batch %d/%d [skip ci]'%(i,len(batches)));git('push','origin','HEAD:'+branch);print('PUSHED bounded archive batch',i,'/',len(batches),flush=True)
git('add','--sparse','-f','--','source','tools','reports','docs/PICON-CATALOG-UPDATES.md','README.md','update.json','update-test.json','assets/warder/downloads/picons/channels','packages/enigma2-skin-fullhdglass17-warder-evolution_1.0.14_all.ipk','packages/enigma2-skin-fullhdglass17-warder-evolution_1.0.14_all.ipk.sha256','.transfer/source-artifact.json')
git('commit','-m','Connect original satellite sizes; preserve existing PNGs and 1.0.13 compatibility [skip ci]');git('push','origin','HEAD:'+branch)
print('PASS: verified release committed on staging:',git('rev-parse','HEAD'),flush=True)
