import json

def alfred(videos):
    items = []
    for key in videos:
        video_info = videos[key]['video_info']
        link = videos[key]['link']
        icon = videos[key]['icon']

        line = {
            'type':'default',
			'title':key,
			'subtitle':video_info,
			'arg':link,
			'icon':{
                "path": icon
			}
        }
        items.append(line)
    result_json = json.dumps({"items":items}, ensure_ascii=False)
    return result_json

