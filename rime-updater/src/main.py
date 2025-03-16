import requests
import zipfile
import io
import sys
import os

from config import rimeConfig
from alfred import FormatToAlfred

alfred = FormatToAlfred()

class RimeUpdater:
    def __init__(self):
        self.link = rimeConfig.INPUTMETHOD_LINK
        self.setting_dir = rimeConfig.setting_dir()


    def check(self):
        if not self.link:
            res = alfred.item_format(title='No link', subtitle='Please set the link in the workflow settings')
            print(res)
            return False
        
        if not self.link.endswith('.zip'):
            res = alfred.item_format(title='Error link', subtitle='Please set the zip file downloadlink')
            print(res)
            return False
        
        return True

    def download(self, mode='dict'):
        check = self.check()
        if not check:
            return

        # 1. 下载ZIP文件内容（不保存到磁盘）
        url = self.link
        response = requests.get(url)

        # 确保下载成功
        if response.status_code == 200:
            # 2. 将下载的二进制数据存储到BytesIO对象中
            zip_data = io.BytesIO(response.content)

            # 3. 使用zipfile模块处理这个BytesIO对象
            with zipfile.ZipFile(zip_data, 'r') as zip_ref:
                # 获取ZIP文件中的所有文件名
                all_zip_contents = zip_ref.namelist()
                if mode == 'dict':
                    zip_contents = [name for name in all_zip_contents if "dict" in name or "zh-hans" in name]
                else:
                    zip_contents = all_zip_contents

                # 获取第一层级的文件夹（假设只有一个第一层级文件夹）
                first_level_folder = None
                for file_name in zip_contents:
                    # 找到第一个文件夹的路径
                    if '/' in file_name:  # 判断是否为文件夹
                        first_level_folder = file_name.split('/')[0]
                    break

                if first_level_folder:
                    # 4. 提取文件到指定的路径
                    output_directory =  self.setting_dir  # 提取内容的目标路径
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

if __name__ == '__main__':
    updater = RimeUpdater()
    mode = sys.argv[1] if len(sys.argv) > 1 else 'dict'
    updater.download(mode=mode)
