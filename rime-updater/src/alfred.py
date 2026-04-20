import json
from pathlib import Path


WORKFLOW_DIR = Path(__file__).resolve().parent.parent
ICON_PATH = str(WORKFLOW_DIR / "icon.png")


def item(title, subtitle="", arg="", uid="", valid=True, icon_path=ICON_PATH, **extra):
    result = {
        "title": title,
        "subtitle": subtitle,
        "arg": arg,
        "valid": valid,
        "icon": {"path": icon_path},
    }
    if uid:
        result["uid"] = uid
    result.update(extra)
    return result


def output(items, cache_seconds=None):
    payload = {"items": items}
    if cache_seconds:
        payload["cache"] = {"seconds": cache_seconds, "loosereload": True}
    print(json.dumps(payload, ensure_ascii=False))


def error_item(message, subtitle="请检查网络、下载源或 Workflow 配置"):
    return item(
        title=message,
        subtitle=subtitle,
        arg="",
        uid="error",
        valid=False,
    )
