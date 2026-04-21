import sys

from alfred import error_item, item, output
from config import MODEL_FILE, RimeConfig
from wanxiang import (
    WanxiangError,
    component_label,
    copied_files_path,
    list_component_assets,
    load_records,
    exclude_file_path,
    records_path,
    source_label,
    status_text,
)


def menu_items():
    status = status_text()
    return [
        item(
            title="更新全部",
            subtitle=f"自动更新方案、词库、模型，完成后部署。{status}",
            arg="all",
            uid="menu-all",
        ),
        item(
            title="更新方案",
            subtitle=f"{RimeConfig.schema_label()}：{RimeConfig.scheme_asset()}",
            arg="scheme",
            uid="menu-scheme",
            autocomplete="更新方案",
        ),
        item(
            title="更新词库",
            subtitle=f"{RimeConfig.schema_label()}：{RimeConfig.dict_asset()}",
            arg="dict",
            uid="menu-dict",
            autocomplete="更新词库",
        ),
        item(
            title="更新模型",
            subtitle=MODEL_FILE,
            arg="model",
            uid="menu-model",
            autocomplete="更新模型",
        ),
        item(
            title="查看当前配置",
            subtitle="进入本地配置和更新记录页面",
            arg="",
            uid="menu-status",
            valid=False,
            autocomplete="status",
        ),
        item(
            title="重新部署",
            subtitle="触发当前输入法引擎重新部署 RIME",
            arg="deploy",
            uid="menu-deploy",
        ),
    ]


def all_item():
    return [
        item(
            title="更新全部",
            subtitle=f"使用 {source_label()} 自动更新方案、词库、模型，完成后部署。{status_text()}",
            arg="all",
            uid="all-latest",
        )
    ]


def deploy_item():
    return [
        item(
            title="重新部署 RIME",
            subtitle=f"使用当前配置触发部署。{status_text()}",
            arg="deploy",
            uid="deploy-rime",
        )
    ]


def status_items():
    records = load_records().get("components", {})
    results = [
        item(
            title="返回主菜单",
            subtitle="回到更新菜单",
            arg="",
            uid="status-back",
            valid=False,
            autocomplete=" ",
        ),
        item(
            title="当前配置",
            subtitle=status_text(),
            arg="",
            uid="status-config",
            valid=False,
        ),
        item(
            title="本地记录文件",
            subtitle=str(records_path()),
            arg="",
            uid="status-record-file",
            valid=False,
        ),
        item(
            title="上次复制文件清单",
            subtitle=str(copied_files_path()),
            arg="",
            uid="status-copied-files",
            valid=False,
        ),
        item(
            title="排除文件",
            subtitle=str(exclude_file_path()),
            arg="",
            uid="status-exclude-file",
            valid=False,
        ),
    ]

    for component in ("scheme", "dict", "model"):
        record = records.get(component)
        if not record:
            results.append(
                item(
                    title=f"{component_label(component)}记录",
                    subtitle="暂无本地记录",
                    arg="",
                    uid=f"status-{component}-empty",
                    valid=False,
                )
            )
            continue
        title = f"{component_label(component)}：{record.get('tag') or '未知版本'}"
        subtitle = (
            f"{record.get('name') or '未知文件'}；"
            f"{record.get('updated_at') or '未知更新时间'}；"
            f"{record.get('source_label') or record.get('source') or '未知源'}；"
            f"{record.get('size') or 0} bytes"
        )
        results.append(
            item(
                title=title,
                subtitle=subtitle,
                arg="",
                uid=f"status-{component}",
                valid=False,
            )
        )

    return results


def component_items(component):
    assets = list_component_assets(component)
    if not assets:
        return [error_item(f"没有找到可用的{component_label(component)}更新")]

    results = []
    for asset in assets:
        results.append(
            item(
                title=f"{asset.release_title} - {asset.name}",
                subtitle=f"{source_label()}；更新时间：{asset.display_time}",
                arg=f"{component}@{asset.tag}@{asset.name}",
                uid=f"{component}-{asset.tag}-{asset.name}",
                match=f"{asset.release_title} {asset.tag} {asset.name}",
                autocomplete=asset.name,
            )
        )
    return results


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "menu"
    query = sys.argv[2].strip().lower() if len(sys.argv) > 2 else ""
    try:
        if mode == "menu" and query == "status":
            output(status_items())
        elif mode == "menu":
            output(menu_items())
        elif mode == "all":
            output(all_item())
        elif mode == "deploy":
            output(deploy_item())
        elif mode in {"scheme", "dict", "model"}:
            output(component_items(mode), cache_seconds=300)
        elif mode == "dicts":
            output(component_items("dict"), cache_seconds=300)
        else:
            output(menu_items())
    except WanxiangError as exc:
        output([error_item(str(exc))])


if __name__ == "__main__":
    main()
