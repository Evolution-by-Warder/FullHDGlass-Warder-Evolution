"""A close-fitting radio cover frame, vertically centred beside the lyrics."""
import struct
import threading
from enigma import eLabel, ePoint, eSize
from skin import parseColor
from Components.Renderer.WarderRadioArtwork import WarderRadioArtwork


def picture_size(path):
    """Read at most 64 KiB of image headers; called only by the sizing worker."""
    try:
        with open(path,'rb') as source:data = source.read(65536)
        size = None
        if data.startswith(b'\x89PNG\r\n\x1a\n') and len(data) >= 24:
            size = struct.unpack('>II',data[16:24])
        elif data[:6] in (b'GIF87a',b'GIF89a') and len(data) >= 10:
            size = struct.unpack('<HH',data[6:10])
        elif data.startswith(b'BM') and len(data) >= 26:
            header = struct.unpack('<I',data[14:18])[0]
            size = struct.unpack('<HH',data[18:22]) if header == 12 else struct.unpack('<ii',data[18:26])
            size = (abs(size[0]),abs(size[1]))
        elif data.startswith(b'RIFF') and data[8:12] == b'WEBP':
            if data[12:16] == b'VP8X' and len(data) >= 30:
                size = (1+int.from_bytes(data[24:27],'little'),1+int.from_bytes(data[27:30],'little'))
            elif data[12:16] == b'VP8L' and len(data) >= 25 and data[20] == 0x2f:
                bits = int.from_bytes(data[21:25],'little')
                size = (1+(bits & 0x3fff),1+((bits >> 14) & 0x3fff))
            elif data[12:16] == b'VP8 ' and len(data) >= 30 and data[23:26] == b'\x9d\x01\x2a':
                width,height = struct.unpack('<HH',data[26:30]);size = (width & 0x3fff,height & 0x3fff)
        elif data.startswith(b'\xff\xd8'):
            position = 2
            while position+4 <= len(data):
                if data[position] != 0xff:break
                while position < len(data) and data[position] == 0xff:position += 1
                if position >= len(data):break
                marker = data[position];position += 1
                if marker in (0xd9,0xda):break
                if marker == 0x01 or 0xd0 <= marker <= 0xd8:continue
                if position+2 > len(data):break
                length = struct.unpack('>H',data[position:position+2])[0]
                if length < 2 or position+length > len(data):break
                if marker in (0xc0,0xc1,0xc2,0xc3,0xc5,0xc6,0xc7,0xc9,0xca,0xcb,0xcd,0xce,0xcf) and length >= 7:
                    height,width = struct.unpack('>HH',data[position+3:position+7]);size = (width,height);break
                position += length
        if size and all(0 < value <= 100000 for value in size):return size
    except (OSError,ValueError,struct.error):pass
    return None


def fitted_cover(width,height,bounds=(316,146,420,700)):
    """Preserve aspect, cap both image axes at 420 px and centre in the slot."""
    x,y,available_width,available_height = bounds
    scale = min(min(420,available_width)/max(1,width),
                min(420,available_height)/max(1,height))
    w,h = max(1,round(width*scale)),max(1,round(height*scale))
    return x+(available_width-w)//2,y+(available_height-h)//2,w,h


def dab_service_reference():
    """Match the native DAB service type; an IPTV station name is insufficient."""
    try:
        import NavigationInstance
        from enigma import eServiceReference
        nav = NavigationInstance.instance
        reference = nav and nav.getCurrentlyPlayingServiceReference()
        if reference and reference.type == eServiceReference.idServiceDAB:
            return reference
    except (AttributeError, ImportError, RuntimeError):
        pass
    return None


