#!/usr/bin/env python3
"""Exercise real opkg ordering with minimal fixtures and real legacy hooks.

All opkg calls have an isolated offline root. Every maintainer hook is guarded
by PKG_ROOT and all absolute receiver paths are rewritten into that root.
No real product IPK is built, published or installed on a receiver.
"""
import argparse
import ast
import gzip
import hashlib
import io
import json
import os
from pathlib import Path
import shlex
import subprocess
import tarfile
import tempfile

ROOT = Path(__file__).resolve().parents[1]


def controls(path):
    raw = Path(path).read_bytes()
    if raw.startswith(b'!<arch>\n'):
        pos = 8
        while pos + 60 <= len(raw):
            header = raw[pos:pos+60]
            name = header[:16].decode().strip().rstrip('/')
            size = int(header[48:58])
            value = raw[pos+60:pos+60+size]
            pos += 60 + size + size % 2
            if name.startswith('control.tar'):
                break
        else:
            raise ValueError('No control archive')
    else:
        with tarfile.open(fileobj=io.BytesIO(raw), mode='r:*') as outer:
            member = next(m for m in outer if m.name.lstrip('./').startswith('control.tar'))
            value = outer.extractfile(member).read()
    with tarfile.open(fileobj=io.BytesIO(value), mode='r:*') as archive:
        return {m.name.lstrip('./'): archive.extractfile(m).read().decode()
                for m in archive if m.isfile()}


def tar(entries):
    output = io.BytesIO()
    with tarfile.open(fileobj=output, mode='w', format=tarfile.GNU_FORMAT) as archive:
        for name, data, mode in entries:
            info = tarfile.TarInfo('./' + name)
            info.mode, info.mtime, info.size = mode, 0, len(data)
            archive.addfile(info, io.BytesIO(data))
    return gzip.compress(output.getvalue(), mtime=0)


def fixture(path, control, hooks, files):
    entries = [('debian-binary', b'2.0\n'),
               ('control.tar.gz', tar([('control', control.encode(), 0o644)] +
                                     [(n, s.encode(), 0o755) for n, s in hooks.items()])),
               ('data.tar.gz', tar([(n, v.encode(), 0o644) for n, v in files.items()]))]
    result = bytearray(b'!<arch>\n')
    for name, data in entries:
        result += ('%-16s%-12s%-6s%-6s%-8s%-10s`\n' %
                   (name+'/', 0, 0, 0, '100644', len(data))).encode()
        result += data + (b'\n' if len(data) % 2 else b'')
    path.write_bytes(result)


def guarded(source, root, label):
    import re
    # One pass: do not process inserted /tmp prefixes a second time.
    source = re.sub(r'/(?:etc|usr|var|tmp)/', lambda m: str(root) + m[0], source)
    # Offline-root .list entries retain receiver paths, whereas rewritten
    # fixture hooks operate on host paths inside PKG_ROOT.
    source = source.replace('-v path="$warder_obsolete"',
                            '-v path="${warder_obsolete#${PKG_ROOT%/}}"')
    prefix = ('#!/bin/sh\ncase "$PKG_ROOT" in ' + shlex.quote(str(root)) +
              '|' + shlex.quote(str(root)+'/') + ') ;; *) exit 73 ;; esac\n' +
              'printf "%s\\n" ' + shlex.quote(label) + '" $*" >> ' + shlex.quote(str(root/'hook-order')) + '\n')
    return prefix + source


def literal_hook(path, variable):
    tree = ast.parse(Path(path).read_text())
    return next(n.value.value for n in ast.walk(tree)
                if isinstance(n, ast.Assign) and isinstance(n.value, ast.Constant)
                and any(isinstance(t, ast.Name) and t.id == variable for t in n.targets))


