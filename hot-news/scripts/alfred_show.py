import json

def alfred(news):
    items = []
    for key in news:
        value = news[key]

        line = {
            'type':'default',
			'title':key,
			'subtitle':f'URL:{value}',
			'arg':value
        }
        items.append(line)
    result_json = json.dumps({"items":items}, ensure_ascii=False)
    return result_json

