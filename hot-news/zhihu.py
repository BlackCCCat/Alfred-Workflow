from getnews import HotNews
from alfred_show import alfred

from getnews import HotNews
from alfred_show import alfred
import sys

def main():
    try:
        n = int(sys.argv[1])
    except:
        n = 2

    hn = HotNews(n)

    zh_hot_url = 'https://www.zhihu.com/billboard'

    zb_news = hn.getZhihuNews(zh_hot_url)
    print(alfred(zb_news))


if __name__ == "__main__":
    main()
    

