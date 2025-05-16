import os



class rimeConfig:
    RIME_ENGINE = os.getenv('rime_engine') # Rime引擎（squirrel/Fcitx）
    SCHEMA = os.getenv('schema') # 输入法辅助方案（小鹤/墨奇/自然码...）


    @classmethod
    def setting_dir(cls):
        if cls.RIME_ENGINE:
            if cls.RIME_ENGINE.lower() == 'squirrel':
                return os.path.join(os.getenv('HOME'), 'Library/Rime')
            elif cls.RIME_ENGINE.lower() == 'fcitx':
                return os.path.join(os.getenv('HOME'), '.local/share/fcitx5/rime')
        else:
            return os.path.join(os.getenv('HOME'), 'Library/Rime')

