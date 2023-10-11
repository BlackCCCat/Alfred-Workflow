import os


class ReadDataBase():
    def __init__(self, db_path, db_name):
        """
        :param db_path: str, 除HOME路径外，剩余部分数据库文件路径
        :param db_name: str, 数据库文件名称
        """
        self.home_dir = os.environ['HOME']
        self.db_path = db_path
        self.db_name = db_name
        # 完整的.sqlite文件路径
        self.db = os.path.join(self.home_dir, self.db_path, self.db_name)
    
    def readNotesTable(self):
        """
        读取表数据，需要重写
        :return: db_res: list(tuple)
        """
        pass

