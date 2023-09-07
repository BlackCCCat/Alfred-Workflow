from bs4 import BeautifulSoup
import os
import sys
import json
import re


class BookMarks():
    def __init__(self, file):
        self.file = file
        self.res = dict()
    
    def getBookmarks(self):
        with open(self.file, 'r') as bks:
            bks_str = bks.read()
        soup = BeautifulSoup(bks_str, 'html.parser')
        a_tags = soup.find_all('a')
        for a_tag in a_tags:
            link = a_tag['href']
            _title = a_tag.text
            self.res[_title] = link
        return self.res

    def show(self, data: dict) -> str:
        items = []
        for _title in data:
            link = data[_title]
    
            line = {
                'type':'default',
                'title':_title,
                'subtitle':f'Bookmark:{link}',
                'arg':link
            }
            
            if sys.argv[2]:
                target = sys.argv[2]
                if re.search(target, _title, flags=re.IGNORECASE):
                    items.append(line)
                elif re.search(target, link, flags=re.IGNORECASE):
                    items.append(line)
            else:
                items.append(line)
        result_json = json.dumps({"items":items}, ensure_ascii=False)
        return result_json



def showNoneFileInfo(wk_path):
    items = [
        {
         'type':'default',
         'title':f"Bookmarks file doesn't exists, please export Bookmarks to current path",
         'subtitle':f'Enter ↵ to open current directory:{wk_path}',
         'arg':wk_path
        }
    ]
    
    result_json = json.dumps({"items":items}, ensure_ascii=False)
    return result_json
    


def main():
    current_dir = os.getcwd()
    file_name = sys.argv[1] # Safari Bookmarks.html
    html_dir = os.path.join(current_dir, file_name)
    exists = os.path.exists(html_dir)
    if exists:
        bk = BookMarks(html_dir)
        data = bk.getBookmarks()
        result_json = bk.show(data)
    else:
        result_json = showNoneFileInfo(current_dir)
    
    print(result_json)


if __name__ == "__main__":
    main()