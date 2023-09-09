import re
# import sys
# import json

from readdb import Database
from mapdata import MapData


class ShowTags():
    @staticmethod
    def searchTag(tags, db_list):
        """
        params: 
        tags: str
        db_list: list(dict), Database instance
        from tb_list: list(dict) search tags with regex
        return bool
        """
        searched_res = []
        for db_dict in db_list:
            if re.search(tags, db_dict['tags'], flags=re.IGNORECASE):
                searched_res.append(db_dict)
            else:
                continue
        return searched_res


    @staticmethod
    def run(search_target):
        DB = Database()
        table_link = DB.readLinkTable()
        try:
            # search_target = sys.argv[1]
            searched_res = ShowTags.searchTag(search_target, table_link)
            # print(searched_res)
            return searched_res
            # result = MapData().loadLink(searched_res)
            # print(result)
        except Exception as e:
            print(e)

def main():
    result = ShowTags.run('python')
    print(result)




if __name__ == "__main__":
    main()