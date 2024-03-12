import json
import os
import re
import sys

from currency import Currency
from formating import FormatToAlfred
from commonmsg import CommonMsg
from configure import Configure

class Converter(FormatToAlfred):
    def __init__(self, api):
        super().__init__()
        self.filename = f'{Currency.LAST_LEVEL_PATH}/currency.json'
        self.currency = Currency
        self.common = CommonMsg
        self.API = api
        # 初始化直接检查是否需要更新
        self.checkCurrency()

    
    def checkCurrency(self):
        """
        检查汇率是否存在已经是否需要更新
        """
        is_exist = os.path.exists(self.filename)
        if not is_exist:
            if not self.API:
                print(self.common.API_NOT_FOUND)
                return
            # print(self.common.GET_MSG)
            currency_data = self.currency.getCurrency(self.API)
            self.currency.save(currency_data)
            return
        
        if not self.readCurrency():
            # print(self.common.GET_MSG)
            if not self.API:
                print(self.common.API_NOT_FOUND)
                return
            currency_data = self.currency.getCurrency(self.API)
            self.currency.save(currency_data)
            return
        
        need_update = self.currency.need_update()
        if need_update:
            # print(self.common.UPDATE_MSG)
            currency_data = self.currency.getCurrency(self.API)
            self.currency.save(data=currency_data)
            return
        
        return
        
    def readCurrency(self):
        """
        读取汇率
        """
        with open(self.filename, 'r') as f:
            currency_data = f.read()
        if currency_data:
            try:
                currency = json.loads(currency_data)
                if currency.get('success'):
                    return currency['rates']
            except:
                return
        
        return
    

    def converter(self, money, from_currency, to_currency):
        """
        汇率转换
        :param money: 要转换的金额
        :param from_currency: 转换源货币
        :param to_currency: 转换目标货币
        """
        # self.checkCurrency()
        currency_data = self.readCurrency()
        if currency_data:
            from_rate = currency_data.get(from_currency.upper(), 1)
            to_rate = currency_data.get(to_currency.upper(), 1)

            to_money = round(money / from_rate * to_rate, 2)
            one_to_money = round(1 / from_rate * to_rate, 2)

            to_money_res = str(to_money) + to_currency.upper()
            one_to_money_res = f'1{from_currency}={one_to_money}{to_currency}'

            _cur_path = os.path.dirname(__file__)
            flag_path = f'{os.path.dirname(_cur_path)}/flags/{to_currency}.png'
            item = self.item_format(title=to_money_res, subtitle=one_to_money_res, arg=to_money, icontype='path', iconpath=flag_path)
            items = self.items_format(item)
            print(items)


    def run(self, sentence):
        """
        运行
        :param sentence: 命令
        """
        regex = r'([0-9]+\.?[0-9]*)\x20?([a-zA-Z]{3})(\x20+to\x20+|\x20+in\x20+|\x20?=\x20?)([a-zA-Z]{3})'
        match = re.match(regex, sentence)
        if match:
            money = float(match.group(1))
            from_currency = match.group(2).upper()
            to_currency = match.group(4).upper()
            self.converter(money, from_currency, to_currency)
        else:
            print(self.common.INPUT_ERROR)

    

def main():
    try:
        api = os.getenv('API', Configure.API)
        params = sys.argv[1:]
        sentence = ' '.join(params)

        if api:
            converter_tool = Converter(api)
            converter_tool.run(sentence)
        else:
            print(CommonMsg.API_NOT_FOUND)
    except:
        print(CommonMsg.PARAM_ERROR)
        
    



if __name__ == "__main__":
    main()