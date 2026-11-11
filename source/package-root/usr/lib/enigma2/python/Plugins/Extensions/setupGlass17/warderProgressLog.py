# -*- coding: utf-8 -*-
"""Small bounded live log for Warder's Enigma2 download screen.

No widget access here. A percent update edits only the current work line;
a new operation appends a line. The visible tail scrolls upwards naturally.
"""
import re


class ProgressLog(object):
    def __init__(self, visible_lines=9, max_entries=160):
        self.visible_lines = visible_lines
        self.max_entries = max_entries
        self.entries = []
        self.active_key = None
        self.active_index = None

    def _add(self, text):
        self.entries.append(text)
        if len(self.entries) > self.max_entries:
            overflow = len(self.entries) - self.max_entries
            del self.entries[:overflow]
            if self.active_index is not None:
                self.active_index -= overflow
        return len(self.entries) - 1

    @staticmethod
    def _sanitize(value):
        return " ".join(str(value).split())[:115]

    @staticmethod
    def _stage_key(text):
        # Byte percentages may update often; do not create a row each time.
        key = re.sub(r"(?:\s+-\s+|:\s*)\d+%$", "", text)
        key = re.sub(r":\s*\d+(?:\.\d+)?\s+MiB$", "", key)
        return key

    def stage(self, description):
        line = self._sanitize(description)
        key = self._stage_key(line)
        if key == self.active_key and self.active_index is not None:
            # In-place update: percent changes never flood the display.
            self.entries[self.active_index] = "[>>] " + line
        else:
            # The previous operation has advanced to the next stage.
            # Keep its line visible instead of silently replacing it.
            if self.active_index is not None and self.active_index < len(self.entries):
                previous = self.entries[self.active_index]
                if previous.startswith("[>>] "):
                    self.entries[self.active_index] = "[OK] " + previous[5:]
            self.active_key = key
            self.active_index = self._add("[>>] " + line)

    def done(self, description, success=True):
        prefix = "[OK] " if success else "[ERROR] "
        if self.active_index is not None and self.active_index < len(self.entries):
            previous = self.entries[self.active_index]
            if previous.startswith("[>>] "):
                self.entries[self.active_index] = prefix + previous[5:]
        self._add(prefix + self._sanitize(description))
        self.active_key = None
        self.active_index = None

    def note(self, description):
        self.active_key = None
        self.active_index = None
        self._add(self._sanitize(description))

    def divider(self):
        """Separate completed packages, without creating an active work step.

        Multiple completion notifications for the same package must not
        produce stacked lines. The separator does not count as a work step.
        """
        self.active_key = None
        self.active_index = None
        line = "-" * 78
        if self.entries and self.entries[-1] != line:
            self._add(line)

    def tail(self):
        return "\n".join(self.entries[-self.visible_lines:])
