#!/usr/bin/env python3
"""Prevent repeat opkg remove_obsolesced_files ENOENT on OpenATV Python 3.13."""
from pathlib import Path
import subprocess,tempfile,unittest,re

ROOT=Path(__file__).resolve().parents[1]
PRE=(ROOT/'source/control/preinst').read_text()
POST=(ROOT/'source/control/postinst').read_text()
PRERM=(ROOT/'source/control/prerm').read_text()
PKG='enigma2-plugin-skins-fullhdglass-warder-evolution'
BEGIN='warder_repair_tracked_missing_bytecode() {'
END='if ! warder_repair_tracked_missing_bytecode; then'

class Tests(unittest.TestCase):
    def test_no_late_pycache_unlink_and_all_helper_python_is_B(self):
        self.assertNotIn('rm -f "$warder_bytecode"',POST)
        self.assertNotIn('Invalidate bytecode for package-owned plugin modules',POST)
        self.assertIn('/usr/bin/python3 -B',PRERM)
        self.assertIn('warder_repair_tracked_missing_bytecode',PRE)

    def harness(self,root):
        start=PRE.index(BEGIN)
        end=PRE.index(END,start)
        body=PRE[start:end]
        py='/usr/lib/enigma2/python/Plugins/Extensions/setupGlass17'
        info='/var/lib/opkg/info'
        body=body.replace(py,str(root/'plugindir')).replace(info,str(root/'opkginfo'))
        body=body.replace('/usr/lib/opkg/info',str(root/'secondary-info'))
        return 'WARDER_PACKAGE_ID='+PKG+'\n'+body+'warder_repair_tracked_missing_bytecode\n'

    def test_repair_only_absent_exact_file_list_entries(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d)
            plug=root/'plugindir'
            cache=plug/'__pycache__'
            cache.mkdir(parents=True)
            info=root/'opkginfo'
            info.mkdir()
            missing=cache/'warderRadioWorld.cpython-313.pyc'
            existing=cache/'warderRadioLive.cpython-313.pyc'
            existing.write_bytes(b'original-bytecode')
            untracked=cache/'do_not_create.cpython-313.pyc'
            foreign=root/'untracked.pyc'
            listed='\n'.join([str(missing),str(existing),str(foreign),
                              str(cache/'__import__.cpython-312.pyc')])+'\n'
            (info/(PKG+'.list')).write_text(listed)
            script=self.harness(root)
            check=subprocess.run(['/bin/sh','-eu','-c',script],
                                 capture_output=True,text=True)
            self.assertEqual(check.returncode,0,check.stderr)
            self.assertTrue(missing.is_file())
            self.assertEqual(missing.read_bytes(),b'')
            self.assertEqual(existing.read_bytes(),b'original-bytecode')
            self.assertFalse(untracked.exists())
            self.assertFalse(foreign.exists())
            again=subprocess.run(['/bin/sh','-eu','-c',script],
                                 capture_output=True,text=True)
            self.assertEqual(again.returncode,0,again.stderr)
            self.assertEqual(existing.read_bytes(),b'original-bytecode')

    def test_never_follow_symlinked_cache_or_tracked_file(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d)
            plug=root/'plugindir'
            plug.mkdir()
            external=root/'personal'
            external.mkdir()
            (plug/'__pycache__').symlink_to(external,target_is_directory=True)
            info=root/'opkginfo'
            info.mkdir()
            target=plug/'__pycache__'/'keep.cpython-313.pyc'
            (info/(PKG+'.list')).write_text(str(target)+'\n')
            run=subprocess.run(['/bin/sh','-eu','-c',self.harness(root)],
                               capture_output=True,text=True)
            self.assertNotEqual(run.returncode,0)
            self.assertFalse((external/target.name).exists())

    def test_untracked_names_are_not_manufactured(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d)
            cache=root/'plugindir'/'__pycache__'
            cache.mkdir(parents=True)
            info=root/'opkginfo'
            info.mkdir()
            (info/(PKG+'.list')).write_text(
                 '/usr/lib/enigma2/python/OtherAddon/secret.cpython-313.pyc\n'
                 +str(cache/'danger.pyc')+'\n')
            run=subprocess.run(['/bin/sh','-eu','-c',self.harness(root)],
                               capture_output=True,text=True)
            self.assertEqual(run.returncode,0,run.stderr)
            self.assertEqual(list(cache.iterdir()),[])

if __name__=='__main__':
    unittest.main()
