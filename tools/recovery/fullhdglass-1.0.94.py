#!/usr/bin/python3
"""Warder Evolution: núdzová obnova pôvodného VU+ Zero s OpenPLi 9.2."""
import base64
import fcntl
import hashlib
import json
import os
import re
import shutil
import ssl
import subprocess
import sys
import tempfile
import time
import urllib.request
from pathlib import Path

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey

REPO = 'Evolution-by-Warder/FullHDGlass-Warder-Evolution'
PACKAGE = 'enigma2-plugin-skins-fullhdglass-warder-evolution'
NAME = 'enigma2-plugin-skins-fullhdglass_1.0.94_all.ipk'
URL = 'https://github.com/' + REPO + '/releases/download/v1.0.94/' + NAME
SIZE = 18848160
DIGEST = '9dd3300cafffcdaa522b308c22dda863b6bc47ee190ba3f6c24ba235bbcd6028'
PUBLIC = 'MCowBQYDK2VwAyEA/fZvbae2PCW50tlQIv7lYkHYdYUl+77bT/1q2vTny6U='
SIGNED = 'eyJiYWxpayI6ImVuaWdtYTItcGx1Z2luLXNraW5zLWZ1bGxoZGdsYXNzLXdhcmRlci1ldm9sdXRpb24iLCJjb21taXQiOiIzZTJiNzEwN2YxYjJhZjU4NGYyMTMzNTgxNWExYmU1NTk0ZDBmNWJmIiwia2FuYWwiOiJzdGFibGUiLCJwcm9qZWt0IjoiRXZvbHV0aW9uLWJ5LVdhcmRlci9GdWxsSERHbGFzcy1XYXJkZXItRXZvbHV0aW9uIiwic2NoZW1hIjoxLCJzaGEyNTYiOiI5ZGQzMzAwY2FmZmZjZGFhNTIyYjMwOGMyMmRkYTg2M2I2YmM0N2VlMTkwYmEzZjZjMjRiYTIzNWJiY2Q2MDI4IiwidmVyemlhIjoiMS4wLjk0IiwidmVyemlhX2JhbGlrYSI6IjEuMC45NC0xIn0K'
SIGNATURE = '68v+Ft446QzIYo94RxGtp59KmM7L8G8goCtHUd4lQEZcgu1gO7WjUM77K/lAu9tvh+jZ3HDTC523I9q5i1hlAg=='
RUNTIME = Path('/usr/lib/enigma2/python/Plugins/Extensions/setupGlass17')
NATIVE = RUNTIME / 'warderResolution.mipsel-linux-gnu.abi3.so'
PYTHON = RUNTIME / 'warderResolution.py'
SETTINGS = Path('/etc/enigma2')
OPKG = '/usr/bin/opkg'
INIT = '/sbin/init'


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def digest(path):
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(131072), b''):
            h.update(block)
    return h.hexdigest()


def run(*args):
    return subprocess.check_output(args, stdin=subprocess.DEVNULL, text=True)


def version():
    data = run(OPKG, 'status', PACKAGE)
    for stanza in data.strip().split('\n\n'):
        fields = dict(line.split(': ', 1) for line in stanza.splitlines() if ': ' in line and not line.startswith(' '))
        if fields.get('Package') == PACKAGE and fields.get('Status','').endswith(' ok installed'):
            return fields.get('Version')
    return None


def receiver():
    require(os.geteuid() == 0, 'Príkaz spusti v relácii root.')
    models = [Path('/proc/stb/info') / name for name in ('vumodel','model')]
    model = next((p.read_text().strip().lower() for p in models if p.is_file()), '')
    require(model in ('','zero','vuzero') and os.uname().machine in ('mips','mipsel') and sys.byteorder == 'little',
            'Obnova je určená pre pôvodný VU+ Zero.')
    require(re.match(r'^openpli 9\.2-release(?:\s|$)', Path('/etc/issue').read_text(), re.I),
            'Prijímač nemá očakávaný OpenPLi 9.2 release.')
    require(re.search(r'^arch vuzero \d+$',run(OPKG,'print-architecture'),re.M),
            'Architektúra OPKG nesúhlasí s modelom prijímača.')


class HTTPSRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        require(newurl.startswith('https://'), 'Nezabezpečené presmerovanie.')
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def fetch(path):
    opener = urllib.request.build_opener(HTTPSRedirect(),
        urllib.request.HTTPSHandler(context=ssl.create_default_context()))
    with opener.open(URL,timeout=45) as response, path.open('xb') as output:
        count = 0
        for block in iter(lambda: response.read(131072), b''):
            count += len(block)
            require(count <= SIZE, 'Nesprávna veľkosť IPK.')
            output.write(block)


def verify(path):
    der = base64.b64decode(PUBLIC, validate=True)
    require(hashlib.sha256(der).hexdigest()=='c30a61ba62b8463fedb55c6e4a650140d293a75dc0e34290ff724c271532ce50','Neznámy vydávací kľúč.')
    raw = base64.b64decode(SIGNED, validate=True)
    Ed25519PublicKey.from_public_bytes(der[-32:]).verify(base64.b64decode(SIGNATURE,validate=True),raw)
    expected = dict(schema=1, projekt=REPO, kanal='stable', balik=PACKAGE, verzia='1.0.94',
                    verzia_balika='1.0.94-1', commit='3e2b7107f1b2af584f21335815a1be5594d0f5bf', sha256=DIGEST)
    require(json.loads(raw)==expected and path.stat().st_size==SIZE and digest(path)==DIGEST,
            'Podpis, veľkosť alebo SHA-256 nezodpovedá vydaniu.')


