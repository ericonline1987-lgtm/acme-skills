"""Marketplace and plugin manifests agree with each other and with the folders."""
import re
import unittest

from helpers import PLUGINS_DIR, ROOT, plugin_dirs, read_json

SEMVER = re.compile(r"^\d+\.\d+\.\d+$")


class ManifestTests(unittest.TestCase):
    def setUp(self):
        self.marketplace = read_json(ROOT / ".claude-plugin" / "marketplace.json")
        self.entries = {p["name"]: p for p in self.marketplace["plugins"]}

    def test_marketplace_has_required_fields(self):
        for field in ("name", "owner", "plugins"):
            self.assertIn(field, self.marketplace)
        self.assertTrue(self.marketplace["plugins"], "marketplace lists no plugins")

    def test_every_plugin_folder_is_listed_and_every_listing_exists(self):
        folders = {p.name for p in plugin_dirs()}
        self.assertEqual(folders, set(self.entries), "marketplace and plugins/ disagree")
        for name, entry in self.entries.items():
            source = (ROOT / entry["source"]).resolve()
            self.assertEqual(source, (PLUGINS_DIR / name).resolve(), f"{name}: source path is wrong")

    def test_plugin_manifests_match_folder_and_marketplace(self):
        for plugin in plugin_dirs():
            manifest = read_json(plugin / ".claude-plugin" / "plugin.json")
            with self.subTest(plugin=plugin.name):
                self.assertEqual(manifest["name"], plugin.name)
                self.assertRegex(manifest["version"], SEMVER)
                self.assertTrue(manifest.get("description", "").strip())
                self.assertEqual(manifest["version"], self.entries[plugin.name]["version"],
                                 "bump the version in plugin.json and marketplace.json together")

    def test_plugin_names_are_lowercase_hyphenated(self):
        for name in self.entries:
            self.assertRegex(name, r"^[a-z0-9]+(-[a-z0-9]+)*$")


if __name__ == "__main__":
    unittest.main()
