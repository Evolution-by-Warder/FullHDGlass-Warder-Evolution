"""Keep vertical list viewports within their allocated area and on whole rows."""
from functools import wraps


def fit_title(component, parent, label):
    instance = getattr(component, 'instance', None)
    if label is None or not isinstance(instance, label):
        return False
    try:
        titles = [parent.get(key) for key in ('Title', 'title', 'ScreenPath')]
        source = component
        seen = set()
        while source is not None and id(source) not in seen:
            if any(source is title for title in titles if title is not None):
                break
            seen.add(id(source))
            source = getattr(source, 'source', None)
        else:
            return False
        font = instance.getFont()
        # Preserve deliberately multiline titles. Compact header fields have
        # room for one line only; a long breadcrumb must not wrap halfway below it.
        if instance.size().height() < 2 * int(font.pointSize):
            instance.setNoWrap(1)
            return True
    except (AttributeError, TypeError, ValueError):
        pass
    return False


def fit(component, listbox, make_size):
    instance = getattr(component, 'instance', None)
    if not isinstance(instance, listbox):
        return False
    try:
        if instance.getOrientation() != listbox.orVertical:
            return False
        # Spaced/grid-style layouts have a different native packing formula.
        attributes = dict(getattr(component, 'skinAttributes', None) or ())
        if any(int(part.strip()) for part in attributes.get('itemSpacing', '0,0').split(',')):
            return False
        size = instance.size()
        current = (size.width(), size.height())
        previous = getattr(component, '_warder_list_row_area', None)
        if previous is None or previous[0] is not instance or current not in (previous[1], previous[2]):
            allocated = current
        else:
            allocated = previous[1]
        row = int(instance.getItemHeight())
        if row <= 0 or allocated[0] <= 0 or allocated[1] < row:
            return False
        target = (allocated[0], allocated[1] // row * row)
        if current != target:
            instance.resize(make_size(*target))
        component._warder_list_row_area = (instance, allocated, target)
        return current != target
    except (AttributeError, TypeError, ValueError):
        # Older image backends may not expose the optional geometry APIs.
        return False


def install(gui_component, is_active, listbox, make_size, label=None):
    original = gui_component.applySkin
    if getattr(original, '_warder_list_rows', False):
        return False

    @wraps(original)
    def apply_skin(self, desktop, parent):
        result = original(self, desktop, parent)
        if not is_active():
            return result
        fit_title(self, parent, label)
        if not isinstance(getattr(self, 'instance', None), listbox):
            return result
        # applySkin has applied the desktop scale and skin's size/itemHeight.
        # A subclass can still change its content row height afterwards, so
        # repeat after the screen's own layout callbacks and when reopening.
        self._warder_list_row_area = None
        fit(self, listbox, make_size)
        callbacks = getattr(parent, 'onLayoutFinish', None)
        if callbacks is not None and not getattr(parent, '_warder_list_rows_finish', False):
            def finish():
                if is_active():
                    for component in list(parent.values()) + list(getattr(parent, 'renderer', ())):
                        fit(component, listbox, make_size)
                        fit_title(component, parent, label)
            callbacks.append(finish)
            if hasattr(parent, 'onShow'):
                parent.onShow.append(finish)
            parent._warder_list_rows_finish = True
        return result

    apply_skin._warder_list_rows = True
    gui_component.applySkin = apply_skin
    return True
