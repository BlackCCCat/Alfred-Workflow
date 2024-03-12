import os


class AccountInfo():
    """
    请填入自己的账号信息
    """
    cookies = {
        "_uuid": os.getenv('uuid'),
        "SESSDATA": os.getenv('sessdata'),
    }