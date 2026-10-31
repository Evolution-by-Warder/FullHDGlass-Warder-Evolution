"""Paged static thumbnails; only explicit selection downloads animation frames."""
import json
from pathlib import Path
import tempfile
import threading
import xml.etree.ElementTree as ET

from Components.ActionMap import ActionMap
from Components.Label import Label
from Components.MenuList import MenuList
from Components.MultiContent import MultiContentEntryText, MultiContentEntryPixmapAlphaBlend
from Screens.Screen import Screen
from enigma import (eListbox, eListboxPythonMultiContent, ePoint, gFont, loadPNG,
                    BT_SCALE, BT_KEEP_ASPECT_RATIO, BT_HALIGN_CENTER, BT_VALIGN_CENTER)
from twisted.internet.threads import deferToThread

from . import warderSpinner as backend
from . import warderSpinnerOnline as online
from .warderDialogSkins import CHOICE_SKIN
from .warderUiText import ui_text


LIST_POSITION = (165, 208)
LIST_SIZE = (1590, 704)
ITEM_HEIGHT = 88
MIN_ITEM_WIDTH = 700
PREVIEW_SIZE = 72
PREVIEW_FLAGS = BT_SCALE | BT_KEEP_ASPECT_RATIO | BT_HALIGN_CENTER | BT_VALIGN_CENTER


