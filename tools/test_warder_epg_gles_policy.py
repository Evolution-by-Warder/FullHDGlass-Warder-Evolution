"""Unit tests for the conservative OpenATV 8.1 / e2egl EPG gate."""
import importlib.util
import os
import tempfile
import unittest

ROOT = os.path.dirname(os.path.dirname(__file__))
POLICY = os.path.join(ROOT, "source/package-root/usr/lib/enigma2/python/Plugins/Extensions/setupGlass17/warderEpgRenderPolicy.py")
spec = importlib.util.spec_from_file_location("warderEpgRenderPolicy", POLICY)
policy = importlib.util.module_from_spec(spec)
spec.loader.exec_module(policy)


class Info:
    def __init__(self, distro="openatv", version="8.1", e2egl=True):
        self.data = {"distro": distro, "imgversion": version, "HasEGLRenderer": e2egl}

    def getItem(self, key):
        return self.data.get(key)


class PolicyTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.NamedTemporaryFile(mode="w", delete=False)
        self.temp.write("distro=openatv\nversion=8.1\n")
        self.temp.close()

    def tearDown(self):
        os.unlink(self.temp.name)

    def allowed(self, **kwargs):
        return policy.allow_channel_epg_overlay(self.temp.name, Info(**kwargs), {"backend": "e2egl"})

    def test_beta_and_daily_builds(self):
        for version in ("8.1.0~beta", "8.1.1", "8.1.25"):
            self.assertTrue(self.allowed(version=version))

    def test_active_e2egl(self):
        self.assertTrue(self.allowed())

    def test_legacy_and_other_images(self):
        for version in ("7.6", "8.0", "8.0.1", "8.2", ""):
            self.assertFalse(self.allowed(version=version))
        self.assertFalse(self.allowed(distro="openpli"))

    def test_optional_capability_key_not_required_when_runtime_is_active(self):
        # Some image builds lack HasEGLRenderer. The native active backend
        # is a stronger signal than that optional capability flag.
        for capability in (None, False, 0, "off", "", "unknown"):
            self.assertTrue(self.allowed(e2egl=capability))

    def test_native_framebuffer_disables_overlay(self):
        self.assertFalse(policy.allow_channel_epg_overlay(self.temp.name, Info(),
                                                          {"backend": "framebuffer"}))

    def test_unknown_backend_disables_overlay(self):
        self.assertFalse(policy.allow_channel_epg_overlay(self.temp.name, Info(),
                                                          {"backend": ""}))

    def test_active_string_backend(self):
        self.assertTrue(self.allowed(e2egl="active"))

    def test_plugin_wires_gate_into_default_menu_and_runtime_skin(self):
        plugin_path = os.path.join(ROOT,
            "source/package-root/usr/lib/enigma2/python/Plugins/Extensions/setupGlass17/plugin.py")
        with open(plugin_path, encoding="utf-8") as stream:
            source = stream.read()
        self.assertIn("ConfigYesNo(default=allow_channel_epg_overlay())", source)
        self.assertIn("epg_scroll_enabled = (allow_channel_epg_overlay()", source)
        self.assertIn("if allow_channel_epg_overlay():", source)

    def test_unknown_image_fails_closed(self):
        self.assertFalse(policy.allow_channel_epg_overlay("/no/such/path", Info(distro="", version="", e2egl=True), {"backend": "e2egl"}))


if __name__ == "__main__":
    unittest.main()
