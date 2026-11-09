"""Conservative performance fallback for verified legacy OpenATV images.

Do not infer the active graphics backend from loaded GL libraries: some GLES
implementations do not expose them by name. This initial guard targets only
OpenATV 8.0.x, where the expensive canvas overlay demonstrably slowed
ChannelSelection on an SF8008. Other images retain existing behavior.
"""


def allow_channel_epg_overlay(image_version_path="/etc/image-version"):
    try:
        with open(image_version_path, "r") as f:
            info = {}
            for raw in f:
                if "=" in raw:
                    key, value = raw.strip().split("=", 1)
                    info[key.strip().lower()] = value.strip().strip(chr(39) + chr(34)).lower()
        distro = (info.get("distro") or info.get("creator") or "").lower()
        version = (info.get("version") or "").lower()
        if "openatv" in distro or distro == "atv":
            if version == "8.0" or version.startswith("8.0."):
                return False
    except (OSError, ValueError, TypeError):
        pass
    return True
