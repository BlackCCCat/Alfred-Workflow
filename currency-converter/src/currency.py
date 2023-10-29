import requests
import os
import time
from configure import Configure


class Currency():
    CURRENT_PATH = os.path.dirname(__file__)
    LAST_LEVEL_PATH = os.path.dirname(CURRENT_PATH)
    @staticmethod
    def getCurrency(api):
        """
        获取汇率
        """
        url = 'http://data.fixer.io/api/latest?'
        params = {
                "access_key": api,
                "format": "1"
            }
        try:
            _ = requests.get(url=url, params=params).content
            result = _.decode('utf-8')
            return result
        except:
            print('获取最新汇率失败')
            return
    

    @staticmethod
    def save(data={}):
        """
        保存汇率
        :param file_name: 文件名
        :param data: 需要保存的数据
        """
        file_name=f'{Currency.LAST_LEVEL_PATH}/currency.json'
        with open(file_name, 'w') as f:
            f.write(data)
    

    @staticmethod
    def need_update(invertal=Configure.INTERVAL):
        """
        检查汇率是否需要更新
        :param invertal: 更新间隔（小时）
        """
        current_time = time.time()
        file_time = os.stat(f'{Currency.LAST_LEVEL_PATH}/currency.json').st_mtime
        time_delta = round((current_time - file_time)/3600)
        return True if time_delta >= invertal else False
        


def main():
    # currency = Currency.getCurrency(Configure.API)
    # print(currency)
    # Currency.save(data=currency)
    print(Currency.LAST_LEVEL_PATH)


if __name__ == "__main__":
    main()