import browser_cookie3

class AccountInfo():
    """
    从浏览器获取cookie
    """
    @staticmethod
    def get_valid_cookie():
        browsers = {
            "chrome": browser_cookie3.chrome,
            "edge": browser_cookie3.edge,
            "firefox": browser_cookie3.firefox,
            "brave": browser_cookie3.brave,
            "opera": browser_cookie3.opera,
            "safari": browser_cookie3.safari,
        }
        cookies_list = []

        for name, loader in browsers.items():
            try:
                cj = loader(domain_name=".bilibili.com")

                if not list(cj):
                    continue

                for cookie in cj:
                    if cookie.name == 'SESSDATA':
                        cookies_list.append({cookie.name: cookie.value})

            except Exception:
                pass

        return cookies_list
