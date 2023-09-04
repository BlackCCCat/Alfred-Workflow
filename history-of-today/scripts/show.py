import json
from history import HistoryOfToday


def alfred(history):
    items = []
    for key in history:
        info = history[key]

        line = {
            'type':'default',
			'title':f'({key}) {info["title"]}',
			'subtitle': info['desc'],
			'arg':info['link']
        }
        items.append(line)
    result_json = json.dumps({"items":items}, ensure_ascii=False)
    return result_json

def main():
    history = HistoryOfToday().get_web_info()
    show = alfred(history)
    print(show)

if __name__ == "__main__":
    main()