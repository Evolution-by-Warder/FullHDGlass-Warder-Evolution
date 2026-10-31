"""Asset, allocation, compositor and reversible candidate-install regressions.

The compositing tests model CPU save/draw/restore. They are not a receiver/GPU
reproduction and do not prove the original hardware fault has disappeared.
"""
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import shutil
import tempfile
import unittest
from unittest.mock import patch

from PIL import Image, ImageChops

ROOT = Path(__file__).resolve().parents[1]
DESIGN = ROOT / 'design/spinner-repair'
RECORD = json.loads((DESIGN / 'candidate.json').read_text())


def module(name, filename):
    spec = importlib.util.spec_from_file_location(name, ROOT / 'tools' / filename)
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


builder = module('spinner_builder', 'build-spinner-assets.py')
rollback = module('spinner_rollback', 'spinner-candidate-control.py')
optimizer = module('spinner_optimizer', 'optimize-png.py')
prepare = module('spinner_prepare', 'prepare-spinner-test.py')


def images():
    return [Image.open(DESIGN / 'frames' / entry['name']).convert('RGBA') for entry in RECORD['frames']]


class AssetTests(unittest.TestCase):
    def test_original_18_frames_are_byte_preserved_and_recorded(self):
        source = json.loads((DESIGN / 'source.json').read_text())
        self.assertEqual(len(source['frames']), 18)
        for entry in source['frames']:
            raw = (DESIGN / 'original' / entry['name']).read_bytes()
            self.assertEqual(hashlib.sha256(raw).hexdigest(), entry['sha256'])
            with Image.open(io.BytesIO(raw)) as image:
                self.assertEqual(image.size, (134, 99))
                self.assertEqual(image.mode, 'P')

    def test_18_distinct_truecolor_frames_in_original_order_without_palette_or_trns(self):
        self.assertEqual([x['name'] for x in RECORD['frames']], ['wait%d.png' % i for i in range(1, 19)])
        self.assertEqual(len({x['rgba_sha256'] for x in RECORD['frames']}), 18)
        for entry in RECORD['frames']:
            raw = (DESIGN / 'frames' / entry['name']).read_bytes()
            self.assertEqual(hashlib.sha256(raw).hexdigest(), entry['sha256'])
            chunks = optimizer.chunks(raw)
            self.assertEqual(raw[25], 6)
            self.assertFalse({b'PLTE', b'tRNS'} & {kind for kind, data in chunks})
            with Image.open(io.BytesIO(raw)) as image:
                self.assertEqual(image.size, (128, 88))
                self.assertEqual(image.mode, 'RGBA')
                self.assertEqual(hashlib.sha256(image.tobytes()).hexdigest(), entry['rgba_sha256'])

    def test_shared_geometry_has_clear_border_and_real_alpha_edges(self):
        partial = 0
        for image in images():
            alpha = image.getchannel('A')
            x0, y0, x1, y1 = alpha.getbbox()
            self.assertGreaterEqual(x0, 2)
            self.assertGreaterEqual(y0, 2)
            self.assertLessEqual(x1, image.width - 2)
            self.assertLessEqual(y1, image.height - 2)
            partial += sum(alpha.histogram()[1:255])
        self.assertGreater(partial, 0)

    def test_rebuilt_animation_keeps_the_exact_reviewed_rgba_pixels(self):
        with tempfile.TemporaryDirectory() as directory:
            rebuilt = builder.build(Path(directory))
        self.assertEqual(RECORD['fixed_transform'], rebuilt['fixed_transform'])
        self.assertEqual([x['rgba_sha256'] for x in RECORD['frames']], [x['rgba_sha256'] for x in rebuilt['frames']])

    def test_png_package_optimization_cannot_reintroduce_palette_or_change_alpha(self):
        for entry in RECORD['frames']:
            raw = (DESIGN / 'frames' / entry['name']).read_bytes()
            encoded = optimizer.optimize(raw)
            self.assertEqual(raw[25], encoded[25])
            self.assertEqual([(k, v) for k, v in optimizer.chunks(raw) if k != b'IDAT'], [(k, v) for k, v in optimizer.chunks(encoded) if k != b'IDAT'])

    def test_decoded_frame_and_every_32bit_work_buffer_stay_under_stock_threshold(self):
        for image in images():
            self.assertEqual(image.width * 4, 512)
            self.assertEqual(image.width * image.height * 4, 45056)
            self.assertLess(image.width * image.height * 4, 48000)
        self.assertGreaterEqual(134 * 99 * 4, 48000)


