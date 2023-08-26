from getnews import HotNews
from alfred_show import alfred
import sys

def main():
    try:
        n = int(sys.argv[1])
    except:
        n = 10

    hn = HotNews(n)

    tb_hot_url = 'https://c.tieba.baidu.com/hottopic/browse/topicList'

    tb_news = hn.getTiebaNews(tb_hot_url)
    print(alfred(tb_news))


if __name__ == "__main__":
    main()