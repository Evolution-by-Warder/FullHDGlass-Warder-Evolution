"""Exercise the actual artwork controllers with native-widget substitutes."""
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import sys
import tempfile
import time
from types import SimpleNamespace
import unittest
from unittest.mock import Mock, patch
import xml.etree.ElementTree as ET

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
PYTHON = ROOT / 'source/package-root/usr/lib/enigma2/python'
PLUGIN = PYTHON / 'Plugins/Extensions/setupGlass17'


def load(name, filename):
    spec = importlib.util.spec_from_file_location(name, filename)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class Widget:
    def __init__(self, parent=None):
        self.position = (0, 0)
        self.dimensions = (420, 700)
        self.visible = False
        self.pictures = []

    def move(self, position): self.position = position
    def resize(self, size): self.dimensions = size
    def hide(self): self.visible = False
    def show(self): self.visible = True
    def setTransparent(self, value): pass
    def setBackgroundColor(self, value): pass
    def setPixmap(self, value): self.pictures.append(value)
    def size(self):
        return SimpleNamespace(width=lambda: self.dimensions[0], height=lambda: self.dimensions[1])


class Timer:
    def __init__(self): self.callback = []; self.active = False; self.delay = None
    def start(self, delay, single): self.active = True; self.delay = delay
    def stop(self): self.active = False
    def isActive(self): return self.active


class Decoder:
    def __init__(self):
        self.callbacks = []
        self.PictureData = SimpleNamespace(get=lambda: self.callbacks)
    def setPara(self, values): self.parameters = values
    def startDecode(self, path): self.path = path; return 0
    def getData(self): return self.path
    def finish(self):
        for callback in self.callbacks: callback()


class Renderer:
    def __init__(self): self.instance = None; self.skinAttributes = []
    def postWidgetCreate(self, instance): self.instance = instance
    def preWidgetRemove(self, instance): self.instance = None
    def applySkin(self, desktop, parent): return True


class DabArtworkTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.slide = Path(self.tmp.name) / 'slide.png'
        Image.new('RGB', (320, 240), 'navy').save(self.slide)
        self.reference = SimpleNamespace(type=4115, toString=lambda: '4115:station-a')
        self.preview = str(self.slide)
        self.service = SimpleNamespace(info=lambda: SimpleNamespace(getInfoString=lambda key: self.preview),
                                       rdsDecoder=lambda: None)
        self.nav = SimpleNamespace(getCurrentlyPlayingServiceReference=lambda: self.reference,
                                   getCurrentService=lambda: self.service)
        native = SimpleNamespace(eLabel=Widget, ePixmap=Widget, ePoint=lambda x,y:(x,y),
                                 eSize=lambda w,h:(w,h), eTimer=Timer, ePicLoad=Decoder,
                                 eServiceReference=SimpleNamespace(idServiceDAB=4115),
                                 iRdsDecoder=SimpleNamespace(RadioText=1),
                                 iServiceInformation=SimpleNamespace(sTagPreviewImage=3))
        self.modules = patch.dict(sys.modules, {
            'enigma': native,
            'skin': SimpleNamespace(parseColor=lambda value:value),
            'NavigationInstance': SimpleNamespace(instance=self.nav),
            'Components.Renderer.Renderer': SimpleNamespace(Renderer=Renderer),
            'Components.Converter.WarderRadioMetadata': SimpleNamespace(current_song=lambda *args:('Artist', 'Song')),
        })
        self.modules.start(); self.addCleanup(self.modules.stop)
        # Load the same native cover logic that is shipped to receivers.
        sys.path.insert(0, str(PLUGIN)); self.addCleanup(sys.path.remove, str(PLUGIN))
        self.art = load('dab_test_artwork', PYTHON / 'Components/Renderer/WarderRadioArtwork.py')
        self.module_names = patch.dict(sys.modules, {'Components.Renderer.WarderRadioArtwork': self.art})
        self.module_names.start(); self.addCleanup(self.module_names.stop)
        self.compact = load('dab_test_compact', PYTHON / 'Components/Renderer/WarderRadioCompactArtwork.py')
        self.compact_name = patch.dict(sys.modules, {'Components.Renderer.WarderRadioCompactArtwork': self.compact})
        self.compact_name.start(); self.addCleanup(self.compact_name.stop)
        self.slides = load('dab_test_slides', PYTHON / 'Components/Renderer/WarderRadioDabSlideshow.py')

    def make_cover(self):
        cover = self.compact.WarderRadioCompactArtwork()
        cover.postWidgetCreate(Widget())
        cover._request = Mock()
        return cover

    def make_slideshow(self):
        slideshow = self.slides.WarderRadioDabSlideshow()
        slideshow.skinAttributes = [('position','316,146'), ('size','420,340')]
        slideshow.applySkin(None, None)
        slideshow.postWidgetCreate(Widget())
        slideshow._request = Mock(side_effect=AssertionError('Slideshow must never search the internet'))
        return slideshow

    def flush(self, artwork):
        deadline = time.monotonic() + 1
        while artwork._fitPending:
            if time.monotonic() > deadline: self.fail('Image sizing worker did not finish')
            time.sleep(.002)
            artwork._poll()

    def test_broadcast_slideshow_does_not_suppress_the_single_song_cover_lookup(self):
        cover, slideshow = self.make_cover(), self.make_slideshow()
        self.assertEqual(self.art.WarderRadioArtwork._dabSlidePath(cover), str(self.slide))
        cover._poll(); slideshow._poll(); self.flush(slideshow)
        cover._request.assert_called_once_with('Artist', 'Song', 'artist|song')
        self.assertEqual(cover._coverBounds, (316,506,420,340))
        self.assertEqual(slideshow._picload.path, str(self.slide))
        self.assertEqual(slideshow.instance.position, (316,158))
        self.assertEqual(slideshow.instance.dimensions, (420,315))
        slideshow._request.assert_not_called()

    def test_ordinary_satellite_and_iptv_radios_keep_original_cover_geometry(self):
        cover = self.make_cover()
        for service_type in (1,4097,5001,5002,8193):
            self.reference.type = service_type
            cover._updateCoverBounds(); cover._placeCover((600,600))
            self.assertEqual(cover._coverBounds, (316,146,420,700))
            self.assertEqual(cover.instance.position, (316,286))
            self.assertEqual(cover.instance.dimensions, (420,420))
            cover._request.reset_mock(); cover._requestedKey = ''; cover._poll()
            cover._request.assert_called_once()

    def test_dab_to_ordinary_radio_transition_restores_the_original_window(self):
        cover = self.make_cover()
        for service_type, expected in [(4115,(356,506,340,340)),(4097,(316,286,420,420)),
                                        (4115,(356,506,340,340)),(1,(316,286,420,420))]:
            self.reference.type = service_type
            cover._updateCoverBounds(); cover._placeCover((600,600))
            self.assertEqual(cover.instance.position+cover.instance.dimensions, expected)

    def test_slideshow_stays_hidden_outside_dab_and_never_decodes_song_placeholders(self):
        slideshow = self.make_slideshow()
        self.assertFalse(slideshow.instance.visible)
        self.assertIsNone(slideshow._picload)
        for service_type in (1,4097,5002):
            self.reference.type = service_type; slideshow._poll()
            self.assertFalse(slideshow.instance.visible)
            self.assertFalse(slideshow._fitPending)
            self.assertIsNone(slideshow._picload)
        slideshow._request.assert_not_called()

    def test_missing_slideshow_does_not_block_cover_lookup(self):
        self.preview = ''
        cover, slideshow = self.make_cover(), self.make_slideshow()
        cover._poll(); slideshow._poll()
        cover._request.assert_called_once()
        self.assertFalse(slideshow.instance.visible)
        self.assertIsNone(slideshow._picload)

    def test_unchanged_slides_are_not_redecoded_but_same_path_updates_are(self):
        slideshow = self.make_slideshow()
        with patch.object(slideshow, '_showPath', wraps=slideshow._showPath) as show:
            slideshow._poll(); self.flush(slideshow)
            for _ in range(30): slideshow._poll()
            self.assertEqual(show.call_count, 1)
            previous = self.slide.stat()
            os.utime(self.slide, ns=(previous.st_atime_ns, previous.st_mtime_ns+1000000000))
            slideshow._poll(); self.flush(slideshow)
            self.assertEqual(show.call_count, 2)
        slideshow._request.assert_not_called()

    def test_old_slide_decoder_cannot_paint_after_station_or_mode_change(self):
        slideshow = self.make_slideshow()
        slideshow._poll(); self.flush(slideshow)
        decoder = slideshow._picload
        self.reference = SimpleNamespace(type=4097, toString=lambda:'4097:iptv-b')
        slideshow._poll(); decoder.finish()
        self.assertFalse(slideshow.instance.visible)
        self.assertEqual(slideshow.instance.pictures, [])
        self.assertTrue(all(not edge.visible for edge in slideshow._edges))

    def test_late_sizing_result_is_rejected_after_slideshow_disappears(self):
        slideshow = self.make_slideshow()
        slideshow._key = 'old-slide'
        slideshow._fitReady = (slideshow._fitGeneration, str(self.slide), (320,240))
        self.preview = ''
        slideshow._poll()
        self.assertIsNone(slideshow._fitReady)
        self.assertIsNone(slideshow._picload)
        self.assertEqual(slideshow.instance.pictures, [])

    def test_portrait_and_square_images_fit_without_overlapping_the_two_slots(self):
        top, bottom = (316,146,420,340), (316,506,420,340)
        for size in ((320,240),(600,600),(300,600),(1200,400),(704,640)):
            for slot in (top,bottom):
                x,y,w,h = self.compact.fitted_cover(*size, bounds=slot)
                self.assertGreaterEqual(x,slot[0]); self.assertGreaterEqual(y,slot[1])
                self.assertLessEqual(x+w,slot[0]+slot[2]); self.assertLessEqual(y+h,slot[1]+slot[3])
                self.assertLess(abs(w/h-size[0]/size[1]),.015)
        self.assertLessEqual(top[1]+top[3]+20,bottom[1])
        self.assertLessEqual(bottom[1]+bottom[3],874)

    def test_disposal_cancels_polling_and_discards_pending_sizing(self):
        slideshow = self.make_slideshow()
        slideshow._fitReady = (slideshow._fitGeneration, str(self.slide), (320,240))
        slideshow.preWidgetRemove(slideshow.instance)
        slideshow._poll()
        self.assertFalse(slideshow._timer.active)
        self.assertIsNone(slideshow._fitReady)


