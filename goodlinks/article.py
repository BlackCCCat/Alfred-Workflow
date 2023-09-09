from mapdata import MapData

def main():
    items = MapData().loadLink()
    print(items)

if __name__ == "__main__":
    main()