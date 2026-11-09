"""Fail-closed ChannelSelection EPG canvas policy.

Only OpenATV 8.1 with an actively initialized e2egl graphics backend may
use the extra canvas. Installed GLES libraries or image build capability
alone are insufficient. Unknown runtime state falls back to native drawing.
"""


def _read_image_version(path):
    try:
        with open(path, "r") as stream:
            result = {}
            for line in stream:
                if "=" in line:
                    key, value = line.strip().split("=", 1)
                    result[key.lower().strip()] = value.strip().strip("'\\\"").lower()
            return result
    except (OSError, ValueError, TypeError):
        return {}


def allow_channel_epg_overlay(image_version_path="/etc/image-version", box_info=None, graphics_info=None):
    """Require OpenATV 8.1 and the active native e2egl backend.

    Test injections are optional; production reads the Enigma2 runtime.
    """
    if box_info is None:
        try:
            from Components.SystemInfo import BoxInfo
            box_info = BoxInfo
        except (ImportError, AttributeError):
            return False
    if graphics_info is None:
        try:
            from enigma import getGraphicsInfo
            graphics_info = getGraphicsInfo()
        except (ImportError, AttributeError, RuntimeError):
            return False
    try:
        data = _read_image_version(image_version_path)
        distro = str(box_info.getItem("distro") or data.get("distro") or data.get("creator") or "").lower()
        version = str(box_info.getItem("imgversion") or data.get("version") or "").lower()
        if distro not in ("openatv", "atv") and "openatv" not in distro:
            return False
        if version != "8.1" and not version.startswith("8.1."):
            return False
        # Runtime backend is authoritative. Requiring HasEGLRenderer
        # as well would incorrectly reject images that do not export
        # that optional capability key, even while EGL is active.
        return isinstance(graphics_info, dict) and graphics_info.get("backend") == "e2egl"
    except (AttributeError, RuntimeError, TypeError, ValueError):
        return False
