import requests
from warnings import filterwarnings
from config import AccountInfo

filterwarnings("ignore")


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

        res = requests.get(url=url, headers=headers, cookies=AccountInfo.cookies, params=params, verify=False)

        whole_json_data = res.json()

        if whole_json_data["code"] != 0:
            message = whole_json_data["message"]
            updated_dynamic["获取动态失败"] = {"video_info": f"{message}，请在官网登录并获取Cookies等信息，点击打开官网", "link": "https://www.bilibili.com"}
            return updated_dynamic

        data_list = whole_json_data["data"]["items"]
        update_num = whole_json_data["data"]["update_num"]
        if not update_num:
            updated_dynamic["暂无新动态"] = {"video_info": "🈳", "link": "https://t.bilibili.com"}
            return updated_dynamic
        

        for data in data_list:
            author = data["modules"]["module_author"]["name"]
            put_time = data["modules"]["module_author"]["pub_time"]
            video_title = data["modules"]["module_dynamic"]["major"]["archive"]["title"]
            video_play = data["modules"]["module_dynamic"]["major"]["archive"]["stat"]["play"]
            video_danmaku = data["modules"]["module_dynamic"]["major"]["archive"]["stat"]["danmaku"]
            video_link = data["modules"]["module_dynamic"]["major"]["archive"]["jump_url"]

            updated_dynamic[video_title] = {"video_info": f"👤{author} 发布于:{put_time} ▶️ {video_play} 🫧 {video_danmaku}", "link": f"https:{video_link}"}
            
        return updated_dynamic
    

if __name__ == "__main__":
    get_dynamic = GetDynamic()
    updated_dynamic = get_dynamic.request_dynamic()
    print(updated_dynamic)