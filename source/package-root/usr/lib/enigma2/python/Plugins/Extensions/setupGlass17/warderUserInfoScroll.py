"""Automatic native ScrollLabel paging for passive user-info overlays.

No custom canvas, focus interception or animation outside the native widget.
One single-shot timer per overflowing field; hidden screens never scroll.
"""

PAGE_DELAY = 5000


class DescriptionScroller:
    def __init__(self, label, timer):
        self.label = label
        self.timer = timer
        self.visible = False
        self.text = None
        self.identity = None
        try:
            self.connection = timer.timeout.connect(self.tick)
        except AttributeError:
            timer.callback.append(self.tick)
            self.connection = None

    def overflowing(self):
        if not getattr(self.label, "instance", None) or not getattr(self.label, "pageHeight", 0):
            return False
        needed = getattr(self.label, "isNavigationNeeded", None)
        if callable(needed):
            return bool(needed())
        height = getattr(self.label, "TotalTextHeight", getattr(self.label, "totalTextHeight", 0))
        return height > self.label.pageHeight

    def schedule(self):
        self.timer.stop()
        if self.visible and self.text and self.overflowing():
            self.timer.start(PAGE_DELAY, True)

    def set(self, text, identity=None):
        text = text or ""
        if text == self.text and identity == self.identity:
            return
        self.text, self.identity = text, identity
        self.label.setText(text)
        self.schedule()

    def show(self):
        self.visible = True
        # Both native implementations reset to the top when setText is called.
        if self.text is not None:
            self.label.setText(self.text)
        self.schedule()

    def hide(self):
        self.visible = False
        self.timer.stop()

    def close(self):
        self.hide()
        if self.connection is not None:
            try:
                self.connection.disconnect()
            except (AttributeError, RuntimeError):
                pass
            self.connection = None
        else:
            try:
                self.timer.callback.remove(self.tick)
            except (AttributeError, ValueError):
                pass

    def tick(self):
        self.timer.stop()
        if not self.visible or not self.overflowing():
            return
        if self.label.isAtLastPage():
            self.label.setText(self.text or "")
        else:
            self.label.pageDown()
        self.schedule()
