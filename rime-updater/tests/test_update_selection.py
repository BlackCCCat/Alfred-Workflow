import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
import main
import wanxiang
from config import RimeConfig


class UpdateSelectionTests(unittest.TestCase):
    def test_cnb_model_release_is_found_after_tenth_page(self):
        def request_json(_url, source=None, params=None):
            page = (params or {}).get("page", 1)
            release = {"tag_name": "model" if page == 11 else f"v{page}.0.0", "assets": []}
            return {"releases": [release]}, {"X-Cnb-Total": "11", "X-Cnb-Page-Size": "1"}

        with patch.object(RimeConfig, "source", return_value="cnb"), patch.object(wanxiang, "request_json", side_effect=request_json) as request:
            releases = wanxiang.list_releases(include_model=True)
        self.assertEqual(request.call_count, 11)
        self.assertEqual(wanxiang._release_tag(releases[-1]), "model")

    def test_cnb_model_release_is_found_without_total_header(self):
        def request_json(_url, source=None, params=None):
            page = (params or {}).get("page", 1)
            release = {"tag_name": "model" if page == 13 else f"v{page}.0.0", "assets": []}
            return {"releases": [release]}, {}

        with patch.object(RimeConfig, "source", return_value="cnb"), patch.object(wanxiang, "request_json", side_effect=request_json) as request:
            releases = wanxiang.list_releases(include_model=True)
        self.assertEqual(request.call_count, 13)
        self.assertEqual(wanxiang._release_tag(releases[-1]), "model")

    def test_cnb_model_pagination_stops_on_repeated_page(self):
        def request_json(_url, source=None, params=None):
            page = (params or {}).get("page", 1)
            return {"releases": [{"tag_name": "v1.0.0", "assets": []}]}, {}

        with patch.object(RimeConfig, "source", return_value="cnb"), patch.object(wanxiang, "request_json", side_effect=request_json) as request:
            releases = wanxiang.list_releases(include_model=True)
        self.assertEqual(request.call_count, 2)
        self.assertEqual(len(releases), 1)

    def test_all_skips_same_sha256_model_across_sources(self):
        with tempfile.TemporaryDirectory() as directory:
            rime_dir = Path(directory)
            (rime_dir / wanxiang.MODEL_FILE).write_bytes(b"model")
            assets = {
                "scheme": wanxiang.Asset("scheme", "v1.0.0", "scheme", "scheme.zip", "https://example.invalid/scheme", 10, "new", "1" * 64),
                "dict": wanxiang.Asset("dict", "v1.0.0", "dict", "dict.zip", "https://example.invalid/dict", 10, "new", "2" * 64),
                "model": wanxiang.Asset("model", "model", "model", wanxiang.MODEL_FILE, "https://example.invalid/model", 5, "new", "3" * 64),
            }
            with patch.object(RimeConfig, "source", return_value="cnb"):
                records = {component: wanxiang._asset_record(asset) for component, asset in assets.items()}
            records["model"].update(source="github", tag="LTS", updated_at="old")

            with patch.object(RimeConfig, "source", return_value="cnb"), patch.object(RimeConfig, "setting_dir", return_value=rime_dir):
                with patch.object(wanxiang, "current_record", side_effect=lambda component: records[component]), patch.object(wanxiang, "download_cache_path", return_value=rime_dir / "missing.part"):
                    with patch.object(main, "latest_asset", side_effect=lambda component, **_kwargs: assets[component]), patch.object(main, "deploy_rime") as deploy:
                        messages, notes = main.run("all")
                        deploy.assert_not_called()
            self.assertIsNone(notes)
            self.assertEqual(len(messages), 4)
            self.assertTrue(all("最新" in message for message in messages))

    def test_matching_model_sha256_does_not_hide_missing_file_or_partial(self):
        asset = wanxiang.Asset("model", "model", "model", wanxiang.MODEL_FILE, "https://example.invalid/model", 5, "new", "3" * 64)
        with tempfile.TemporaryDirectory() as directory:
            rime_dir = Path(directory)
            partial = rime_dir / "model.part"
            record = {"source": "github", "tag": "LTS", "name": asset.name, "identity": asset.identity, "size": asset.size}
            with patch.object(RimeConfig, "source", return_value="cnb"), patch.object(RimeConfig, "setting_dir", return_value=rime_dir):
                with patch.object(wanxiang, "current_record", return_value=record), patch.object(wanxiang, "download_cache_path", return_value=partial):
                    self.assertTrue(wanxiang.asset_needs_update(asset))
                    (rime_dir / wanxiang.MODEL_FILE).write_bytes(b"model")
                    self.assertFalse(wanxiang.asset_needs_update(asset))
                    partial.write_bytes(b"incomplete")
                    self.assertTrue(wanxiang.asset_needs_update(asset))


if __name__ == "__main__":
    unittest.main()
