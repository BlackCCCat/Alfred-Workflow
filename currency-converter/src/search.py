import re

class Search():
    @staticmethod
    def searchItem(item, target, type=None):
        """
        搜索item内容,type为item的键,不指定时搜索title、subtitle、arg
        :return: True或者False
        """
        try:
            origin_str = item[type]
        except:
            origin_str = item['title'] + item['subtitle'] + item['arg']



        if origin_str:
            search_res = re.search(target, origin_str, flags=re.IGNORECASE)
            return True if search_res else False

        return True