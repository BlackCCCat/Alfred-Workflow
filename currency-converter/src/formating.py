import json

class FormatToAlfred():
    def __init__(self):
        """
        初始化空列表,用于存放item
        初始化空字典,用于存放key:items, value:items_list
        """
        self.items_list = []
        self.items = dict()

    def item_format(self,
        uid = '',
        type = 'default',
        title = 'No title',
        subtitle = '',
        arg = '',
        **kwargs
    ):
        """
        :param uid: str, 每个item的唯一标识
        :param type: str, item的类型
        :param title: str, item的title,就是Alfred显示的每行的标题
        :param subtitle: str, item的subtitle,就是Alfred显示的每行的副标题
        :param arg: str, item的arg,会做为输出,传到下一个动作中
        :param kwargs: dict, 额外的参数,如icon等信息
        :return: item,生成单个item格式
        Note: 一般至少要给item添加title,subtitle,arg三个参数
        """
        item = {
            "uid": uid,
            "type": type,
            "title": title,
            "subtitle": subtitle,
            "arg": arg,
        }

        icon = dict()
        if kwargs.get('icontype'):
            icontype = {"type": kwargs.get('icontype')}
            icon.update(icontype)
        if kwargs.get('iconpath'):
            iconpath = {"path":kwargs.get('iconpath')}
            icon.update(iconpath)
        
        icon_info = {"icon": icon}
        item.update(icon_info)
        
        return item
    
    def items_format(self, item):
        """
        格式化items
        :param item: item_format方法的输出
        :return: items,Alfred可以正确读取的JSON格式
        """
        self.items_list.append(item)
        self.items.update({"items":self.items_list})
        items = json.dumps(self.items, ensure_ascii=False)
        return items

    
