from getnews import HotNews
from alfred_show import alfred
import sys

def main():
    try:
        n = int(sys.argv[1])
    except:
        n = 10

    hn = HotNews(n)


    v2ex_news = hn.getV2exNews()
    print(alfred(v2ex_news))


if __name__ == "__main__":
    main()