def run_case(args, product, force, parent):
    root = parent / (product + ('-force' if force else '-normal'))
    root.mkdir()
    (root/'tmp').mkdir()
    (root/'usr/share/enigma2/skin_default').mkdir(parents=True)
    (root/'usr/share/enigma2/skin_default/skin.xml').write_text('<skin><parameters/></skin>')
    (root/'etc/enigma2').mkdir(parents=True)
    settings = root/'etc/enigma2/settings'
    settings.write_text('config.skin.primary_skin=hd_glass17/skin.xml\ncustom=preserve\n')
    before_settings = settings.read_bytes()
    config = root/'opkg.conf'
    config.write_text('dest root /\narch all 100\noption check_signature 0\n')
    command = [str(args.opkg), '-o', str(root), '-f', str(config),
               '-t', str(root/'tmp'), '--force-postinstall']
    bindir = root/'bin'
    bindir.mkdir()
    wrapper = bindir/'opkg'
    wrapper.write_text('#!/bin/sh\nexec ' + shlex.join(command) + ' "$@"\n')
    wrapper.chmod(0o755)
    env = dict(os.environ, PATH=str(bindir)+':'+os.environ['PATH'], D='')
    if product == 'skin':
        old = controls(args.legacy_skin)
        new_control = (ROOT/'source/control/control').read_text()
        new_preinst = args.preinst.read_text() if args.preinst else (ROOT/'source/control/preinst').read_text()
        legacy_files = {'usr/share/enigma2/hd_glass17/skin.xml': '<skin>old</skin>',
                        'usr/lib/enigma2/python/Plugins/Extensions/setupGlass17/plugin.py': '# old\n'}
        new_files = {'usr/share/enigma2/hd_glass17/skin.xml': '<skin>new</skin>',
                     'usr/lib/enigma2/python/Plugins/Extensions/setupGlass17/plugin.py': '# new\n',
                     'usr/lib/enigma2/python/Plugins/Extensions/setupGlass17/version': '1.0.49\n'}
        legacy_id = 'enigma2-skin-fullhdglass17'
        current_id = 'enigma2-plugin-skins-fullhdglass-warder-evolution'
        critical = 'usr/share/enigma2/hd_glass17/skin.xml'
    else:
        old = controls(args.legacy_picons)
        builder = args.picon_root/'plugin/tools/build_ipk.py'
        new_preinst = literal_hook(builder, 'preinst')
        current_id = 'enigma2-plugin-extensions-piconhub-warder-evolution'
        legacy_id = 'enigma2-plugin-extensions-chocholousek-picons'
        new_control = ('Package: '+current_id+'\nVersion: 0.1.33\nArchitecture: all\n' +
                       'Conflicts: '+legacy_id+'\nReplaces: '+legacy_id+'\n')
        legacy_files = {'usr/lib/enigma2/python/Plugins/Extensions/ChocholousekPicons/plugin.py': '# old\n',
                        'usr/lib/enigma2/python/Plugins/Extensions/ChocholousekPicons/version.txt': '5.0.240904\n'}
        new_files = {'usr/lib/enigma2/python/Plugins/Extensions/WarderPiconHub/plugin.py': '# new\n',
                     'usr/lib/enigma2/python/Plugins/Extensions/WarderPiconHub/version.txt': '0.1.33\n',
                     'usr/lib/enigma2/python/Plugins/Extensions/ChocholousekPicons/version.txt': '0.1.33\n'}
        critical = 'usr/lib/enigma2/python/Plugins/Extensions/WarderPiconHub/plugin.py'
    old_control = '\n'.join(l for l in old['control'].splitlines() if not l.startswith('Depends:'))+'\n'
    old_hooks = {n: guarded(old[n], root, 'old-'+n) for n in ('prerm', 'postrm') if n in old}
    self_deleted = []
    if product == 'skin' and args.legacy_self_deleted:
        # The original postinst removes both shipped entries, while opkg still
        # owns them. Model exactly that side effect, not the entire old runtime.
        assert 'rm -rf /tmp/plugin-17.py' in old['postinst']
        assert 'rm -rf $SCREENPATH/Menu-new17-38.py' in old['postinst']
        self_deleted = ['tmp/plugin-17.py',
                        'usr/lib/enigma2/python/Screens/Menu-new17-38.py']
        legacy_files.update({name: '# legacy temporary payload\n' for name in self_deleted})
        old_hooks['postinst'] = guarded(
            'rm -f /tmp/plugin-17.py /usr/lib/enigma2/python/Screens/Menu-new17-38.py\n',
            root, 'old-postinst')
    # The test guard and rewritten paths necessarily change the old hook hash.
    # Substitute its fixture hash only in the test copy of the new preinst.
    # The production allowlist retains the untouched original hook's hash.
    if product == 'skin':
        new_preinst = new_preinst.replace(hashlib.sha256(old['postrm'].encode()).hexdigest(),
                                        hashlib.sha256(old_hooks['postrm'].encode()).hexdigest())
        guard = '#!/bin/sh\n# FullHDGlass verified legacy upgrade guard v1\ncase "${1:-}" in upgrade|failed-upgrade|abort-upgrade|disappear) exit 0 ;; esac\n'
        new_preinst = new_preinst.replace(hashlib.sha256((guard+old['postrm']).encode()).hexdigest(),
                                        hashlib.sha256((guard+old_hooks['postrm']).encode()).hexdigest())
    new_hooks = {'preinst': guarded(new_preinst, root, 'new-preinst'),
                 'postinst': guarded('exit 0\n', root, 'new-postinst')}
    first, second = root/'old-fixture.ipk', root/'new-fixture.ipk'
    fixture(first, old_control, old_hooks, legacy_files)
    fixture(second, new_control, new_hooks, new_files)
    def call(argv):
        result = subprocess.run(command+argv, env=env, text=True, stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT, timeout=40)
        return {'exit_code': result.returncode, 'output': result.stdout}
    install_old = call(['install', str(first)])
    if install_old['exit_code']:
        raise RuntimeError('Fixture setup failed: '+install_old['output'])
    if self_deleted:
        assert all(not (root/name).exists() for name in self_deleted)
        listing=root/'var/lib/opkg/info'/str(legacy_id+'.list')
        tracked = {line.split('\t')[0] for line in listing.read_text().splitlines()}
        assert all('/'+name in tracked for name in self_deleted)
    if args.transition_manifest and product == 'skin':
        manifest=root/'var/lib/fullhdglass17/package-transition-v1/manifest.json'
        manifest.parent.mkdir(parents=True,exist_ok=True)
        manifest.write_text('{}\n')
    result = call((['--force-reinstall', '--force-overwrite'] if force else []) + ['install', str(second)])
    trace = (root/'hook-order').read_text().splitlines() if (root/'hook-order').exists() else []
    status_new, status_old = call(['status', current_id]), call(['status', legacy_id])
    critical_exists = (root/critical).is_file()
    critical_matches = critical_exists and (root/critical).read_text() == new_files[critical]
    recovery = None
    if result['exit_code']:
        recovery_result = call(['--force-reinstall', 'install', str(second)])
        recovery = {'install': recovery_result, 'status_new': call(['status', current_id]),
                    'critical_matches_new': (root/critical).is_file() and (root/critical).read_text() == new_files[critical]}
    return {'product': product, 'force_reinstall_and_overwrite': force,
            'new_install': result, 'hook_order': trace,
            'new_critical_file_exists': critical_exists,
            'new_critical_file_matches': critical_matches,
            'settings_unchanged': settings.read_bytes() == before_settings,
            'status_new': status_new, 'status_old': status_old, 'second_attempt_recovery': recovery,
            'legacy_tracked_but_self_deleted': self_deleted,
            'transition_manifest_present': bool(args.transition_manifest and product == 'skin'),
            'obsolete_removal_errors': result['output'].count('unlinking ') + result['output'].count('Failed to determine obsolete files'),
            'scope': 'Real opkg; minimal synthetic data and inert new postinst; actual rewritten preinst/legacy postrm. Not a full product or receiver install.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--opkg', type=Path, required=True)
    parser.add_argument('--legacy-skin', type=Path, required=True)
    parser.add_argument('--legacy-picons', type=Path, required=True)
    parser.add_argument('--picon-root', type=Path, required=True)
    parser.add_argument('--preinst', type=Path, help='Optional original preinst for before/after comparison')
    parser.add_argument('--legacy-self-deleted', action='store_true',
                        help='Model original postinst deletion of two still-tracked payload entries')
    parser.add_argument('--transition-manifest', action='store_true',
                        help='Model retained transition metadata from an earlier installation')
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    version = subprocess.check_output([str(args.opkg), '--version'], text=True).strip()
    with tempfile.TemporaryDirectory(prefix='warder-opkg-order-') as folder:
        results = [run_case(args, product, force, Path(folder))
                   for product in ('skin', 'picons') for force in (False, True)]
    report = {'schema': 1, 'date': '2026-10-31', 'opkg_version': version,
              'source_inputs': {str(p): hashlib.sha256(p.read_bytes()).hexdigest()
                                for p in (args.legacy_skin, args.legacy_picons)},
              'cases': results, 'receiver_modified': False, 'published_ipk_created': False}
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n')
    for case in results:
        print(case['product'], 'force='+str(case['force_reinstall_and_overwrite']),
              'exit='+str(case['new_install']['exit_code']),
              'critical='+str(case['new_critical_file_exists']), case['hook_order'])


if __name__ == '__main__':
    main()
