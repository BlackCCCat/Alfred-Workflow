import requests
from lxml import etree
import re
import json
from bs4 import BeautifulSoup

class HotNews(object):
    headers = {
            "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
        }
    

    def __init__(self, n):
        """
        param: n: 需要获取的热搜数量 
        """
        self.n = n

    def getweiboNews(self):
        """
        微博热榜
        """
        cookies = {
        'SUB': '_2AkMTtDIMf8NxqwFRmP8RzWLkbY10zwrEieKl6MPXJRMxHRl-yT9vqhMDtRB6ODQc4yM_gWCs-qcHIFpIc0srV4-ZzbJK'
        }
        url = 'https://s.weibo.com/top/summary'

        res = requests.get(url=url, headers=self.headers, cookies=cookies, verify=False)
        tree = etree.HTML(res.content)
        
        wb_hot_news = dict()
        
        for i in range(self.n + 5):
            counter = len(wb_hot_news)
            link_suffix = tree.xpath(f'//*[@id="pl_top_realtimehot"]/table/tbody/tr[{i}]/td[2]/a/@href')
            title = tree.xpath(f'//*[@id="pl_top_realtimehot"]/table/tbody/tr[{i}]/td[2]/a/text()')
            count_str = tree.xpath(f'//*[@id="pl_top_realtimehot"]/table/tbody/tr[{i}]/td[2]/span/text()')

            if link_suffix and title and count_str:
                link = 'https://s.weibo.com' + str(link_suffix[0])
                hot_count = re.sub('[\D]', '', count_str[0])
                if hot_count:
                    title_hot = str(title[0])
                    if counter < self.n:
                        wb_hot_news[title_hot] = {'hot': '🔥' + str(hot_count), 'link': link}

        return wb_hot_news
    
    
    def getZhihuNews(self):
        """
        知乎热榜
        """
        url = 'https://www.zhihu.com/billboard'
        res = requests.get(url=url, headers=self.headers, verify=False)
        tree = etree.HTML(res.content)

        zh_news = dict()

        _ = tree.xpath('//*[@id="js-initialData"]/text()')
        json_data = _[0].encode('utf-8')
        dict_data = dict(json.loads(json_data))
        list_data = dict_data['initialState']['topstory']['hotList']
        for data in list_data:
            counter = len(zh_news)
            title = data['target']['titleArea']['text']
            link = data['target']['link']['url']
            hot_count = data['target']['metricsArea']['text'].replace('热度', '')

            if counter < self.n:
                zh_news[title] = {'hot': '🔥' + hot_count, 'link': link}
                continue
            
        return zh_news
    
    def getTiebaNews(self):
        """
        百度贴吧热榜
        """
        cookies = {
                "BAIDUID": "402F999DB23145A3CEFDE2358591947C:FG=1",
            }
        params={
                "res_type": "1",
            }
        url = 'https://c.tieba.baidu.com/hottopic/browse/topicList'

        res = requests.get(url=url, headers=self.headers, cookies=cookies, params=params, verify=False)
        html = res.text

        soup = BeautifulSoup(html, 'html.parser')

        tb_hot_news = dict()

        for i in range(self.n + 5):
            counter = len(tb_hot_news)
            text_infos = soup.select(f"body > div.wrap1 > div > div.bang-bg > div > div.topic-body.clearfix > div.main > ul > li:nth-child({i}) > div > div > a")
            count_strs = soup.select(f"body > div.wrap1 > div > div.bang-bg > div > div.topic-body.clearfix > div.main > ul > li:nth-child({i}) > div > div > span.topic-num")

            if text_infos and count_strs:
                for text_info in text_infos:
                    link = text_info.get('href')
                    title = text_info.text
                        
                for count_str in count_strs:
                    counter_str = count_str.text.replace('实时讨论','')

                if counter < self.n:
                    tb_hot_news[title] = {'hot': '🔥' + counter_str, 'link': link}
        
        return tb_hot_news
    
    def getZHribaoNews(self):
        """
        知乎日报
        """
        url = 'https://daily.zhihu.com/'
        res = requests.get(url=url, verify=False)
        tree = etree.HTML(res.content.decode())

        rb_hot_news = dict()

        for i in range(self.n + 5):
            counter  = len(rb_hot_news)
            title = tree.xpath(f'/html/body/div[3]/div/div[2]/div/div[1]/div[{i}]/div/a/span/text()')
            link_suffix = tree.xpath(f'/html/body/div[3]/div/div[2]/div/div[1]/div[{i}]/div/a/@href')
            if title and link_suffix:
                title = str(title[0])
                link = 'https://daily.zhihu.com' + str(link_suffix[0])
                if counter < self.n:
                    rb_hot_news[title] = {'hot': '', 'link': link}
        
        return rb_hot_news
        
    def getV2exNews(self, tab='hot'):
        """
        v2ex热门帖子
        """
        url = 'https://www.v2ex.com/'
        params={
                "tab": tab, # "hot",
            }
        res = requests.get(url=url, params=params, verify=False)
        html = etree.HTML(res.text)

        temp_v2ex = dict()

        # 提取id包含topic-link的所有内容，返回列表
        html_result = html.xpath('//*[contains(@id, "topic-link")]')

        for result in html_result:
            # 列表中每个元素转换为字符串
            result_new = etree.tostring(result, encoding='utf-8').decode()
            # HTML解析
            soup = BeautifulSoup(result_new, 'html.parser')
            
            # 获取a元素
            a_tag = soup.find('a')
            
            # 获取链接信息
            href_value = a_tag['href']
            # 拼接完整链接
            link = 'https://www.v2ex.com' + href_value
            # 获取标题文本
            text_content = a_tag.text
            # 取出链接中回复情况拼接到标题
            title = text_content
            reply_count = href_value.split('#')[-1].replace('reply', '')
            
            temp_v2ex[title] = {'hot': '💬' + reply_count, 'link': link}
            
        v2ex_hot_news = dict()
        total = len(temp_v2ex)
        if self.n > total:
            counter = total
        else:
            counter = self.n
        
        v2ex_hot_news = {k: temp_v2ex[k] for k in list(temp_v2ex.keys())[:counter]}
        return v2ex_hot_news
    
    def getAppinnNews(self):
        """
        小众软件帖子
        """
        url = 'https://meta.appinn.net'
        res = requests.get(url=url, verify=False)
        html = etree.HTML(res.text)
        # 转为string，便于BeautifulSoup处理
        string_html = etree.tostring(html, encoding='utf-8').decode()
        
        soup = BeautifulSoup(string_html, 'html.parser')
        a_tags = soup.find_all('a')

        temp_appinn = dict()
        for a_tag in a_tags:
            # 网页链接
            href_value = a_tag['href']
            if re.search('topic/\d+', href_value):
                title = a_tag.text
                if title != '欢迎来到小众软件论坛':
                    temp_appinn[title] = {'hot': '', 'link': href_value}
        
        total = len(temp_appinn)
        appinn_hot_news = dict()
        if self.n > total:
            counter = total
        else:
            counter = self.n
        
        appinn_hot_news = {k: temp_appinn[k] for k in list(temp_appinn.keys())[:counter]}
        return appinn_hot_news



def main():
    hotnews = HotNews(2)
    # wb_news = hotnews.getweiboNews()
    # zh_news = hotnews.getZhihuNews()
    # print(wb_news)
    # print(zh_news)
    # tb_news = hotnews.getTiebaNews()
    # print(tb_news)
    # rb_news = hotnews.getZHribaoNews()
    # print(rb_news)
    # print(hotnews.getV2exNews())

    appinn_news = hotnews.getAppinnNews()
    print(appinn_news)
    pass
    

if __name__ == "__main__":
    main()
