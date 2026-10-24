"""Owned settings dialogs. Native Enigma2 screens remain untouched elsewhere."""
from Components.ActionMap import ActionMap
from Components.Label import Label
from Components.MenuList import MenuList
from Components.ScrollLabel import ScrollLabel
from Screens.Screen import Screen
from Screens.MessageBox import MessageBox as NativeMessageBox
from Screens.InputBox import InputBox as NativeInputBox
from .warderDialogSkins import MESSAGE_SKIN, CHOICE_SKIN, INPUT_SKIN
from .warderUiText import ui_text
from .warderUpdateText import update_text
from Components.config import config


class MessageText(ScrollLabel):
    def applySkin(self, desktop, parent):
        # ScrollLabel applies zPosition to its inner labels, not its outer
        # eWidget. Raise the container above the opaque settings panel too.
        result = ScrollLabel.applySkin(self, desktop, parent)
        self.instance.setZPosition(5)
        return result


class MessageBox(NativeMessageBox):
    skin = MESSAGE_SKIN

    def __init__(self, session, *args, **kwargs):
        NativeMessageBox.__init__(self, session, *args, **kwargs)
        self.skin = MESSAGE_SKIN
        self.skinName = ["WarderSettingsMessage"]
        self["text"] = MessageText(self.text)
        self["line_red"] = Label("")
        self["line_green"] = Label("")
        self["key_red"] = Label(ui_text("Back"))
        self["key_green"] = Label(update_text("confirm", "FullHDGlass Warder Evolution", language=config.osd.language.value) if self.list else "")
        enabled = kwargs.get("enable_input", True) and kwargs.get("enableInput", True)
        self["warderActions"] = ActionMap(["ColorActions"], {"red": self.cancel, "green": self.select}, -3)
        self["warderActions"].setEnabled(enabled)
        self["warderScroll"] = ActionMap(["DirectionActions"], {"up": self["text"].pageUp, "down": self["text"].pageDown}, -3)
        self["warderScroll"].setEnabled(enabled and not bool(self.list))
        if not self.list:
            self["line_green"].hide()
        if not enabled:
            self["line_red"].hide()
            self["key_red"].hide()
            self["key_green"].hide()
        self.onClose.append(self.timer.stop)

    def autoResize(self):
        # The settings layout has explicit bounds independent of text length.
        pass


class ChoiceBox(Screen):
    skin = CHOICE_SKIN

    def __init__(self, session, title="", list=None, keys=None, selection=0, **kwargs):
        Screen.__init__(self, session)
        self.skinName = ["WarderSettingsChoice"]
        self.setTitle(title or kwargs.get("windowTitle", ""))
        self["list"] = MenuList(list or [], enableWrapAround=True)
        self["line_red"] = Label("")
        self["line_green"] = Label("")
        self["key_red"] = Label(ui_text("Back"))
        self["key_green"] = Label(ui_text("Confirm selection"))
        self["hint"] = Label(ui_text("Choose with OK"))
        self["actions"] = ActionMap(["OkCancelActions", "ColorActions"], {
            "ok": self.choose, "green": self.choose,
            "cancel": self.cancel, "red": self.cancel,
        }, -2)
        self.warderSelection = selection
        self.onLayoutFinish.append(self._warderLayoutFinished)

    def _warderLayoutFinished(self):
        # OpenATV requires a bound method; plain functions are treated as script text.
        self["list"].moveToIndex(self.warderSelection)

    def choose(self):
        current = self["list"].getCurrent()
        if current is not None:
            self.close(current)

    def cancel(self):
        self.close(None)


class InputBox(NativeInputBox):
    skin = INPUT_SKIN

    def __init__(self, session, *args, **kwargs):
        NativeInputBox.__init__(self, session, *args, **kwargs)
        self.skin = INPUT_SKIN
        self.skinName = ["WarderSettingsInput"]
        self["line_red"] = Label("")
        self["line_green"] = Label("")
        self["key_red"] = Label(ui_text("Back"))
        self["key_green"] = Label(ui_text("Confirm"))
        self["warderActions"] = ActionMap(["ColorActions"], {"red": self.cancel, "green": self.go}, -3)
