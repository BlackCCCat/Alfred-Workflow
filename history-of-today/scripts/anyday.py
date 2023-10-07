import sys
import json

from history import HistoryOfToday
from show import alfred

class AnyDay(HistoryOfToday):
    def __init__(self, month, day):
        super().__init__()
        self.now_month = "{:02d}".format(month)
        self.now_day = "{:02d}".format(day)


def get_date(md):
    """
    :param md: md is month and day(must be 4 digits), e.g. 0101 means month="01" and day="01"
    :return: month, day
    """
    month, day = int(md[0:2]), int(md[2:])
    return month, day



def main():
    date_info = sys.argv[1]
    if len(date_info) == 4:
        month, day = get_date(date_info)
        any = AnyDay(month, day)
        data = any.get_web_info()
        print(alfred(data))
    else:
        items = [
            {
            'type':'default',
			'title':'请输入正确日期',
			'subtitle': '日期格式为四位数，如0101为1月1日',
        }
        ]
        result = json.dumps({"items":items}, ensure_ascii=False)
        print(result)


if __name__ == "__main__":
    main()
