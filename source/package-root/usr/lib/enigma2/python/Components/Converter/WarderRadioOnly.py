# -*- coding: utf-8 -*-
# Radio and TV converters deliberately have independent concrete classes:
# skin.py shares converters with isinstance(), including subclasses.
from Components.Converter.Converter import Converter
from Components.Element import cached
import NavigationInstance


def is_native_dab(ref):
    try:
        from enigma import eServiceReference
        return ref is not None and ref.type == eServiceReference.idServiceDAB
    except (ImportError, AttributeError):
        return False


def is_radio_reference(ref):
    try:
        from ServiceReference import isRadioServiceReference
        return bool(isRadioServiceReference(ref)) if ref is not None else False
    except (ImportError, AttributeError, TypeError, ValueError):
        pass
    if is_native_dab(ref):
        return True
    try:
        fields = ref.toString().split(":") if ref is not None else []
        return len(fields) > 2 and fields[2].upper() in ("2", "A")
    except Exception:
        return False


def is_radio_source(source):
    ref = None
    try:
        getter = getattr(source, "getCurrentServiceReference", None)
        ref = getter() if callable(getter) else getattr(source, "serviceref", None)
    except Exception:
        pass
    if ref is None:
        try:
            nav = NavigationInstance.instance
            ref = nav.getCurrentlyPlayingServiceReference() if nav else None
        except Exception:
            pass
    return is_radio_reference(ref)


class WarderRadioOnly(Converter):
    def __init__(self, type):
        Converter.__init__(self, type)

    @cached
    def getBoolean(self):
        return is_radio_source(self.source)

    boolean = property(getBoolean)

    def changed(self, what):
        Converter.changed(self, what)
