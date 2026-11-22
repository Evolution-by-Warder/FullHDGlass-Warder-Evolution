#!/usr/bin/env python3
"""Exact TEST-only local 224 radio world and selected broadcaster-logo sources."""
import hashlib,json
from pathlib import Path
import sys,tempfile,unittest
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'source/package-root/usr/lib/enigma2/python'))
from Plugins.Extensions.setupGlass17 import warderRadioLocalTestAssets as kits
from Plugins.Extensions.setupGlass17 import warderRadioWorld as world

class Tests(unittest.TestCase):
    def setUp(self):
        t=tempfile.TemporaryDirectory();self.addCleanup(t.cleanup)
        base=Path(t.name);self.root=base/'hdg17_files';self.root.mkdir()
        self.directory=base/'enigma2';self.directory.mkdir()
        folder=self.root/kits.BASE;folder.mkdir()
        self.worldfile=folder/kits.WORLD_ARCHIVE
        self.worldfile.write_bytes(b'tiny fake pinned 224 world')
        self.logo=folder/'MX.zip'
        self.logo.write_bytes(b'test pinned MX image ZIP')
    def test_local_world_verified_digest_and_exact_224_expected(self):
        digest=hashlib.sha256(self.worldfile.read_bytes()).hexdigest()
        with patch.object(kits,'WORLD_SHA',digest),patch.object(world,'install_world',
              return_value={'changed':True,'countries':224}) as install:
            self.assertEqual(kits.sync_local_world(self.root,False)['countries'],224)
            args,kwargs=install.call_args
            self.assertEqual(args[:3],(self.worldfile,digest,self.root))
            self.assertEqual(kwargs['expected_countries'],224)
        with self.assertRaisesRegex(ValueError,'SHA mismatch'):
            kits.sync_local_world(self.root,False)
    def test_local_logo_sha_and_verified_external_isolation(self):
        expected=hashlib.sha256(self.logo.read_bytes()).hexdigest()
        source=self.root/'radio-world'
        for folder in ('catalog','bouquets','manifests'):
            d=source/folder
            d.mkdir(parents=True,exist_ok=True)
            (d/('MX.'+{'catalog':'json','bouquets':'radio','manifests':'json'}[folder])).write_bytes(
                b'exact signed fixture')
        own=source/world.OWNER
        own.write_text('{}')
        info={'logo_sha256':expected,'logo_package_complete':True}
        with patch.object(kits.world,'_owner_ok',return_value=True),\
             patch.object(kits.world,'_json_file',side_effect=lambda p,maxsize:
                {'archive_sha256':kits.WORLD_SHA} if Path(p).name==world.OWNER else
                {'countries':{'MX':info}}),\
             patch.object(kits.world,'_verify_index',
               return_value={'MX':info}),\
             patch('Plugins.Extensions.setupGlass17.warderRadioBundleFetch._country_really_selected',
               return_value=True),\
             patch.object(kits.packages,'install_logos',
               return_value={'changed':True,'country':'MX','logos':1375}) as install:
            got=kits.sync_local_logos(self.root,self.directory,'MX',False)
            self.assertEqual(got['logos'],1375)
            source_folder=Path(install.call_args.args[0])
            # source folder is removed after the loader returns, so inspect
            # exact flags and destination passed to the verified installer.
            self.assertEqual(install.call_args.args[1],'MX')
            self.assertEqual(install.call_args.args[2],self.root/'picon')
        self.logo.write_bytes(b'tampered')
        with patch.object(kits.world,'_owner_ok',return_value=True),\
             patch.object(kits.world,'_json_file',side_effect=lambda p,maxsize:
                {'archive_sha256':kits.WORLD_SHA} if Path(p).name==world.OWNER else
                {'countries':{'MX':info}}),\
             patch.object(kits.world,'_verify_index',return_value={'MX':info}),\
             patch('Plugins.Extensions.setupGlass17.warderRadioBundleFetch._country_really_selected',
               return_value=True):
            with self.assertRaisesRegex(ValueError,'digest mismatch'):
                kits.sync_local_logos(self.root,self.directory,'MX',False)
    def test_missing_kit_and_changed_country_do_not_write(self):
        self.logo.unlink()
        self.assertEqual(kits.sync_local_logos(self.root,self.directory,'MX',False)['skipped'],
                         'missing-local-country-originals')
        self.assertFalse((self.root/'picon').exists())
        self.assertEqual(kits.sync_local_logos(self.root,self.directory,'../MX',False)['skipped'],
                         'missing-local-test-kit')

if __name__=='__main__':unittest.main()
