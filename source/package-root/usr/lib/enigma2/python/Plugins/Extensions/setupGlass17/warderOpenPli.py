"""Adapt FullHDGlass captions to OpenPLi without changing files or controllers."""
from copy import deepcopy


COLOURS = ('key_red', 'key_green', 'key_yellow', 'key_blue')
GUI_CAPTIONS = {
    'ChannelSelection': COLOURS,
    'ChannelSelectionRadio': COLOURS,
    'SimpleChannelSelection': COLOURS[:2],
    'LocationBox': COLOURS[:2],
    'PluginBrowser': COLOURS[:2],
    'ServiceScan': COLOURS[:2],
}
SOURCE_CAPTIONS = {'TimerEditList': COLOURS,
                   'HotkeySetupSelect': COLOURS[:3]}


def adapt_screen(element):
    """Clone a loaded template; retain all geometry, colours and native actions."""
    result = deepcopy(element)
    name = result.get('name')
    for widget in result.iter('widget'):
        field = widget.get('name') or widget.get('source')
        if not field or '.' in field:
            continue
        # Some OpenATV captions/information fields do not exist in OpenPLi.
        # Let OpenPLi's own conditional handling skip only absent components.
        # Existing explicit visibility conditions keep their original meaning.
        if not any(key in widget.attrib for key in ('conditional', 'includes', 'excludes')):
            widget.set('conditional', field)
        if field in GUI_CAPTIONS.get(name, ()) and widget.get('source') == field:
            # Reviewed captions have a plain Label renderer, no converters.
            if widget.get('render') == 'Label' and not list(widget):
                widget.attrib.pop('source')
                widget.attrib.pop('render')
                widget.set('name', field)
        elif field in SOURCE_CAPTIONS.get(name, ()) and widget.get('name') == field:
            widget.attrib.pop('name')
            widget.set('source', field)
            widget.set('render', 'Label')
    return result


def install(registry, primary_skin, distro):
    """Only replace this skin's in-memory entries on an identified OpenPLi."""
    if primary_skin != 'hd_glass17/skin.xml' or str(distro).strip().lower() != 'openpli':
        return 0
    count = 0
    prefix = '/usr/share/enigma2/hd_glass17/'
    # OpenPLi spells its modern controller VirtualKeyBoard. The historical
    # same-named template has neither prompt nor modern colour/help captions.
    # Reuse the already packaged complete keyboard, retaining native actions.
    modern_keyboard = registry.get('VirtualKeyboard')
    for key, entry in list(registry.items()):
        element, path = entry
        if not isinstance(path, str) or not (path == prefix[:-1] or path.startswith(prefix)):
            continue
        if key == 'VirtualKeyBoard' and modern_keyboard:
            modern, modern_path = modern_keyboard
            if isinstance(modern_path, str) and modern_path.startswith(prefix):
                element = deepcopy(modern)
                element.set('name', key)
        registry[key] = (adapt_screen(element), path)
        count += 1
    return count
