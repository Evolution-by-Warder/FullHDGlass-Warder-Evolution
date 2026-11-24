"""Smooth native ScrollLabel motion for passive user-info overlays.

Use the channel description's 2px/55ms cadence without a custom canvas.
One single-shot timer per overflowing field; no drawing while hidden/closed.
"""

START_DELAY = 5000
END_DELAY = 5000
STEP_PIXELS = 2
STEP_DELAY = 55


class DescriptionScroller:
    def __init__(self, label, timer):
        self.label = label
        self.timer = timer
        self.visible = False
        self.closed = False
        self.text = None
        self.identity = None
        self.direction = 1
        try:
            self.connection = timer.timeout.connect(self.tick)
        except AttributeError:
            timer.callback.append(self.tick)
            self.connection = None

    def _ready(self):
        return (not self.closed and self.visible and self.label is not None
                and getattr(self.label, "instance", None) is not None
                and getattr(self.label, "pageHeight", 0) > 0)

    def _limits(self):
        if not self._ready() or not callable(getattr(self.label, "setPos", None)):
            return None
        # OpenATV uses totalTextHeight/currentPosition; OpenPLi uses
        # TotalTextHeight/curPos. Both provide native pixel-based setPos.
        height = getattr(self.label, "totalTextHeight",
                         getattr(self.label, "TotalTextHeight", None))
        pos = getattr(self.label, "currentPosition",
                      getattr(self.label, "curPos", None))
        if height is None or pos is None:
            return None
        limit = max(0, height - self.label.pageHeight)
        return max(0, min(pos, limit)), limit

    def overflowing(self):
        limits = self._limits()
        return limits is not None and limits[1] > 0

    def schedule(self, delay=START_DELAY):
        if self.closed:
            return
        self.timer.stop()
        if self.visible and self.text and self.overflowing():
            self.timer.start(delay, True)

    def _reset(self):
        self.direction = 1
        if self._ready() and self.text is not None:
            self.label.setText(self.text)

    def set(self, text, identity=None):
        if self.closed:
            return
        text = text or ""
        if text == self.text and identity == self.identity:
            return
        self.text, self.identity = text, identity
        self.timer.stop()
        # The wake-up callback may update EPG before the show callback.
        # Cache it and do not touch native GUI objects while hidden.
        if self._ready():
            self._reset()
            self.schedule()

    def show(self):
        if self.closed:
            return
        self.visible = True
        self.timer.stop()
        self._reset()
        self.schedule()

    def hide(self):
        self.visible = False
        if not self.closed:
            self.timer.stop()

    def close(self):
        if self.closed:
            return
        self.hide()
        self.closed = True
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
        # Release references only after stopping and disconnecting the timer.
        self.label = None
        self.timer = None

    def tick(self):
        if self.closed:
            return
        self.timer.stop()
        limits = self._limits()
        if not self.text or limits is None or limits[1] <= 0:
            return
        pos, limit = limits
        target = max(0, min(limit, pos + self.direction * STEP_PIXELS))
        delay = STEP_DELAY
        try:
            if target != pos:
                self.label.setPos(target)
                # OpenPLi's setPos moves the text but does not update the
                # scrollbar. OpenATV updates it internally.
                update = getattr(self.label, "updateScrollbar", None)
                if (not hasattr(self.label, "currentPosition")
                        and callable(update)
                        and getattr(self.label, "showscrollbar", True)
                        and getattr(self.label, "scrollbar", None) is not None):
                    update()
            # Pause at either end and reverse without jumping whole pages.
            if target == limit:
                self.direction = -1
                delay = END_DELAY
            elif target == 0:
                self.direction = 1
                delay = START_DELAY
        except (AttributeError, RuntimeError, TypeError, ValueError):
            # A torn-down or unsupported native widget must not be retried.
            return
        self.schedule(delay)
