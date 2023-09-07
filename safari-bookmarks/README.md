# Safari Bookmarks and History
**本Workflow需要Alfred添加访问所有磁盘权限**

## Bookmarks
快速查看Safari的书签，包括Bookmarks、Favorites


## **使用方式**
1. 安装Workflow
2. `sbs`调用Workflow，显示所有Bookmarks及Favorites
3. 如果Safari浏览器中未添加任何Bookmarks或Favorites，回车打开Safari浏览器
4. `sbs [str]`可选参数，进行对输入的`str`进行模糊搜索以定位需要找到的书签

## History
快速查看Safari的历史浏览记录

## **使用方式**
1. 安装Workflow
2. `shs`调用Workflow，显示所有History
3. `shs [str]`可选参数，进行对输入的`str`进行模糊搜索以定位需要找到的历史记录


# 其他
- 所用基本都是Python自带的包
- 需下载`sqlite3`


> 写好后发现Alfred自带有书签查看功能，不过还是有一点区别，该Workflow可以直接显示所有书签
