"""Keep framed video in the same physical rectangle as a calibrated OSD.

Only the skin's framed previews use this subclass. Native decoder/PiP handling
and fullscreen restoration remain with the image renderer. No proc nodes are
written here, and unknown framebuffer coordinate spaces use native geometry.
"""
from pathlib import Path
from Components.Renderer.Pig import Pig
from enigma import ePoint, eSize, getDesktop

FULL_VIEWPORT = (0, 0, 720, 576)


def read_viewport(root=Path('/proc/stb/fb')):
    try:
        values = tuple(int((root / ('dst_' + name)).read_text().strip(), 16)
                       for name in ('left', 'top', 'width', 'height'))
    except (OSError, ValueError):
        return None
    left, top, width, height = values
    if (left < 0 or top < 0 or width <= 0 or height <= 0 or
            left + width > 720 or top + height > 576):
        return None
    return values


def project_rectangle(rect, framebuffer, viewport):
    """Map absolute widget pixels through the driver's 720x576 OSD viewport."""
    x, y, width, height = rect
    fb_width, fb_height = framebuffer
    if not viewport or viewport == FULL_VIEWPORT or fb_width <= 0 or fb_height <= 0:
        return rect
    left, top, view_width, view_height = viewport
    x1 = (left * fb_width + x * view_width) // 720
    y1 = (top * fb_height + y * view_height) // 576
    x2 = (left * fb_width + (x + width) * view_width) // 720
    y2 = (top * fb_height + (y + height) * view_height) // 576
    return x1, y1, max(1, x2 - x1), max(1, y2 - y1)


class FramedVideoMixin:
    def applySkin(self, desktop, parent):
        result = super().applySkin(desktop, parent)
        if result:
            size = getDesktop(0).size()
            self._framed_framebuffer = (size.width(), size.height())
            self._align_framed_video()
        return result

    def _align_framed_video(self):
        instance = self.instance
        position, size = self.Position, self.Size
        if instance is None or position is None or size is None:
            return
        framebuffer = getattr(self, '_framed_framebuffer', None)
        if framebuffer is None:
            return
        # Derive the current parent offset, not the previously projected child
        # position. The original Position/Size remain native layout state.
        absolute_position = getattr(instance, 'getAbsolutePosition', None)
        if not callable(absolute_position):
            return
        current, absolute = instance.position(), absolute_position()
        parent_x, parent_y = absolute.x() - current.x(), absolute.y() - current.y()
        original = (parent_x + position.x(), parent_y + position.y(),
                    size.width(), size.height())
        x, y, width, height = project_rectangle(original, framebuffer, read_viewport())
        relative = (x - parent_x, y - parent_y)
        changed = False
        current_size = instance.size()
        if (current_size.width(), current_size.height()) != (width, height):
            instance.resize(eSize(width, height))
            changed = True
        if (current.x(), current.y()) != relative:
            instance.move(ePoint(*relative))
            changed = True
        refresh = getattr(instance, 'updateVideoPosition', None)
        if changed and callable(refresh):
            refresh()

    def onShow(self):
        super().onShow()
        self._align_framed_video()


class WarderFramedPig(FramedVideoMixin, Pig):
    pass
