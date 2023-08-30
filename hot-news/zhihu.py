from getnews import HotNews
from alfred_show import alfred

from getnews import HotNews
from alfred_show import alfred
import sys

def main():
    try:
        n = int(sys.argv[1])
    except:
        n = 10

    hn = HotNews(n)


    zb_news = hn.getZhihuNews()
    print(alfred(zb_news))


if __name__ == "__main__":
    main()
    

