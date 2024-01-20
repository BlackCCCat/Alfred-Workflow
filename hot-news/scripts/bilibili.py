from getnews import HotNews
from alfred_show import alfred
import sys

def main():
    try:
        n = int(sys.argv[1])
    except:
        n = 10

    hn = HotNews(n)


    bilibili_hots = hn.getBilibiliHots()
    print(alfred(bilibili_hots))


if __name__ == "__main__":
    main()