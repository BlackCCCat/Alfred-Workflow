#!/usr/bin/env python3
import json
import os
import subprocess
import sys
import time
import uuid
from pathlib import Path

from tasklog import append_log, read_latest_task, read_log, read_state, write_latest_task, write_state
from tasklog import state_path


WORKFLOW_DIR = Path(__file__).resolve().parent.parent


def command_from_argv():
    if len(sys.argv) > 1 and sys.argv[1].strip():
        return sys.argv[1].strip()
    query = os.getenv("query") or os.getenv("alfred_workflow_keyword") or ""
    return query.strip()


def start_task(command):
    task_id = uuid.uuid4().hex[:12]
    write_state(task_id, status="starting", command=command, created_at=time.strftime("%Y-%m-%d %H:%M:%S"))
    write_latest_task(command, task_id)
    append_log(task_id, f"准备执行：{command}")
    subprocess.Popen(
        [sys.executable, str(WORKFLOW_DIR / "src" / "main.py"), "--task-id", task_id, command],
        cwd=str(WORKFLOW_DIR),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        start_new_session=True,
    )
    return task_id


def response_for(task_id, command):
    state = read_state(task_id)
    log_text = read_log(task_id).strip()
    status = state.get("status", "starting")
    title = {
        "starting": "准备更新",
        "running": "正在更新",
        "completed": "更新完成",
        "failed": "更新失败",
    }.get(status, status)

    lines = [
        f"# {title}",
        "",
        f"- 任务：`{command}`",
        f"- 状态：`{status}`",
    ]
    if state.get("error"):
        lines.append(f"- 错误：{state['error']}")
    if state.get("result"):
        lines.append(f"- 结果：{state['result']}")
    lines.extend(["", "## 日志", "", "```text"])
    lines.append(log_text or "等待后台任务写入日志...")
    lines.append("```")
    return "\n".join(lines), status


def main():
    command = command_from_argv()
    task_id = os.getenv("task_id", "").strip()
    if not command:
        print(json.dumps({"response": "没有收到更新命令。", "footer": "关闭窗口后重试。"}, ensure_ascii=False))
        return

    if not task_id:
        latest_task_id = read_latest_task(command)
        latest_state = read_state(latest_task_id) if latest_task_id else {}
        if latest_state.get("status") in {"starting", "running"}:
            task_id = latest_task_id
        elif latest_state.get("status") in {"completed", "failed"}:
            try:
                fresh = time.time() - state_path(latest_task_id).stat().st_mtime < 15
            except OSError:
                fresh = False
            if fresh:
                task_id = latest_task_id

    if not task_id or not read_state(task_id):
        task_id = start_task(command)

    response, status = response_for(task_id, command)
    payload = {
        "variables": {"task_id": task_id},
        "response": response,
        "footer": "自动刷新更新日志；Esc 关闭" if status in {"starting", "running"} else "任务已结束；Esc 关闭",
        "behaviour": {
            "response": "replace",
            "scroll": "end",
        },
    }
    if status in {"starting", "running"}:
        payload["rerun"] = 1
    print(json.dumps(payload, ensure_ascii=False))


if __name__ == "__main__":
    main()
