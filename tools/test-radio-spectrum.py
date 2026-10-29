#!/usr/bin/env python3
"""Check drawing-operation budget, real artwork and receiver timer lifecycle."""
import importlib.util
import hashlib
import json
from pathlib import Path
import sys
import types
import unittest
from unittest.mock import patch
import xml.etree.ElementTree as ET
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT/'source/package-root/usr/lib/enigma2/python/Components/Renderer/WarderRadioSpectrum.py'


class Pixmap:
    def __init__(self): self.paints=0; self.visible=True; self.frame=None
    def setPixmap(self, frame): self.frame=frame; self.paints+=1
    def setAlphatest(self, value): self.alphatest=value
    def isVisible(self): return self.visible
    # Deliberately no fillRect/clear/drawLine: using eCanvas must fail this suite.


class Base:
    def __init__(self): self.instance=None; self.skinAttributes=[]
    def postWidgetCreate(self, instance): self.instance=instance
    def preWidgetRemove(self, instance): self.instance=None


class Timer:
    def __init__(self, modern):
        self.callback=[]; self.active=False; self.starts=[]
        if modern: self.timeout=types.SimpleNamespace(connect=lambda cb:self.callback.append(cb))
    def start(self, interval, single=False):
        self.interval=interval; self.single=single; self.active=True; self.starts.append((interval,single))
    def stop(self): self.active=False
    def fire(self):
        if self.active:
            if self.single:self.active=False
            for callback in self.callback:callback()


def load(modern=True, loader=None):
    timers=[]; loads=[]
    def factory():
        timer=Timer(modern);timers.append(timer);return timer
    def decode(path, cached=None):
        loads.append((path,cached))
        return loader(path) if loader else object()
    native=types.SimpleNamespace(ePixmap=Pixmap,eTimer=factory)
    with patch.dict(sys.modules,{'enigma':native,
                                'Tools.LoadPixmap':types.SimpleNamespace(LoadPixmap=decode),
                                'Components.Renderer.Renderer':types.SimpleNamespace(Renderer=Base)}):
        spec=importlib.util.spec_from_file_location('native_spectrum_test',PATH)
        module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    return module,timers,loads


def show(module):
    renderer=module.WarderRadioSpectrum();canvas=Pixmap();renderer.postWidgetCreate(canvas)
    return renderer,canvas


