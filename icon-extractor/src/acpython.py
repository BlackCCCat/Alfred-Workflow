# coding: UTF-8

import sys, os

qr = sys.argv[1]
argument = sys.argv[2]

# 从环境变量中获取COUNTRY和LIMIT信息，分别是搜索地区和显示条数限制
COUNTRY = os.getenv('COUNTRY')
LIMIT = os.getenv('LIMIT')

if argument == '--list':

    import urllib.parse, urllib.error, urllib.request, json, re

    def lookup(query, country=COUNTRY):
        """
        通过app在App Store中的链接搜索
        """
        # appid = re.search('(^.*/id)([0-9]*)(\?.*$)', query).group(2)
        # 上面一条正则无法正确匹配到id信息，最新的App Store链接可能不含第三个捕获组的内容，因此做出如下调整
        appid = re.search('(^.*/id)([0-9]*)(\?.*$)?', query).group(2)
        # 1. urlopen()模拟浏览器向指定链接发送请求  2.read()读取网页HTML源码，返回结果为二进制数据
        dictionary = urllib.request.urlopen('https://itunes.apple.com/lookup?id=' + appid + '&country' + country).read()
        # 由于脚本开头指定了UTF-8，因此直接json.loads转为Python对象，否则需要json.loads(dictionary.decode('utf-8'))
        return json.loads(dictionary)

    def results(query, media='software', country=COUNTRY, entity='software,iPadSoftware,macSoftware', limit=LIMIT):
        """
        通过app名称搜索
        """
        query = urllib.parse.quote_plus(query)
        dictionary = urllib.request.urlopen('https://itunes.apple.com/search?term='+ query + '&country=' + country + '&entity=' + entity + '&limit=' + str(limit) + '&media=' + media).read()
        return json.loads(dictionary)

    def device(item):
        '''if item['supportedDevices'] == ['AppleTV4']:
            return 'AppleTV'''
        if item['kind'] == 'software':
            return 'iOS'
        elif item['kind'] == 'mac-software':
            return 'macOS'

    def loop(item, num):
        for i in range (0,num):
            print ('<item>')
            print ('<arg><![CDATA[' + item[i]['artworkUrl512'] + '^' + item[i]['trackName'] + '^' + device(item[i]) + ']]></arg>')
            print ('<title><![CDATA[' + item[i]['trackName'] + ']]></title>')
            print ('<subtitle><![CDATA[', device(item[i]), '|', item[i]['formattedPrice'], '| by:', item[i]['sellerName'], ']]></subtitle>')
            print ('</item>')

    if qr.startswith("http"):
        appsearch = lookup(qr)
    else:
        appsearch = results(qr)

    number = appsearch['resultCount']

    print ('<?xml version="1.0"?><items>')

    if number == 0:
        print ('<item><title>Couldn\'t find any apps</title></item>')
    else:
        item = appsearch['results']
        loop(item, number)

    print ('</items>')

elif argument =='--local':
    import json
    # from subprocess import Popen, PIPE
    # 导入处理.plist文件的包
    import plistlib

    nameof = sys.argv[3]

    def plist_to_dictionary(filename):
        # "Pipe the binary plist through plutil and parse the JSON output"
        # with open(filename, "rb") as f:
        #     content = f.read()
        # args = ["plutil", "-convert", "json", "-o", "-", "--", "-"]
        # p = Popen(args, stdin=PIPE, stdout=PIPE)
        # p.stdin.write(content)
        # out, err = p.communicate()
        # return json.loads(out)
        # 二进制读取.plist文件，用plistlib.load()转为JSON对象
        with open(filename, "rb") as f:
            json_data = plistlib.load(f)
        return json_data

    if nameof == '--icon':
        print(plist_to_dictionary(qr)['CFBundleIconFile'])
    elif nameof == '--name':
        print(plist_to_dictionary(qr)['CFBundleExecutable'])

elif argument == '--mask':
    try:
        from PIL import Image, ImageOps

        im = Image.open(qr)

        w, h = im.size

        if w == 512 and h == 307:
            mask = Image.open('maskTV.png').convert('L')
        elif w == 512:
            mask = Image.open('mask512.png').convert('L')
        else:
            mask = Image.open('mask.png').convert('L')

        
        output = ImageOps.fit(im, mask.size, centering=(0.5,0.5))
        output.putalpha(mask)
        output.save(qr + '.png')
    except Exception:
        pass

    print (qr)