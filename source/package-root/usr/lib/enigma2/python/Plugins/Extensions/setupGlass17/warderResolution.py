"""FullHDGlass-owned 1920x1080 layouts on other Enigma2 desktops.

Native Screen scales XML; these helpers scale only Python-generated geometry.
Nothing is installed on global Enigma2 classes or other plugins.
"""
import re
from Components import MultiContent as _content
from Screens.Screen import Screen as NativeScreen
from enigma import (BT_SCALE, eListbox, ePixmap, ePoint as _point, eSize as _size,
                    gFont as _font, getDesktop)
from .warderListRows import fit


def factors():
    size = getDesktop(0).size()
    return size.width()/1920.0, size.height()/1080.0


def pixel(value, axis=1):
    return round(value*factors()[axis])


def logical(value, axis=1):
    return round(value/factors()[axis]) if factors()[axis] != 1 else value


def ePoint(x, y):
    sx, sy = factors()
    return _point(round(x*sx), round(y*sy))


def eSize(width, height):
    sx, sy = factors()
    return _size(round(width*sx), round(height*sy))


def gFont(name, points):
    return _font(name, max(1, pixel(points)))


gFont._warder_native_font = _font


def reference_skin(value):
    if not isinstance(value, str):
        return value
    opening = re.search(r'<screen\b[^>]*>', value)
    if opening is None or re.search(r'\b(?:resolution|id)\s*=', opening.group()):
        return value
    return value[:opening.start()] + opening.group().replace('<screen', '<screen resolution="1920,1080"', 1) + value[opening.end():]


def _entry(name, args, kwargs):
    sx, sy = factors()
    if sx == sy == 1:
        return getattr(_content, name)(*args, **kwargs)
    args = list(args); kwargs = dict(kwargs)
    for index, key in enumerate(('pos', 'size')):
        if index < len(args):
            pair = args[index]; args[index] = (round(pair[0]*sx), round(pair[1]*sy))
        elif key in kwargs:
            pair = kwargs[key]; kwargs[key] = (round(pair[0]*sx), round(pair[1]*sy))
    if name != 'MultiContentEntryText':
        if len(args) >= 6:
            args[5] |= BT_SCALE
        else:
            kwargs['flags'] = kwargs.get('flags', 0) | BT_SCALE
    return getattr(_content, name)(*args, **kwargs)


def MultiContentEntryText(*args, **kwargs):
    return _entry('MultiContentEntryText', args, kwargs)


def MultiContentEntryPixmap(*args, **kwargs):
    return _entry('MultiContentEntryPixmap', args, kwargs)


def MultiContentEntryPixmapAlphaTest(*args, **kwargs):
    return _entry('MultiContentEntryPixmapAlphaTest', args, kwargs)


def MultiContentEntryPixmapAlphaBlend(*args, **kwargs):
    return _entry('MultiContentEntryPixmapAlphaBlend', args, kwargs)


class Screen(NativeScreen):
    _warder_owned_resolution = True

    def __setattr__(self, name, value):
        NativeScreen.__setattr__(self, name, reference_skin(value) if name == 'skin' else value)

    def __init__(self, *args, **kwargs):
        if isinstance(getattr(self, 'skin', None), str):
            self.skin = self.skin
        NativeScreen.__init__(self, *args, **kwargs)

    def fit_lists(self):
        for component in self.values():
            fit(component, eListbox, _size)

    def applySkin(self):
        result = NativeScreen.applySkin(self)
        self.fit_lists()
        if factors() != (1, 1):
            widgets = list(self.values()) + list(getattr(self, 'renderer', ())) + list(getattr(self, 'additionalWidgets', ()))
            for widget in widgets:
                instance = getattr(widget, 'instance', None)
                if isinstance(instance, ePixmap):
                    instance.setScale(1)
        return result

    def show(self):
        result = NativeScreen.show(self)
        self.fit_lists()
        return result
