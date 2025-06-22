import requests
import zipfile
import io
import sys
import os
import re

from config import rimeConfig
class RimeUpdater:
    def __init__(self):
        self.model_link = "https://github.com/amzxyz/RIME-LMDG/releases/download/LTS/wanxiang-lts-zh-hans.gram"
        

    def download(self, zip_name):
        """下载RIME输入法文件"""
        if 'dict' in zip_name:
            setting_dir = os.path.join(rimeConfig.setting_dir(), "zh_dicts_pro")
        else:
            setting_dir = rimeConfig.setting_dir()
        
        url = f"https://github.com/amzxyz/rime_wanxiang/releases/download/{zip_name}"

        # 1. 下载ZIP文件内容（不保存到磁盘）
        response = requests.get(url)

        # 确保下载成功
        if response.status_code == 200:
            # 2. 将下载的二进制数据存储到BytesIO对象中
            zip_data = io.BytesIO(response.content)

            # 3. 使用zipfile模块处理这个BytesIO对象
            with zipfile.ZipFile(zip_data, 'r') as zip_ref:
                # 获取ZIP文件中的所有文件名
                zip_contents = zip_ref.namelist()
                for file_name in zip_contents:
                    if file_name.endswith('/'):
                        os.makedirs(os.path.join(setting_dir, file_name), exist_ok=True)
                    else:
                        out_put_path = os.path.join(setting_dir, file_name)
                        with open(out_put_path, 'wb') as f:
                            f.write(zip_ref.read(file_name))

            print("下载完成，请重新部署")
        else:
            print(f"下载失败，状态码: {response.status_code}")


    def download_model(self):
        """下载模型文件"""
        url = self.model_link
        response = requests.get(url)
        if response.status_code == 200:
            with open(os.path.join(rimeConfig.setting_dir(), 'wanxiang-lts-zh-hans.gram'), 'wb') as f:
                f.write(response.content)
            print("下载模型完成，请重新部署")
        else:
            print(f"下载失败，状态码: {response.status_code}")

def main(zip_name):
    updater = RimeUpdater()
    updater.download(zip_name)
    updater.download_model()

if __name__ == '__main__':
    zip_name = sys.argv[1]
    main(zip_name)