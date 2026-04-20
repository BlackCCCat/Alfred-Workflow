import json
import hashlib
from datetime import datetime
from pathlib import Path


WORKFLOW_DIR = Path(__file__).resolve().parent.parent
TASKS_DIR = WORKFLOW_DIR / "cache" / "tasks"


def task_dir(task_id: str) -> Path:
    return TASKS_DIR / task_id


def state_path(task_id: str) -> Path:
    return task_dir(task_id) / "state.json"


def log_path(task_id: str) -> Path:
    return task_dir(task_id) / "progress.log"


def command_key(command: str) -> str:
    return hashlib.sha256(command.encode("utf-8")).hexdigest()[:16]


def latest_path(command: str) -> Path:
    return TASKS_DIR / f"latest-{command_key(command)}.txt"


def read_latest_task(command: str) -> str:
    path = latest_path(command)
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8").strip()


def write_latest_task(command: str, task_id: str) -> None:
    TASKS_DIR.mkdir(parents=True, exist_ok=True)
    latest_path(command).write_text(task_id, encoding="utf-8")


def now_text() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def append_log(task_id: str, message: str) -> None:
    directory = task_dir(task_id)
    directory.mkdir(parents=True, exist_ok=True)
    with log_path(task_id).open("a", encoding="utf-8") as handle:
        handle.write(f"[{now_text()}] {message}\n")


def read_log(task_id: str) -> str:
    path = log_path(task_id)
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def read_state(task_id: str) -> dict:
    path = state_path(task_id)
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}


def write_state(task_id: str, **updates) -> dict:
    directory = task_dir(task_id)
    directory.mkdir(parents=True, exist_ok=True)
    state = read_state(task_id)
    state.update(updates)
    state["updated_at"] = now_text()
    state_path(task_id).write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")
    return state
