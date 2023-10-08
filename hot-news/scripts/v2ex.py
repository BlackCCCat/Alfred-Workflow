import sys

from getnews import HotNews
from alfred_show import alfred

def main():
    n = 10
    tab = 'hot'
    
    if len(sys.argv) == 3:
        n = int(sys.argv[2])
        tab = sys.argv[1]
    if len(sys.argv) == 2:
        try:
            n = int(sys.argv[1])
        except:
            tab = sys.argv[1]


    hn = HotNews(n)

    v2ex_news = hn.getV2exNews(tab=tab)
    print(alfred(v2ex_news))


if __name__ == "__main__":
    main()