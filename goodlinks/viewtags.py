import re
import sys
import json
import os

from showtags import ShowTags
from readdb import Database as DB

def search(target, ld):
    items_list = []
    searched_res = []

    content_list_dict = DB().readContentTable()

    for db_dict in ld:
        target = re.escape(target)
        if re.search(target, str(db_dict['title']) + str(db_dict['summary'] + str([content_dict['content'] for content_dict in content_list_dict if content_dict['id'] == db_dict['id']])), flags=re.IGNORECASE):
            searched_res.append(db_dict)
        else:
            continue
    
    abs_file_path = os.path.abspath(__file__)
    abs_path = os.path.dirname(abs_file_path)

    
    for result in searched_res:
        is_read = True if result['readAt'] else False
        if is_read:
            icon_path = os.path.join(abs_path, 'assets', 'read.png')
        else:
            icon_path = os.path.join(abs_path, 'assets', 'unread.png')

        for content_dict in content_list_dict:
            if content_dict['id'] == result['id']:
                article_content = content_dict['content']
            else:
                continue

        search_result = {
                "type": "default",
                "title": result['title'],
                "subtitle": result['summary'],
                "arg": f"goodlinks://x-callback-url/open?id={result['id']}",
                "icon":{
                    "path": icon_path
                },
                "quicklookurl": result['url'],
                "text": {
                    "copy": result['url'],
                    "largetype": article_content
                },
            }
        items_list.append(search_result)
        
    return json.dumps({"items": items_list}, ensure_ascii=False)


def main():
    if len(sys.argv) == 3:
        tag_target = sys.argv[1]
        target = sys.argv[2]
    elif len(sys.argv) == 2:
        tag_target = sys.argv[1]
        target = ''
    else:
        tag_target = ''
        target = ''
    

    ld = ShowTags.run(tag_target)
    result = search(target, ld)
    print(result)


if __name__ == "__main__":
    main()