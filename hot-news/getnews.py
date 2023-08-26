import requests
from lxml import etree
import re
import json

class HotNews(object):
    headers = {
            "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
        }
    

    def __init__(self, n):
        """
        param: n: 需要获取的热搜数量 
        """
        self.n = n

    def getweiboNews(self, url):
        cookies = {
        'SUB': '_2AkMTtDIMf8NxqwFRmP8RzWLkbY10zwrEieKl6MPXJRMxHRl-yT9vqhMDtRB6ODQc4yM_gWCs-qcHIFpIc0srV4-ZzbJK'
        }
        res = requests.get(url=url, headers=self.headers, cookies=cookies, verify=False)
        tree = etree.HTML(res.content)
        
        wb_hot_news = dict()
        
        for i in range(self.n + 2):
            counter = len(wb_hot_news)
            link_suffix = tree.xpath(f'//*[@id="pl_top_realtimehot"]/table/tbody/tr[{i}]/td[2]/a/@href')
            title = tree.xpath(f'//*[@id="pl_top_realtimehot"]/table/tbody/tr[{i}]/td[2]/a/text()')
            count_str = tree.xpath(f'//*[@id="pl_top_realtimehot"]/table/tbody/tr[{i}]/td[2]/span/text()')

            if link_suffix and title and count_str:
                link = 'https://s.weibo.com' + str(link_suffix[0])
                hot_count = re.sub('[\D]', '', count_str[0])
                if hot_count:
                    title_hot = str(title[0]) + f'({hot_count})'
                    if counter < self.n:
                        wb_hot_news[title_hot] = link

        return wb_hot_news
    
    
    def getZhihuNews(self, url):
        res = requests.get(url=url, headers=self.headers, verify=False)
        tree = etree.HTML(res.content)

        zh_news = dict()

        _ = tree.xpath('//*[@id="js-initialData"]/text()')
        json_data = _[0].encode('utf-8')
        dict_data = dict(json.loads(json_data))
        list_data = dict_data['initialState']['topstory']['hotList']
        for data in list_data:
            counter = len(zh_news)
            title = data['target']['titleArea']['text'] + '(' + data['target']['metricsArea']['text'] + ')'
            link = data['target']['link']['url']
            if counter < self.n:
                zh_news[title] = link
                continue
            
        return zh_news



def main():
    # hotnews = HotNews(5)
    # wb_news = hotnews.getweiboNews('https://s.weibo.com/top/summary')
    # zh_news = hotnews.getZhihuNews('https://www.zhihu.com/billboard')
    # print(wb_news)
    # print(zh_news)
    pass
    

if __name__ == "__main__":
    main()