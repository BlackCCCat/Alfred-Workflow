from bilibili import GetDynamic
from alfred import alfred

def main():
    dynamic = GetDynamic().request_dynamic()
    result = alfred(dynamic)
    print(result)


if __name__ == "__main__":
    main()