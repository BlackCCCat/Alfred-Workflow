import os
import sys
import json
import re
import plistlib


class BookMarks():
    res = dict()
    
    @staticmethod
    def getPlistFile():
        home_dir = os.environ['HOME']
        # 书签文件名称
        filename = 'Bookmarks.plist'
        # 书签文件路径
        file_path = os.path.join(home_dir, 'Library/Safari', filename)
        is_exists = os.path.exists(file_path)
        return file_path if is_exists else None, is_exists
    
    @staticmethod
    def readPlistBookmarks():
        """
        从系统路径中读取Safari的书签文件，需要授予磁盘访问权限
        返回字典
        """
        file_path = BookMarks.getPlistFile()[0]
        # 加载plist文件
        with open(file_path, 'rb') as fp:
            plist_data = plistlib.load(fp)
        # 取出包含书签标题和链接的数据 返回list
        data_list = plist_data['Children'][1]['Children']

        if data_list:
            for data_dict in data_list:
                try:
                    # bookmark title
                    bm_title = data_dict['URIDictionary']['title']
                    if bm_title:
                        # 对应bookmark title 的 bookmark link
                        bm_link = data_dict['URLString']
                        BookMarks.res.update({bm_title: bm_link})
                except:
                    _children_list = data_dict['Children']
                    if _children_list:
                        for children_dict in _children_list:
                            bm_title = children_dict['URIDictionary']['title']
                            bm_link = children_dict['URLString']
                            BookMarks.res.update({bm_title: bm_link})
        return BookMarks.res

    @staticmethod
    def show(data: dict) -> str:
        items = []
        for _title in data:
            link = data[_title]
    
            line = {
                'type':'default',
                'title':_title,
                'subtitle':f'Bookmark:{link}',
                'arg':link
            }
            
            try:
                target = sys.argv[1]
                if re.search(target, _title, flags=re.IGNORECASE):
                    items.append(line)
                elif re.search(target, link, flags=re.IGNORECASE):
                    items.append(line)
            except:
                items.append(line)
        result_json = json.dumps({"items":items}, ensure_ascii=False)
        return result_json



def showNoneFileInfo(wk_path):
    items = [
        {
         'type':'default',
         'title':f"Bookmarks file doesn't exists, please export Bookmarks to current path",
         'subtitle':f'Enter ↵ to open current directory:{wk_path}',
         'arg':'↵'
        }
    ]
    
    result_json = json.dumps({"items":items}, ensure_ascii=False)
    return result_json
    


def main():
    current_dir = os.getcwd()
    exists = BookMarks.getPlistFile()[1]
    if exists:
        data = BookMarks.readPlistBookmarks()
        result_json = BookMarks.show(data)
    else:
        result_json = showNoneFileInfo(current_dir)
    
    print(result_json)


if __name__ == "__main__":
    main()