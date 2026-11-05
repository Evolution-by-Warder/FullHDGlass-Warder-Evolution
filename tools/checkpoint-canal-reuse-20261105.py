from pathlib import Path
import subprocess,os
base='assets/warder/downloads/picons/channels/'
r=subprocess.check_output(['git','ls-files','--others','--exclude-standard','-z',base]);files=[n.decode() for n in r.split(b'\0') if n and n.decode().endswith(tuple('.part%02d'%i for i in range(1000)))];total=sum(Path(f).stat().st_size for f in files)
if files and (total>=200*1024*1024 or os.environ.get('FINAL_CANAL_CHECKPOINT')=='1'):
 subprocess.run(['git','add','--sparse','--',*files],check=True)
 subprocess.run(['git','diff','--cached','--check'],check=True)
 subprocess.run(['git','commit','-m','Stage immutable CANAL artwork reuse archives'],check=True)
 subprocess.run(['git','push','origin','HEAD:refs/heads/picons/canal-reuse-20261105'],check=True)
