# Word Segment
使用Python的第三方包jieba实现中文分词
# 安装所需模块
- 如果使用的是macOS自带Python环境(也是Alfred默认使用Python环境):
/usr/bin/python3 -m pip install -r requirements.txt
- 其他
pip install -r requirements.txt
# 使用方法
`wdcc [query]`默认使用精确模式进行分词
`wdca [query]`使用全模式进行分词
`wdcs [query]`使用搜索模式进行分词

> `[query]`为可选参数,无输入时,读取剪切板进行分词
