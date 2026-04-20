import json
import os
import re
import shutil
import subprocess
import tempfile
import urllib.error
import urllib.parse
import urllib.request
import zipfile
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Optional

from config import (
    CNB_HEADERS,
    CNB_RELEASES_API,
    DEFAULT_EXCLUDES,
    GITHUB_HEADERS,
    GITHUB_MODEL_API,
    GITHUB_RELEASES_API,
    MODEL_FILE,
    REQUEST_TIMEOUT,
    SCHEME_SKIP_FILES,
    RimeConfig,
)


WORKFLOW_DIR = Path(__file__).resolve().parent.parent


class WanxiangError(Exception):
    pass


@dataclass(frozen=True)
class Asset:
    component: str
    tag: str
    release_title: str
    name: str
    url: str
    size: int
    updated_at: str
    identity: str = ""
    body: str = ""

    @property
    def display_time(self) -> str:
        if not self.updated_at:
            return "未知时间"
        try:
            dt = datetime.strptime(self.updated_at, "%Y-%m-%dT%H:%M:%SZ")
            return dt.strftime("%Y-%m-%d %H:%M UTC")
        except ValueError:
            return self.updated_at


def source_label() -> str:
    return "CNB" if RimeConfig.source() == "cnb" else "GitHub"


def component_label(component: str) -> str:
    return {
        "scheme": "方案",
        "dict": "词库",
        "model": "模型",
        "all": "全部",
        "deploy": "部署",
    }.get(component, component)


def records_path() -> Path:
    return WORKFLOW_DIR / "cache" / "alfred_records.json"


def exclude_file_path() -> Path:
    configured = (os.getenv("exclude_file_path") or "").strip()
    if configured:
        return Path(configured).expanduser()
    return WORKFLOW_DIR / "cache" / "user_exclude_file.txt"


def load_records() -> dict:
    path = records_path()
    if not path.exists():
        return {"components": {}}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {"components": {}}
    if not isinstance(data, dict):
        return {"components": {}}
    components = data.get("components")
    if not isinstance(components, dict):
        data["components"] = {}
    return data


def _asset_record(asset: Asset) -> dict:
    return {
        "component": asset.component,
        "source": RimeConfig.source(),
        "source_label": source_label(),
        "schema": RimeConfig.schema(),
        "schema_label": RimeConfig.schema_label(),
        "tag": asset.tag,
        "name": asset.name,
        "updated_at": asset.updated_at,
        "size": asset.size,
        "identity": asset.identity,
        "recorded_at": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
    }


def save_record(asset: Asset) -> None:
    path = records_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    data = load_records()
    data.setdefault("components", {})[asset.component] = _asset_record(asset)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def asset_needs_update(asset: Asset) -> bool:
    record = load_records().get("components", {}).get(asset.component)
    if not record:
        return True

    expected = _asset_record(asset)
    keys = ["source", "tag", "name", "identity"]
    if asset.component in {"scheme", "dict"}:
        keys.append("schema")
    if not record.get("identity"):
        keys.extend(["updated_at", "size"])
    for key in keys:
        if record.get(key) != expected.get(key):
            return True
    return False


def local_records_summary() -> str:
    components = load_records().get("components", {})
    if not components:
        return "本地记录：暂无"

    lines = []
    for component in ("scheme", "dict", "model"):
        record = components.get(component)
        if not record:
            lines.append(f"{component_label(component)}：暂无")
            continue
        tag = record.get("tag") or "未知版本"
        name = record.get("name") or "未知文件"
        updated_at = record.get("updated_at") or "未知时间"
        source = record.get("source_label") or record.get("source") or "未知源"
        lines.append(f"{component_label(component)}：{tag} / {name} / {updated_at} / {source}")
    return "本地记录：" + "；".join(lines)


def request_json(url: str, source: Optional[str] = None, params: Optional[dict] = None):
    headers = CNB_HEADERS if (source or RimeConfig.source()) == "cnb" else GITHUB_HEADERS
    if params:
        url = f"{url}?{urllib.parse.urlencode(params)}"
    request = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(request, timeout=REQUEST_TIMEOUT) as response:
            body = response.read().decode("utf-8")
            return json.loads(body), response.headers
    except urllib.error.HTTPError as exc:
        raise WanxiangError(f"请求失败：HTTP {exc.code} {url}") from exc
    except urllib.error.URLError as exc:
        raise WanxiangError(f"请求失败：{exc.reason}") from exc
    except json.JSONDecodeError as exc:
        raise WanxiangError("接口返回不是有效 JSON") from exc


