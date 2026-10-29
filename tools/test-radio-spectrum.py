#!/usr/bin/env python3
"""Exercise real native drawing, colour flow and hidden-screen timer lifecycle."""
import importlib.util
from pathlib import Path
import sys
import types
import unittest
from unittest.mock import patch
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT/'source/package-root/usr/lib/enigma2/python/Components/Renderer/WarderRadioSpectrum.py'


class Canvas:
    def __init__(self): self.rects=[]; self.clears=0
    def clear(self, color): self.background=color; self.rects=[]; self.clears+=1
    def fillRect(self, rect, color): self.rects.append((rect, color))
    def setSize(self, size): self.size=size


class Base:
    def __init__(self): self.instance=None; self.skinAttributes=[]
    def postWidgetCreate(self, instance): self.instance=instance
    def preWidgetRemove(self, instance): self.instance=None
    def applySkin(self, *args): return True


class Timer:
    def __init__(self, modern):
        self.callback=[]; self.active=False
        if modern: self.timeout=types.SimpleNamespace(connect=lambda cb:self.callback.append(cb))
    def start(self, interval): self.interval=interval; self.active=True
    def stop(self): self.active=False


def load(modern=True):
    timers=[]
    def factory():
        timer=Timer(modern);timers.append(timer);return timer
    native=types.SimpleNamespace(eCanvas=Canvas,eRect=lambda *v:v,eSize=lambda *v:v,
                                gRGB=lambda *v:v,eTimer=factory)
    with patch.dict(sys.modules,{'enigma':native,'skin':types.SimpleNamespace(parseColor=lambda v:v),
                                'Components.Renderer.Renderer':types.SimpleNamespace(Renderer=Base)}):
        spec=importlib.util.spec_from_file_location('native_spectrum_test',PATH)
        module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
        renderer=module.WarderRadioSpectrum()
    return renderer,timers[0]


class SpectrumTests(unittest.TestCase):
    def test_exact_approved_geometry_and_transparent_clear(self):
        renderer,timer=load();canvas=Canvas();renderer.postWidgetCreate(canvas)
        for unused in range(120):renderer._tick()
        self.assertEqual(canvas.background,(0,0,0,255))
        self.assertEqual(renderer._bars,84)
        xs=sorted({rect[0] for rect,color in canvas.rects})
        self.assertEqual(xs,list(range(7,340,4)))
        for (x,y,w,h),color in canvas.rects:
            self.assertEqual(w,3);self.assertIn(h,(1,2))
            self.assertGreaterEqual(y,0);self.assertLessEqual(y+h,126)
            self.assertLessEqual(x+w,350);self.assertEqual(color[3],0)
        self.assertEqual(timer.interval,50)

    def test_many_colours_and_continuous_colour_drift(self):
        renderer,unused=load();canvas=Canvas();renderer.postWidgetCreate(canvas)
        renderer._visible=[20.0]*84;renderer._visible_peaks=[23.0]*84
        renderer._paint();before=[color for rect,color in canvas.rects]
        self.assertGreater(len(set(before)),100)
        renderer._color_time=2.0;renderer._paint()
        self.assertNotEqual(before,[color for rect,color in canvas.rects])

    def test_independent_motion_interpolates_without_file_io(self):
        renderer,unused=load();renderer.postWidgetCreate(Canvas())
        with patch('builtins.open',side_effect=AssertionError('Spectrum must perform no file I/O')):
            for unused in range(100):renderer._tick()
        self.assertGreater(len(set(renderer._levels)),5)
        self.assertTrue(any(value!=int(value) for value in renderer._visible))
        self.assertTrue(all(2<=value<=30 for value in renderer._visible))

    def test_both_timer_apis_stop_while_hidden_even_after_source_changes(self):
        for modern in (False,True):
            with self.subTest(modern=modern):
                renderer,timer=load(modern);canvas=Canvas();renderer.postWidgetCreate(canvas)
                self.assertEqual(len(timer.callback),1);self.assertTrue(timer.active)
                renderer.onHide();before=canvas.clears
                renderer.changed((0,));renderer._tick()
                self.assertFalse(timer.active);self.assertEqual(before,canvas.clears)
                renderer.onShow();self.assertTrue(timer.active)
                renderer.preWidgetRemove(canvas);self.assertFalse(timer.active)

    def test_canvas_sizing_and_all_three_screen_positions_are_preserved(self):
        renderer,unused=load();renderer.instance=Canvas()
        renderer.skinAttributes=[('size','350,126'),('transparent','1')]
        self.assertTrue(renderer.applySkin(None,None));self.assertEqual(renderer.instance.size,(350,126))
        skin=ET.parse(ROOT/'source/package-root/usr/share/enigma2/hd_glass17/skin.xml').getroot()
        found=[]
        for screen in skin.findall('screen'):
            for widget in screen.findall("widget[@render='WarderRadioSpectrum']"):
                found.append((screen.get('name'),widget.get('position')))
                self.assertEqual(widget.get('size'),'350,126');self.assertEqual(widget.get('transparent'),'1')
        self.assertEqual(sorted(found),[('RadioInfoBar','1470,2'),('RdsDisplay','1470,876'),('RdsInfoDisplay','1470,876')])


if __name__=='__main__':unittest.main()
