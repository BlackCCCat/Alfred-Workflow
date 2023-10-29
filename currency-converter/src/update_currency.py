import sys

from currency import Currency
from configure import Configure


def update_currency(api):
    apikey = api
    currency_data = Currency.getCurrency(apikey)
    if currency_data:
        Currency.save(currency_data)
        print('Currency Update Success')
    else:
        print('Currency Update Failed')


if __name__ == "__main__":
    try:
        api = sys.argv[1]
    except:
        api = Configure.API
    update_currency(api)