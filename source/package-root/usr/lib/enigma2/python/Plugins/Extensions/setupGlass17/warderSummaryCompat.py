"""Supply setup fields when a native generic summary selects a setup display."""
from functools import wraps


class Selection:
    def __init__(self, summary, parent, text_source):
        self.summary, self.parent = summary, parent
        self.watchers = []
        for key in ('entry', 'value', 'SetupTitle', 'SetupEntry', 'SetupValue'):
            if key not in summary:
                summary[key] = text_source('')

    def read(self, method, fallback=''):
        getter = getattr(self.parent, method, None)
        if not callable(getter):
            return fallback
        try:
            return getter()
        except Exception:
            return fallback

    def update(self):
        entry = self.read('getCurrentEntry')
        value = self.read('getCurrentValue')
        if not entry and not callable(getattr(self.parent, 'getCurrentEntry', None)):
            try:
                current = self.parent['config'].getCurrent()
                entry = current[0] if current else ''
                value = current[1].getText() if current and len(current) > 1 else ''
            except Exception:
                entry, value = '', ''
        for key, text in (('entry', entry), ('SetupEntry', entry),
                          ('value', value), ('SetupValue', value),
                          ('SetupTitle', self.read('getTitle'))):
            self.summary[key].setText('' if text is None else str(text))

    def show(self):
        candidates = [getattr(self.parent, name, None)
                      for name in ('onChangedEntry', 'onConfigEntryChanged')]
        try:
            candidates.append(self.parent['config'].onSelectionChanged)
        except (AttributeError, KeyError, TypeError):
            pass
        for callbacks in candidates:
            if isinstance(callbacks, list) and self.update not in callbacks:
                callbacks.append(self.update)
                self.watchers.append(callbacks)
        self.update()

    def hide(self):
        for callbacks in self.watchers:
            if self.update in callbacks:
                callbacks.remove(self.update)
        self.watchers = []


def install(screen_summary, is_active, text_source):
    original = screen_summary.__init__
    if getattr(original, '_warder_setup_summary', False):
        return False

    @wraps(original)
    def initialize(self, session, parent):
        original(self, session, parent)
        names = getattr(self, 'skinName', ())
        names = (names,) if isinstance(names, str) else names
        # Native SetupSummary already supplies these fields and its own watchers.
        # Patch only the generic controller selecting a SetupSummary display.
        if not is_active() or type(self) is not screen_summary or 'SetupSummary' not in names:
            return
        selection = Selection(self, parent, text_source)
        self.onShow.append(selection.show)
        self.onHide.append(selection.hide)
        if hasattr(self, 'onClose'):
            self.onClose.append(selection.hide)
        selection.update()

    initialize._warder_setup_summary = True
    screen_summary.__init__ = initialize
    return True
