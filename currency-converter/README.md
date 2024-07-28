# 汇率转换
通过第三方API汇率接口进行汇率转换（[申请API](https://fixer.io/)）

# 使用方式
下载Alfred Workflow并导入
## 配置API
### 在configure workflow中配置API
在configure workflow中填写API，interval选项为以小时为单位的时间间隔，代表汇率更新的时间间隔，默认6小时，可不填

### 在`configure.py`中配置API
```Python
class Configure():
    API = "" # 填入自己申请的API：https://fixer.io
    INTERVAL = 6
```
在上面填入自己的API和INTERVAL

## 开始使用
1. ~~`money query`进行转换，该方式会按照configure workflow中的时间间隔自动更新汇率，`query`格式应该为以下几种（字母不区分大小写）：~~ 直接使用以下方式进行汇率转换
    - 1usd in cny、1cny to jpy
    - 1eur=usd、1gbp = jpy
    - 1 usd in cny、1 usd to cny
2. `moneyup`进行汇率的手动更新

