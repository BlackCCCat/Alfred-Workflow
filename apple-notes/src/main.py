import sys
import sqlite3

from formating import FormatToAlfred
from search import Search
from data import ReadDataBase

class ReadNotesDB(ReadDataBase):
    def __init__(self, db_path, db_name):
        super().__init__(db_path, db_name)
    
    def readNotesTable(self):
        """
        读取表数据
        :return: db_res: list(tuple)
        """
        try:
            conn = sqlite3.connect(self.db)
            cursor = conn.cursor()
            cursor.execute("""
                           select ztitle1
                                ,zsnippet
                                ,ZWIDGETSNIPPET
                            from ZICCLOUDSYNCINGOBJECT
                            where ZWIDGETSNIPPET is not null
                           """)
            db_res = cursor.fetchall()
            return db_res
        except sqlite3.Error as e:
            raise Exception(f"SQL Error: {e}")

def main():
    db_path = 'Library/Group Containers/group.com.apple.notes'
    db_name = 'NoteStore.sqlite'
    db = ReadNotesDB(db_path, db_name)
    db_res_list = db.readNotesTable()

    fmt = FormatToAlfred()

    for db_res in db_res_list:
        title, subtitle, arg = db_res[0], db_res[1], db_res[2]
        item = fmt.item_format(
            title = title,
            subtitle = subtitle,
            arg = arg,
        )

        try:
            if len(sys.argv) == 2:
                target = sys.argv[1]
            if len(sys.argv) > 2:
                target = ' '.join(sys.argv[1:])
            search_res = Search.searchItem(item, target)
        except:
            search_res = True

        if search_res:
            items = fmt.items_format(item)
        else:
            pass
    print(items)



if __name__ == "__main__":
    main()