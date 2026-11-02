#!/usr/bin/env python3
"""Verify the actual shipped install checker, OpenPLi adapter and Python payload."""
import argparse
import ast
import hashlib
import io
import json
from pathlib import Path,PurePosixPath
import runpy
import subprocess
import sys
import tarfile
import tempfile
from types import SimpleNamespace
import xml.etree.ElementTree as ET

VERSION='1.0.62-test5'
PACKAGE='enigma2-plugin-skins-fullhdglass-warder-evolution'
PLUGIN='usr/lib/enigma2/python/Plugins/Extensions/setupGlass17'

def verify(package,report,upstream):
    raw=package.read_bytes()
    with tarfile.open(fileobj=io.BytesIO(subprocess.check_output(['ar','p',str(package),'control.tar.gz'])),mode='r:gz') as archive:
        control=archive.extractfile('./control').read().decode()
        postinst=archive.extractfile('./postinst').read().decode()
        assert 'Package: '+PACKAGE+'\n' in control
        assert 'Version: '+VERSION+'-1\n' in control
        assert 'warderInstallHealth.py --payload-only || exit 1' in postinst
    with tempfile.TemporaryDirectory(prefix='fullhdglass-openpli-install-') as folder:
        root=Path(folder);python_files=0
        with tarfile.open(fileobj=io.BytesIO(subprocess.check_output(['ar','p',str(package),'data.tar.gz'])),mode='r:gz') as archive:
            for member in archive:
                parts=PurePosixPath(member.name)
                assert not parts.is_absolute() and '..' not in parts.parts,'Unsafe member path'
                if not member.isfile():continue
                data=archive.extractfile(member).read()
                target=root/parts;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(data)
                assert not member.name.endswith(('.pyc','.pyo')) and '__pycache__' not in parts.parts
                if target.suffix=='.py':
                    ast.parse(data,filename=member.name,feature_version=(3,9));python_files+=1
        plugin=root/PLUGIN;skin=root/'usr/share/enigma2/hd_glass17'
        health=runpy.run_path(str(plugin/'warderInstallHealth.py'))
        assert health['verify_payload'](VERSION,plugin,skin)==VERSION
        status='Package: '+PACKAGE+'\nVersion: '+VERSION+'-1\nStatus: install ok installed\n'
        def installed(*args,**kwargs):return SimpleNamespace(returncode=0,stdout=status)
        assert health['verify_installation'](VERSION,plugin,skin,runner=installed)==VERSION
        assert (plugin/'version').read_text().strip()==VERSION
        for filename in ('history.txt','history.txtSk'):assert (plugin/filename).read_text().startswith('FullHDGlass '+VERSION)
        adapter=runpy.run_path(str(plugin/'warderOpenPli.py'))
        document=ET.parse(skin/'skin.xml').getroot()
        registry={s.get('name'):(s,'/usr/share/enigma2/hd_glass17/') for s in document.findall('screen')}
        channel=registry['ChannelSelection'][0]
        assert channel.find("widget[@source='key_red']") is not None
        assert adapter['install'](registry,'hd_glass17/skin.xml','openpli')>0
        assert registry['ChannelSelection'][0].find("widget[@name='key_red']") is not None
        browser=registry['PluginBrowser'][0]
        assert browser.find("widget[@name='list']") is not None
        assert browser.find("widget[@source='pluginList']") is None
        assert browser.find("widget[@source='pluginGrid']") is None
        assert browser.find("widget[@name='list']").get('itemHeight')=='90'
        keys={w.get('name') or w.get('source') for w in registry['VirtualKeyBoard'][0].iter('widget')}
        assert {'prompt','text','list','locale','key_red','key_green','key_yellow','key_blue'}.issubset(keys)
        # The shared source XML and shipped native image classes remain untouched.
        assert channel.find("widget[@source='key_red']") is not None
        subprocess.run([sys.executable,str(Path(__file__).with_name('test-openpli-crash-regressions.py')),'--upstream',str(upstream),'--package-root',str(root),'-q'],check=True)
        result={'version':VERSION,'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest(),
                'python_payloads_compiled_for_39_grammar':python_files,
                'shipped_postinst_payload_function_passed':True,
                'installed_version_status_fixture_passed':True,
                'packaged_openpli_adapter_and_keyboard_passed':True,
                'packaged_native_plugin_list_present':True,
                'packaged_native_dialog_regressions_passed':True,
                'physical_receiver_verified':False,'production_feeds_changed':False}
        report.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('package',type=Path)
    parser.add_argument('--report',type=Path,required=True)
    parser.add_argument('--upstream',type=Path,required=True)
    args=parser.parse_args();verify(args.package,args.report,args.upstream)
