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
            setting_dir = os.path.join(rimeConfig.setting_dir(), "cn_dicts")
        else:
            setting_dir = rimeConfig.setting_dir()
        
        url = f"https://github.com/amzxyz/rime_wanxiang_pro/releases/download/{zip_name}"

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

                # 获取第一层级的文件夹（假设只有一个第一层级文件夹）
                first_level_folder = None
                for file_name in zip_contents:
                    # 找到第一个文件夹的路径
                    if '/' in file_name:  # 判断是否为文件夹
                        first_level_folder = file_name.split('/')[0]
                    break

                if first_level_folder:
                    # 4. 提取文件到指定的路径
                    output_directory =  setting_dir  # 提取内容的目标路径
                    os.makedirs(output_directory, exist_ok=True)  # 创建目标目录，如果不存在的话

                    for file_name in zip_contents:
                        if file_name.startswith(first_level_folder + '/'):
                            # 去除第一层级文件夹部分，提取文件
                            extracted_path = os.path.join(output_directory, file_name[len(first_level_folder)+1:])

                            # 创建目标路径所在的目录
                            if not file_name.endswith('/'):  # 判断是不是文件
                                os.makedirs(os.path.dirname(extracted_path), exist_ok=True)


                                # 解压文件内容到目标路径
                                with open(extracted_path, 'wb') as f:
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