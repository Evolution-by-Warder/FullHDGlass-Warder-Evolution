"""Fit CoolTVGuide event captions without changing its events or navigation."""
from functools import wraps
from types import MethodType


def captions(entries, text_type, wrap_flag, ellipsis_flag):
    result = []
    for entry in entries:
        if (isinstance(entry, (tuple, list)) and len(entry) >= 8
                and entry[0] == text_type and isinstance(entry[6], int)
                and entry[6] & wrap_flag):
            updated = list(entry)
            updated[6] = (entry[6] & ~wrap_flag) | ellipsis_flag
            if isinstance(entry[7], str):
                updated[7] = ' '.join(entry[7].split())
            result.append(tuple(updated) if isinstance(entry, tuple) else updated)
        else:
            result.append(entry)
    return result


def adapt(component, is_active, text_type, wrap_flag, ellipsis_flag):
    if not is_active() or type(component).__module__ != 'Plugins.Extensions.CoolTVGuide.plugin':
        return False
    # Verified against the user's Coolman V8.0 Python 3 package. The remaining
    # obfuscated list classes are other guides and must keep their own builders.
    if type(component).__name__ != 'fAzez':
        return False
    original = getattr(component, 'ZiGNvxobF', None)
    content = getattr(component, 'l', None)
    if not callable(original) or not callable(getattr(content, 'setBuildFunc', None)):
        return False
    if getattr(component, '_warder_cool_text_content', None) is content:
        return False

    @wraps(original)
    def draw(self, *args, **kwargs):
        entries = original(*args, **kwargs)
        if not is_active():
            return entries
        return captions(entries, text_type, wrap_flag, ellipsis_flag)

    callback = MethodType(draw, component)
    content.setBuildFunc(callback)
    component._warder_cool_text_content = content
    component._warder_cool_text_callback = callback
    return True


def install(gui_component, is_active, text_type, wrap_flag, ellipsis_flag):
    original = gui_component.applySkin
    if getattr(original, '_warder_cool_text', False):
        return False

    @wraps(original)
    def apply_skin(self, desktop, parent):
        result = original(self, desktop, parent)
        adapt(self, is_active, text_type, wrap_flag, ellipsis_flag)
        return result

    apply_skin._warder_cool_text = True
    gui_component.applySkin = apply_skin
    return True
