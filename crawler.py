import json
import os
import random
import time
import pandas as pd

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC

import Const
from Login import  login_simulate,is_logged_in
from Cookies import load_cookies,has_cookies_file,is_expired

# 预防反爬
options = Options()
# 更改User-Agent
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
options.add_argument('--headless')  # 启用无头模式，不显示图形界面
options.add_argument(f'user-agent={user_agent}')
options.add_argument('--disable-javascript')
options.add_argument('disable-infobars')
options.add_experimental_option('detach', True)
options.add_argument('-disable-blink-features=AutomationControlled')

#随机延时函数，用来模拟动作比较快的点击操作
def random_delay(time_start, time_end):
    delay = random.uniform(time_start, time_end)
    time.sleep(delay)


def crawler():
    # 创建 Chrome WebDriver 实例（需要梯子）
    browser = webdriver.Edge(options=options)

    try:
        is_login_by_cookie=False
        # 判断cookie文件是否存在
        if has_cookies_file(Const.Cookies_file):
            # 读取cookie文件
            with open(Const.Cookies_file, 'r', encoding='utf-8') as f:
                cookies = json.load(f)
            # 判断cookie是否过期
            if is_expired(cookies):
                is_login_by_cookie=False
            else:
                # 写入cookie进行登录
                load_cookies(browser, cookies)
                # 再次判断登录是否成功(仅根据时间戳可能会失败)
                if is_logged_in(browser):
                    is_login_by_cookie=True
                    print("cookie登录成功.")
                    random_delay(1,2)
        # 无法使用cookie登录就直接模拟登录
        if is_login_by_cookie==False:
            print("cookie登录失败，进行模拟登录.")
            Login_url = Const.Login_url
            login_simulate(browser,Login_url,Const.Username,Const.Password)
            random_delay(1, 2)


        # 打开网页开始爬取数据
        Target_url = Const.Target_url  # 正确的 URL 格式
        browser.get(Target_url)
        # 等待表格元素加载完成，这里使用显式等待确保元素加载
        table = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.ID, 'flex_cb'))
        )
        random_delay(1, 2)

        # 提取到表头
        tr_element = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="flex_cb"]/thead/tr[2]'))
        )
        th_elements = tr_element.find_elements(By.TAG_NAME, 'th')# 遍历tr标签下的th标签
        headers = [th.text for th in th_elements]# 提取每个th元素的文本
        headers = [header.replace('\n', '').replace(' ', '') for header in headers[:-1]] #清洗
        print(f"大概需要{random.randint(100,130)}s...")

        # 提取表格内容td
        rows = table.find_elements(By.TAG_NAME, "tr")[1:]  # 获取所有的行，跳过表头
        lst = []  # 存储表格内容为list
        for row in rows:
            td_content = row.find_elements(By.TAG_NAME, "td")  # 进一步定位到表格内容所在的td节点
            lst.append([element.text for element in td_content[:-1]])  # 提取每行的td文本并添加到列表中
        # 数据清洗
        lst= lst[1:-1]# 删除第一个和最后一个元素
        # print("转债数据爬取完毕")  # 输出表格内容

        # 确保data文件夹存在
        data_folder = Const.data_path
        if not os.path.exists(data_folder):
            os.makedirs(data_folder)

        # 存储到xls表格中
        current_time = time.strftime("%Y-%m-%d_%H-%M")
        file_name = f"{data_folder}/可转债_{current_time}.xls"
        df = pd.DataFrame(lst, columns=headers)
        df.to_excel(file_name, index=False, engine='openpyxl')

    finally:
        # 关闭浏览器
        browser.quit()