def _release_tag(release: dict) -> str:
    return release.get("tag_name") or release.get("tag_ref", "").split("/")[-1]


def _release_title(release: dict) -> str:
    return release.get("name") or release.get("title") or _release_tag(release)


def _asset_size(asset: dict) -> int:
    return int(asset.get("size") or asset.get("size_in_byte") or asset.get("sizeInByte") or 0)


def _asset_url(asset: dict) -> str:
    if asset.get("browser_download_url"):
        return asset["browser_download_url"]
    if asset.get("path"):
        return "https://cnb.cool" + asset["path"]
    return ""


def _normalise_asset(component: str, release: dict, asset: dict) -> Asset:
    digest = asset.get("digest", "")
    identity = (
        digest.split(":", 1)[-1]
        if digest
        else str(asset.get("cnb_id") or asset.get("id") or asset.get("asset_id") or "")
    )
    if not identity:
        identity = "|".join(
            [
                _release_tag(release),
                asset.get("name", ""),
                asset.get("updated_at") or release.get("published_at") or "",
                str(_asset_size(asset)),
            ]
        )
    return Asset(
        component=component,
        tag=_release_tag(release),
        release_title=_release_title(release),
        name=asset.get("name", ""),
        url=_asset_url(asset),
        size=_asset_size(asset),
        updated_at=asset.get("updated_at") or release.get("published_at") or "",
        identity=identity,
        body=release.get("body", ""),
    )


def _version_key(tag: str) -> tuple:
    nums = re.findall(r"\d+", tag)
    return tuple(int(num) for num in nums) if nums else (0,)


def _is_scheme_release(release: dict) -> bool:
    tag = _release_tag(release)
    title = _release_title(release)
    return re.fullmatch(r"v\d+\.\d+\.\d+", tag) is not None or "万象拼音输入方案" in title


def _is_dict_release(release: dict) -> bool:
    tag = _release_tag(release)
    title = _release_title(release)
    return tag in {"dict-nightly", "v1.0.0"} or "词库" in title or "实时全量预览" in title


def _is_model_release(release: dict) -> bool:
    return _release_tag(release) in {"model", "LTS"}


