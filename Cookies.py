import os
import json
import time
import Const


# 判断是否已经有cookie文件
def has_cookies_file(file_path):
    if os.path.exists(file_path):
        return True
    else:
        print("cookies文件不存在.")
        return False

# 判断cookie是否过期
def is_expired(cookies):
    # 获取当前时间戳
    current_timestamp = int(time.time())
    # 判断每个cookie是否过期
    expired_cookies = []
    for cookie in cookies:
        if 'expiry' in cookie and cookie['expiry'] < current_timestamp:
            expired_cookies.append(cookie['name'])

    # 返回结果
    if expired_cookies:
        print("不可使用cookie登录，以下cookie已过期：", expired_cookies)
        return True
    else:
        print("所有cookie均未过期")
        return False


# 向请求中添加cookie
def load_cookies(driver, cookies):
    # 需要先发起一下请求，否则会卡顿（selenium问题）
    driver.get(Const.First_url)
    for cookie in cookies:
        driver.add_cookie(cookie)
    time.sleep(1)
    driver.get(Const.Homepage_url)
    driver.refresh()  # 刷新页面以应用 Cookie


# 保存cookies
def save_cookies(driver, file_path):
    cookies = driver.get_cookies()
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(cookies, f, ensure_ascii=False, indent=4)
    print("cookies.json已生成")