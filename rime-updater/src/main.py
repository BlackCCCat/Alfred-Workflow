import sys

from tasklog import append_log, write_state
from wanxiang import (
    WanxiangError,
    asset_needs_update,
    component_label,
    deploy_rime,
    install_asset,
    latest_asset,
    parse_command,
    status_text,
)


def update_component(component, tag="", name="", force=True, log=None, state_writer=None):
    if log:
        log(f"检查远端{component_label(component)}资源")
    asset = latest_asset(component, selected_tag=tag, selected_name=name)
    if log:
        log(f"远端{component_label(component)}资源：{asset.tag} / {asset.name}")
    should_update = force or asset_needs_update(asset)
    if not should_update:
        if log:
            log(f"本地记录匹配，跳过{component_label(component)}更新")
        return f"{component_label(component)}已是最新：{asset.tag} / {asset.name}", False, None

    notes = None
    if component == "scheme":
        notes = scheme_release_notes(asset)
        if state_writer and notes:
            state_writer(scheme_notes=notes)

    if not force and log:
        log(f"本地记录不匹配，开始更新{component_label(component)}")
    return install_asset(asset, log=log), True, notes


def scheme_release_notes(asset):
    body = (asset.body or "").strip()
    if not body:
        return "该版本没有提供更新说明。"

    marker = "## 📝 更新日志"
    if marker in body:
        body = body.split(marker, 1)[1].strip()
        for next_marker in ("\n## ", "\n# "):
            if next_marker in body:
                body = body.split(next_marker, 1)[0].strip()
                break
        return f"{marker}\n{body}".strip()
    return body


def run(command, log=None, state_writer=None):
    component, tag, name = parse_command(command)
    if component == "status":
        return [status_text(include_records=True)], None

    if component == "all":
        messages = []
        updated = False
        scheme_notes = None
        for item in ("scheme", "dict", "model"):
            message, did_update, notes = update_component(
                item,
                force=False,
                log=log,
                state_writer=state_writer,
            )
            messages.append(message)
            updated = updated or did_update
            if item == "scheme" and did_update:
                scheme_notes = notes
        if updated:
            messages.append(deploy_rime(log=log))
        else:
            messages.append("本地记录已是最新，跳过部署")
        return messages, scheme_notes

    if component == "deploy":
        return [deploy_rime(log=log)], None

    if component in {"scheme", "dict", "model"}:
        message, _updated, notes = update_component(
            component,
            tag,
            name,
            force=True,
            log=log,
            state_writer=state_writer,
        )
        return [message], notes

    raise WanxiangError(f"未知命令：{command}")


def run_task(task_id, command):
    write_state(task_id, status="running", command=command)
    append_log(task_id, f"任务开始：{command}")

    def log(message):
        append_log(task_id, message)

    def update_state(**updates):
        write_state(task_id, **updates)

    try:
        messages, scheme_notes = run(command, log=log, state_writer=update_state)
    except WanxiangError as exc:
        append_log(task_id, f"任务失败：{exc}")
        write_state(task_id, status="failed", command=command, error=str(exc))
        return 1

    if scheme_notes:
        update_state(scheme_notes=scheme_notes)

    for message in messages:
        append_log(task_id, message)
    append_log(task_id, "任务完成")
    write_state(task_id, status="completed", command=command, result="；".join(messages))
    return 0


def main():
    if len(sys.argv) > 3 and sys.argv[1] == "--task-id":
        raise SystemExit(run_task(sys.argv[2], sys.argv[3]))

    command = sys.argv[1] if len(sys.argv) > 1 else "status"
    component, _tag, _name = parse_command(command)
    try:
        messages, _scheme_notes = run(command)
        suffix = "。" if component in {"all", "deploy", "status"} else "。请重新部署 RIME。"
        print("；".join(messages) + suffix)
    except WanxiangError as exc:
        print(f"更新失败：{exc}")


if __name__ == "__main__":
    main()
