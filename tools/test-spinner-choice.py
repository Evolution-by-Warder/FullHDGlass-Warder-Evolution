#!/usr/bin/env python3
"""Exercise native frame sets, user-file protection, rollback and saved selection."""
import ast
import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path
import shutil
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch
import zipfile

from PIL import Image, ImageChops

ROOT = Path(__file__).resolve().parents[1]
SKIN = ROOT / 'source/package-root/usr/share/enigma2/hd_glass17'
PLUGIN = ROOT / 'source/package-root/usr/lib/enigma2/python/Plugins/Extensions/setupGlass17'


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


spinner = load('spinner_choice_test', PLUGIN / 'warderSpinner.py')
DATA = spinner.catalog()


def content(folder):
    return {path.name: path.read_bytes() for path in folder.iterdir() if path.is_file()}


class AssetTests(unittest.TestCase):
    def test_exact_original_dove_is_retained_and_each_theme_is_pinned(self):
        approved = json.loads((ROOT / 'design/spinner-repair/production.json').read_text())
        self.assertEqual(len(DATA['themes']['dove']['frames']), 18)
        self.assertEqual(len(DATA['themes']['bakussa']['frames']), 20)
        for theme_id, theme in DATA['themes'].items():
            folder = SKIN / 'spinner-themes' / theme_id
            self.assertEqual(set(content(folder)), {entry['name'] for entry in theme['frames']})
            for entry in theme['frames']:
                raw = (folder / entry['name']).read_bytes()
                self.assertEqual(hashlib.sha256(raw).hexdigest(), entry['sha256'])
                with Image.open(io.BytesIO(raw)) as image:
                    self.assertEqual(image.mode, 'RGBA')
                    self.assertEqual(list(image.size), theme['size'])
                    self.assertLess(image.width * image.height * 4, 48000)
                    self.assertEqual(image.getchannel('A').getextrema()[0], 0)
        for entry in approved['assets']:
            self.assertEqual(hashlib.sha256((SKIN / 'spinner-themes/dove' / Path(entry['path']).name).read_bytes()).hexdigest(), entry['sha256'])

    def test_submitted_artwork_frame_order_and_transparency_are_preserved(self):
        source = ROOT / 'assets/warder/downloads/ui/spinners/bakussa-original.zip'
        self.assertEqual(hashlib.sha256(source.read_bytes()).hexdigest(), DATA['themes']['bakussa']['source_sha256'])
        with zipfile.ZipFile(source) as archive:
            for index in range(1, 21):
                name = 'wait%d.png' % index
                original = Image.open(io.BytesIO(archive.read('HG glass17 spinner  (bakussa)/' + name)))
                expected = original.convert('RGBa').resize((104, 104), Image.Resampling.LANCZOS).convert('RGBA')
                actual = Image.open(SKIN / 'spinner-themes/bakussa' / name)
                self.assertEqual(actual.tobytes(), expected.tobytes())

    def test_package_png_optimizer_keeps_runtime_hash_verification_valid(self):
        optimizer = load('spinner_package_optimizer', ROOT / 'tools/optimize-png.py')
        for theme_id, theme in DATA['themes'].items():
            for entry in theme['frames']:
                raw = (SKIN / 'spinner-themes' / theme_id / entry['name']).read_bytes()
                self.assertEqual(optimizer.optimize(raw), raw)

    def test_native_background_restore_has_no_residual_pixels(self):
        for theme_id, theme in DATA['themes'].items():
            size = tuple(theme['size'])
            saved = Image.linear_gradient('L').resize(size).convert('RGBA')
            screen = saved.copy()
            for entry in theme['frames'] * 3:
                frame = Image.open(SKIN / 'spinner-themes' / theme_id / entry['name'])
                screen.paste(Image.alpha_composite(saved, frame))
                expected = Image.alpha_composite(saved, frame)
                self.assertIsNone(ImageChops.difference(screen, expected).getbbox())
            screen.paste(saved)
            self.assertEqual(screen.tobytes(), saved.tobytes())

    def test_exact_owner_labels_and_twenty_locales(self):
        self.assertEqual(DATA['themes']['bakussa']['title'], 'HDGlass - bakussa')
        self.assertEqual(DATA['themes']['bakussa']['author'], 'bakussa')
        self.assertNotIn('author_url', DATA['themes']['bakussa'])
        cfg = SimpleNamespace(osd=SimpleNamespace(language=SimpleNamespace(value='sk_SK')))
        with patch.dict(sys.modules, {'Components.config': SimpleNamespace(config=cfg)}):
            text = load('spinner_text', PLUGIN / 'warderUiText.py')
        self.assertEqual(spinner.choices(text.ui_text), [('dove', 'Holubica'), ('bakussa', 'HDGlass - bakussa')])
        for code in ('al','cs','de','en','es','et','fa','fr','hu','it','lt','nl','pl','pt','ro','ru','sk','tr','uk','zh'):
            cfg.osd.language.value = code + '_XX'
            self.assertTrue(text.ui_text('Dove'))
            self.assertIn('Dove', text.TEXT[code])
            self.assertEqual(spinner.choices(text.ui_text)[1][1], 'HDGlass - bakussa')


class SelectionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / 'hd_glass17'
        self.root.mkdir()
        shutil.copytree(SKIN / 'spinner-themes', self.root / 'spinner-themes')
        shutil.copytree(SKIN / 'spinner', self.root / 'spinner')
        self.before = content(self.root / 'spinner')

    def apply(self, selected):
        return spinner.apply(selected, self.root)

    def assert_clean(self):
        self.assertEqual({p.name for p in self.root.iterdir()}, {'spinner', 'spinner-themes'})

    def test_switch_both_directions_and_remove_obsolete_twenty_frame_tail(self):
        self.assertTrue(self.apply('bakussa'))
        self.assertEqual(content(self.root / 'spinner'), content(self.root / 'spinner-themes/bakussa'))
        self.assertTrue(self.apply('dove'))
        self.assertEqual(content(self.root / 'spinner'), self.before)
        self.assert_clean()

    def test_unchanged_selection_causes_no_flash_writes(self):
        with patch.object(spinner.os, 'rename', side_effect=AssertionError('unexpected rename')), patch.object(spinner.tempfile, 'mkdtemp', side_effect=AssertionError('unexpected write')):
            self.assertFalse(self.apply('dove'))
        self.assert_clean()

    def test_upgrade_overlay_preserves_saved_bakussa_and_drops_tail_when_dove_selected(self):
        for selected in ('bakussa', 'dove'):
            self.apply('bakussa')
            for path in (SKIN / 'spinner').iterdir():
                shutil.copyfile(path, self.root / 'spinner' / path.name)
            self.apply(selected)
            self.assertEqual(content(self.root / 'spinner'), content(self.root / 'spinner-themes' / selected))
            self.assert_clean()

    def test_corrupt_last_source_frame_prevents_any_change(self):
        (self.root / 'spinner-themes/bakussa/wait20.png').write_bytes(b'broken')
        with self.assertRaises(ValueError):
            self.apply('bakussa')
        self.assertEqual(content(self.root / 'spinner'), self.before)
        self.assert_clean()

    def test_unknown_user_file_prevents_whole_operation(self):
        (self.root / 'spinner/personal.txt').write_text('keep')
        before = content(self.root / 'spinner')
        with self.assertRaises(ValueError):
            self.apply('bakussa')
        self.assertEqual(content(self.root / 'spinner'), before)

    def test_custom_frame_is_never_overwritten(self):
        (self.root / 'spinner/wait18.png').write_bytes(b'custom')
        before = content(self.root / 'spinner')
        with self.assertRaises(ValueError):
            self.apply('bakussa')
        self.assertEqual(content(self.root / 'spinner'), before)

    def test_linked_active_directory_is_never_followed(self):
        active = self.root / 'spinner'
        active.rename(self.root / 'personal')
        active.symlink_to(self.root / 'personal', target_is_directory=True)
        with self.assertRaises(ValueError):
            self.apply('bakussa')
        self.assertTrue(active.is_symlink())
        self.assertEqual(content(self.root / 'personal'), self.before)

    def test_linked_library_or_frame_is_never_followed(self):
        library = self.root / 'spinner-themes'
        library.rename(self.root / 'personal')
        library.symlink_to(self.root / 'personal', target_is_directory=True)
        with self.assertRaises(ValueError):
            self.apply('bakussa')
        library.unlink()
        (self.root / 'personal').rename(library)
        last = library / 'bakussa/wait20.png'
        last.unlink()
        last.symlink_to(library / 'bakussa/wait19.png')
        with self.assertRaises(ValueError):
            self.apply('bakussa')
        self.assertEqual(content(self.root / 'spinner'), self.before)

    def test_failed_second_rename_restores_all_original_frames(self):
        real_rename = os.rename
        def rename(source, target):
            if Path(source).name.startswith('.warder-spinner-stage-'):
                raise OSError('injected rename failure')
            return real_rename(source, target)
        with patch.object(spinner.os, 'rename', side_effect=rename), self.assertRaises(OSError):
            self.apply('bakussa')
        self.assertEqual(content(self.root / 'spinner'), self.before)
        self.assert_clean()

    def test_failed_copy_leaves_previous_active_set_and_no_staging_files(self):
        with patch.object(spinner.os, 'fsync', side_effect=OSError('injected full disk')), self.assertRaises(OSError):
            self.apply('bakussa')
        self.assertEqual(content(self.root / 'spinner'), self.before)
        self.assert_clean()

    def test_interrupted_swap_is_recovered_before_selection(self):
        (self.root / 'spinner').rename(self.root / '.warder-spinner-previous')
        self.assertTrue(self.apply('bakussa'))
        self.assertEqual(content(self.root / 'spinner'), content(self.root / 'spinner-themes/bakussa'))
        self.assert_clean()

    def test_leftover_previous_set_is_cleaned_only_when_owned(self):
        shutil.copytree(self.root / 'spinner', self.root / '.warder-spinner-previous')
        self.assertFalse(self.apply('dove'))
        self.assert_clean()
        shutil.copytree(self.root / 'spinner', self.root / '.warder-spinner-previous')
        (self.root / '.warder-spinner-previous/custom.txt').write_text('keep')
        with self.assertRaises(ValueError):
            self.apply('bakussa')
        self.assertEqual(content(self.root / 'spinner'), self.before)

    def test_missing_active_directory_is_recreated_from_verified_assets(self):
        shutil.rmtree(self.root / 'spinner')
        self.assertTrue(self.apply('bakussa'))
        self.assert_clean()

    def test_uninstall_can_remove_every_owned_frame_without_a_longer_theme_tail(self):
        self.apply('bakussa')
        self.assertEqual(len(content(self.root / 'spinner')), 20)
        self.apply('dove')
        # Simulate opkg deleting only the eighteen paths in its package list.
        for path in (SKIN / 'spinner').iterdir():
            (self.root / 'spinner' / path.name).unlink()
        self.assertEqual(list((self.root / 'spinner').iterdir()), [])

    def test_invalid_theme_does_not_change_any_files(self):
        with self.assertRaises(ValueError):
            self.apply('../skin_default')
        self.assertEqual(content(self.root / 'spinner'), self.before)

    def test_third_theme_is_available_and_persisted_without_controller_changes(self):
        data = json.loads(json.dumps(DATA))
        data['themes']['third-theme'] = dict(data['themes']['bakussa'], title='Another author', author='Another author')
        path = Path(self.temp.name) / 'catalog.json'
        path.write_text(json.dumps(data))
        shutil.copytree(self.root / 'spinner-themes/bakussa', self.root / 'spinner-themes/third-theme')
        self.assertEqual(spinner.choices(lambda text:text, path)[-1], ('third-theme', 'Another author'))
        self.assertTrue(spinner.apply('third-theme', self.root, path))
        self.assertEqual(content(self.root / 'spinner'), content(self.root / 'spinner-themes/third-theme'))
        settings = Path(self.temp.name) / 'settings'
        settings.write_text(spinner.SETTING + '=third-theme\n')
        self.assertEqual(spinner.saved_theme(settings, path), 'third-theme')

    def test_saved_selection_defaults_without_modifying_settings(self):
        settings = Path(self.temp.name) / 'settings'
        self.assertEqual(spinner.saved_theme(settings), 'dove')
        for value, expected in [('bakussa','bakussa'), ('dove','dove'), ('../../../etc','dove')]:
            original = ('config.skin.primary_skin=hd_glass17/skin.xml\n' + spinner.SETTING + '=' + value + '\n').encode()
            settings.write_bytes(original)
            self.assertEqual(spinner.saved_theme(settings), expected)
            self.assertEqual(settings.read_bytes(), original)


