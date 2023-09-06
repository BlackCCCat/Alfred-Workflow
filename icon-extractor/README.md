# 说明
修复原Workflow（get app icon）的bug及完善：
- 使用pyenv管理的Python版本
- 添加代码注释
- 添加使用说明
- acpython.py 脚本中 `plist_to_dictionary` 函数 bug 修复（解决无法正确将.plist文件转为json的bug）
- 修复通过App Store获取的app链接无法搜索和下载的问题


> 原Workflow请移步：https://github.com/packal/repository/tree/master/com.mcskrzypczak.extracticon

# 使用
- `icon [app name]` 获取本机已安装的app的图标
- `icon`之后选中`search app icon online` 
    - 通过app名称进行搜索
    - 通过App Store链接进行搜索
