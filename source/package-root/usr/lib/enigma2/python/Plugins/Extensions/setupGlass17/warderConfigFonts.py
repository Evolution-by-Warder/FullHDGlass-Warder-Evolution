"""Keep inherited configuration fonts within each plugin's actual row height."""
from functools import wraps

DEFAULTS = {'entry': 'Prive3;33', 'value': 'Prive3;30'}

def limits(height):
    height = max(1, int(height))
    return {'entry': max(1, height * 88 // 100 - 2),
            'value': max(1, height * 80 // 100 - 2)}

def install(config_list, is_active, make_font, parse_font):
    original = config_list.applySkin
    if getattr(original, '_warder_config_fonts', False):
        return False

    @wraps(original)
    def apply_skin(self, desktop, parent):
        attributes = list(self.skinAttributes or [])
        result = original(self, desktop, parent)
        if not is_active() or self.instance is None:
            return result
        instance = self.instance
        try:
            height = instance.getItemHeight()
            if height <= 0:
                return result
            maximum = limits(height)
        except (AttributeError, TypeError, ValueError):
            return result
        requested = dict(DEFAULTS)
        for name, value in attributes:
            if name in ('font', 'entryFont'):
                requested['entry'] = value
            elif name in ('valueFont', 'secondFont', 'secondfont'):
                requested['value'] = value
        previous = set(getattr(self, '_warder_capped_fonts', ()))
        scale = getattr(parent, 'scale', ((1, 1), (1, 1)))
        for role, names in (('entry', ('setEntryFont', 'setFont')),
                            ('value', ('setValueFont', 'setSecondFont'))):
            setter = next((getattr(instance, name) for name in names
                           if callable(getattr(instance, name, None))), None)
            if setter is None:
                continue
            try:
                font = parse_font(requested[role], scale)
                size = int(font.pointSize)
                fitted = min(size, maximum[role])
                if fitted < size or role in previous:
                    setter(make_font(font.family, fitted))
                if fitted < size:
                    previous.add(role)
                else:
                    previous.discard(role)
            except (AttributeError, TypeError, ValueError):
                continue
        self._warder_capped_fonts = previous
        return result

    apply_skin._warder_config_fonts = True
    config_list.applySkin = apply_skin
    return True