class SpectrumTests(unittest.TestCase):
    def test_frame_budget_one_native_update_and_one_decode_max_per_tick(self):
        module,timers,loads=load();renderer,canvas=show(module);timer=timers[0]
        self.assertEqual((canvas.paints,len(loads)),(0,0))
        for _ in range(1000):
            paints,decodes=canvas.paints,len(loads)
            timer.fire()
            self.assertEqual(canvas.paints-paints,1)
            self.assertLessEqual(len(loads)-decodes,1)
            self.assertEqual(timer.interval,100);self.assertTrue(timer.single)
        self.assertEqual(len(loads),48)
        self.assertTrue(all(cached is False for path,cached in loads))
        self.assertEqual(canvas.alphatest,1)

    def test_all_native_screens_share_one_bounded_decode_cache(self):
        module,timers,loads=load();renderers=[show(module) for _ in range(3)]
        for _ in range(200):
            for timer in timers:timer.fire()
        self.assertEqual(len(loads),48)
        self.assertEqual(len(module._FRAMES),48)
        self.assertIs(renderers[0][1].frame,renderers[1][1].frame)
        self.assertLessEqual(350*126*4*len(module._FRAMES),9*1024*1024)

    def test_metadata_storm_does_not_add_paints_or_restart_active_timer(self):
        module,timers,loads=load();renderer,canvas=show(module);timer=timers[0]
        for _ in range(5000):renderer.changed((0,));renderer.onShow()
        self.assertEqual((len(timer.starts),canvas.paints,len(loads)),(1,0,0))
        timer.fire();self.assertEqual(canvas.paints,1)

    def test_both_timer_apis_stop_while_hidden_even_after_source_changes(self):
        for modern in (False,True):
            with self.subTest(modern=modern):
                module,timers,loads=load(modern);renderer,canvas=show(module);timer=timers[0]
                self.assertEqual(len(timer.callback),1)
                timer.fire();renderer.onHide();before=canvas.paints
                renderer.changed((0,));renderer._tick();timer.fire()
                self.assertFalse(timer.active);self.assertEqual(before,canvas.paints)
                renderer.onShow();timer.fire();self.assertEqual(canvas.paints,before+1)
                renderer.preWidgetRemove(canvas);renderer._tick();self.assertFalse(timer.active)

    def test_native_parent_hidden_without_onHide_never_decodes_or_paints(self):
        module,timers,loads=load();renderer,canvas=show(module);timer=timers[0]
        canvas.visible=False
        for _ in range(100):timer.fire()
        self.assertEqual((canvas.paints,len(loads)),(0,0))
        self.assertEqual(timer.interval,500)
        canvas.visible=True;timer.fire();self.assertEqual(canvas.paints,1)
        self.assertEqual(timer.interval,100)

    def test_timer_rearmed_after_slow_load_and_paint_not_before(self):
        module,timers,loads=load();renderer,canvas=show(module);timer=timers[0]
        def delayed(path,cached=None):
            self.assertFalse(timer.active)
            return object()
        module.LoadPixmap=delayed
        original=canvas.setPixmap
        def paint(frame):
            self.assertFalse(timer.active)
            original(frame)
        canvas.setPixmap=paint
        timer.fire();self.assertTrue(timer.active)

    def test_missing_or_failed_optional_frame_stops_without_retry_storm(self):
        for failure in ('none','exception'):
            def decoder(path):
                if failure=='exception':raise OSError('corrupt PNG')
                return None
            module,timers,loads=load(loader=decoder);renderer,canvas=show(module);timer=timers[0]
            timer.fire()
            for _ in range(100):renderer.changed((0,));renderer.onShow();renderer._tick();timer.fire()
            self.assertFalse(timer.active);self.assertEqual(len(loads),1)
            self.assertEqual(canvas.paints,0)

    def test_loop_uses_adjacent_frames_at_both_ends(self):
        module,timers,loads=load();renderer,canvas=show(module)
        seen=[]
        for _ in range(250):
            seen.append(renderer._frame);timers[0].fire()
        self.assertEqual(seen[:50],list(range(48))+[46,45])
        self.assertTrue(all(abs(a-b)==1 for a,b in zip(seen,seen[1:])))
        self.assertEqual(min(seen),0);self.assertEqual(max(seen),47)

    def test_real_assets_have_approved_geometry_colours_transparency_and_hashes(self):
        manifest=json.loads((ROOT/'design/radio-spectrum/frames.json').read_text())
        self.assertEqual(manifest['frames'],48)
        paths={ROOT/'source/package-root'/entry['path'] for entry in manifest['assets']}
        self.assertEqual(paths,set((ROOT/'source/package-root/usr/share/enigma2/hd_glass17/warder-spectrum').glob('*.png')))
        self.assertEqual(len(paths),48)
        images=[]
        for entry in manifest['assets']:
            path=ROOT/'source/package-root'/entry['path']
            self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(),entry['sha256'])
            with Image.open(path) as raw:
                image=raw.convert('RGBA');self.assertEqual(image.size,(350,126))
            pixels=image.load();xs=set();colors=set()
            for y in range(126):
                for x in range(350):
                    red,green,blue,alpha=pixels[x,y]
                    self.assertIn(alpha,(0,255))
                    if alpha:
                        self.assertGreaterEqual(x,7);self.assertLess(x,342)
                        self.assertLess((x-7)%4,3)
                        xs.add(x);colors.add((red,green,blue))
            self.assertEqual(xs,{7+i*4+offset for i in range(84) for offset in range(3)})
            self.assertGreater(len(colors),100)
            images.append(image.tobytes())
        self.assertEqual(len(set(images)),48)

    def test_all_three_screen_positions_and_size_are_preserved(self):
        skin=ET.parse(ROOT/'source/package-root/usr/share/enigma2/hd_glass17/skin.xml').getroot()
        found=[]
        for screen in skin.findall('screen'):
            for widget in screen.findall("widget[@render='WarderRadioSpectrum']"):
                found.append((screen.get('name'),widget.get('position')))
                self.assertEqual(widget.get('size'),'350,126');self.assertEqual(widget.get('transparent'),'1')
        self.assertEqual(sorted(found),[('RadioInfoBar','1470,2'),('RdsDisplay','1470,876'),('RdsInfoDisplay','1470,876')])


if __name__=='__main__':unittest.main()
