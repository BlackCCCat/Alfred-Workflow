import os


class ReadDataBase():
    def __init__(self, db_path, db_name):
        self.home_dir = os.environ['HOME']
        self.db_path = db_path
        self.db_name = db_name
        self.db = os.path.join(self.home_dir, self.db_path, self.db_name)
    
    def readNotesTable(self):
        """
        读取表数据
        :return: db_res: list(tuple)
        """
        pass

