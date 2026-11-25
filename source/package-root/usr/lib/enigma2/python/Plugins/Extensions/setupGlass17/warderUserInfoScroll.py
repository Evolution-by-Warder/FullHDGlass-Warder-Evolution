"""Smooth native ScrollLabel motion for passive user-info overlays.

Use configurable pixel motion without a custom canvas.
One single-shot timer per overflowing field; no drawing while hidden/closed.
"""

START_DELAY = 5000
END_DELAY = 5000
STEP_PIXELS = 2
STEP_DELAY = 55
SPEED_DELAYS = {'10': 200, '20': 100, '36': 55, '50': 40, '67': 30}


def settings(config):
    """Read live HDG options, retaining the old default cadence."""
    try:
        hdg = config.plugins.setupGlass17
        mode = hdg.par76.value
        raw = hdg.par77.value
        delay = START_DELAY if raw == 'default' else max(0, int(raw) * 1000)
        speed = getattr(getattr(hdg, 'descriptionScrollSpeed', None), 'value', '36')
        return mode, delay, SPEED_DELAYS.get(speed, STEP_DELAY)
    except (AttributeError, TypeError, ValueError):
        return 'Roll back', START_DELAY, STEP_DELAY


class DescriptionScroller:
    def __init__(self, label, timer, options=None):
        self.label = label
        self.timer = timer
        self.options = options or (lambda: ('Roll back', START_DELAY, STEP_DELAY))
        self.visible = False
        self.closed = False
        self.text = None
        self.identity = None
        self.direction = 1
        self.finished = False
        try:
            self.connection = timer.timeout.connect(self.tick)
        except AttributeError:
            timer.callback.append(self.tick)
            self.connection = None

    def _ready(self):
        if (self.closed or not self.visible or self.label is None
                or getattr(self.label, "instance", None) is None
                or getattr(self.label, "pageHeight", 0) <= 0):
            return False
        # A native ScrollLabel can lose its child labels before the outer
        # widget pointer disappears. Never touch a partially deleted widget.
        for attr in ("leftText", "rightText", "long_text"):
            if hasattr(self.label, attr) and getattr(self.label, attr) is None:
                # OpenPLi uses right_text (not rightText) for split mode.
                return False
        return True

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

    def schedule(self, delay=None):
        if self.closed:
            return
        self.timer.stop()
        mode, start_delay, _ = self.options()
        if mode != 'None' and not self.finished and self.visible and self.text and self.overflowing():
            self.timer.start(start_delay if delay is None else delay, True)

    def _reset(self):
        self.direction = 1
        self.finished = False
        if self._ready() and self.text is not None:
            try:
                self.label.setText(self.text)
            except (AttributeError, RuntimeError, TypeError, ValueError):
                self.visible = False

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
        mode, _, step_delay = self.options()
        if self.finished or mode == 'None':
            return
        limits = self._limits()
        if not self.text or limits is None or limits[1] <= 0:
            return
        pos, limit = limits
        target = max(0, min(limit, pos + self.direction * STEP_PIXELS))
        delay = step_delay
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
            # One smooth round trip: pause at the bottom, return to the
            # beginning, then remain static until a new event or show.
            if target == limit:
                if mode == 'Autostop':
                    self.finished = True
                    return
                self.direction = -1
                delay = END_DELAY
            elif target == 0:
                self.finished = True
                return
        except (AttributeError, RuntimeError, TypeError, ValueError):
            # A torn-down or unsupported native widget must not be retried.
            return
        self.schedule(delay)
