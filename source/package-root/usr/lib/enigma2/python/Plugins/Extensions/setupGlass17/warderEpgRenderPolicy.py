"""Fail-closed ChannelSelection EPG canvas policy.

Only OpenATV 8.1 with an explicitly active e2egl feature may use the
extra canvas. Merely having GLES libraries installed is insufficient.
If the current image does not expose a trustworthy runtime feature flag,
keep the native renderer and hide its optional setting.
"""


def _enabled(value):
    if value is True or value == 1:
        return True
    return isinstance(value, str) and value.strip().lower() in ("true", "yes", "on", "1", "enabled", "active")


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
    """Require OpenATV 8.1, EGL capability, and the active e2egl backend.

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
        # HasEGLRenderer reports capability; getGraphicsInfo reports
        # the active native graphics device. Unknown means fallback.
        return (_enabled(box_info.getItem("HasEGLRenderer"))
                and isinstance(graphics_info, dict)
                and graphics_info.get("backend") == "e2egl")
    except (AttributeError, RuntimeError, TypeError, ValueError):
        return False