def list_releases(include_model=False) -> list[dict]:
    source = RimeConfig.source()
    if source == "github":
        data, _headers = request_json(GITHUB_RELEASES_API, source="github")
        return data

    first_page, headers = request_json(CNB_RELEASES_API, source="cnb")
    releases = list(first_page.get("releases", []))
    if not include_model or any(_is_model_release(release) for release in releases):
        return releases

    total = int(headers.get("X-Cnb-Total") or headers.get("X-CNB-Total") or len(releases))
    page_size = int(headers.get("X-Cnb-Page-Size") or headers.get("X-CNB-Page-Size") or len(releases) or 1)
    last_page = min((total + page_size - 1) // page_size, 10)
    for page in range(2, last_page + 1):
        data, _headers = request_json(CNB_RELEASES_API, source="cnb", params={"page": page})
        releases.extend(data.get("releases", []))
        if any(_is_model_release(release) for release in releases):
            break
    return releases


def _find_asset(releases: list[dict], component: str, asset_name: str, selected_tag: str = "") -> list[Asset]:
    candidates = []
    for release in releases:
        if selected_tag and _release_tag(release) != selected_tag:
            continue
        if component == "scheme" and not _is_scheme_release(release):
            continue
        if component == "dict" and not _is_dict_release(release):
            continue
        if component == "model" and not _is_model_release(release):
            continue
        for asset in release.get("assets", []):
            if asset.get("name") == asset_name:
                candidates.append(_normalise_asset(component, release, asset))
    return sorted(candidates, key=lambda item: _version_key(item.tag), reverse=True)


def list_component_assets(component: str, limit: int = 8) -> list[Asset]:
    if component == "model":
        return [latest_asset("model")]

    asset_name = RimeConfig.scheme_asset() if component == "scheme" else RimeConfig.dict_asset()
    releases = list_releases()
    return _find_asset(releases, component, asset_name)[:limit]


def latest_asset(component: str, selected_tag: str = "", selected_name: str = "") -> Asset:
    asset_name = selected_name
    if component == "scheme":
        asset_name = selected_name or RimeConfig.scheme_asset()
        matches = _find_asset(list_releases(), component, asset_name, selected_tag)
    elif component == "dict":
        asset_name = selected_name or RimeConfig.dict_asset()
        matches = _find_asset(list_releases(), component, asset_name, selected_tag)
    elif component == "model":
        if RimeConfig.source() == "github":
            release, _headers = request_json(GITHUB_MODEL_API, source="github")
            matches = _find_asset([release], component, selected_name or MODEL_FILE, selected_tag or "LTS")
        else:
            matches = _find_asset(list_releases(include_model=True), component, selected_name or MODEL_FILE, selected_tag or "model")
    else:
        raise WanxiangError(f"未知更新类型：{component}")

    if not matches:
        raise WanxiangError(f"未找到 {source_label()} 上的{component_label(component)}资源：{asset_name}")
    return matches[0]


def decode_zip_member_name(name: str) -> str:
    try:
        return name.encode("cp437").decode("utf-8")
    except (UnicodeEncodeError, UnicodeDecodeError):
        return name


def safe_target(base_dir: Path, member_name: str) -> Path:
    target = (base_dir / member_name).resolve()
    base = base_dir.resolve()
    if target != base and base not in target.parents:
        raise WanxiangError(f"压缩包包含不安全路径：{member_name}")
    return target


def download_asset(asset: Asset, temp_dir: Path, log=None) -> Path:
    if not asset.url:
        raise WanxiangError(f"{asset.name} 缺少下载地址")
    target = temp_dir / asset.name
    if log:
        log(f"开始下载 {asset.name}")
    request = urllib.request.Request(asset.url, headers=CNB_HEADERS if RimeConfig.source() == "cnb" else GITHUB_HEADERS)
    try:
        with urllib.request.urlopen(request, timeout=REQUEST_TIMEOUT) as response, target.open("wb") as fh:
            downloaded = 0
            next_report = 0
            while True:
                chunk = response.read(1024 * 256)
                if not chunk:
                    break
                fh.write(chunk)
                downloaded += len(chunk)
                if log and asset.size:
                    percent = int(downloaded * 100 / asset.size)
                    if percent >= next_report:
                        log(f"下载进度 {asset.name}: {percent}% ({downloaded}/{asset.size} bytes)")
                        next_report += 10
    except urllib.error.HTTPError as exc:
        raise WanxiangError(f"下载失败：HTTP {exc.code} {asset.name}") from exc
    except urllib.error.URLError as exc:
        raise WanxiangError(f"下载失败：{exc.reason}") from exc

    if asset.size and target.stat().st_size != asset.size:
        raise WanxiangError(f"{asset.name} 大小校验失败，期望 {asset.size}，实际 {target.stat().st_size}")
    if log:
        log(f"下载完成 {asset.name} ({target.stat().st_size} bytes)")
    return target


def extract_zip(zip_path: Path, temp_dir: Path, log=None) -> Path:
    extract_dir = temp_dir / zip_path.stem
    extract_dir.mkdir(parents=True, exist_ok=True)
    if log:
        log(f"开始解压 {zip_path.name}")
    with zipfile.ZipFile(zip_path) as zip_ref:
        for info in zip_ref.infolist():
            member_name = decode_zip_member_name(info.filename)
            if not member_name or member_name.endswith("/"):
                safe_target(extract_dir, member_name).mkdir(parents=True, exist_ok=True)
                continue
            target = safe_target(extract_dir, member_name)
            target.parent.mkdir(parents=True, exist_ok=True)
            with zip_ref.open(info) as source, target.open("wb") as destination:
                shutil.copyfileobj(source, destination)
    children = [path for path in extract_dir.iterdir() if path.name != "__MACOSX"]
    if len(children) == 1 and children[0].is_dir():
        result = children[0]
    else:
        result = extract_dir
    if log:
        log(f"解压完成 {zip_path.name}")
    return result


def ensure_exclude_file() -> Path:
    exclude_file = exclude_file_path()
    if not exclude_file.exists():
        exclude_file.parent.mkdir(parents=True, exist_ok=True)
        exclude_file.write_text(
            "\n".join(["# 排除文件本身（请勿删除）", *DEFAULT_EXCLUDES, ""]) ,
            encoding="utf-8",
        )
    return exclude_file


def read_excludes() -> set[str]:
    exclude_file = ensure_exclude_file()
    excludes = set(DEFAULT_EXCLUDES)
    for line in exclude_file.read_text(encoding="utf-8").splitlines():
        value = line.strip()
        if value and not value.startswith("#"):
            excludes.add(value)
    return excludes


def should_skip(relative_path: str, excludes: set[str], component: str) -> bool:
    normalised = relative_path.replace(os.sep, "/")
    if component == "scheme" and Path(normalised).name in SCHEME_SKIP_FILES:
        return True
    return normalised in excludes


def backup_existing(target: Path, backup_dir: Path, relative_path: Path) -> bool:
    if not target.exists() or target.is_dir():
        return False
    backup_path = backup_dir / relative_path
    backup_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(target, backup_path)
    return True


def copy_tree(source_dir: Path, target_dir: Path, component: str, log=None) -> tuple[int, int]:
    target_dir.mkdir(parents=True, exist_ok=True)
    backup_dir = RimeConfig.backup_root() / datetime.now().strftime("%Y%m%d-%H%M%S") / component
    excludes = read_excludes() if component == "scheme" else set()
    copied = 0
    backed_up = 0

    for source in source_dir.rglob("*"):
        if source.is_dir():
            continue
        relative = source.relative_to(source_dir)
        relative_text = relative.as_posix()
        if should_skip(relative_text, excludes, component):
            continue
        target = target_dir / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        if backup_existing(target, backup_dir, relative):
            backed_up += 1
        shutil.copy2(source, target)
        copied += 1
        if log and copied % 20 == 0:
            log(f"已复制 {component_label(component)}文件 {copied} 个")

    return copied, backed_up


def install_asset(asset: Asset, log=None) -> str:
    RimeConfig.setting_dir().mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="wanxiang-alfred-") as tmp:
        temp_dir = Path(tmp)
        downloaded = download_asset(asset, temp_dir, log=log)

        if asset.component == "model":
            backup_dir = RimeConfig.backup_root() / datetime.now().strftime("%Y%m%d-%H%M%S") / "model"
            target = RimeConfig.setting_dir() / MODEL_FILE
            target.parent.mkdir(parents=True, exist_ok=True)
            backed_up = 1 if backup_existing(target, backup_dir, Path(MODEL_FILE)) else 0
            if log:
                log(f"写入模型文件 {target}")
            shutil.copy2(downloaded, target)
            save_record(asset)
            if log:
                log(f"模型记录已更新：{asset.tag} / {asset.name}")
            return f"模型已更新：{asset.name}（备份 {backed_up} 个文件）"

        extracted = extract_zip(downloaded, temp_dir, log=log)
        target_dir = RimeConfig.setting_dir() if asset.component == "scheme" else RimeConfig.dict_dir()
        if log:
            log(f"开始写入 {component_label(asset.component)} 到 {target_dir}")
        copied, backed_up = copy_tree(extracted, target_dir, asset.component, log=log)
        save_record(asset)
        if log:
            log(f"{component_label(asset.component)}记录已更新：{asset.tag} / {asset.name}")
        return f"{component_label(asset.component)}已更新：{asset.name}（复制 {copied} 个文件，备份 {backed_up} 个文件）"


