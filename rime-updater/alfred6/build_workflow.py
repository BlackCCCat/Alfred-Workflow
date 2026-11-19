#!/usr/bin/python3
import copy
import plistlib
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
UI_DIR = Path(__file__).resolve().parent / "wanxiang.alfredui"
OUTPUT = ROOT / "wanxiang-updater-alfred6.alfredworkflow"
UI_TYPE = "alfred.workflow.userinterface.alfredui"
TEXT_TYPE = "alfred.workflow.userinterface.text"
REMOVED_TYPES = {
    "alfred.workflow.utility.conditional",
    "alfred.workflow.output.callexternaltrigger",
    "alfred.workflow.trigger.external",
}


def build_plist():
    with (ROOT / "info.plist").open("rb") as handle:
        data = plistlib.load(handle)
    data["bundleid"] = "com.blackcccat.alfred.rime-wanxiang-updater.v6"
    data["name"] = "万象 Rime 更新 (Alfred 6)"
    data["version"] = "6.0.0"
    data["readme"] = (Path(__file__).resolve().parent / "README.md").read_text(encoding="utf-8")

    ui_uid = ""
    menu_uid = ""
    objects = []
    for item in data["objects"]:
        if item["type"] in REMOVED_TYPES:
            continue
        if item["type"] == TEXT_TYPE:
            ui_uid = item["uid"]
            item.update(type=UI_TYPE, version=1, config={
                "launchmode": 1,
                "path": "wanxiang.alfredui",
                "stackview": False,
            })
        elif item.get("config", {}).get("keyword") == "rimew":
            menu_uid = item["uid"]
            item.update(type="alfred.workflow.input.keyword", version=1, config={
                "argumenttype": 2,
                "keyword": "rimew",
                "text": "万象 Rime 更新",
                "subtext": "打开状态与更新面板",
                "withspace": False,
            })
        objects.append(item)
    if not ui_uid or not menu_uid:
        raise ValueError("Alfred 5 workflow 缺少主菜单或进度节点")
    data["objects"] = objects
    kept = {item["uid"] for item in objects}
    data["connections"] = {
        source: [edge for edge in edges if edge["destinationuid"] in kept]
        for source, edges in data["connections"].items() if source in kept
    }
    edge = copy.deepcopy(next(edges[0] for edges in data["connections"].values() if edges and edges[0]["destinationuid"] == ui_uid))
    data["connections"][menu_uid] = [edge]
    data["uidata"] = {uid: value for uid, value in data["uidata"].items() if uid in kept}
    return plistlib.dumps(data, sort_keys=False)


def main():
    with zipfile.ZipFile(OUTPUT, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        archive.writestr("info.plist", build_plist())
        archive.write(ROOT / "icon.png", "icon.png")
        archive.write(Path(__file__).resolve().parent / "README.md", "README.md")
        for path in sorted((ROOT / "src").glob("*.py")):
            archive.write(path, f"src/{path.name}")
        for path in sorted(UI_DIR.rglob("*")):
            if path.is_file() and path.suffix in {".py", ".json"}:
                archive.write(path, f"wanxiang.alfredui/{path.relative_to(UI_DIR)}")
    print(OUTPUT)


if __name__ == "__main__":
    main()