class WarderRadioCompactArtwork(WarderRadioArtwork):
    # The approved bundled fallback is pinned by the package graphics checks.
    FALLBACK_SIZE = (704,640)

    def __init__(self):
        WarderRadioArtwork.__init__(self)
        self._coverBounds = (316,146,420,700)
        self._normalCoverBounds = self._coverBounds
        self._fitLock = threading.Lock()
        self._fitGeneration = 0
        self._fitReady = None
        self._fitPending = False
        self._activeSize = None
        self._edges = []

    def postWidgetCreate(self,instance):
        self._edges = [eLabel(instance) for i in range(4)]
        for edge in self._edges:
            edge.setTransparent(0)
            edge.setBackgroundColor(parseColor('#003ccfff'))
            edge.hide()
        WarderRadioArtwork.postWidgetCreate(self,instance)

    def applySkin(self,desktop,parent):
        position = self._coverBounds[:2];size = self._coverBounds[2:]
        for name,value in self.skinAttributes or []:
            if name == 'position':position = tuple(map(int,value.split(',')))
            elif name == 'size':size = tuple(map(int,value.split(',')))
        self._coverBounds = position+size
        self._normalCoverBounds = self._coverBounds
        result = WarderRadioArtwork.applySkin(self,desktop,parent)
        if self._activeSize is not None:self._placeCover(self._activeSize)
        return result

    def _showPath(self,path):
        with self._fitLock:
            self._fitGeneration += 1
            generation = self._fitGeneration
            self._fitReady = None
            self._fitPending = path != self.FALLBACK_ARTWORK
        self._decodeToken += 1  # Immediately reject an older native decoder.
        self._picload = None
        if self.instance is not None:self.instance.hide()
        if path == self.FALLBACK_ARTWORK:
            if self.instance is not None:
                self._placeCover(self.FALLBACK_SIZE)
                WarderRadioArtwork._showPath(self,path)
            return
        def work():
            size = picture_size(path) or (1,1)
            with self._fitLock:
                if generation == self._fitGeneration:
                    self._fitReady = (generation,path,size)
        threading.Thread(target=work,name='WarderCoverSize',daemon=True).start()

    def _placeCover(self,size):
        self._activeSize = size
        x,y,w,h = fitted_cover(size[0],size[1],self._coverBounds)
        self.instance.move(ePoint(x,y))
        self.instance.resize(eSize(w,h))
        stroke = min(2,w,h)
        rectangles = ((0,0,w,stroke),(0,h-stroke,w,stroke),(0,0,stroke,h),(w-stroke,0,stroke,h))
        for edge,rectangle in zip(self._edges,rectangles):
            ex,ey,ew,eh = rectangle
            edge.move(ePoint(ex,ey));edge.resize(eSize(ew,eh));edge.show()

    def _dabSlidePath(self):
        # Slideshow has its own DAB-only window. This renderer keeps the one
        # existing song lookup and its cache/retry policy for every radio type.
        return ""

    def _updateCoverBounds(self):
        x,y,w,h = self._normalCoverBounds
        bounds = (x,y+(h+20)//2,w,(h-20)//2) if dab_service_reference() else self._normalCoverBounds
        if bounds != self._coverBounds:
            self._coverBounds = bounds
            if self._activeSize is not None:self._placeCover(self._activeSize)

    def _decodeSizedPicture(self):
        with self._fitLock:
            ready,self._fitReady = self._fitReady,None
        if ready is not None and ready[0] == self._fitGeneration and self.instance is not None:
            generation,path,size = ready
            self._fitPending = False
            self._placeCover(size)
            WarderRadioArtwork._showPath(self,path)

    def _clearPicture(self):
        with self._fitLock:
            self._fitGeneration += 1
            self._fitReady = None
            self._fitPending = False
        self._decodeToken += 1
        self._picload = None
        self._activeSize = None
        if self.instance is not None:self.instance.hide()
        for edge in self._edges:edge.hide()

    def _poll(self):
        if self.instance is None:return
        self._updateCoverBounds()
        self._decodeSizedPicture()
        WarderRadioArtwork._poll(self)
        if self._fitPending and self.instance is not None:
            self._timer.start(50,True)

    def preWidgetRemove(self,instance):
        with self._fitLock:
            self._fitGeneration += 1
            self._fitReady = None
            self._fitPending = False
        self._edges = []
        WarderRadioArtwork.preWidgetRemove(self,instance)
