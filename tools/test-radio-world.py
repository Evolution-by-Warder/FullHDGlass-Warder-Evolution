#!/usr/bin/env python3
"""Radio Live: verified world ZIP import and local country selection tests."""
from io import BytesIO
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest
from zipfile import ZIP_DEFLATED, ZipFile

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'source/package-root/usr/lib/enigma2/python'))
from Plugins.Extensions.setupGlass17 import warderRadioWorld as world
from Plugins.Extensions.setupGlass17 import warderRadioCountry as country
from Plugins.Extensions.setupGlass17 import warderRadioLive as live
import importlib.util
_fixture = ROOT / 'tools/test-radio-packages.py'
_spec = importlib.util.spec_from_file_location('world_country_package_fixtures', _fixture)
_fixtures = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_fixtures)
example = _fixtures.example


def snapshot(root, codes=('ET','FR')):
    base=root/'source'
    index={'schema':1,'source':'WarderRadio.RadioBrowser',
           'countries':{},'country_count':len(codes),'station_count':0}
    for code in codes:
        name={'ET':'Ethiopia','FR':'France','DE':'Deutschland'}[code]
        rows,meta=example(base,code,name,size=3)
        index['countries'][code]={
            'name':name,'stations':len(rows),
            'bouquet_sha256':meta['files'][f'bouquets/{code}.radio']['sha256'],
            'catalog_sha256':meta['files'][f'catalog/{code}.json']['sha256'],
            'logo_sha256':meta['files'][f'logos/{code}.zip']['sha256'],
            'logo_package_complete':True,'logos_found':3}
        index['station_count']+=len(rows)
    raw=BytesIO()
    with ZipFile(raw,'w',compression=ZIP_DEFLATED) as archive:
        archive.writestr('index.json',json.dumps(index))
        for code in codes:
            for cat,suffix in [('bouquets','radio'),('catalog','json'),('manifests','json')]:
                rel=f'{cat}/{code}.{suffix}'
                archive.writestr(rel,(base/rel).read_bytes())
    data=raw.getvalue()
    p=root/'world-bouquets.zip'
    p.write_bytes(data)
    return p,hashlib.sha256(data).hexdigest()


