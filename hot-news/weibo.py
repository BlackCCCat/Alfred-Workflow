from getnews import HotNews
from alfred_show import alfred
import sys

def main():
    try:
        if sys.argv[1]:
            n = int(sys.argv[1])
    except:
        n = 10

    hn = HotNews(n)

    wb_hot_url = 'https://s.weibo.com/top/summary'

    wb_news = hn.getweiboNews(wb_hot_url)
    print(alfred(wb_news))


if __name__ == "__main__":
    main()