"""Place the skin shortcut under Main menu > Ostatné when this submenu exists.

Read actual Enigma2 menu.xml rather than assuming every image has an
identically named submenu. Use Main menu only as a fallback.
"""

def target_key(dom=None):
    if dom is None:
        try:
            from Screens.Menu import menuDom
            dom = menuDom()
        except (ImportError, AttributeError, TypeError, RuntimeError):
            return 'mainmenu'
    if dom is None:
        return 'mainmenu'
    try:
        main = dom.find(".//menu[@key='mainmenu']")
        if main is None:
            return 'mainmenu'
        for child in main.findall('./menu'):
            label = str(child.get('text', '')).strip().lower()
            key = str(child.get('key', '')).strip()
            if key and (label in ('other', 'others', 'other items', 'ostatné', 'ostatne', 'ostatní', 'sonstiges')
                        or key.lower() in ('other', 'others', 'misc', 'extras')):
                return key
    except (AttributeError, TypeError, ValueError):
        pass
    return 'mainmenu'
