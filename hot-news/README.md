
# **通过Alfred调用会出现多个Python进程，占用大量CPU，正在学习如何解决**


# Hot News
使用Python获取微博和知乎的热搜榜
# 安装所需模块
- 如果使用的是macOS自带Python环境(也是Alfred默认使用Python环境):
/usr/bin/python3 -m pip install -r requirements.txt
- 其他
pip install -r requirements.txt
# 使用方法
`wb [n]`获取微博热搜榜前`n`个热搜
`zh [n]`获取知乎热搜榜前`n`个热搜

> `[n]`为可选参数,无输入时,默认获取前10个热搜榜
