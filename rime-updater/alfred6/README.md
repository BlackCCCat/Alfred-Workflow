# 万象 Rime 更新 · Alfred 6

此版本需要 Alfred 6，使用 Alfred UI 显示本地版本、下载进度、更新说明和日志。Alfred 5 用户继续使用原有的 `wanxiang-updater.alfredworkflow`。

`rimew` 打开更新面板；`rimes`、`rimed`、`rimem`、`rimeall` 继续提供快捷更新入口。`rimee` 用于切换输入法，`rimef` 用于手动部署。面板中的“更新全部”仅更新有变化的组件，完成后自动部署；单独更新会重新下载。关闭面板不会取消正在执行的后台任务，重新打开可查看进度。

输入法、下载源、方案类型和 GitHub 下载加速可在面板中切换，并对快捷命令生效；选择“恢复 Workflow 配置”可撤销面板中的覆盖。CNB / GitHub Token、用户目录和排除文件路径仍在 Workflow 配置中设置。更新记录仍保存在对应输入法方案目录的 `custom/update_records.json`，任务日志、下载分片和面板选项保存在当前 Workflow 的 `cache/`；安装包不包含这些运行时文件。

Alfred 5 和 Alfred 6 版本使用不同的 bundle ID，能分别安装。两者的快捷指令相同，同时启用会出现重复结果，建议只启用当前使用的版本。新版本的 Workflow 配置需要单独填写，但同一输入法目录下的更新记录可以继续读取。
