"""Keep native Enigma2 ConfigList values clear of long labels in wide screens.

OpenATV's ConfigList normally uses a fixed 200px label/value separator.
FullHDGlass renders native setup labels around 33px, so this causes native
sliders to overlap Czech/Slovak and other translated captions.

Adjust only *wide* native configuration lists after their skin geometry is
known. Smaller plugin windows and our own g17ConfigList are left untouched.
This is a presentation-only, reversible runtime adjustment; no image code,
stored settings or widget actions are modified.
"""

MIN_WIDE_CONFIG_WIDTH = 1200
LABEL_COLUMN_PERCENT = 55
MIN_VALUE_COLUMN = 450


def separator_for_width(width):
    """Return a safe scaled separator, or None for narrow lists."""
    if width < MIN_WIDE_CONFIG_WIDTH:
        return None
    return min(width * LABEL_COLUMN_PERCENT // 100, width - MIN_VALUE_COLUMN)


def install():
    """Install once for native Components.ConfigList only; fail open."""
    try:
        from Components.ConfigList import ConfigList
    except (ImportError, AttributeError):
        return False

    original = ConfigList.applySkin
    if getattr(original, "_warder_wide_config_spacing", False):
        return True

    def applySkin(self, desktop, parent):
        result = original(self, desktop, parent)
        try:
            # Skin size is available only *after* the native skin was applied.
            width = self.instance.size().width()
            separator = separator_for_width(width)
            if separator is not None:
                self.l.setSeperation(separator)  # Native Enigma2 spelling.
        except Exception:
            # An image may have a different ConfigList binding. Never break
            # its setup screens because of optional spacing customization.
            pass
        return result

    applySkin._warder_wide_config_spacing = True
    ConfigList.applySkin = applySkin
    return True
