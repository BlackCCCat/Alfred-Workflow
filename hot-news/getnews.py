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
        res = requests.get(url=url, headers=self.headers, cookies=cookies)
        tree = etree.HTML(res.content)
        
        wb_hot_news = dict()
        count = len(wb_hot_news)
        while count < self.n:
            for i in range(self.n + 2):
                link_suffix = tree.xpath(f'//*[@id="pl_top_realtimehot"]/table/tbody/tr[{i}]/td[2]/a/@href')
                title = tree.xpath(f'//*[@id="pl_top_realtimehot"]/table/tbody/tr[{i}]/td[2]/a/text()')
                count_str = tree.xpath(f'//*[@id="pl_top_realtimehot"]/table/tbody/tr[{i}]/td[2]/span/text()')

                if link_suffix and title and count_str:
                    link = 'https://s.weibo.com' + str(link_suffix[0])
                    count = re.sub('[\D]', '', count_str[0])
                    if count:
                        title_hot = str(title[0]) + f'({count})'
                        wb_hot_news[title_hot] = link
                    else:
                        continue
                else:
                    continue
            count = len(wb_hot_news)

        return wb_hot_news
    
    def getDouyinNews(self, url):
        cookies = {
        'ttwid': '1%7Cmns2y1MMwDY-AsscJIte7mdr_NWXWp3zJaT0_vxBiNk%7C1692980220%7C0d894bf0d237160b050060adcbbf9448d616ea4cf59debfb75e47d85c0403656'
        }
        res = requests.get(url=url, headers=self.headers, cookies=cookies)
        tree = etree.HTML(res.content)

        dy_hot_news = dict()
        count = len(dy_hot_news)
        while count < self.n:
            for i in range(self.n + 2):
                link_suffix = tree.xpath(f'//*[@id="douyin-right-container"]/div[3]/div/div[3]/ul/li[{i}]/div[2]/div[1]/a/@href')
                title = tree.xpath(f'//*[@id="douyin-right-container"]/div[3]/div/div[3]/ul/li[{i}]/div[2]/div[1]/a/h3/text()')
                count_str = tree.xpath(f'//*[@id="douyin-right-container"]/div[3]/div/div[3]/ul/li[{i}]/div[2]/div[2]/span[1]/text()')
                
                if link_suffix and title:
                    link = 'https://www.douyin.com' + str(link_suffix[0])
                    count = count_str[0]
                    title_hot = str(title[0]) + f'({count})'
                    dy_hot_news[title_hot] = link
                else:
                    continue
            count = len(dy_hot_news)

        return dy_hot_news
    

    def getZhihuNews(self, url):
        res = requests.get(url=url, headers=self.headers, verify=False)
        tree = etree.HTML(res.content)

        zh_hot_news = dict()
        count = len(zh_hot_news)
        while count < self.n:
            for i in range(self.n + 2):
                _ = tree.xpath('//*[@id="js-initialData"]/text()')
                json_data = _[0].encode('utf-8')
                dict_data = dict(json.loads(json_data))
                list_data = dict_data['initialState']['topstory']['hotList']
                for data in list_data:
                    title = data['target']['titleArea']['text'] + '(' + data['target']['metricsArea']['text'] + ')'
                    link = data['target']['link']['url']
                    zh_hot_news[title] = link
            count = len(zh_hot_news)
            
        return zh_hot_news



def main():
    # hotnews = HotNews(10)
    # wb_news = hotnews.getweiboNews('https://s.weibo.com/top/summary')
    # dy_news = hotnews.getDouyinNews('https://www.douyin.com/hot')
    # zh_news = hotnews.getZhihuNews('https://www.zhihu.com/billboard')
    # print(wb_news)
    # print(dy_news)
    # print(zh_news)
    pass

if __name__ == "__main__":
    main()