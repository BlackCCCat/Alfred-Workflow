import os
from pathlib import Path


OWNER = "amzxyz"
GITHUB_REPO = "rime_wanxiang"
CNB_REPO = "rime-wanxiang"
MODEL_REPO = "RIME-LMDG"
MODEL_TAG = "LTS"
MODEL_FILE = "wanxiang-lts-zh-hans.gram"

GITHUB_RELEASES_API = f"https://api.github.com/repos/{OWNER}/{GITHUB_REPO}/releases"
GITHUB_MODEL_API = f"https://api.github.com/repos/{OWNER}/{MODEL_REPO}/releases/tags/{MODEL_TAG}"
CNB_RELEASES_API = f"https://cnb.cool/{OWNER}/{CNB_REPO}/-/releases"

REQUEST_TIMEOUT = 30

CNB_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
    "Accept": "application/vnd.cnb.web+json",
}

GITHUB_HEADERS = {
    "User-Agent": "Alfred-Rime-Wanxiang-Updater/4.0",
    "Accept": "application/vnd.github+json",
}

GITHUB_TOKEN = (os.getenv("github_token") or "").strip()
if GITHUB_TOKEN:
    GITHUB_HEADERS["Authorization"] = f"Bearer {GITHUB_TOKEN}"

SCHEMA_LABELS = {
    "base": "标准版",
    "moqi": "墨奇辅助码",
    "flypy": "小鹤辅助码",
    "zrm": "自然码辅助码",
    "tiger": "虎码辅助码",
    "wubi": "五笔辅助码",
    "hanxin": "汉心辅助码",
    "shouyou": "首右辅助码",
}

SCHEME_ASSETS = {
    "base": "rime-wanxiang-base.zip",
    "moqi": "rime-wanxiang-moqi-fuzhu.zip",
    "flypy": "rime-wanxiang-flypy-fuzhu.zip",
    "zrm": "rime-wanxiang-zrm-fuzhu.zip",
    "tiger": "rime-wanxiang-tiger-fuzhu.zip",
    "wubi": "rime-wanxiang-wubi-fuzhu.zip",
    "hanxin": "rime-wanxiang-hanxin-fuzhu.zip",
    "shouyou": "rime-wanxiang-shouyou-fuzhu.zip",
}

DICT_ASSETS = {
    "base": "base-dicts.zip",
    "moqi": "pro-moqi-fuzhu-dicts.zip",
    "flypy": "pro-flypy-fuzhu-dicts.zip",
    "zrm": "pro-zrm-fuzhu-dicts.zip",
    "tiger": "pro-tiger-fuzhu-dicts.zip",
    "wubi": "pro-wubi-fuzhu-dicts.zip",
    "hanxin": "pro-hanxin-fuzhu-dicts.zip",
    "shouyou": "pro-shouyou-fuzhu-dicts.zip",
}

DEFAULT_EXCLUDES = [
    "custom/user_exclude_file.txt",
    "lua/sequence.userdb",
    "lua/sequence.txt",
    "lua/input_stats.lua",
    "zc.userdb",
    "wanxiang.userdb",
    "installation.yaml",
    "user.yaml",
    "default.custom.yaml",
    "wanxiang_pro.custom.yaml",
    "wanxiang_reverse.custom.yaml",
    "wanxiang_mixedcode.custom.yaml",
]

SCHEME_SKIP_FILES = {
    "custom_phrase.txt",
    "squirrel.yaml",
    "weasel.yaml",
    "简纯+.trime.yaml",
}


class RimeConfig:
    @classmethod
    def engine(cls) -> str:
        return (os.getenv("rime_engine") or "squirrel").strip().lower()

    @classmethod
    def source(cls) -> str:
        source = (os.getenv("source") or os.getenv("download_source") or "cnb").strip().lower()
        return source if source in {"cnb", "github"} else "cnb"

    @classmethod
    def schema(cls) -> str:
        schema = (os.getenv("schema") or "moqi").strip().lower()
        return schema if schema in SCHEMA_LABELS else "moqi"

    @classmethod
    def schema_label(cls) -> str:
        return SCHEMA_LABELS[cls.schema()]

    @classmethod
    def scheme_asset(cls) -> str:
        return SCHEME_ASSETS[cls.schema()]

    @classmethod
    def dict_asset(cls) -> str:
        return DICT_ASSETS[cls.schema()]

    @classmethod
    def setting_dir(cls) -> Path:
        custom_dir = (os.getenv("rime_user_dir") or "").strip()
        if custom_dir:
            return Path(custom_dir).expanduser()

        home = Path.home()
        engine = cls.engine()
        if engine == "squirrel":
            return home / "Library" / "Rime"
        if engine in {"fcitx", "fcitx5"}:
            return home / ".local" / "share" / "fcitx5" / "rime"
        return home / "Library" / "Rime"

    @classmethod
    def dict_dir(cls) -> Path:
        return cls.setting_dir() / "dicts"

    @classmethod
    def backup_root(cls) -> Path:
        return cls.setting_dir() / "UpdateBackups"
