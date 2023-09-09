from mapdata import MapData

def main():
    items = MapData().loadState()
    print(items)

if __name__ == "__main__":
    main()