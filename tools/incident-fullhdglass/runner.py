"""Skúška verejných vydaní na nezmenenom používateľskom priestore OpenPLi 9.2 VU+ Zero."""
from pathlib import Path
import os,re,shutil,subprocess,sys,zipfile,hashlib
from urllib.parse import urljoin,urlparse
from urllib.request import Request,urlopen

def obtain(url,target,limit=240*1024*1024):
    if urlparse(url).scheme!='https': raise ValueError('HTTPS')
    with urlopen(Request(url,headers={'User-Agent':'Mozilla/5.0 Warder-OpenPLi-verification'}),timeout=50) as src,target.open('wb') as dst:
        while data:=src.read(65536):
            if dst.tell()+len(data)>limit: raise ValueError('Veľkosť vstupu')
            dst.write(data)

def image(target):
    # Všetky skúšané adresy patria projektu OpenPLi.
    links=[]
    for page in ('https://openpli.org/download/vuplus/Zero','https://downloads.openpli.org/builds/vuzero/'):
        try:
            html=urlopen(Request(page,headers={'User-Agent':'Mozilla/5.0'}),timeout=25).read(2000000).decode()
            for link in re.findall(r'''href=["']([^"']+openpli-9\.2-release-vuzero-[0-9]{8}_usb\.zip)["']''',html):
                url=urljoin(page,link)
                if urlparse(url).hostname in {'downloads.openpli.org','openpli.org','www.openpli.org'}: links.append(url)
            for name in re.findall(r'openpli-9\.2-release-vuzero-[0-9]{8}_usb\.zip',html):
                links.append('https://downloads.openpli.org/builds/vuzero/'+name)
        except OSError: pass
    links+=['https://downloads.openpli.org/builds/vuzero/openpli-9.2-release-vuzero-20261108_usb.zip','https://downloads.openpli.org/usb/vuzero']
    for url in dict.fromkeys(links):
        try:
            obtain(url,target)
            if zipfile.is_zipfile(target):
                print('Firmware',url,hashlib.sha256(target.read_bytes()).hexdigest(),flush=True)
                return
        except OSError as e: print('OpenPLi',str(e),flush=True)
    raise RuntimeError('Oficiálny obraz VU+ Zero sa nepodarilo prevziať.')

def run(*args): subprocess.run(list(map(str,args)),check=True)
base=Path(os.environ['RUNNER_TEMP'])/'warder-incident'
base.mkdir()
kit=base/'kit';kit.mkdir()
for name in ['test-receiver.sh','obnova-fullhdglass.sh']:
    shutil.copy(Path(__file__).with_name(name),kit/name)
(kit/'izolovane').touch()
for version,sha in [('1.0.94','9dd3300cafffcdaa522b308c22dda863b6bc47ee190ba3f6c24ba235bbcd6028'),('1.0.96','a0cee9a6eb464887f3ebdde297a56fc958d05fdbce29519a5881f6f64c45cb78')]:
    name='enigma2-plugin-skins-fullhdglass_'+version+'_all.ipk'
    obtain('https://github.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/releases/download/v'+version+'/'+name,kit/name)
    assert hashlib.sha256((kit/name).read_bytes()).hexdigest()==sha
image(base/'image.zip')
with zipfile.ZipFile(base/'image.zip') as z:
    entry,=[i for i in z.infolist() if re.fullmatch(r'vuplus/zero/root_cfe_auto\.(bin|jffs2|ubi)',i.filename)]
    assert entry.file_size<500*1024*1024
    with z.open(entry) as src,(base/'root.bin').open('wb') as dest: shutil.copyfileobj(src,dest)
# Extraktor pracuje ako neprivilegovaný používateľ, bez siete a prístupu k repozitáru.
out=base/'fs';out.mkdir();out.chmod(0o777)
venv=Path(os.environ['RUNNER_TEMP'])/'firmware-tools'
with (base/'root.bin').open('rb') as file: magic=file.read(4)
parser=['ubireader_extract_files','-o','/out','/in'] if magic==b'UBI#' or magic==bytes.fromhex('31181006') else ['jefferson','/in','-d','/out/root']
run('sudo','bwrap','--uid','65534','--gid','65534','--unshare-all','--die-with-parent','--ro-bind','/usr','/usr','--symlink','usr/lib','/lib','--symlink','usr/lib64','/lib64','--symlink','usr/bin','/bin','--ro-bind',venv,venv,'--ro-bind',base/'root.bin','/in','--bind',out,'/out','--dev','/dev','--proc','/proc','--tmpfs','/tmp',venv/'bin'/parser[0],*parser[1:])
candidates=[p.parent for p in out.rglob('etc') if (p/'os-release').exists()]
root,=candidates
# Firmware môže mať absolútne symlinky. Testovaciu konfiguráciu vytvárame až v izolovanom koreni.
(kit/'mock').mkdir()
init=kit/'mock/init'
init.write_text('#!/bin/sh\nprintf "%s\\n" "$1" >> /tmp/init-events\n');init.chmod(0o755)
model=kit/'model';model.write_text('zero\n')
# binfmt sprístupní emuláciu aj procesom spúšťaným z OPKG hookov.
run('sudo','bwrap','--unshare-all','--die-with-parent','--new-session','--bind',root,'/','--dev','/dev','--proc','/real-proc','--tmpfs','/proc',
    '--symlink','/real-proc/self','/proc/self','--symlink','/real-proc/meminfo','/proc/meminfo','--symlink','/real-proc/mounts','/proc/mounts','--symlink','/real-proc/cpuinfo','/proc/cpuinfo',
    '--tmpfs','/tmp','--tmpfs','/run','--ro-bind',kit,'/skuska',
    '--dir','/proc/stb','--dir','/proc/stb/info','--ro-bind',model,'/proc/stb/info/vumodel',
    '--ro-bind','/usr/bin/qemu-mipsel-static','/usr/bin/qemu-mipsel-static','--clearenv','--setenv','PATH','/skuska/mock:/usr/sbin:/usr/bin:/sbin:/bin','--uid','0','--gid','0','/bin/sh','/skuska/test-receiver.sh')
