import os
import sqlite3
import json
import re

from getpath import getPath

class Database():
    """
    get goodlinks app database data
    """
    def __init__(self):
        """
        params: db : str, sqlite3 file absolute path
        """
        _, self.db = getPath('goodlinks')
    
    def readLinkTable(self):
        """
        load table link
        TABLE "link" :
        ("id" TEXT PRIMARY KEY, "url" TEXT NOT NULL COLLATE NOCASE, "originalURL" TEXT COLLATE NOCASE, "title" TEXT COLLATE NOCASE, "summary" TEXT COLLATE NOCASE, "author" TEXT COLLATE NOCASE, "preview" TEXT COLLATE NOCASE, "tags" TEXT COLLATE NOCASE, "starred" BOOLEAN NOT NULL, "readAt" DOUBLE NOT NULL, "addedAt" DOUBLE NOT NULL, "modifiedAt" DOUBLE NOT NULL, "fetchStatus" INTEGER NOT NULL, "status" INTEGER NOT NULL, "highlightTotal" INTEGER)
        return: table_link: list(dict)
        """
        table_link = []
        try:
            conn = sqlite3.connect(self.db)
            cursor = conn.cursor()
            # readAt:read time(timestamp), addedAt:add time(timestamp)
            cursor.execute("""
                           select id, url, title, summary, preview, tags, starred, readAt, addedAt
                           from link
                           """)
            # table_link_origin = cursor.fetchall()
            
            for row in cursor: 
                row_dict = dict()
                row_dict['id'], row_dict['url'], row_dict['title'], row_dict['summary'] = row[0], row[1], row[2], row[3]
                row_dict['preview'], row_dict['tags'], row_dict['starred'] =  row[4], row[5], row[6]
                row_dict['readAt'], row_dict['addedAt'] = row[7], row[8]
                table_link.append(row_dict)
            return table_link
        except sqlite3.Error as e:
            raise Exception(f"SQL Error: {e}")
        
    
    def readStateTable(self):
        """
        load table state
        TABLE "state" :
        CREATE TABLE "state" ("id" TEXT PRIMARY KEY, "data" BLOB NOT NULL)
        return: table_state: list(dict)
        """
        table_state = []
        try:
            conn = sqlite3.connect(self.db)
            cursor = conn.cursor()
            cursor.execute("""
                           select data
                           from state 
                           where id='ListState'
                           """)
            # table_state_origin is list(tuple)
            table_state_origin = cursor.fetchall()
            # state_data_bytes is bytes
            state_data_bytes = table_state_origin[0][0]
            state_data_json = json.loads(state_data_bytes.decode('utf-8'))
            state_data_list = state_data_json['lists']
            for i in state_data_list:
                if isinstance(i ,dict):
                    # key id and index 0 is untagged and key name is empty
                    if re.search('untagged', i['id'][0]) and i['name'] == '':
                        i['name'] = 'untagged'
                    # key id and index 0 is tag and key name is not empty
                    elif re.search('tag', i['id'][0]) and i['name'] != '':
                        pass
                    else:
                        continue # i['name'] = i['id'][0]
                    table_state.append(i)
            return table_state
        except sqlite3.Error as e:
            raise Exception(f"SQL Error: {e}")



def main():
    DB = Database()
    # table_state = DB.readStateTable()
    # print(table_state)

    table_link = DB.readLinkTable()
    print(table_link)

if __name__ == "__main__":
    main()