import json

def alfred(news):
    items = []
    for key in news:
        hot_count = news[key]['hot']
        link = news[key]['link']

        line = {
            'type':'default',
			'title':key,
			'subtitle':hot_count,
			'arg':link
        }
        items.append(line)
    result_json = json.dumps({"items":items}, ensure_ascii=False)
    return result_json

