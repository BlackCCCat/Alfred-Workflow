# 万象 Rime 更新

Alfred Workflow，用于更新 Rime 万象方案、词库和语法模型。

## 配置

导入 Workflow 后先打开 `Configure Workflow...`：

- 输入法引擎：`squirrel` 或 `fcitx5`
- 下载源：默认 `CNB`，也可切换到 `GitHub`
- GitHub Token：可选，选择 GitHub 源时填写，用于 GitHub API 请求
- 方案类型：标准版、墨奇、小鹤、自然码、虎码、五笔、汉心、首右
- Rime 用户目录：可选，留空时按输入法引擎自动判断
- 排除文件列表路径：可选，留空时使用 Workflow 目录下的 `cache/user_exclude_file.txt`

默认目录：

- 鼠须管 Squirrel：`~/Library/Rime`
- 小企鹅 Fcitx5：`~/.local/share/fcitx5/rime`

## 用法

- `rimew`：打开更新菜单
- `rimes`：选择并更新方案
- `rimed`：选择并更新词库
- `rimem`：更新语法模型
- `rimeall`：自动更新方案、词库、模型
- `rimef`：手动触发重新部署

更新前会把被覆盖的文件备份到 Rime 用户目录下的 `UpdateBackups/`。更新成功后会把本地记录写入 Workflow 目录下的 `cache/alfred_records.json`。

使用 `rimeall` 自动更新全部内容时，会先根据本地记录判断方案、词库和模型是否需要更新；只有存在更新时才下载并在完成后自动触发部署。单项更新会直接重新下载并刷新本地记录。

在 `rimew` 中选择“查看当前配置”会进入信息页，显示当前配置和本地记录。

执行更新或部署时会打开 Text View 进度页。实际任务在后台执行，日志写入 `cache/tasks/`，Text View 会自动刷新显示下载、解压、复制和部署进度。

方案更新会尊重排除文件列表。如果配置项留空，会使用 Workflow 目录下的 `cache/user_exclude_file.txt`；如果文件不存在，会自动创建一个默认排除列表。排除列表每行一个相对 Rime 用户目录的路径，`#` 开头为注释。

## 说明

Workflow 使用 Python 标准库实现，不依赖 `requests` 等第三方包。
