import hashlib
import io
import ssl
import sys
import tempfile
import unittest
import urllib.error
from pathlib import Path
from unittest.mock import patch


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
import wanxiang


class DownloadResumeTests(unittest.TestCase):
    def test_github_rate_limit_is_reported_from_python_response(self):
        url = "https://api.github.com/repos/example/releases"
        error = urllib.error.HTTPError(
            url, 403, "Forbidden",
            {"X-RateLimit-Remaining": "0"}, None,
        )
        with patch.object(wanxiang.urllib.request, "urlopen", side_effect=error):
            with self.assertRaisesRegex(wanxiang.WanxiangError, "稍后重试.*GitHub Token"):
                wanxiang.request_json(url, source="github")

    def test_certificate_failure_stays_in_python(self):
        error = urllib.error.URLError(ssl.SSLCertVerificationError("Missing Authority Key Identifier"))
        with patch.object(wanxiang.urllib.request, "urlopen", side_effect=error):
            with self.assertRaisesRegex(wanxiang.WanxiangError, "Python 证书验证失败"):
                wanxiang.request_json("https://api.github.com/repos/example/releases", source="github")

    def test_interrupted_download_resumes_across_tasks(self):
        payload = b"wanxiang-download" * 64
        requests = []
        state = {"complete": False}

        def urlopen(request, timeout):
            range_header = request.get_header("Range")
            requests.append(range_header)
            offset = int(range_header[6:-1]) if range_header else 0
            body = payload[offset:]
            response = io.BytesIO(body if state["complete"] else body[:10])
            response.status = 206 if range_header else 200
            response.headers = {"Content-Range": f"bytes {offset}-{len(payload) - 1}/{len(payload)}"} if range_header else {}
            return response

        asset = wanxiang.Asset(
            "model", "LTS", "model", "model.gram",
            "https://example.invalid/model.gram",
            len(payload), "today", hashlib.sha256(payload).hexdigest(),
        )
        with patch.object(wanxiang.urllib.request, "urlopen", side_effect=urlopen):
            with tempfile.TemporaryDirectory() as workflow_dir, patch.object(wanxiang, "WORKFLOW_DIR", Path(workflow_dir)):
                with self.assertRaises(wanxiang.WanxiangError):
                    wanxiang.download_asset(asset)
                state["complete"] = True
                second_task_request = len(requests)
                result = wanxiang.download_asset(asset)
                self.assertEqual(result.read_bytes(), payload)
            self.assertTrue(requests[second_task_request].startswith("bytes="))

    def test_server_ignoring_range_restarts_cleanly(self):
        payload = b"complete download" * 64
        requests = []

        def urlopen(request, timeout):
            requests.append(request.get_header("Range"))
            response = io.BytesIO(payload[:10] if len(requests) <= 3 else payload)
            response.status = 200
            response.headers = {}
            return response

        asset = wanxiang.Asset(
            "model", "LTS", "model", "model.gram",
            "https://example.invalid/model.gram",
            len(payload), "today", hashlib.sha256(payload).hexdigest(),
        )
        with patch.object(wanxiang.urllib.request, "urlopen", side_effect=urlopen):
            with tempfile.TemporaryDirectory() as workflow_dir, patch.object(wanxiang, "WORKFLOW_DIR", Path(workflow_dir)):
                with self.assertRaises(wanxiang.WanxiangError):
                    wanxiang.download_asset(asset)
                result = wanxiang.download_asset(asset)
                self.assertEqual(result.read_bytes(), payload)
        self.assertTrue(requests[3].startswith("bytes="))

    def test_install_clears_completed_cache_and_rejects_bad_hash(self):
        payload = b"model data" * 32
        asset = wanxiang.Asset(
            "model", "LTS", "model", "model.gram",
            "https://example.invalid/model.gram",
            len(payload), "today", hashlib.sha256(payload).hexdigest(),
        )

        def urlopen(request, timeout):
            response = io.BytesIO(payload)
            response.status = 200
            response.headers = {}
            return response

        with tempfile.TemporaryDirectory() as root:
            workflow_dir = Path(root) / "workflow"
            rime_dir = Path(root) / "rime"
            with patch.object(wanxiang, "WORKFLOW_DIR", workflow_dir), patch.object(wanxiang.RimeConfig, "setting_dir", return_value=rime_dir), patch.object(wanxiang.urllib.request, "urlopen", side_effect=urlopen):
                wanxiang.install_asset(asset)
                self.assertEqual((rime_dir / wanxiang.MODEL_FILE).read_bytes(), payload)
                self.assertEqual(list((workflow_dir / "cache" / "downloads").glob("*.part")), [])

                bad_asset = wanxiang.Asset(
                    "model", "LTS", "model", "model.gram",
                    asset.url, len(payload), "today", "0" * 64,
                )
                with self.assertRaisesRegex(wanxiang.WanxiangError, "SHA256"):
                    wanxiang.download_asset(bad_asset)
                self.assertEqual(list((workflow_dir / "cache" / "downloads").glob("*.part")), [])

    def test_wrong_range_does_not_append_to_partial_file(self):
        payload = b"range check" * 64
        requests = []

        def urlopen(request, timeout):
            requests.append(request.get_header("Range"))
            response = io.BytesIO(payload[:10] if len(requests) <= 3 else payload[10:])
            response.status = 200 if len(requests) <= 3 else 206
            response.headers = {} if len(requests) <= 3 else {
                "Content-Range": f"bytes 0-{len(payload) - 11}/{len(payload)}",
            }
            return response

        asset = wanxiang.Asset(
            "model", "LTS", "model", "model.gram",
            "https://example.invalid/model.gram",
            len(payload), "today", hashlib.sha256(payload).hexdigest(),
        )
        with patch.object(wanxiang.urllib.request, "urlopen", side_effect=urlopen):
            with tempfile.TemporaryDirectory() as workflow_dir, patch.object(wanxiang, "WORKFLOW_DIR", Path(workflow_dir)):
                with self.assertRaises(wanxiang.WanxiangError):
                    wanxiang.download_asset(asset)
                with self.assertRaisesRegex(wanxiang.WanxiangError, "续传响应范围不匹配"):
                    wanxiang.download_asset(asset)
                self.assertEqual(list((Path(workflow_dir) / "cache" / "downloads").glob("*.part")), [])
        self.assertTrue(requests[3].startswith("bytes="))

    def test_all_retries_partial_even_when_record_matches(self):
        asset = wanxiang.Asset(
            "model", "LTS", "model", "model.gram",
            "https://example.invalid/model.gram", 100, "today", "0" * 64,
        )
        def urlopen(request, timeout):
            response = io.BytesIO(b"partial")
            response.status = 200
            response.headers = {}
            return response

        with tempfile.TemporaryDirectory() as workflow_dir, patch.object(wanxiang, "WORKFLOW_DIR", Path(workflow_dir)):
            with patch.object(wanxiang.RimeConfig, "source", return_value="github"), patch.object(wanxiang.urllib.request, "urlopen", side_effect=urlopen):
                record = wanxiang._asset_record(asset)
                with patch.object(wanxiang, "current_record", return_value=record):
                    self.assertFalse(wanxiang.asset_needs_update(asset))
                    with self.assertRaises(wanxiang.WanxiangError):
                        wanxiang.download_asset(asset)
                    self.assertTrue(wanxiang.asset_needs_update(asset))


if __name__ == "__main__":
    unittest.main()
