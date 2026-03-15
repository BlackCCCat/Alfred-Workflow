import requests
import os
from warnings import filterwarnings
from config import AccountInfo

filterwarnings("ignore")

file_dir = os.path.dirname(os.path.abspath(__file__))

class GetDynamic():
    def request_dynamic(self):
        updated_dynamic = {}

        url = "https://api.bilibili.com/x/polymer/web-dynamic/v1/feed/all"
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2.1 Safari/605.1.15"
        }

        params = {
            "type": "video",
        }

        cookies_list = AccountInfo.get_valid_cookie()
        if not cookies_list:
            updated_dynamic["获取动态失败"] = {"video_info": "未找到有效的bilibili.com cookie，请在官网登录并获取Cookies等信息，点击打开官网", "link": "https://www.bilibili.com", "icon": os.path.join(file_dir, 'icon.png')}
            return updated_dynamic

        for cookie in cookies_list:
            res = requests.get(url=url, headers=headers, cookies=cookie, params=params, verify=False)

            whole_json_data = res.json()

            if whole_json_data["code"] == 0:
                break

        data_list = whole_json_data["data"]["items"]
#         update_num = whole_json_data["data"]["update_num"]
#         if not update_num:
#             updated_dynamic["暂无新动态"] = {"video_info": "🈳", "link": "https://t.bilibili.com", "icon": os.path.join(file_dir, 'icon.png')}
#             return updated_dynamic


        for data in data_list:
            author = data["modules"]["module_author"]["name"]
            put_time = data["modules"]["module_author"]["pub_time"]
            put_ts = data["modules"]["module_author"]["pub_ts"]
            video_title = data["modules"]["module_dynamic"]["major"]["archive"]["title"]
            video_cover = data["modules"]["module_dynamic"]["major"]["archive"]["cover"]
            video_play = data["modules"]["module_dynamic"]["major"]["archive"]["stat"]["play"]
            video_danmaku = data["modules"]["module_dynamic"]["major"]["archive"]["stat"]["danmaku"]
            video_link = data["modules"]["module_dynamic"]["major"]["archive"]["jump_url"]
            is_download = self.downloadIMG(author, put_ts, video_cover)

            if is_download:
                updated_dynamic[video_title] = {"video_info": f"👤{author} 发布于:{put_time} ▶️ {video_play} 🫧 {video_danmaku}", "link": f"https:{video_link}", "icon": os.path.join(file_dir, 'images', f'{author}_{put_ts}.png')}
            else:
                updated_dynamic[video_title] = {"video_info": f"👤{author} 发布于:{put_time} ▶️ {video_play} 🫧 {video_danmaku}", "link": f"https:{video_link}", "icon": os.path.join(file_dir, 'icon.png')}

        return updated_dynamic


    def downloadIMG(self, author, put_ts, imgurl):
        subdir = 'images'
        if not os.path.exists(subdir):
            os.makedirs(subdir)
        image_path = os.path.join(subdir, f'{author}_{put_ts}.png')
        res = requests.get(url=imgurl, verify=False)
        if res.status_code == 200:
            # 打开一个文件（以二进制写入模式），用来保存图片
            with open(image_path, 'wb') as f:
                # 将响应的二进制内容写入文件
                f.write(res.content)
            return True
        else:
            return False


if __name__ == "__main__":
    get_dynamic = GetDynamic()
    updated_dynamic = get_dynamic.request_dynamic()
    print(updated_dynamic)
