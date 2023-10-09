# 搜索Apple Notes中的笔记
通过读取SQLite数据文件，获取macOS端苹果自带notes.app中的笔记内容。
# 下载与使用
直接下载Workflow文件导入使用：
- `snote [str]`显示笔记，`[str]`为可选参数，可以通过该参数进行搜索
- `↵`回车复制笔记内容到剪切板
- `⌘+↵`Command+回车通过largetype查看内容
- `→`进入选项，可以结合[Word Segment](https://github.com/BlackCCCat/Alfred-Workflow/tree/main/word-segment)，将笔记内容分词复制需要的内容，也可以直接在Alfred显示界面中通过鼠标复制内容