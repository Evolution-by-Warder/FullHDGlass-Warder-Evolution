"""Native clipped eLabel with automatic plain-text scrolling and child-process I/O."""
import json
import os
import time
from Components.Renderer.Renderer import Renderer
from Components.Converter.WarderRadioOnly import is_radio_reference
from Components.Converter.WarderRadioMetadata import current_song, native_song, split_song
from enigma import eLabel, eWidget, ePoint, eSize, eTimer, gFont, iRdsDecoder
import NavigationInstance
from Plugins.Extensions.setupGlass17.warderLyrics import identity


def message(kind):
    from Components.Language import language
    code=language.getLanguage().split('_')[0]
    rows={
        'sk':('Čakám na údaje o skladbe.','Vyhľadávam text piesne…','Text piesne sa nenašiel.','Text piesne je dočasne nedostupný.'),
        'cs':('Čekám na údaje o skladbě.','Vyhledávám text písně…','Text písně nebyl nalezen.','Text písně je dočasně nedostupný.'),
        'de':('Warte auf Titelinformationen.','Liedtext wird gesucht…','Kein passender Liedtext gefunden.','Liedtext vorübergehend nicht verfügbar.'),
        'hu':('Várakozás a dal adataira.','Dalszöveg keresése…','Nem található megfelelő dalszöveg.','A dalszöveg átmenetileg nem érhető el.'),
        'ru':('Ожидание данных о песне.','Поиск текста песни…','Подходящий текст песни не найден.','Текст песни временно недоступен.'),
        'fr':('En attente des informations du titre.','Recherche des paroles…','Aucune parole correspondante trouvée.','Paroles temporairement indisponibles.'),
        'it':('In attesa dei dati del brano.','Ricerca del testo…','Nessun testo corrispondente trovato.','Testo temporaneamente non disponibile.'),
        'es':('Esperando los datos de la canción.','Buscando la letra…','No se encontró una letra coincidente.','Letra temporalmente no disponible.')}
    fallback=('Waiting for song information.','Looking up lyrics…','No matching lyrics found.','Lyrics temporarily unavailable.')
    return rows.get(code,fallback)[('waiting','loading','missing','offline').index(kind)]


class LyricsWorker:
    def __init__(self, callback):
        self.callback = callback
        self.output = bytearray()
    def outReceived(self, data):
        if len(self.output)+len(data) <= 131072:self.output.extend(data)
    def complete(self, code):
        result = None
        if code == 0:
            try:result = json.loads(self.output.decode('utf-8'))
            except (ValueError, UnicodeError):pass
        self.callback(result)


class WarderRadioLyrics(Renderer):
    GUI_WIDGET = eWidget

    def __init__(self):
        Renderer.__init__(self)
        self.label = None
        self._font = ('Regular',34)
        self._worker = None
        self._key = None
        self._pending_since = 0
        self._requested = None
        self._generation = 0
        self._text = ''
        self._offset = 0
        self._overflow = 0
        self._pause_until = 0
        self._shown = True
        self._timer = eTimer();self._timer.callback.append(self._poll)
        self._scroll = eTimer();self._scroll.callback.append(self._tick)
        self._timeout = eTimer();self._timeout.callback.append(self._kill_worker)

    def postWidgetCreate(self, instance):
        Renderer.postWidgetCreate(self, instance)
        instance.setTransparent(1)
        self.label = eLabel(instance)
        self.label.setTransparent(1)
        self.label.setNoWrap(0)
        self.label.setFont(gFont(*self._font))
        from skin import parseColor
        self.label.setForegroundColor(parseColor('#00ffffff'))
        self._set_text(message('waiting'))
        self._timer.start(750)

    def applySkin(self, desktop, parent):
        attributes = []
        for name, value in self.skinAttributes or []:
            if name == 'font':
                family, size = value.split(';');self._font = (family,int(size))
            else:attributes.append((name,value))
        self.skinAttributes = attributes
        result = Renderer.applySkin(self,desktop,parent)
        if self.label is not None:
            self.label.setFont(gFont(*self._font))
            self._set_text(self._text)
        return result

    def _set_text(self, text):
        self._text = text
        self._offset = 0
        self._scroll.stop()
        if self.label is None or self.instance is None:return
        width = max(1,self.instance.size().width())
        viewport = max(1,self.instance.size().height())
        self.label.move(ePoint(0,0))
        self.label.resize(eSize(width,viewport))
        self.label.setText(text)
        height = max(viewport,self.label.calculateSize().height()+self._font[1]) if text else viewport
        self.label.resize(eSize(width,height))
        self._overflow = max(0,height-viewport)
        self._pause_until = time.monotonic()+4
        if self._overflow and self._shown:self._scroll.start(80)

    def _tick(self):
        if not self._shown or self.label is None or time.monotonic() < self._pause_until:return
        if self._offset >= self._overflow:
            self._offset = 0
            self._pause_until = time.monotonic()+5
        else:
            self._offset = min(self._overflow,self._offset+1)
            if self._offset == self._overflow:self._pause_until=time.monotonic()+6
        self.label.move(ePoint(0,-self._offset))

    def _kill_worker(self):
        worker,self._worker=self._worker,None
        self._timeout.stop()
        if worker is not None:
            try:worker.transport.kill()
            except Exception:pass

    def _poll(self):
        try:
            nav=NavigationInstance.instance
            reference=nav and nav.getCurrentlyPlayingServiceReference()
            service=nav and nav.getCurrentService()
            if not self._shown or not is_radio_reference(reference):
                candidate=None
            else:
                artist,title=native_song(service)
                announcement = bool(title and not artist)
                if not (artist and title) and not announcement:
                    decoder=service and service.rdsDecoder()
                    artist,title=split_song(decoder.getText(iRdsDecoder.RadioText) if decoder else '')
                if not (artist and title) and not announcement:artist,title=current_song(service,reference)
                candidate=(reference.toString(),identity(artist),identity(title)) if artist and title else None
        except Exception:
            candidate=None;artist=title=''
        if candidate != self._key:
            self._generation += 1
            self._key=candidate;self._requested=None
            self._pending_since=time.monotonic()
            self._kill_worker();self._set_text(message('waiting'))
        if candidate is None or self._requested == candidate or time.monotonic()-self._pending_since < 2:return
        self._requested=candidate
        self._set_text(message('loading'))
        generation=self._generation
        def finished(result):
            if generation != self._generation:return
            self._worker=None;self._timeout.stop()
            if isinstance(result,dict) and result.get('text'):
                self._set_text(result['text'])
            else:
                self._set_text(message('offline' if not isinstance(result,dict) or result.get('status') == 'offline' else 'missing'))
        try:
            from Plugins.Extensions.setupGlass17.warderHelpPreview import _NativeLoop
            from Plugins.Extensions.setupGlass17 import warderLyrics
            worker=LyricsWorker(finished);self._worker=worker
            executable='/usr/bin/python3';helper=os.path.abspath(warderLyrics.__file__)
            _NativeLoop().spawnProcess(worker,executable,[executable,helper,artist,title],env=dict(os.environ))
            self._timeout.start(20000,True)
        except Exception:finished(None)

    def changed(self, what):
        if self.instance is not None:self._poll()

    def onShow(self):
        self._shown=True;self._timer.start(750)
        if self._overflow:self._scroll.start(80)

    def onHide(self):
        self._shown=False;self._timer.stop();self._scroll.stop()
        self._generation+=1;self._requested=None;self._kill_worker()

    def preWidgetRemove(self, instance):
        self.onHide();self.label=None
        Renderer.preWidgetRemove(self,instance)
