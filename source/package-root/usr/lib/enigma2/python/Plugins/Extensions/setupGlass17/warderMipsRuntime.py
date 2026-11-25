"""Opt-in runtime safeguards for positively identified MIPS receivers only.

Never infer MIPS from the historical helper-download fallback. No settings
writes, no global GUI patches, no changes to ARM/AArch64/unknown machines.
"""
import os


def is_mips(machine=None):
    if machine is None:
        try:
            machine = os.uname().machine
        except (AttributeError, OSError):
            return False
    return str(machine).strip().lower() in (
        "mips", "mipsel", "mipsle", "mips32", "mips32el", "mips32le",
        "mips64", "mips64el", "mips64le")


MIPS_RUNTIME = is_mips()


def memory_kib(path="/proc/meminfo"):
    try:
        with open(path) as stream:
            for line in stream:
                if line.startswith("MemTotal:"):
                    return int(line.split()[1])
    except (OSError, ValueError, IndexError):
        pass
    return None


# Read once, and only on an identified MIPS receiver. Unknown RAM uses the
# conservative budget; do not poll /proc during painting or scrolling.
MIPS_MEMORY_KIB = memory_kib() if MIPS_RUNTIME else None


def weather_frame_indices(count, mips=MIPS_RUNTIME, ram_kib=MIPS_MEMORY_KIB):
    if not mips:
        return range(count)
    limit = 12 if ram_kib is None or ram_kib <= 256 * 1024 else 24
    if count <= limit:
        return range(count)
    return tuple(i * (count - 1) // (limit - 1) for i in range(limit))


def weather_delay(delay, mips=MIPS_RUNTIME, ram_kib=MIPS_MEMORY_KIB):
    if not mips:
        return delay
    return max(delay, 150 if ram_kib is None or ram_kib <= 256 * 1024 else 100)


class RendererTimerGuard:
    """MIPS-only lifecycle owner; callback disconnected before widget removal."""
    def __init__(self, timer, callback):
        self.timer = timer
        self.callback = callback
        self.connection = None
        self.callbacks = None
        self.attached = False
        self.suspended = True

    def attach(self):
        if self.attached:
            return
        try:
            self.connection = self.timer.timeout.connect(self.callback)
        except AttributeError:
            try:
                self.callbacks = self.timer.callback
            except AttributeError:
                self.callbacks = self.timer.timeout.get()
            self.callbacks.append(self.callback)
        self.attached = True

    def detach(self):
        self.attached = False
        self.suspended = True
        self.timer.stop()
        if self.connection is not None:
            try:
                self.connection.disconnect()
            except (AttributeError, RuntimeError):
                pass
            self.connection = None
        if self.callbacks is not None:
            try:
                self.callbacks.remove(self.callback)
            except ValueError:
                pass
            self.callbacks = None

    def suspend(self, suspended):
        self.suspended = bool(suspended)
        if self.suspended:
            self.timer.stop()

    def ready(self, instance):
        return self.attached and not self.suspended and instance is not None
