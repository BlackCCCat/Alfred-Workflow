import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
import tasklog


class TaskLogTests(unittest.TestCase):
    def test_failed_replace_keeps_previous_readable_state(self):
        with tempfile.TemporaryDirectory() as directory, patch.object(tasklog, "TASKS_DIR", Path(directory)):
            tasklog.write_state("test", status="running")
            with patch.object(Path, "replace", side_effect=OSError("replace failed")):
                with self.assertRaises(OSError):
                    tasklog.write_state("test", status="completed")
            self.assertEqual(tasklog.read_state("test")["status"], "running")
            tasklog.write_state("test", status="completed")
            self.assertEqual(tasklog.read_state("test")["status"], "completed")


if __name__ == "__main__":
    unittest.main()
