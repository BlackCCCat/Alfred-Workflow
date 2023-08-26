# Hot News
使用Python获取微博、知乎、贴吧的热搜榜
## 效果展示
- **贴吧**
![CleanShot 2023-08-26 at 19.01.28@2x](assets/CleanShot%202023-08-26%20at%2019.01.28@2x.png)
![CleanShot 2023-08-26 at 19.02.57@2x](assets/CleanShot%202023-08-26%20at%2019.02.57@2x.png)

- 微博
![CleanShot 2023-08-26 at 19.02.08@2x](assets/CleanShot%202023-08-26%20at%2019.02.08@2x.png)
![CleanShot 2023-08-26 at 19.03.08@2x](assets/CleanShot%202023-08-26%20at%2019.03.08@2x.png)

- 知乎
![CleanShot 2023-08-26 at 19.02.46@2x](assets/CleanShot%202023-08-26%20at%2019.02.46@2x.png)
![CleanShot 2023-08-26 at 19.03.25@2x](assets/CleanShot%202023-08-26%20at%2019.03.25@2x.png)



# 安装所需模块
- 如果使用的是macOS自带Python环境(也是Alfred默认使用Python环境):
```shell
/usr/bin/python3 -m pip install -r requirements.txt
```
- 其他
```shell
pip install -r requirements.txt
```
# 使用方法
- `wb [n]`获取微博热搜榜前`n`个热搜
- `zh [n]`获取知乎热搜榜前`n`个热搜
- `tb [n]`获取贴吧热搜榜前`n`个热搜

> `[n]`为可选参数,无输入时,默认获取前10个热搜榜
