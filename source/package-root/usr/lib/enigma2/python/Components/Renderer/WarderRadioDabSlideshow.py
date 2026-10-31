"""The native DAB slideshow, independently of current-song cover lookup."""
import os
from Components.Renderer.WarderRadioArtwork import WarderRadioArtwork
from Components.Renderer.WarderRadioCompactArtwork import WarderRadioCompactArtwork, dab_service_reference


class WarderRadioDabSlideshow(WarderRadioCompactArtwork):
    def _showFallback(self):
        # No song-cover placeholder in the broadcast slideshow window.
        self._clearPicture()

    def _poll(self):
        if self.instance is None:return
        reference = dab_service_reference()
        path = WarderRadioArtwork._dabSlidePath(self) if reference else ""
        key = ""
        if path:
            try:
                status = os.stat(path)
                key = (reference.toString(),path,status.st_mtime_ns,status.st_size)
            except OSError:
                path = ""
        if key != self._key:
            self._key = key
            if path:self._showPath(path)
            else:self._clearPicture()
        self._decodeSizedPicture()
        # No network requests, song lookup or additional disk cache. Decode
        # only when the station's native picture changes, including same-path
        # updates. The extra window stays hidden outside DAB.
        self._timer.start(50 if self._fitPending else (250 if reference else 1000),True)
