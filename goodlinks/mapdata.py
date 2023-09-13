#! -*- coding: utf-8 -*-

import json
import re
import sys
import os

from readdb import Database as DB



class MapData():
    """
    load db data into alfred workflow items
    """

    @staticmethod
    def search(items, type):
        """
        search items[type] with target(which is the second param of this script)
        """
        if len(sys.argv) == 2:
            target = re.escape(sys.argv[1])
            if items[type]:
                search_res = re.search(target, items[type], flags=re.IGNORECASE)
                return True if search_res else False
            else:
                pass
        elif len(sys.argv) == 3:
            target = re.escape(sys.argv[2])
            if items[type]:
                search_res = re.search(target, items[type], flags=re.IGNORECASE)
                return True if search_res else False
            else:
                pass
        else:# without target, search all items
            return True




    def loadState(self, state_list_dict=DB().readStateTable()):
        """
        load state table data to alfred workflow items data
        return :items: {"items":[{}]}
        """
        # state_list_dict = DB().readStateTable()
        items_list = []
        for state_dict in state_list_dict:
            item = {
                "type": "default",
                "title": state_dict['name'],
                "subtitle": f"Unread: {state_dict['unreadTotal']}   Total:{state_dict['total']}",
                "arg": state_dict['name'],
                "icon": {
                    "path": os.path.join(os.path.dirname(__file__), 'tags.png')
                }
            }

            if MapData.search(item, 'title'):
                items_list.append(item)

        # `ensure_ascii=False` make sure output is Chinese
        items = json.dumps({"items":items_list}, ensure_ascii=False)
        return items
    

    def loadLink(self, link_list_dict=DB().readLinkTable()):
        """
        load link table data to alfred workflow items data
        """
        abs_file_path = os.path.abspath(__file__)
        abs_path = os.path.dirname(abs_file_path)
        
        # link_list_dict = DB().readLinkTable()
        content_list_dict = DB().readContentTable()

        items_list = []
        for link_dict in link_list_dict:
            is_read = True if link_dict['readAt'] else False
            if is_read:
                icon_path = os.path.join(abs_path, 'assets', 'read.png')
            else:
                icon_path = os.path.join(abs_path, 'assets', 'unread.png')
            
            for content_dict in content_list_dict:
                if content_dict['id'] == link_dict['id']:
                    article_content = content_dict['content']
                else:
                    continue

            item = {
                "type": "default",
                "title": link_dict['title'],
                "subtitle": link_dict['summary'],
                "arg": f"goodlinks://x-callback-url/open?id={link_dict['id']}", # f"goodlinks://x-callback-url/open?url={link_dict['url']}",
                "icon":{
                    "path": icon_path
                },
                "quicklookurl": link_dict['url'],
                "text": {
                    "copy": link_dict['url'],
                    "largetype": article_content
                },
            }

            if MapData.search(item, 'title') or MapData.search(item, 'subtitle') or MapData.search(item['text'], 'largetype'):
                items_list.append(item)
            
        # `ensure_ascii=False` make sure output is Chinese
        items = json.dumps({"items":items_list}, ensure_ascii=False)
        return items


def main():
    items = MapData().loadLink()
    print(items)

if __name__ == "__main__":
    main()