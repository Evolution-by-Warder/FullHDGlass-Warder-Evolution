"""Behavioral tests for conservative OpenATV 8.0.x renderer fallback."""
from pathlib import Path
import importlib.util
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "source/package-root/usr/lib/enigma2/python/Plugins/Extensions/setupGlass17/warderEpgRenderPolicy.py"
spec = importlib.util.spec_from_file_location("warder_epg_policy", POLICY)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class RenderPolicyTests(unittest.TestCase):
    def allowed(self, content):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "image-version"
            path.write_text(content)
            return module.allow_channel_epg_overlay(str(path))

    def test_openatv_801_uses_fast_native_list(self):
        self.assertFalse(self.allowed("distro=openatv\nversion=8.0.1\n"))

    def test_openatv_80_uses_fast_native_list(self):
        self.assertFalse(self.allowed("creator=OpenATV\nversion=8.0\n"))

    def test_openatv_81_preserves_canvas_overlay(self):
        self.assertTrue(self.allowed("distro=openatv\nversion=8.1\n"))

    def test_other_images_preserve_existing_behavior(self):
        self.assertTrue(self.allowed("distro=openpli\nversion=8.0.1\n"))
        self.assertTrue(self.allowed("version=8.0.1\n"))

    def test_missing_metadata_preserves_existing_behavior(self):
        self.assertTrue(module.allow_channel_epg_overlay("/nonexistent/warder-image-version"))

if __name__ == "__main__":
    unittest.main()
