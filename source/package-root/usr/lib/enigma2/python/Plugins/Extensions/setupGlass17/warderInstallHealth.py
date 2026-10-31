"""Check actual installed files and package state before announcing success."""
from pathlib import Path
import re
import subprocess
import xml.etree.ElementTree as ET

PACKAGE = 'enigma2-plugin-skins-fullhdglass-warder-evolution'
PLUGIN = Path(__file__).parent
SKIN = Path('/usr/share/enigma2/hd_glass17')


def verify_payload(expected_version=None, plugin=PLUGIN, skin=SKIN):
    plugin, skin = Path(plugin), Path(skin)
    for path in (plugin/'plugin.py', plugin/'version', skin/'skin.xml'):
        if not path.is_file() or path.stat().st_size == 0:
            raise ValueError('Incomplete FullHDGlass installation: missing ' + str(path))
    installed = (plugin/'version').read_text().strip()
    if not re.fullmatch(r'\d+\.\d+\.\d+(?:-[a-z]+\d+)?', installed):
        raise ValueError('Invalid installed FullHDGlass version')
    if expected_version is not None and installed != expected_version:
        raise ValueError('Installed FullHDGlass version does not match the downloaded release')
    try:
        document = ET.parse(skin/'skin.xml').getroot()
    except ET.ParseError as error:
        raise ValueError('Installed FullHDGlass skin.xml is invalid') from error
    if document.tag != 'skin' or document.find("screen[@name='InfoBar']") is None:
        raise ValueError('Installed FullHDGlass skin.xml has no InfoBar screen')
    return installed


def verify_installation(expected_version, plugin=PLUGIN, skin=SKIN, runner=subprocess.run, manager='opkg'):
    installed = verify_payload(expected_version, plugin, skin)
    if manager == 'opkg':
        command = ['opkg', 'status', PACKAGE]
    elif manager == 'dpkg':
        command = ['dpkg-query', '-W', '-f', 'Package: ${Package}\nVersion: ${Version}\nStatus: ${Status}\n', PACKAGE]
    else:
        raise ValueError('Unsupported package manager')
    result = runner(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, timeout=10)
    if result.returncode != 0:
        raise ValueError('Could not verify installed FullHDGlass package state')
    for paragraph in result.stdout.split('\n\n'):
        fields = dict(line.split(': ', 1) for line in paragraph.splitlines() if ': ' in line and not line[:1].isspace())
        if fields.get('Package') != PACKAGE:
            continue
        version = fields.get('Version', '')
        if (fields.get('Status', '').split() == ['install', 'ok', 'installed'] and
                (version == installed or re.fullmatch(re.escape(installed) + r'-(?:r)?\d+', version))):
            return installed
    raise ValueError('FullHDGlass package is not completely installed')


if __name__ == '__main__':
    import sys
    if sys.argv[1:] != ['--payload-only']:
        sys.exit(2)
    try:
        verify_payload()
    except (OSError, ValueError) as error:
        print(str(error), file=sys.stderr)
        sys.exit(1)
