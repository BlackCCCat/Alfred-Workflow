import json

class FormatToAlfred():
    def __init__(self):
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
        生成单个item格式
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
        """
        self.items_list.append(item)
        self.items.update({"items":self.items_list})
        items = json.dumps(self.items, ensure_ascii=False)
        return items

    
