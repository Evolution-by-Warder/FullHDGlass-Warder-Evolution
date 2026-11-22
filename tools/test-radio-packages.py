#!/usr/bin/env python3
"""Offline regression for fast signed country snapshots and isolated radio picons."""
import hashlib
from io import BytesIO
import json
from pathlib import Path
import sys
import tempfile
import unittest
from zipfile import ZipFile, ZIP_STORED

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'source/package-root/usr/lib/enigma2/python'))
from Plugins.Extensions.setupGlass17 import warderRadioPackages as pkg
from Plugins.Extensions.setupGlass17 import warderRadioCountry as country
from Plugins.Extensions.setupGlass17 import warderRadioLive as live

PNG = b'\x89PNG\r\n\x1a\n' + b'original-radio-plugin-png'

def example(root, code, name, size=3, zip_name=None, partial=False):
    rows = []
    for i in range(size):
        uuid = '12345678-1234-1234-1234-%012x' % (i+(1000 if code == 'DE' else 0))
        rows.append({'stationuuid': uuid, 'countrycode': code,
                     'stem': live.service_stem(uuid),
                     'name': '%s Radio %d' % (name, i),
                     'url': 'https://example.org/%s/%d' % (code, i),
                     'favicon': 'https://example.org/logo.png',
                     'homepage': 'https://example.org'})
    raw = live._bouquet([(name, rows)])
    listing = json.dumps({'schema':1,'country':code,'name':name,'stations':rows,
                          'catalogue_complete':not partial},
                         ensure_ascii=False,separators=(',',':')).encode()
    z = BytesIO()
    with ZipFile(z,mode='w',compression=ZIP_STORED) as archive:
        if zip_name:
            archive.writestr(zip_name, PNG)
            count = 1
        else:
            for item in rows:
                archive.writestr(item['stem']+'.png',PNG)
            count = len(rows)
    entries = {'bouquets/'+code+'.radio':raw, 'catalog/'+code+'.json':listing,
               'logos/'+code+'.zip':z.getvalue()}
    manifest = {'country':code,'name':name,'stations':len(rows),
                'catalogue_complete':not partial,'logo_package_complete':True,
                'logos_found':count,'files':{}}
    for rel, content in entries.items():
        dest = root/rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(content)
        manifest['files'][rel]={'bytes':len(content),
                                'sha256':hashlib.sha256(content).hexdigest()}
    target=root/'manifests'/f'{code}.json'
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(manifest), encoding='utf-8')
    return rows, manifest

class RadioBundleTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.packages = self.root/'bundles'
        self.packages.mkdir()
        self.etc = self.root/'enigma2'
        self.etc.mkdir()
        (self.etc/'settings').write_text('config.osd.language=sk_SK\n')
        self.index=self.etc/'bouquets.radio'
        self.index.write_bytes(b'#NAME Bouquets (Radio)\n'
            b'#SERVICE 1:7:2:0:0:0:0:0:0:0:FROM BOUQUET "userbouquet.personal.radio" ORDER BY bouquet\n')
        self.picons=self.root/'hdg17_files'/'picon'
        self.picons.mkdir(parents=True)
        example(self.packages,'FR','France')

    def test_read_exact_signed_country_bouquet(self):
        raw, source, manifest = pkg.verified_country(self.packages,'FR')
        self.assertEqual(raw,(self.packages/'bouquets/FR.radio').read_bytes())
        self.assertIn(b'"stations":',source)
        self.assertEqual(manifest['stations'],3)

    def test_signed_140_character_name_with_terminal_space_is_safe(self):
        rows,manifest=example(self.packages,'DE','Deutschland',size=2)
        rows[0]['name']='X'*139+' '
        raw=live._bouquet([('Deutschland',rows)])
        catalog_path=self.packages/'catalog/DE.json'
        country_file=self.packages/'bouquets/DE.radio'
        catalog={'schema':1,'country':'DE','name':'Deutschland',
                 'stations':rows,'catalogue_complete':True}
        payload=json.dumps(catalog,ensure_ascii=False,separators=(',',':')).encode()
        country_file.write_bytes(raw)
        catalog_path.write_bytes(payload)
        for name,data in [('bouquets/DE.radio',raw),('catalog/DE.json',payload)]:
            manifest['files'][name]={'sha256':hashlib.sha256(data).hexdigest(),
                                      'bytes':len(data)}
        (self.packages/'manifests/DE.json').write_text(json.dumps(manifest))
        checked,_,_=pkg.verified_country(self.packages,'DE')
        self.assertEqual(checked,raw)
        # A renamed or internally spaced station must still be rejected,
        # even if a local test fixture updates its manifest checksums.
        rows[0]['name']='X  Y'
        raw=live._bouquet([('Deutschland',rows)])
        catalog['stations']=rows
        payload=json.dumps(catalog,ensure_ascii=False,separators=(',',':')).encode()
        country_file.write_bytes(raw)
        catalog_path.write_bytes(payload)
        for name,data in [('bouquets/DE.radio',raw),('catalog/DE.json',payload)]:
            manifest['files'][name]={'sha256':hashlib.sha256(data).hexdigest(),
                                      'bytes':len(data)}
        (self.packages/'manifests/DE.json').write_text(json.dumps(manifest))
        with self.assertRaisesRegex(ValueError,'Unsafe station row'):
            pkg.verified_country(self.packages,'DE')

    def test_select_local_country_without_network_or_other_bouquet_changes(self):
        country.bootstrap(self.etc)
        personal=self.index.read_bytes()
        old_bouquet=(self.etc/live.FILE).read_bytes()
        result=pkg.activate_local(self.packages,'FR',self.etc)
        self.assertTrue(result['changed'])
        self.assertEqual(result['country'],'FR')
        self.assertEqual(result['stations'],3)
        self.assertNotEqual((self.etc/live.FILE).read_bytes(),old_bouquet)
        self.assertEqual(country.diagnose(self.etc)['active'],'FR')
        self.assertEqual(country.diagnose(self.etc)['visible_country_sections'],['France'])
        self.assertIsNone(country.diagnose(self.etc)['pending'])
        self.assertIn(b'userbouquet.personal.radio',self.index.read_bytes())
        self.assertEqual(personal.count(b'userbouquet.personal.radio'),1)

    def test_tampered_manifest_checksum_does_not_replace_bouquet(self):
        country.bootstrap(self.etc)
        original=(self.etc/live.FILE).read_bytes()
        (self.packages/'bouquets/FR.radio').write_bytes(b'bad data')
        with self.assertRaisesRegex(ValueError,'SHA-256 mismatch'):
            pkg.activate_local(self.packages,'FR',self.etc)
        self.assertEqual((self.etc/live.FILE).read_bytes(),original)

    def test_incomplete_sample_cannot_be_activated(self):
        example(self.packages,'ET','Ethiopia',partial=True)
        with self.assertRaisesRegex(ValueError,'Incomplete'):
            pkg.verified_country(self.packages,'ET')

    def test_first_logo_import_and_safe_switch_to_second_country(self):
        first=pkg.install_logos(self.packages,'FR',self.picons,require_external=False)
        self.assertTrue(first['changed'])
        self.assertEqual(first['logos'],3)
        fr_png=list((self.picons/'radio').glob('*.png'))
        self.assertEqual(len(fr_png),3)
        unrelated=(self.picons/'satellite.png')
        unrelated.write_bytes(b'untouched')
        example(self.packages,'DE','Deutschland',2)
        second=pkg.install_logos(self.packages,'DE',self.picons,require_external=False)
        self.assertEqual(second['country'],'DE')
        self.assertEqual(second['logos'],2)
        self.assertEqual(len(list((self.picons/'radio').glob('*.png'))),2)
        self.assertFalse(any(p.exists() for p in fr_png))
        self.assertEqual(unrelated.read_bytes(),b'untouched')

    def test_country_changed_during_extraction_preserves_previous_pngs(self):
        first=pkg.install_logos(self.packages,'FR',self.picons,
                                require_external=False)
        self.assertEqual(first['logos'],3)
        prior={p.name:p.read_bytes() for p in (self.picons/'radio').glob('*.png')}
        example(self.packages,'DE','Deutschland',size=2)
        result=pkg.install_logos(self.packages,'DE',self.picons,
                                 require_external=False,
                                 still_selected=lambda code: False)
        self.assertEqual(result['skipped'],'country-superseded')
        self.assertFalse(result['changed'])
        self.assertEqual({p.name:p.read_bytes() for p in
                          (self.picons/'radio').glob('*.png')},prior)
        allowed=pkg.install_logos(self.packages,'DE',self.picons,
                                  require_external=False,
                                  still_selected=lambda code: code=='DE')
        self.assertTrue(allowed['changed'])
        self.assertEqual(allowed['logos'],2)

    def test_unsafe_storage_never_touches_internal_flash(self):
        result=pkg.install_logos(self.packages,'FR',self.picons)
        self.assertEqual(result['skipped'],'unsafe-storage')
        self.assertFalse((self.picons/'radio').exists())

    def test_user_owned_radio_folder_is_not_deleted(self):
        folder=self.picons/'radio'
        folder.mkdir()
        (folder/'mylogo.png').write_bytes(b'user')
        result=pkg.install_logos(self.packages,'FR',self.picons,require_external=False)
        self.assertEqual(result['skipped'],'unowned-radio-folder')
        self.assertEqual((folder/'mylogo.png').read_bytes(),b'user')

    def test_modified_owned_picon_protects_whole_folder(self):
        pkg.install_logos(self.packages,'FR',self.picons,require_external=False)
        old=next((self.picons/'radio').glob('*.png'))
        old.write_bytes(b'user-replacement')
        example(self.packages,'DE','Deutschland',2)
        result=pkg.install_logos(self.packages,'DE',self.picons,require_external=False)
        self.assertEqual(result['skipped'],'unowned-radio-folder')
        self.assertEqual(old.read_bytes(),b'user-replacement')

    def test_zip_path_traversal_is_rejected_before_replacement(self):
        example(self.packages,'FR','France',zip_name='../escape.png')
        with self.assertRaisesRegex(ValueError,'Unsafe logo ZIP member'):
            pkg.install_logos(self.packages,'FR',self.picons,require_external=False)
        self.assertFalse((self.root/'escape.png').exists())
        self.assertFalse((self.picons/'radio').exists())

    def test_country_manifest_symlink_refused(self):
        folder=self.packages/'catalog'
        target=self.packages/'catalog/FR.json'
        target.unlink()
        target.symlink_to(self.etc/'settings')
        with self.assertRaisesRegex(ValueError,'Symlink'):
            pkg.verified_country(self.packages,'FR')

if __name__=='__main__':
    unittest.main(verbosity=2)
