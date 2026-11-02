"""Adapt FullHDGlass captions to OpenPLi without changing files or controllers."""
from copy import deepcopy
from xml.etree.ElementTree import Element


COLOURS = ('key_red', 'key_green', 'key_yellow', 'key_blue')
GUI_CAPTIONS = {
    'ChannelSelection': COLOURS,
    'ChannelSelectionRadio': COLOURS,
    'SimpleChannelSelection': COLOURS[:2],
    'LocationBox': COLOURS[:2],
    'PluginBrowser': COLOURS[:2],
    'PluginBrowserList': COLOURS[:2],
    'PluginBrowserGrid': COLOURS[:2],
    'ServiceScan': COLOURS[:2],
}
SOURCE_CAPTIONS = {'TimerEditList': COLOURS,
                   'HotkeySetupSelect': COLOURS[:3]}
PLUGIN_ROW_HEIGHT = 90


def adapt_screen(element, plugin_row_height=PLUGIN_ROW_HEIGHT):
    """Clone a loaded template; retain all geometry, colours and native actions."""
    result = deepcopy(element)
    name = result.get('name')
    if name in ('PluginBrowser', 'PluginBrowserList', 'PluginBrowserGrid'):
        # OpenPLi supplies a GUI PluginList named "list", not OpenATV's two
        # source lists. Keeping only those conditional sources makes an empty
        # browser even though the native controller populated its own list.
        for widget in list(result):
            if widget.tag == 'widget' and widget.get('source') in ('pluginList', 'pluginGrid'):
                result.remove(widget)
        if result.find("widget[@name='list']") is None:
            result.insert(0, Element('widget', {
                'name':'list', 'position':'15,20', 'size':'1620,720',
                'itemHeight':str(plugin_row_height), 'scrollbarMode':'showOnDemand'}))
    if name in ('PluginBrowser', 'PluginBrowserList', 'PluginBrowserGrid', 'PluginDownloadBrowser'):
        for widget in result.findall("widget[@name='list']"):
            widget.set('itemHeight', str(plugin_row_height))
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


def install(registry, primary_skin, distro, font_registry=None):
    """Only replace this skin's in-memory entries on an identified OpenPLi."""
    if primary_skin != 'hd_glass17/skin.xml' or str(distro).strip().lower() != 'openpli':
        return 0
    # Native PluginList reads this skin alias when it constructs its content.
    # Both the content and its listbox need the same row height. The existing
    # description ends at y=81, so the historical 60 px alias clips that line.
    if font_registry is None:
        try:
            from skin import fonts as font_registry
        except ImportError:
            pass
    row_height = PLUGIN_ROW_HEIGHT
    if font_registry is not None:
        current = font_registry.get('PluginBrowser0', ('Regular', 30, row_height))
        row_height = max(row_height, int(current[2]))
        font_registry['PluginBrowser0'] = current[:2] + (row_height,) + current[3:]
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
        registry[key] = (adapt_screen(element, row_height), path)
        count += 1
    return count
