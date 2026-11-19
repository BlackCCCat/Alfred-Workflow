import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
import config


class RuntimeSettingsTests(unittest.TestCase):
    def test_ui_overrides_apply_to_quick_commands_and_reset_independently(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "runtime_settings.json"
            environment = {
                "rime_engine": "cobra",
                "source": "github",
                "schema": "base",
                "github_download_accelerator": "gh-proxy",
            }
            with patch.object(config, "RUNTIME_SETTINGS_FILE", path), patch.dict(os.environ, environment):
                config.set_runtime_engine("squirrel")
                config.set_runtime_option("source", "cnb")
                config.set_runtime_option("schema", "moqi")
                config.set_runtime_option("github_download_accelerator", "none")
                self.assertEqual(config.RimeConfig.engine(), "squirrel")
                self.assertEqual(config.RimeConfig.source(), "cnb")
                self.assertEqual(config.RimeConfig.schema(), "moqi")
                self.assertEqual(config.RimeConfig.github_download_accelerator(), "")

                config.clear_runtime_engine()
                self.assertEqual(config.RimeConfig.engine(), "cobra")
                self.assertEqual(config.RimeConfig.source(), "cnb")
                config.clear_runtime_option("source")
                config.clear_runtime_option("schema")
                config.clear_runtime_option("github_download_accelerator")
                self.assertEqual(config.RimeConfig.source(), "github")
                self.assertEqual(config.RimeConfig.schema(), "base")
                self.assertEqual(config.RimeConfig.github_download_accelerator(), "gh-proxy")
                self.assertFalse(path.exists())

    def test_invalid_runtime_choice_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory, patch.object(config, "RUNTIME_SETTINGS_FILE", Path(directory) / "settings.json"):
            with self.assertRaises(ValueError):
                config.set_runtime_option("source", "unknown")
            with self.assertRaises(ValueError):
                config.clear_runtime_option("unknown")


if __name__ == "__main__":
    unittest.main()
