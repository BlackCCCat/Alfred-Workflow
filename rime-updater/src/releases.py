import requests
import sys
import os
from datetime import datetime

from config import rimeConfig
from alfred import FormatToAlfred

ABS_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

class GetReleases:
    def __init__(self):
        self.full_releases = []
        self.dicts = []
        self.full = []
        self.releases_api = "https://api.github.com/repos/amzxyz/rime_wanxiang_pro/releases"


    def get_releases(self):
        """获取releases信息"""
        response = requests.get(self.releases_api)
        if response.status_code == 200:
            self.full_releases = response.json()
            for release in self.full_releases:
                if 'dict' in release['tag_name']:
                    self.dicts.append(release)
                else:
                    self.full.append(release)
        else:
            print(f"获取版本信息失败，状态码: {response.status_code}")
        

    def output_dicts(self):
        """使用Alfred接口输出词库的releases信息"""
        dicts_alfred = FormatToAlfred()
        dicts_name = []
        for dict in self.dicts:
            for asset in dict['assets']:
                if asset.get('name'):
                    dicts_name.append(asset.get('name', ''))
            
            for name in set(dicts_name):
                if rimeConfig.SCHEMA in name:
                    dicts_alfred.item_format(
                            title=dict['name'],
                            type="default",
                            subtitle=dict['published_at'],
                            arg=f"{dict['tag_name']}/{name}",
                            icontype="",
                            iconpath=f"{ABS_DIR}/icon.png",
                        )
        print(dicts_alfred.json_dumps_items)

    def output_full(self):
        """使用Alfred接口输出完整输入方案的releases信息"""
        full_alfred = FormatToAlfred()
        asset_name = []
        for release in self.full:
            for asset in release['assets']:
                if asset.get('name'):
                    asset_name.append(asset.get('name', ''))

            for name in set(asset_name):
                if rimeConfig.SCHEMA in name:
                    full_alfred.item_format(
                        title=release['name'],
                        type="default",
                        subtitle=release['published_at'],
                        arg=f"{release['tag_name']}/{name}",
                        icontype="",
                        iconpath=f"{ABS_DIR}/icon.png",
                    )
        print(full_alfred.json_dumps_items)


def main():
    releases = GetReleases()
    releases.get_releases()
    if len(sys.argv) > 1 and sys.argv[1] == 'dicts':
        releases.output_dicts()
    else:
        releases.output_full()
    

if __name__ == "__main__":
    main()