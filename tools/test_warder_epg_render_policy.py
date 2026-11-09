"""Behavioral regression for the fail-closed OpenATV 8.1 active-GLES EPG policy."""
from pathlib import Path
import importlib.util
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "source/package-root/usr/lib/enigma2/python/Plugins/Extensions/setupGlass17/warderEpgRenderPolicy.py"
spec = importlib.util.spec_from_file_location("warder_epg_policy", POLICY)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class Box:
    def __init__(self, distro="openatv", version="8.1.0~beta"):
        self.data = {"distro": distro, "imgversion": version}

    def getItem(self, name):
        return self.data.get(name)


class RenderPolicyTests(unittest.TestCase):
    def allowed(self, content, box=None, graphics=None):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "image-version"
            path.write_text(content)
            return module.allow_channel_epg_overlay(
                str(path),
                box if box is not None else Box(),
                graphics if graphics is not None else {"backend": "e2egl"},
            )

    def test_openatv_81_active_gles_allows_overlay(self):
        self.assertTrue(self.allowed("distro=openatv\nversion=8.1\n"))
        self.assertTrue(self.allowed("distro=openatv\nversion=8.1.0~beta\n", Box(version="8.1.0~beta")))

    def test_openatv_80_and_legacy_keep_native(self):
        for version in ("8.0", "8.0.1", "7.6"):
            self.assertFalse(self.allowed("distro=openatv\nversion=" + version, Box(version=version)))

    def test_other_images_keep_native(self):
        self.assertFalse(self.allowed("distro=openpli\nversion=8.1", Box(distro="openpli")))

    def test_framebuffer_and_unknown_backend_keep_native(self):
        for graphics in ({"backend": "framebuffer"}, {"backend": ""}, {}):
            self.assertFalse(self.allowed("distro=openatv\nversion=8.1", graphics=graphics))

    def test_missing_image_metadata_uses_box_info_only(self):
        self.assertTrue(module.allow_channel_epg_overlay(
            "/nonexistent/warder-image-version", Box(), {"backend": "e2egl"}
        ))
        self.assertFalse(module.allow_channel_epg_overlay(
            "/nonexistent/warder-image-version", Box(distro="", version=""), {"backend": "e2egl"}
        ))


if __name__ == "__main__":
    unittest.main()
