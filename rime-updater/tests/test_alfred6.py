import importlib.util
import json
import plistlib
import subprocess
import tempfile
import unittest
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
V6_PACKAGE = ROOT / "wanxiang-updater-alfred6.alfredworkflow"
BUILD_SCRIPT = ROOT / "alfred6" / "build_workflow.py"


class Alfred6WorkflowTests(unittest.TestCase):
    def test_new_workflow_preserves_old_package_and_quick_commands(self):
        old_package = ROOT / "wanxiang-updater.alfredworkflow"
        with zipfile.ZipFile(old_package) as archive:
            old = plistlib.loads(archive.read("info.plist"))
        with zipfile.ZipFile(V6_PACKAGE) as archive:
            new = plistlib.loads(archive.read("info.plist"))

        self.assertNotEqual(old["bundleid"], new["bundleid"])
        self.assertTrue(any(item["type"] == "alfred.workflow.userinterface.text" for item in old["objects"]))
        ui = next(item for item in new["objects"] if item["type"] == "alfred.workflow.userinterface.alfredui")
        self.assertEqual(ui["config"]["launchmode"], 1)
        self.assertEqual(ui["config"]["path"], "wanxiang.alfredui")
        keywords = {item["config"]["keyword"]: item for item in new["objects"] if "keyword" in item.get("config", {})}
        self.assertEqual(set(keywords), {"rimew", "rimes", "rimed", "rimem", "rimeall", "rimee", "rimef"})
        self.assertEqual(keywords["rimew"]["type"], "alfred.workflow.input.keyword")
        self.assertEqual(new["connections"][keywords["rimew"]["uid"]][0]["destinationuid"], ui["uid"])
        self.assertEqual(old["userconfigurationconfig"], new["userconfigurationconfig"])
        known = {item["uid"] for item in new["objects"]}
        self.assertTrue(all(edge["destinationuid"] in known for edges in new["connections"].values() for edge in edges))

    def test_ui_package_contains_executable_bridge_and_no_runtime_data(self):
        with zipfile.ZipFile(V6_PACKAGE) as archive:
            names = set(archive.namelist())
            self.assertIn("wanxiang.alfredui/ui.json", names)
            bridge_name = "wanxiang.alfredui/scripts/bridge.py"
            self.assertIn(bridge_name, names)
            self.assertTrue((archive.getinfo(bridge_name).external_attr >> 16) & 0o111)
            self.assertFalse(any(name.startswith("cache/") or name.endswith("update_records.json") for name in names))
            ui = json.loads(archive.read("wanxiang.alfredui/ui.json"))
            variables = ui["variablesconfig"]
            self.assertEqual(variables["command"]["src"], "args[0]")
            self.assertTrue(variables["github_token"]["scriptenv"])
            content = ui["window"]["root"]["components"][1]
            self.assertEqual((content["layout"], content["rows"]), ("flex", 2))
            self.assertEqual(content["components"][0]["components"][1]["type"], "markdownarea")
            self.assertEqual(content["components"][1]["components"][1]["type"], "textarea")

            with tempfile.TemporaryDirectory() as directory:
                archive.extractall(directory)
                result = subprocess.run(
                    ["/usr/bin/python3", str(Path(directory) / bridge_name), "poll"],
                    cwd=directory, capture_output=True, text=True, check=True,
                )
                payload = json.loads(result.stdout)
                self.assertIn("download_progress", payload["update"]["ids"])
                self.assertIn("scheme_record", payload["update"]["ids"])

    def test_plist_source_can_be_rebuilt(self):
        spec = importlib.util.spec_from_file_location("build_workflow_v6", BUILD_SCRIPT)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        generated = plistlib.loads(module.build_plist())
        with zipfile.ZipFile(V6_PACKAGE) as archive:
            packaged = plistlib.loads(archive.read("info.plist"))
        self.assertEqual(generated, packaged)


if __name__ == "__main__":
    unittest.main()
