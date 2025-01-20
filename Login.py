import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Cookies import save_cookies



#模拟登录
def login_simulate(driver,url,username,password):
    # 访问登录页面
    driver.get(url)

    # 输入用户名和密码
    username_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, 'user_name'))
    )
    username_input.send_keys(username)
    password_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, 'password'))
    )
    password_input.send_keys(password)

    # 点击同意登录
    Agree_span = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'agree_text'))
    )
    Agree_span.click()

    time.sleep(1) # 延时
    #进行登录
    login_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, 'btn-jisilu'))
    )
    login_button.click()

    # 等待登录成功（可能需要处理验证码）
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'inbox_unread'))
    )

    # 保存 Cookie 到 JSON 文件
    save_cookies(driver,'cookies.json')

# 判断是否登录成功
def is_logged_in(driver):
    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'page_detail'))
        )
        return True
    except:
        return False