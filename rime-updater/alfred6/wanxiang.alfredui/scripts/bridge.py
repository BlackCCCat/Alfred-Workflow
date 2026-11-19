#!/usr/bin/python3
import json
import sys
from pathlib import Path


WORKFLOW_DIR = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(WORKFLOW_DIR / "src"))

from config import (
    ENGINE_LABELS,
    RimeConfig,
    clear_runtime_engine,
    clear_runtime_option,
    set_runtime_engine,
    set_runtime_option,
)
from progress import is_running_task_fresh, start_task
from tasklog import TASKS_DIR, read_log, read_state
from wanxiang import component_label, current_record


def task_ids():
    if not TASKS_DIR.exists():
        return []
    return [path.name for path in sorted(TASKS_DIR.iterdir(), key=lambda path: path.stat().st_mtime, reverse=True) if path.is_dir()]


def active_task():
    for task_id in task_ids():
        if read_state(task_id).get("status") in {"starting", "running"} and is_running_task_fresh(task_id):
            return task_id
    return ""


def record_text(component):
    record = current_record(component)
    if not record:
        return f"{component_label(component)}：暂无本地记录"
    return f"{component_label(component)}：{record.get('tag') or '未知版本'}  ·  {record.get('name') or '未知文件'}"


def snapshot(task_id="", message=""):
    if not task_id or not read_state(task_id):
        task_id = next(iter(task_ids()), "")
    state = read_state(task_id) if task_id else {}
    status = state.get("status", "")
    phase = state.get("phase", "")
    downloaded = max(0, int(state.get("downloaded") or 0))
    total = max(0, int(state.get("total") or 0))
    ratio = min(1.0, downloaded / total) if total else 0.0
    downloading = status == "running" and phase == "downloading" and total > 0
    updates = {
        "download_progress": {
            "progress": ratio,
            "hidden": not downloading,
            "tooltip": f"下载进度 {int(ratio * 100)}%" if downloading else "下载进度",
        },
        "path_status": {"text": f"方案目录：{RimeConfig.setting_dir()}"},
        "engine_picker": {"selected": RimeConfig.engine()},
        "source_picker": {"selected": RimeConfig.source()},
        "schema_picker": {"selected": RimeConfig.schema()},
        "accelerator_picker": {
            "selected": RimeConfig.github_download_accelerator() or "none",
            "enabled": RimeConfig.source() == "github",
        },
        "scheme_record": {"text": record_text("scheme")},
        "dict_record": {"text": record_text("dict")},
        "model_record": {"text": record_text("model")},
        "notes_area": {"text": state.get("scheme_notes") or "暂无更新说明"},
        "log_area": {"text": read_log(task_id) if task_id else "暂无任务日志"},
    }
    result = {"variables": {"task_id": task_id}, "update": {"ids": updates}}
    result["pulse"] = {"interval": 1 if status in {"starting", "running"} else 0}
    if message:
        result["notification"] = {"post": {"title": "万象 Rime 更新", "text": message}}
    return result


def main():
    action = sys.argv[1] if len(sys.argv) > 1 else "poll"
    value = sys.argv[2] if len(sys.argv) > 2 else ""
    selected = sys.argv[3] if len(sys.argv) > 3 else ""
    try:
        if action in {"open", "start"} and value:
            if value.split("@", 1)[0] not in {"all", "scheme", "dict", "model", "deploy"}:
                raise ValueError("未知更新命令")
            running = active_task()
            payload = snapshot(running or start_task(value), "已有更新任务正在运行" if running else "")
        elif action == "switch":
            if active_task():
                payload = snapshot(message="更新进行中，请完成后再切换输入法")
            else:
                if value not in {"default", *ENGINE_LABELS}:
                    raise ValueError("未知输入法引擎")
                if value != (RimeConfig.runtime_engine() or "default"):
                    if value == "default":
                        clear_runtime_engine()
                    else:
                        set_runtime_engine(value)
                payload = snapshot(message="输入法已切换")
        elif action == "configure":
            if active_task():
                payload = snapshot(message="更新进行中，请完成后再切换配置")
            else:
                if selected == "default":
                    clear_runtime_option(value)
                else:
                    set_runtime_option(value, selected)
                payload = snapshot(message="配置已更新")
        else:
            payload = snapshot(value if action == "poll" else "")
        if action == "poll":
            for picker in ("engine_picker", "source_picker", "schema_picker", "accelerator_picker"):
                payload["update"]["ids"].pop(picker)
    except (OSError, ValueError) as exc:
        payload = snapshot(message=str(exc))
    print(json.dumps(payload, ensure_ascii=False))


if __name__ == "__main__":
    main()
