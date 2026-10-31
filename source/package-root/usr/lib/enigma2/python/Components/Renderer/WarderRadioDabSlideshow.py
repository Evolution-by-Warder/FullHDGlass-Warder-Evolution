"""The native DAB slideshow, independently of current-song cover lookup."""
import os
from enigma import eLabel, ePoint, eSize, gFont
from skin import parseColor
from Components.Renderer.WarderRadioArtwork import WarderRadioArtwork
from Components.Renderer.WarderRadioCompactArtwork import WarderRadioCompactArtwork, dab_service_reference
try:
    from Plugins.Extensions.setupGlass17.warderUiText import ui_text
except ImportError:
    from warderUiText import ui_text


class WarderRadioDabSlideshow(WarderRadioCompactArtwork):
    FALLBACK_ARTWORK = '/usr/share/enigma2/hd_glass17/warder-dab-information.png'
    FALLBACK_SIZE = (1448,1086)

    def __init__(self):
        self._caption = None
        self._captionValue = None
        self._captionSize = None
        self._captionShown = False
        self._usingFallback = False
        WarderRadioCompactArtwork.__init__(self)

    def postWidgetCreate(self,instance):
        WarderRadioCompactArtwork.postWidgetCreate(self,instance)
        self._caption = eLabel(instance)
        self._caption.hide()
        self._caption.setTransparent(1)
        self._caption.setNoWrap(1)
        self._caption.setFont(gFont('Regular',24))
        self._caption.setForegroundColor(parseColor('#00d2f5ff'))
        self._caption.setHAlign(eLabel.alignCenter)
        self._caption.setVAlign(eLabel.alignCenter)
        self._updateCaption()

    def _updateCaption(self):
        if self._caption is None:return
        if not self._usingFallback or self.instance is None:
            if self._captionShown:self._caption.hide()
            self._captionShown = False
            return
        text = ui_text('DAB+ information')
        if text != self._captionValue:
            self._caption.setText(text)
            self._captionValue = text
        size = (self.instance.size().width(),self.instance.size().height())
        if size != self._captionSize:
            self._caption.move(ePoint(12,max(0,size[1]-65)))
            self._caption.resize(eSize(max(1,size[0]-24),42))
            self._captionSize = size
        if not self._captionShown:self._caption.show()
        self._captionShown = True

    def _placeCover(self,size):
        WarderRadioCompactArtwork._placeCover(self,size)
        self._updateCaption()

    def _showPath(self,path):
        self._usingFallback = path == self.FALLBACK_ARTWORK
        WarderRadioCompactArtwork._showPath(self,path)
        self._updateCaption()

    def _clearPicture(self):
        self._usingFallback = False
        WarderRadioCompactArtwork._clearPicture(self)
        self._updateCaption()

    def _showFallback(self):
        reference = dab_service_reference()
        if reference:
            self._key = (reference.toString(),'fallback')
            self._showPath(self.FALLBACK_ARTWORK)
        else:
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
        if reference and not path:key = (reference.toString(),'fallback')
        if key != self._key:
            self._key = key
            if path:self._showPath(path)
            elif reference:self._showFallback()
            else:self._clearPicture()
        self._decodeSizedPicture()
        if self._usingFallback:self._updateCaption()
        # No network requests, song lookup or additional disk cache. Decode
        # only when the station's native picture changes, including same-path
        # updates. The extra window stays hidden outside DAB.
        self._timer.start(50 if self._fitPending else (250 if reference else 1000),True)

    def preWidgetRemove(self,instance):
        self._caption = None
        self._captionShown = False
        WarderRadioCompactArtwork.preWidgetRemove(self,instance)
