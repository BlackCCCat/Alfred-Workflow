import requests
import json
import datetime
from bs4 import BeautifulSoup

class HistoryOfToday():
    def __init__(self):
        self.today = datetime.date.today()
        self.now_month = "{:02d}".format(self.today.month)
        self.now_day = "{:02d}".format(self.today.day)


    def html_parser(self, target, picker, is_text=True):
        result = BeautifulSoup(target[picker], 'html.parser')
        if is_text:
            str_result = result.text
        else:
            str_result = result
        return str_result
    
    def get_web_info(self):
        result_dict = dict()
        url = f'https://baike.baidu.com/cms/home/eventsOnHistory/{self.now_month}.json'
        res = requests.get(url)
        history_info_json = json.loads(res.text)
        month_day = self.now_month + self.now_day
        info_list = history_info_json[self.now_month][month_day]
        for info in info_list:
            _middle_dict = dict()
            year = self.html_parser(info, 'year')
            title = self.html_parser(info, 'title', False)
            desc = self.html_parser(info, 'desc')
            link = title.find('a')['href']

            _middle_dict['title'] = title.text
            _middle_dict['desc'] = desc + '...'
            _middle_dict['link'] = link

            result_dict[year] = _middle_dict

        sorted_result = dict(sorted(result_dict.items(), key=lambda x: int(x[0]), reverse=True))
        return sorted_result


def main():
    # hot = HistoryOfToday()
    # data = hot.get_web_info()
    # print(data)
    pass


if __name__ == "__main__":
    main()