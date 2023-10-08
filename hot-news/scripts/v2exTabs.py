import requests
from lxml import etree
import json


def getTabs():
    """
    :return: list: tabs of v2ex
    """
    url = 'https://www.v2ex.com/'
    res = requests.get(url=url, verify=False)
    tree = etree.HTML(res.content)
    # res = tree.xpath('//*[@id="Tabs"]/a[5]/text()')
    res_list = tree.xpath('//*[@id="Tabs"]/a/@href')
    result = []
    for res in res_list:
        result.append(res.split('=')[-1])
    
    return result

def showTags():
    """
    :return: alfred items
    """
    items = []
    res_list = getTabs()
    for res in res_list:
        line = {
                'type':'default',
                'title':res,
                'subtitle': '',
                'arg':res
            }
        items.append(line)
    
    result_json = json.dumps({"items":items}, ensure_ascii=False)
    return result_json

def main():
    res = showTags()
    print(res)


if __name__ == "__main__":
    main()