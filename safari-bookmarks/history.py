import sqlite3
import os
import shutil
import sys
import datetime
import re
import json


class History():

    @staticmethod
    def sql(db: str) -> list:
        """
        Executes SQL depending on History path
        provided in db: str

        Args:
            db (str): Path to History file

        Returns:
            list: result list of dictionaries (Url, Title, VisiCount)
        """
        res = []
        history_db = os.getcwd()

        try:
            shutil.copy2(db, history_db)
            c = sqlite3.connect(os.path.join(history_db, "History.db"))
            cursor = c.cursor()
            # SQL satement for Safari
            if "Safari" in db:
                select_statement = f"""
                    SELECT history_items.url, history_visits.title, history_items.visit_count,(history_visits.visit_time + 978307200)
                    FROM history_items
                        INNER JOIN history_visits
                        ON history_visits.history_item = history_items.id
                    WHERE history_items.url IS NOT NULL AND
                        history_visits.TITLE IS NOT NULL AND
                        history_items.url != '' order by visit_time DESC
                """
            # SQL statement for Chromium Brothers
            else:
                select_statement = f"""
                    SELECT DISTINCT urls.url, urls.title, urls.visit_count, (urls.last_visit_time/1000000 + (strftime('%s', '1601-01-01')))
                    FROM urls, visits
                    WHERE urls.id = visits.url AND
                    urls.title IS NOT NULL AND
                    urls.title != '' order by last_visit_time DESC; """
            cursor.execute(select_statement)
            r = cursor.fetchall()
            res.extend(r)
            os.remove(os.path.join(history_db, 'History.db'))  # Delete History file in current dir
            os.remove(os.path.join(history_db, 'History.db-shm'))
            os.remove(os.path.join(history_db, 'History.db-wal'))
        except sqlite3.Error as e:
            raise Exception(f"SQL Error: {e}")
        return res
    
    @staticmethod
    def format(data:tuple):
        """
        将SQL输出结果格式化为dict
        """
        items = list()
        def timeFormat(timestamp):
            """
            时间戳转换
            """
            # 将时间戳转换为 datetime 对象
            dt_object = datetime.datetime.fromtimestamp(int(timestamp))
            # 将 datetime 对象格式化为指定的时间字符串
            formatted_time = dt_object.strftime('%Y-%m-%d %H:%M:%S')
            return formatted_time

        for line in data:
            _title = line[1]
            link = line[0]
            visit_count = line[2]
            _time = line[3]
            visit_time = timeFormat(_time)
            line_dict = {
            'type': 'default',
            'title': link if _title == '' else _title,
            'subtitle': f'{visit_count} visits on {visit_time} - {link}',
            'arg': link
            }
            items.append(line_dict)
    
        return items
    

    @staticmethod
    def show(items):
        re_list = []
        for item in items:
            if len(sys.argv) == 2:
                target = sys.argv[1]
                _title = item['title']
                link = item['arg']
                if re.search(target, _title, flags=re.IGNORECASE):
                    re_list.append(item)
                elif re.search(target, link, flags=re.IGNORECASE):
                    re_list.append(item)
            else:
                re_list.append(item)

        result_json = json.dumps({"items":re_list}, ensure_ascii=False)
        return result_json
            



def main():
    # Get History file path
    history_db_path = os.environ['HOME'] + '/Library/Safari/History.db'
    # Get History file content
    history_db = History.sql(history_db_path)
    items = History.format(history_db)
    output = History.show(items)
    print(output)


if __name__ == "__main__":
    main()
    