def deploy_rime(log=None) -> str:
    engine = RimeConfig.engine()
    if engine == "squirrel":
        executable = Path("/Library/Input Methods/Squirrel.app/Contents/MacOS/Squirrel")
        args = ["--reload"]
    elif engine in {"fcitx", "fcitx5"}:
        executable = Path("/Library/Input Methods/Fcitx5.app/Contents/bin/fcitx5-curl")
        args = ["/config/addon/rime/deploy", "-X", "POST", "-d", "{}"]
    else:
        raise WanxiangError(f"未知输入法引擎：{engine}")

    if not executable.exists():
        raise WanxiangError(f"找不到部署程序：{executable}")
    if not os.access(executable, os.X_OK):
        raise WanxiangError(f"部署程序不可执行：{executable}")

    if log:
        log(f"开始部署：{executable} {' '.join(args)}")
    try:
        result = subprocess.run(
            [str(executable), *args],
            check=False,
            capture_output=True,
            text=True,
            timeout=120,
        )
    except subprocess.SubprocessError as exc:
        raise WanxiangError(f"部署失败：{exc}") from exc

    if result.returncode != 0:
        detail = (result.stderr or result.stdout or "").strip()
        raise WanxiangError(f"部署失败：{detail or result.returncode}")
    if log:
        log("部署命令执行完成")
    return "已触发 RIME 重新部署"


def parse_command(command: str) -> tuple[str, str, str]:
    parts = command.split("@", 2)
    component = parts[0].strip()
    tag = parts[1].strip() if len(parts) > 1 else ""
    name = parts[2].strip() if len(parts) > 2 else ""
    return component, tag, name


def status_text(include_records: bool = False) -> str:
    text = (
        f"源：{source_label()}；方案：{RimeConfig.schema_label()}；"
        f"引擎：{RimeConfig.engine()}；目录：{RimeConfig.setting_dir()}"
    )
    if include_records:
        text = f"{text}；记录文件：{records_path()}；排除文件：{exclude_file_path()}；{local_records_summary()}"
    return text
