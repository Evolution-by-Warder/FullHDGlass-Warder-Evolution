# -*- coding: utf-8 -*-
"""Background I/O for Warder channel picons. Never access Enigma2 widgets here."""
import os
import shutil
import tempfile
import threading
try:
    from queue import Queue, Empty
except ImportError:
    from Queue import Queue, Empty


class ChannelWorker(object):
    def __init__(self, job, destination, wanted, fetch, install):
        self.job = dict(job)
        self.destination = destination
        self.wanted = wanted
        self.fetch = fetch
        self.install = install
        self.events = Queue()
        self.thread = threading.Thread(target=self.run, name="WarderChannelDownload")
        self.thread.daemon = True

    def start(self):
        self.thread.start()

    def drain(self):
        while True:
            try:
                yield self.events.get_nowait()
            except Empty:
                return

    def run(self):
        archive = None
        try:
            needed = int((int(self.job.get("bytes", 0)) * 2.2) / (1024 * 1024)) + 10
            if int(shutil.disk_usage("/tmp").free / (1024 * 1024)) < needed:
                raise ValueError("insufficient temporary space for Warder channel package")
            if os.path.islink(self.destination) or not os.path.isdir(self.destination):
                raise ValueError("unsafe Warder picon destination")
            if int(shutil.disk_usage(self.destination).free / (1024 * 1024)) < needed:
                raise ValueError("insufficient destination space for Warder channel package")
            fd, archive = tempfile.mkstemp(prefix="warder-channel-", suffix=".zip", dir="/tmp")
            os.close(fd)
            self.events.put(("stage", "Downloading channel package"))
            self.fetch(self.job, archive, lambda done, total: self.events.put(("bytes", (done, total))))
            self.events.put(("stage", "Checking and installing PNG files"))
            installed, available = self.install(archive, self.destination, self.wanted)
            self.events.put(("done", (installed, available)))
        except Exception as error:
            self.events.put(("error", str(error)))
        finally:
            if archive:
                try:
                    os.unlink(archive)
                except OSError:
                    pass
