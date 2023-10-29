import json

class CommonMsg():
    """
    输出的常规信息
    """

    # 更新信息
    _UPDATE_MSG = {"items": [
        {
            "type": "default",
            "title": "Updating Currency...",
        }
    ]}
    UPDATE_MSG = json.dumps(_UPDATE_MSG, ensure_ascii=False)

    # 更新信息
    _UPDATE_SUCCESS = {"items": [
        {
            "type": "default",
            "title" : "",
            "arg": "Update Success",
        }
    ]}
    UPDATE_SUCCESS = json.dumps(_UPDATE_SUCCESS, ensure_ascii=False)

    # 更新失败
    _UPDATE_FAILED = {"items": [
        {
            "type": "default",
            "title": "",
            "arg": "Update Failed, Please retry",
        }
    ]}
    UPDATE_FAILED = json.dumps(_UPDATE_FAILED, ensure_ascii=False)


    # 获取信息
    _GET_MSG = {"items": [
        {
            "type": "default",
            "title": "Getting Currency...",
        }
    ]}
    GET_MSG = json.dumps(_GET_MSG, ensure_ascii=False)
    
    # 汇率未找到
    _CURRENCY_NOT_FOUND = {"items": [
        {
            "type": "default",
            "title": "Currency Not Found",
        }
    ]}
    CURRENCY_NOT_FOUND = json.dumps(_CURRENCY_NOT_FOUND, ensure_ascii=False)

    # API未找到
    _API_NOT_FOUND = {"items": [
        {
            "type": "default",
            "title": "API Not Found",
            "subtitle": "Please check your API key",
            "arg": "https://fixer.io/"
        }
    ]}
    API_NOT_FOUND = json.dumps(_API_NOT_FOUND, ensure_ascii=False)

    # 输入格式错误
    _INPUT_ERROR = {"items": [
        {
            "type": "default",
            "title": "Input Error",
        }
    ]}
    INPUT_ERROR = json.dumps(_INPUT_ERROR, ensure_ascii=False)

    # 参数错误
    _PARAM_ERROR = {"items": [
        {
            "type": "default",
            "title": "Param Error",
            "subtitle": "Please check your input",
        }
    ]}
    PARAM_ERROR = json.dumps(_PARAM_ERROR, ensure_ascii=False)