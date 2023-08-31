from getnews import HotNews
from alfred_show import alfred
import sys

def main():
    try:
        n = int(sys.argv[1])
    except:
        n = 10

    hn = HotNews(n)


    rb_news = hn.getZHribaoNews()
    print(alfred(rb_news))


if __name__ == "__main__":
    main()