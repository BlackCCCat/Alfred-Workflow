import sys
import jieba
import json
import pyperclip
import re


url_pattern = r'(?:https?:\/\/)?(?:www\.)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b(?:[-a-zA-Z0-9@:%_\+.~#?&\/\/=]*)'

url_regex = re.compile(url_pattern)

try:
	input_text = sys.argv[1]
except:
	input_text = pyperclip.paste()

items = []
match_urls = url_regex.findall(input_text)
if match_urls:
	for url in match_urls:
		items.append({'type':'default',
					 'title':url,
					 'subtitle':'URL/Email',
					 'arg':url
}
)

# word segment
jieba_result = jieba.cut(input_text) # 精确模式
# jieba_result = jieba.cut(input_text,cut_all=True) # 全模式
# jieba_result = jieba.cut_for_search(input_text) # 搜索模式
result = [i for i in jieba_result if i!='' and i!='\n' and i!='\r']
items = []

if result:
	for idx,query in enumerate(result):
		items.append({'type':'default',
					 'title':query,
					 'subtitle':f'分词结果{idx+1}',
					 'arg':query
					})

result_json = json.dumps({"items":items})
print(result_json)

