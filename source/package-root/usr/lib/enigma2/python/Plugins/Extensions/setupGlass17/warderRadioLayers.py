# -*- coding: utf-8 -*-
"""Keep the native radio OSD visible below transparent InfoPanel artwork."""
import re
from xml.etree import ElementTree as ET


def prepare_radio_layers(skin):
    """Keep each selected InfoPanel graphic in both TV and radio modes.

    ePixmap's alpha-off path marks a full-size widget opaque. This lets the
    desktop discard the lower RDS window even where the PNG has alpha zero.
    Radio alpha-blends the original InfoPanel graphic over the native RDS
    scene. Its opaque lower panel separates the InfoBar fields from the radio
    footer, while transparent areas preserve the scene above. TV retains its
    original image and alpha mode.
    Only self-contained full-frame ePixmap tags are touched; all other skin
    text, widgets, coordinates, callbacks and artwork remain as supplied.
    """
    def replace(match):
        original = match.group(0)
        try:
            panel = ET.fromstring(original)
        except ET.ParseError:
            return original
        attributes = panel.attrib
        if attributes.get("position", "").replace(" ", "") != "0,0":
            return original
        if attributes.get("size", "").replace(" ", "") != "1920,1080":
            return original
        if not attributes.get("pixmap", "").lower().endswith(".png"):
            return original
        if attributes.get("alphaTest", attributes.get("alphatest", "off")) != "off":
            return original
        output = []
        for converter, radio in (("WarderTVOnly", False), ("WarderRadioOnly", True)):
            values = dict(attributes)
            values.pop("name", None)
            values.update(source="session.CurrentService", render="Pixmap")
            if radio:
                values.pop("alphaTest", None)
                values.pop("transparent", None)
                values["alphatest"] = "blend"
            widget = ET.Element("widget", values)
            ET.SubElement(widget, "convert", type=converter)
            ET.SubElement(widget, "convert", type="ConditionalShowHide")
            output.append(ET.tostring(widget, encoding="unicode"))
        return "\n".join(output)

    return re.sub(r"<ePixmap\b[^<>]*/>", replace, skin)