def page_layout(width, height, grid=True):
    """Use complete readable cells; derive capacity from the actual widget."""
    columns = max(1, width // MIN_ITEM_WIDTH) if grid else 1
    rows = max(1, height // ITEM_HEIGHT)
    return columns, rows * columns, width // columns


def screen_skin():
    root = ET.fromstring(CHOICE_SKIN)
    root.set('name', 'WarderSpinnerChoice')
    widget = root.find("widget[@name='list']")
    widget.set('position', '%d,%d' % LIST_POSITION)
    widget.set('size', '%d,%d' % LIST_SIZE)
    widget.set('itemHeight', str(ITEM_HEIGHT))
    widget.set('font', 'Regular;28')
    widget.set('scrollbarMode', 'showNever')
    hint = root.find("widget[@name='hint']")
    hint.set('position', '165,920')
    hint.set('size', '1590,30')
    return ET.tostring(root, encoding='unicode')


class SpinnerChoice(Screen):
    skin = screen_skin()

    def __init__(self, session, selected='dove'):
        Screen.__init__(self, session)
        self.skinName = ['WarderSpinnerChoice']
        self.setTitle(ui_text('Spinner'))
        self['list'] = MenuList([], content=eListboxPythonMultiContent)
        self['list'].l.setItemHeight(ITEM_HEIGHT)
        self['list'].l.setFont(0, gFont('Regular', 28))
        self['list'].l.setFont(1, gFont('Regular', 22))
        self.columns, self.page_size, self.item_width = page_layout(*LIST_SIZE, grid=False)
        self['hint'] = Label(ui_text('Loading spinner list...'))
        self['line_red'] = Label('')
        self['line_green'] = Label('')
        self['key_red'] = Label(ui_text('Back'))
        self['key_green'] = Label(ui_text('Confirm selection'))
        self['actions'] = ActionMap(['OkCancelActions', 'ColorActions', 'DirectionActions'], {
            'ok': self.choose, 'green': self.choose, 'cancel': self.cancel, 'red': self.cancel,
            'up': lambda:self.step(-self.columns), 'down': lambda:self.step(self.columns),
            'left': lambda:self.step(-1), 'right': lambda:self.step(1),
        }, -3)
        self.selected, self.cursor, self.page = selected, 0, -1
        self.closed, self.busy, self.thumb_busy = False, False, False
        self.stop = threading.Event()
        self.generation = 0
        self.pending_page = None
        self.temp = tempfile.TemporaryDirectory(prefix='fullhdglass-spinner-previews-')
        self.pictures = {}
        self.rows = self.local_rows()
        self.onLayoutFinish.append(self.start)
        self.onClose.append(self.cleanup)

    def local_rows(self):
        catalog = backend.catalog()
        rows = []
        for key, theme in catalog['themes'].items():
            source = Path(catalog['downloaded_sources'].get(key, backend.SKIN_ROOT/'spinner-themes'/key))
            image = source/theme.get('preview_frame', theme['frames'][0]['name'])
            rows.append({'id':key, 'title':theme['title'], 'author':theme['author'],
                         'local_id':key, 'local_picture':str(image)})
        return rows

    def start(self):
        instance = self['list'].instance
        size = instance.size()
        grid = (hasattr(eListbox, 'orGrid') and hasattr(instance, 'setOrientation')
                and hasattr(instance, 'setItemWidth') and hasattr(self['list'].l, 'setItemWidth')
                and hasattr(self['list'].l, 'setOrientation'))
        self.columns, self.page_size, self.item_width = page_layout(size.width(), size.height(), grid)
        instance.setItemHeight(ITEM_HEIGHT)
        if grid:
            instance.setOrientation(eListbox.orGrid)
            self['list'].l.setOrientation(eListbox.orGrid)
            instance.setItemWidth(self.item_width)
            self['list'].l.setItemWidth(self.item_width)
            if hasattr(instance, 'setItemSpacing'):
                instance.setItemSpacing(ePoint(0, 0))
        if hasattr(self['list'], 'enableAutoNavigation'):
            self['list'].enableAutoNavigation(False)
        self.cursor = next((i for i,r in enumerate(self.rows) if r['id']==self.selected), 0)
        self.show_page()
        deferToThread(lambda:online.parse_catalog(online.fetch(online.CATALOG_URL, online.MAX_CATALOG))).addCallbacks(self.loaded, self.offline)

    def loaded(self, rows):
        if self.closed:
            return
        local = {r['id']:r for r in self.local_rows()}
        available = backend.catalog()['themes']
        for row in rows:
            key = row['id'] if row['id'] in available and online.frame_digest(available[row['id']]['frames'])==row['frames_sha256'] else 'dl-'+row['archive']['sha256'][:16]
            if key in local:
                row.update(local_id=key, local_picture=local[key]['local_picture'])
        self.rows = rows
        self.cursor = next((i for i,r in enumerate(rows) if r.get('local_id')==self.selected), 0)
        self.page = -1
        self.show_page()

    def offline(self, failure):
        if not self.closed:
            self['hint'].setText(ui_text('Online list unavailable. Installed spinners are available.'))

    def step(self, delta):
        if self.busy or not self.rows:
            return
        self.cursor = (self.cursor+delta) % len(self.rows)
        self.show_page()

    def show_page(self):
        page = self.cursor//self.page_size
        if page != self.page:
            self.page = page
            self.generation += 1
            self.pictures.clear()
            for path in Path(self.temp.name).glob('*.png'):
                path.unlink()
            self.pending_page = (self.generation, list(self.rows[page*self.page_size:(page+1)*self.page_size]))
            self.redraw()
            self.load_thumbnails()
        else:
            self['list'].moveToIndex(self.cursor % self.page_size)
        self['hint'].setText('%d / %d  ·  ' % (self.cursor+1, len(self.rows)) + ui_text('Choose with OK'))

    def redraw(self):
        if self.closed:
            return
        entries = []
        for row in self.rows[self.page*self.page_size:(self.page+1)*self.page_size]:
            item = [row,
                    MultiContentEntryText(pos=(96,8), size=(self.item_width-112,36), font=0, text=ui_text(row['title'])),
                    MultiContentEntryText(pos=(96,48), size=(self.item_width-112,30), font=1, text=row['author'])]
            image = self.pictures.get(row['id'])
            if image is None and row.get('local_picture'):
                try:image = loadPNG(row['local_picture'])
                except Exception:image = None
            if image is not None:
                item.append(MultiContentEntryPixmapAlphaBlend(pos=(8,8), size=(PREVIEW_SIZE,PREVIEW_SIZE), png=image, flags=PREVIEW_FLAGS))
            entries.append(item)
        self['list'].setList(entries)
        self['list'].moveToIndex(self.cursor % self.page_size)

    def load_thumbnails(self):
        if self.closed or self.thumb_busy or self.pending_page is None:
            return
        generation, rows = self.pending_page
        self.pending_page = None
        self.thumb_busy = True
        def worker():
            pictures = []
            for row in rows:
                if self.stop.is_set() or generation != self.generation:
                    break
                if row.get('local_picture') or 'thumbnail' not in row:
                    continue
                try:
                    raw = online.checked_resource(row['thumbnail'], 'png', online.MAX_THUMB)
                    pictures.append((row['id'], online.png(raw, (80,80))))
                except Exception:
                    pass  # A missing picture never hides a selectable name.
            return generation, pictures
        deferToThread(worker).addBoth(self.thumbnails_done)

    def thumbnails_done(self, result):
        self.thumb_busy = False
        if self.closed:
            return
        if isinstance(result, tuple) and result[0] == self.generation:
            for key, raw in result[1]:
                path = Path(self.temp.name)/(key+'.png')
                path.write_bytes(raw)
                self.pictures[key] = loadPNG(str(path))
            self.redraw()
        self.load_thumbnails()

    def choose(self):
        if self.busy or not self.rows:
            return
        row = self.rows[self.cursor]
        if row.get('local_id'):
            self.close((row['title'], row['local_id']))
            return
        self.busy = True
        self['hint'].setText(ui_text('Downloading selected spinner...'))
        def worker():
            raw = online.checked_resource(row['archive'], 'zip', online.MAX_ZIP)
            if self.stop.is_set():
                return None
            return online.install_selected(row, raw, backend)
        deferToThread(worker).addCallbacks(lambda key:self.downloaded(row, key), self.failed)

    def downloaded(self, row, key):
        if not self.closed and key is not None:
            self.close((row['title'], key))

    def failed(self, failure):
        if not self.closed:
            self.busy = False
            self['hint'].setText(ui_text('Spinner download failed. Try again.'))

    def cancel(self):
        self.close(None)

    def cleanup(self):
        self.closed = True
        self.stop.set()
        self.pictures.clear()
        self.temp.cleanup()
