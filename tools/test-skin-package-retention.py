import importlib.util
from pathlib import Path
import unittest

spec=importlib.util.spec_from_file_location('retention',Path(__file__).with_name('prune-stale-skin-packages.py'))
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
def path(version):return 'packages/enigma2-plugin-skins-fullhdglass_'+version+'_all.ipk'
def feed(version,location=None):return {'version':version,'package_url':m.p.RAW+(location or path(version).removeprefix('packages/'))}

class RetentionTests(unittest.TestCase):
    def test_current_previous_and_migration_aliases_and_checksums_are_protected(self):
        names={path(v) for v in ('1.0.18','1.0.41','1.0.42','1.0.43')}
        names|={n+'.sha256' for n in names};names.add(path('1.0.43').replace('fullhdglass_','fullhdglass-warder-evolution_'))
        removed,versions=m.retention(names,[feed('1.0.43'),feed('1.0.43'),feed('1.0.18')],'1.0.43','1.0.42')
        self.assertEqual(set(removed),{path('1.0.41'),path('1.0.41')+'.sha256'})
        self.assertEqual(versions,{'1.0.18','1.0.42','1.0.43'})
    def test_unreferenced_test_packages_are_removed_but_active_test_feed_is_protected(self):
        active='test/'+path('1.0.43').split('/')[-1]
        unused='packages/test/enigma2-skin-fullhdglass17-warder-evolution_1.0.5-test1_all.ipk'
        removed,_=m.retention({'packages/'+active,unused},[feed('1.0.43',active)],'1.0.43','1.0.42')
        self.assertEqual(removed,[unused])
    def test_missing_or_external_active_packages_abort(self):
        for feeds in ([feed('1.0.43')],[{'version':'1.0.43','package_url':'https://attacker.invalid/package.ipk'}]):
            with self.assertRaises(AssertionError):m.retention(set(),feeds,'1.0.43','1.0.42')
    def test_unrelated_archives_or_foreign_packages_are_untouched(self):
        names={path('1.0.43'),'assets/help.zip','packages/unrelated_1.0.1_all.ipk'}
        removed,_=m.retention(names,[feed('1.0.43')],'1.0.43','1.0.42');self.assertEqual(removed,[])
    def test_release_retention_keeps_active_future_and_auxiliary_releases(self):
        def release(v,assets=None):return {'tag_name':'v'+v,'assets':assets if assets is not None else [{'name':path(v).split('/')[-1]}]}
        releases=[release('1.0.18'),release('1.0.41'),release('1.0.42'),release('1.0.43'),release('1.0.44'),release('1.0.23',[{'name':'help.zip'}])]
        self.assertEqual(m.obsolete_releases(releases,{'1.0.18','1.0.42','1.0.43'},'1.0.43'),[releases[1]])

if __name__=='__main__':unittest.main()