class PinnedLayoutTests(unittest.TestCase):
    def test_only_two_reviewed_radio_screens_gain_the_one_extra_slideshow_widget(self):
        record = json.loads((ROOT/'design/radio-dab-split/layout.json').read_text())
        text = (ROOT/'source/package-root/usr/share/enigma2/hd_glass17/skin.xml').read_text()
        self.assertEqual(hashlib.sha256(text.encode()).hexdigest(), record['updated_skin_sha256'])
        self.assertEqual({edit['name'] for edit in record['edits']}, {'RdsInfoDisplay','RdsDisplay'})
        for edit in record['edits']:
            screen = ET.fromstring(edit['updated_screen'])
            slideshow = screen.find("widget[@render='WarderRadioDabSlideshow']")
            self.assertEqual(slideshow.get('position'),'316,146')
            self.assertEqual(slideshow.get('size'),'420,340')
            cover = screen.find("widget[@render='WarderRadioCompactArtwork']")
            self.assertEqual(cover.get('position'),'316,146')
            self.assertEqual(cover.get('size'),'420,700')
            screen.remove(slideshow)
            self.assertEqual([ET.tostring(node) for node in screen],
                             [ET.tostring(node) for node in ET.fromstring(edit['original_screen'])])
            self.assertEqual(text.count(edit['updated_screen']),1)
            text = text.replace(edit['updated_screen'],edit['original_screen'],1)
        self.assertEqual(hashlib.sha256(text.encode()).hexdigest(),record['before_skin_sha256'])


if __name__ == '__main__': unittest.main()
