import os



class rimeConfig:
    INPUTMETHOD_LINK = os.getenv('input_method_link') # 输入法地址压缩包地址，如https://github.com/amzxyz/rime_wanxiang_pro/archive/refs/heads/main.zip
    DICT_LINK = os.getenv('dict_link') if os.getenv('dict_link') else os.getenv('input_method_link') # 词库地址压缩包地址，如https://github.com/amzxyz/rime_wanxiang_pro/archive/refs/heads/main.zip
    RIME_ENGINE = os.getenv('rime_engine') # Rime引擎（squirrel/Fcitx）


    @classmethod
    def setting_dir(cls):
        if cls.RIME_ENGINE:
            if cls.RIME_ENGINE.lower() == 'squirrel':
                return os.path.join(os.getenv('HOME'), 'Library/Rime')
            elif cls.RIME_ENGINE.lower() == 'fcitx':
                return os.path.join(os.getenv('HOME'), '.local/share/fcitx5/rime')
        else:
            return os.path.join(os.getenv('HOME'), 'Library/Rime')

