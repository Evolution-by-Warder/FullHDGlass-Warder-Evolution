"""Apply framed-OSD alignment while preserving the legacy MiniTV PiP lifecycle."""
from Components.Renderer.g17MiniTV import g17MiniTV
from Components.Renderer.WarderFramedPig import FramedVideoMixin


class WarderFramedMiniTV(FramedVideoMixin, g17MiniTV):
    pass