class Tests(unittest.TestCase):
    def setUp(self):
        t=tempfile.TemporaryDirectory()
        self.addCleanup(t.cleanup)
        self.root=Path(t.name)
        self.paths=self.root/'hdg17_files'
        self.paths.mkdir()
        (self.paths/'picon').mkdir()
        self.etc=self.root/'enigma2'
        self.etc.mkdir()
        (self.etc/'settings').write_text('config.osd.language=fr_FR\n')
        (self.etc/'bouquets.radio').write_bytes(
            b'#NAME Bouquets (Radio)\n'
            b'#SERVICE 1:7:2:0:0:0:0:0:0:0:FROM BOUQUET "userbouquet.personal.radio" ORDER BY bouquet\n')
        self.archive,self.digest=snapshot(self.root)

    def test_install_full_world_and_activate_fr_locally(self):
        res=world.install_world(self.archive,self.digest,self.paths,False)
        self.assertTrue(res['changed'])
        self.assertEqual(res['countries'],2)
        self.assertEqual(res['stations'],6)
        self.assertEqual(world.install_world(self.archive,self.digest,self.paths,False)['skipped'],
                         'already-current')
        country.bootstrap(self.etc)
        before=(self.etc/'bouquets.radio').read_bytes()
        result=world.activate_from_world(self.paths,'FR',self.etc)
        self.assertEqual(result['country'],'FR')
        self.assertTrue(result['local'])
        self.assertEqual(country.diagnose(self.etc)['active'],'FR')
        self.assertEqual(country.diagnose(self.etc)['visible_country_sections'],['France'])
        self.assertEqual((self.etc/'bouquets.radio').read_bytes().count(
            b'userbouquet.personal.radio'),1)
        self.assertEqual(before.count(b'userbouquet.personal.radio'),1)
        self.assertFalse(any(self.paths.glob('picon/radio/*')))

    def test_country_logo_must_have_exact_service_identity(self):
        from Plugins.Extensions.setupGlass17 import warderRadioPackages as packs
        source=self.root/'radio-artifacts'
        foreign=live.service_stem('aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa')+'.png'
        example(source,'FR','France',size=3,zip_name=foreign)
        with self.assertRaisesRegex(ValueError,'Unsafe logo ZIP member'):
            packs.install_logos(source,'FR',self.paths/'picon',
                               require_external=False)
        self.assertFalse((self.paths/'picon/radio').exists())

    def test_world_checksum_mismatch_never_modifies_cache(self):
        with self.assertRaisesRegex(ValueError,'SHA-256 mismatch'):
            world.install_world(self.archive,'0'*64,self.paths,False)
        self.assertFalse((self.paths/'radio-world').exists())

    def test_unknown_world_member_rejected_before_install(self):
        raw=BytesIO()
        with ZipFile(self.archive) as original, ZipFile(raw,'w') as dest:
            for item in original.infolist():
                dest.writestr(item.filename,original.read(item.filename))
            dest.writestr('picon/TV.png',b'foreign')
        modified=self.root/'malicious.zip'
        modified.write_bytes(raw.getvalue())
        with self.assertRaisesRegex(ValueError,'foreign'):
            world.install_world(modified,hashlib.sha256(modified.read_bytes()).hexdigest(),
                                self.paths,False)
        self.assertFalse((self.paths/'radio-world').exists())

    def test_ownership_guard_prevents_removing_user_modified_file(self):
        world.install_world(self.archive,self.digest,self.paths,False)
        target=self.paths/'radio-world/bouquets/FR.radio'
        target.write_bytes(b'user changed')
        fresh,digest=snapshot(self.root,('ET','DE'))
        self.assertEqual(world.install_world(fresh,digest,self.paths,False)['skipped'],
                         'unowned-world-folder')
        self.assertEqual(target.read_bytes(),b'user changed')

    def test_unowned_radio_world_folder_never_deleted(self):
        folder=self.paths/'radio-world'
        folder.mkdir()
        (folder/'my_favourite.txt').write_bytes(b'mine')
        self.assertEqual(world.install_world(self.archive,self.digest,self.paths,False)['skipped'],
                         'unowned-world-folder')
        self.assertEqual((folder/'my_favourite.txt').read_bytes(),b'mine')

    def test_new_world_revision_replaces_owned_cache_not_other_picons(self):
        world.install_world(self.archive,self.digest,self.paths,False)
        (self.paths/'picon/TV.png').write_bytes(b'tv-unmodified')
        next_archive,next_sha=snapshot(self.root,('ET','DE'))
        result=world.install_world(next_archive,next_sha,self.paths,False)
        self.assertEqual(result['countries'],2)
        self.assertFalse((self.paths/'radio-world/bouquets/FR.radio').exists())
        self.assertTrue((self.paths/'radio-world/bouquets/DE.radio').is_file())
        self.assertEqual((self.paths/'picon/TV.png').read_bytes(),b'tv-unmodified')
        self.assertEqual(world.activate_from_world(self.paths,'DE',self.etc)['country'],'DE')

    def test_diagnostics_verify_only_active_country_logo_ownership(self):
        from Plugins.Extensions.setupGlass17 import warderRadioPackages as packs
        world.install_world(self.archive, self.digest, self.paths, False)
        country.bootstrap(self.etc)
        world.activate_from_world(self.paths, 'FR', self.etc)
        source = self.root / 'source'
        result = packs.install_country_logos(
            source, 'FR', self.paths / 'picon', require_external=False)
        self.assertTrue(result['changed'])
        # A second independent country must not change the active report.
        packs.install_country_logos(
            source, 'ET', self.paths / 'picon', require_external=False)
        report = world.diagnose(self.paths, self.etc)
        self.assertTrue(report['world_owned_integrity_valid'])
        self.assertTrue(report['radio_picons_owned_integrity_valid'])
        self.assertEqual(report['radio_logo_country'], 'FR')
        self.assertEqual(report['radio_png_count'], 3)
        # User-edited artwork cannot be silently reported as trusted.
        logo = next((self.paths / 'picon' / 'radio' / 'FR').glob('*.png'))
        logo.write_bytes(b'user modified logo')
        self.assertFalse(world.diagnose(
            self.paths, self.etc)['radio_picons_owned_integrity_valid'])

    def test_external_mount_required_in_production(self):
        report=world.install_world(self.archive,self.digest,self.paths)
        self.assertEqual(report['skipped'],'unsafe-storage')
        self.assertFalse((self.paths/'radio-world').exists())

    def test_missing_cached_country_fails_closed(self):
        world.install_world(self.archive,self.digest,self.paths,False)
        with self.assertRaises(ValueError):
            world.activate_from_world(self.paths,'DE',self.etc)

    def test_existing_world_path_symlink_is_not_followed(self):
        real=self.root/'personal'
        real.mkdir()
        (real/'keep.txt').write_text('never delete')
        (self.paths/'radio-world').symlink_to(real)
        self.assertEqual(world.install_world(self.archive,self.digest,self.paths,False)['skipped'],
                         'unowned-world-folder')
        self.assertEqual((real/'keep.txt').read_text(),'never delete')


if __name__=='__main__':
    unittest.main(verbosity=2)