def state():
    paths = {}
    def visit(folder):
        for item in folder.iterdir():
            if item.is_symlink():
                paths[item] = ('link',os.readlink(item))
            elif item.is_dir():
                visit(item)
            elif item.is_file():
                paths[item] = ('file',digest(item))
    visit(SETTINGS)
    return paths


def preflight():
    require(SETTINGS.is_dir() and not SETTINGS.is_symlink() and (SETTINGS/'settings').is_file(),
            'Chýbajú očakávané nastavenia Enigma2.')
    for name in ('settings','skin_user-hdg17.xml','skin_user-172.xml','skin_user-173.xml'):
        require(not (SETTINGS/name).is_symlink(), 'Neočakávaný odkaz v nastaveniach.')
    for name, expected in [('skin_user-172.xml','2f85d3e06cacca943e3afaa7c5677c8065a9205d397c6916f2dd968777da624d'),
                           ('skin_user-173.xml','7de7efb6197103393b6a1a9a20e60ba424ed4a39a3b0dcdd4d0ee84209609005')]:
        p=SETTINGS/name
        require(not p.exists() or (p.is_file() and digest(p)==expected), 'Používateľ zmenil súbor balíka '+str(p))
    for path in ('/var/lib/fullhdglass17/package-transition-v1','/tmp/skin_user-hdg17.xml.warder-upgrade'):
        require(not os.path.lexists(path), 'Existuje nedokončená staršia migrácia. Obnova sa zastavila.')
    roots = [d for d in (Path('/var/lib/opkg/info'), Path('/usr/lib/opkg/info')) if (d/(PACKAGE+'.list')).is_file()]
    require(len({d.resolve() for d in roots})==1, 'Nejednoznačná evidencia súborov OPKG.')
    db=roots[0]
    for hook, sha in [('prerm','64d40250d005356ebb9be81567934f2321ab4db93cb6b8d672b6e17e33dd8a3a'),
                      ('postrm','accf53d7f2d0199a85c9ba10612f9b88e86a94cb89b3404408b893e5e4d8ed19')]:
        p=db/(PACKAGE+'.'+hook)
        require(p.is_file() and not p.is_symlink() and digest(p)==sha,'Neočakávaný odinštalačný skript '+hook)
    require(str(NATIVE) in run(OPKG,'files',PACKAGE).splitlines(),
            'OPKG nepotvrdil pôvod chybného modulu.')
    require(shutil.disk_usage('/').free >= 32*1024**2 and shutil.disk_usage('/tmp').free >= SIZE+16*1024**2,
            'Na transakciu OPKG nie je dosť voľného miesta.')


def healthy():
    files = run(OPKG,'files',PACKAGE).splitlines()
    require(version()=='1.0.94-1' and str(PYTHON) in files and str(NATIVE) not in files
            and not os.path.lexists(NATIVE) and PYTHON.is_file() and not PYTHON.is_symlink()
            and digest(PYTHON)=='fa121a535f0fb7a4f0009e8aa3a506e7fd679fa8ba2404da0c040b546dacc761',
            'OPKG alebo spúšťací modul nepotvrdil úspešnú obnovu.')


def recover():
    receiver()
    if version()=='1.0.94-1':
        healthy()
        print('FullHDGlass 1.0.94 je v poriadku.')
        return
    require(version()=='1.0.96-1','OPKG nepotvrdil úplnú inštaláciu 1.0.96.')
    preflight()
    with tempfile.TemporaryDirectory(prefix='warder-',dir='/tmp') as work:
        ipk=Path(work)/NAME
        print('Sťahujem a overujem FullHDGlass 1.0.94.',flush=True)
        if len(sys.argv) == 2:
            ipk = Path(sys.argv[1]).resolve(strict=True)
        elif len(sys.argv) == 1:
            fetch(ipk)
        else:
            raise RuntimeError('Očakáva sa najviac jedna cesta k originálnemu IPK.')
        verify(ipk)
        subprocess.run([OPKG,'--noaction','--force-downgrade','install',str(ipk)],check=True,stdin=subprocess.DEVNULL)
        require(version()=='1.0.96-1','Stav OPKG sa medzitým zmenil.')
        run(INIT,'4')
        for wait in range(30):
            if subprocess.run(['pidof','enigma2'],stdout=subprocess.DEVNULL).returncode==1: break
            time.sleep(1)
        else: raise RuntimeError('GUI sa nezastavilo.')
        before=state()
        subprocess.run([OPKG,'--force-downgrade','install',str(ipk)],check=True,stdin=subprocess.DEVNULL)
        healthy()
        after=state()
        for path, old in before.items():
            require(after.get(path)==old,'Kontrola používateľských nastavení zlyhala pri '+str(path))
        os.sync()
        run(INIT,'3')
        print('FullHDGlass 1.0.94 obnovený. Nastavenia sú zachované. Spúšťa sa GUI.')


if __name__=='__main__':
    try:
        os.umask(0o022)
        lock=os.open('/run',os.O_RDONLY|os.O_DIRECTORY)
        fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
        recover()
    except Exception as error:
        sys.exit('Obnova zastavená: '+(str(error) or type(error).__name__))