class CpuCompositorTests(unittest.TestCase):
    def test_all_transitions_and_hide_restore_background_on_hd_and_fullhd(self):
        # The exact native save/temp/blend/copy sequence; no GPU is simulated.
        for size, position in (((1280, 720), (50, 50)), ((1920, 1080), (75, 75))):
            source = Image.linear_gradient('L').resize(size).convert('RGBA')
            source.putalpha(255)
            bounds = (*position, position[0] + 128, position[1] + 88)
            saved = source.crop(bounds)
            screen = source.copy()
            for frame in images() * 3:
                screen.paste(Image.alpha_composite(saved, frame), position)
                expected = source.copy()
                expected.paste(Image.alpha_composite(saved, frame), position)
                self.assertIsNone(ImageChops.difference(screen, expected).convert('RGB').getbbox())
            screen.paste(saved, position)
            self.assertEqual(screen.tobytes(), source.tobytes())

    def test_transparent_pixels_and_frame_gaps_never_retain_previous_dove_pixels(self):
        saved = Image.new('RGBA', (128, 88), (47, 119, 173, 255))
        for frame in images():
            drawn = Image.alpha_composite(saved, frame)
            transparent = frame.getchannel('A').point(lambda alpha: 255 if alpha == 0 else 0)
            self.assertIsNone(ImageChops.difference(drawn, saved).convert('RGB').getbbox() if transparent.getextrema() == (255, 255) else ImageChops.multiply(ImageChops.difference(drawn, saved).convert('L'), transparent).getbbox())


class RollbackTests(unittest.TestCase):
    def owned(self, parent):
        folder = Path(parent) / 'spinner'
        folder.mkdir()
        frames = []
        for entry in RECORD['frames']:
            raw = (DESIGN / 'frames' / entry['name']).read_bytes()
            (folder / entry['name']).write_bytes(raw)
            frames.append({'name': entry['name'], 'sha256': hashlib.sha256(raw).hexdigest()})
        (folder / rollback.MARKER).write_text(json.dumps({'product': 'FullHDGlass-spinner-candidate', 'frames': frames}))
        return folder

    def test_only_owned_frames_removed_and_unknown_user_file_preserved(self):
        with tempfile.TemporaryDirectory() as directory:
            folder = self.owned(directory)
            (folder / 'personal.txt').write_text('preserve')
            self.assertEqual(rollback.disable(folder), 18)
            self.assertEqual([p.name for p in folder.iterdir()], ['personal.txt'])

    def test_clean_owned_directory_is_removed(self):
        with tempfile.TemporaryDirectory() as directory:
            folder = self.owned(directory)
            self.assertEqual(rollback.disable(folder), 18)
            self.assertFalse(folder.exists())

    def test_changed_last_frame_prevents_any_partial_deletion(self):
        with tempfile.TemporaryDirectory() as directory:
            folder = self.owned(directory)
            (folder / 'wait18.png').write_bytes(b'user data')
            with self.assertRaises(ValueError):
                rollback.disable(folder)
            self.assertTrue((folder / 'wait1.png').exists())
            self.assertTrue((folder / rollback.MARKER).exists())

    def test_symlinked_directory_or_frame_is_never_followed(self):
        with tempfile.TemporaryDirectory() as directory:
            folder = self.owned(directory)
            link = Path(directory) / 'linked'
            link.symlink_to(folder, target_is_directory=True)
            with self.assertRaises(ValueError):
                rollback.disable(link)
            first = folder / 'wait1.png'
            first.unlink()
            first.symlink_to(folder / 'wait2.png')
            with self.assertRaises(ValueError):
                rollback.disable(folder)
            self.assertTrue((folder / 'wait18.png').exists())


class PackagePreparationTests(unittest.TestCase):
    def test_prepare_adds_only_private_skin_frames_helper_and_test_identity(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            payload = root / 'source/package-root'
            plugin = payload / 'usr/lib/enigma2/python/Plugins/Extensions/setupGlass17'
            plugin.mkdir(parents=True)
            control = root / 'source/control'
            control.mkdir()
            for name, contents in (('version', '1.0.45\n'), ('plugin.py', 'value = \'text="1.0.45"\'\n'), ('history.txt', 'old'), ('history.txtSk', 'old')):
                (plugin / name).write_text(contents)
            (control / 'control').write_text('Package: enigma2-plugin-skins-fullhdglass-warder-evolution\nVersion: 1.0.45-1\n')
            (root / 'tools').mkdir()
            shutil.copyfile(ROOT / 'tools/spinner-candidate-control.py', root / 'tools/spinner-candidate-control.py')
            shutil.copyfile(ROOT / 'tools/optimize-png.py', root / 'tools/optimize-png.py')
            with patch.multiple(prepare, ROOT=root, PAYLOAD=payload, PLUGIN=plugin):
                prepare.main()
                with self.assertRaises(ValueError):
                    prepare.main()
            self.assertEqual((plugin / 'version').read_text().strip(), '1.0.46-test1')
            self.assertEqual(len(list((payload / 'usr/share/enigma2/hd_glass17/spinner').glob('wait*.png'))), 18)
            self.assertFalse((payload / 'usr/share/enigma2/skin_default').exists())
            self.assertFalse((payload / 'etc').exists())


if __name__ == '__main__':
    unittest.main()