class ControllerTests(unittest.TestCase):
    def method(self, name):
        tree = ast.parse((PLUGIN / 'plugin.py').read_text())
        cls = next(n for n in tree.body if isinstance(n, ast.ClassDef) and n.name == 'setupGlass17ScreenSetup')
        return next(n for n in cls.body if isinstance(n, ast.FunctionDef) and n.name == name)

    def test_actual_other_settings_menu_contains_one_catalog_selector(self):
        setup = SimpleNamespace(**{'par%d' % n: SimpleNamespace(value=False) for n in range(1, 231)})
        branch = next(n for n in ast.walk(self.method('runSetup')) if isinstance(n, ast.If) and ast.unparse(n.test) == 'tt == 28')
        screen = SimpleNamespace(list=[])
        scope = {'self':screen, 'config':SimpleNamespace(plugins=SimpleNamespace(setupGlass17=setup)),
                 'S0':'%s', 'ui_text':lambda text:text, '_':lambda text:text,
                 'getConfigListEntry':lambda title, value:(title, value), 'os':os,
                 'PYTHONPATH':'/no-receiver-plugins/', 'ISVTI':False, 'EFIFO':False,
                 'ECL':False, 'isATV':True, 'ENA_ONOFF':False}
        exec(compile(ast.Module(body=branch.body, type_ignores=[]), 'actual-menu', 'exec'), scope)
        rows = [(title, value) for title, value in screen.list if value is setup.par230]
        self.assertEqual(rows, [('Spinner', setup.par230)])

    def test_ok_opens_two_choices_in_catalog_order_and_callback_is_cancel_safe(self):
        setup = SimpleNamespace(par124=object(), par230=SimpleNamespace(value='dove'))
        cfg = SimpleNamespace(plugins=SimpleNamespace(setupGlass17=setup))
        events = []
        callback = self.method('spinnerChoiceSelected')
        activate = self.method('ActivateselectedFnc')
        class Screen:
            isMainMenu = False
            session = SimpleNamespace(openWithCallback=lambda *args, **kw:events.append((args, kw)))
            def __getitem__(self, key):
                return SimpleNamespace(getCurrent=lambda:('Spinner', setup.par230), invalidateCurrent=lambda:events.append('invalidate'))
            def doMyHelpWindow(self):
                events.append('help')
        screen = Screen()
        scope = {'config':cfg, 'warderSpinner':SimpleNamespace(choices=lambda translate:[('dove','Holubica'),('bakussa','HDGlass - bakussa')]), 'ui_text':lambda text:text, 'ChoiceBox':object()}
        exec(compile(ast.Module(body=[activate, callback], type_ignores=[]), 'actual-choice-box', 'exec'), scope)
        screen.spinnerChoiceSelected = lambda answer:scope['spinnerChoiceSelected'](screen, answer)
        scope['ActivateselectedFnc'](screen)
        self.assertEqual(events[0][1], {'title':'Spinner', 'list':[('Holubica','dove'),('HDGlass - bakussa','bakussa')], 'selection':0})
        screen.spinnerChoiceSelected(None)
        self.assertEqual(setup.par230.value, 'dove')
        screen.spinnerChoiceSelected(('HDGlass - bakussa','bakussa'))
        self.assertEqual(setup.par230.value, 'bakussa')
        self.assertEqual(events[-2:], ['invalidate','help'])

    def test_actual_help_shows_restart_instruction_without_starting_animation(self):
        selected = SimpleNamespace(value='bakussa')
        values = {'config':SimpleNamespace(getCurrent=lambda: ('Spinner', selected))}
        events = []
        class Widget:
            def hide(self):
                events.append(('hide',))
            def setText(self, text):
                events.append(('text', text))
        values.update({name:Widget() for name in ('help_pict','selected_item','help_txt')})
        class Screen:
            isMainMenu = False
            list = [('Spinner', selected)]
            def __getitem__(self, key):
                return values[key]
            def sampleColor(self, value):
                pass
        scope = {'config':SimpleNamespace(plugins=SimpleNamespace(setupGlass17=SimpleNamespace(par230=selected))),
                 'ENA_ANIM':False, 'ui_text':lambda text:text}
        exec(compile(ast.Module(body=[self.method('doMyHelpWindow')], type_ignores=[]), 'actual-help', 'exec'), scope)
        scope['doMyHelpWindow'](Screen())
        self.assertIn(('text', 'Choose the waiting animation. Save to apply it after a GUI restart.'), events)

    def test_actual_cancel_discards_spinner_preference_without_applying_it(self):
        events = []
        setup = SimpleNamespace(dict=lambda: {'par230':SimpleNamespace(cancel=lambda:events.append(('cancel',)))})
        scope = {'config':SimpleNamespace(plugins=SimpleNamespace(setupGlass17=setup)),
                 'ALL_CFG':[''] * 229 + ['Spinner theme'], 'setPathFiles':lambda:None}
        screen = SimpleNamespace(rst=False, destroyTimers=lambda:True, close=lambda:events.append(('close',)))
        exec(compile(ast.Module(body=[self.method('exitNow')], type_ignores=[]), 'actual-cancel', 'exec'), scope)
        scope['exitNow'](screen)
        self.assertEqual(events, [('cancel',), ('close',)])

    def saving(self, theme, fail=False):
        tree = ast.parse((PLUGIN / 'plugin.py').read_text())
        cls = next(n for n in tree.body if isinstance(n, ast.ClassDef) and n.name == 'setupGlass17ScreenSetup')
        node = next(n for n in cls.body if isinstance(n, ast.FunctionDef) and n.name == 'saving')
        events = []
        setup = SimpleNamespace(par230=SimpleNamespace(value=theme), par13=SimpleNamespace(value='same'), par43=SimpleNamespace(value=False), dict=lambda: {})
        cfg = SimpleNamespace(plugins=SimpleNamespace(setupGlass17=setup))
        def apply(value):
            events.append(('apply', value))
            if fail:
                raise ValueError('custom user file')
        self_scope = SimpleNamespace(_spinnerAtOpen='dove', _weatherCityAtOpen='same', rst=True,
            session=SimpleNamespace(open=lambda *args: events.append(('error', args))),
            sDr=lambda: events.append(('restart',)), destroyTimers=lambda: True,
            close=lambda: events.append(('close',)))
        scope = {'config':cfg, 'warderSpinner':SimpleNamespace(apply=apply),
                 'configfile':SimpleNamespace(save=lambda: events.append(('save',))),
                 'ALL_CFG':[], 'MessageBox':SimpleNamespace(TYPE_ERROR=1), 'ui_text':lambda t:t}
        exec(compile(ast.Module(body=[node], type_ignores=[]), 'actual-saving', 'exec'), scope)
        scope['saving'](self_scope)
        return events, self_scope

    def test_actual_save_applies_before_settings_and_gui_restart(self):
        events, _ = self.saving('bakussa')
        self.assertEqual(events, [('apply','bakussa'), ('save',), ('restart',)])

    def test_failed_selection_does_not_save_or_restart(self):
        events, screen = self.saving('bakussa', True)
        self.assertEqual([e[0] for e in events], ['apply', 'error'])
        self.assertFalse(screen.rst)

    def test_unchanged_choice_does_not_copy_frames(self):
        events, _ = self.saving('dove')
        self.assertEqual(events, [('save',), ('restart',)])


if __name__ == '__main__':
    unittest.main()
