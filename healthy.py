import datetime
from email.header import Header
from email.mime.text import MIMEText
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import smtplib


username = "####"
password = "####"
mail_host="smtp.qq.com"
mail_port = 465
sender = '####'
mail_pass="####"
receiver = '####'


def upload(username, password):
    options = webdriver.ChromeOptions()
    # options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    # options.add_argument('headless')
    options.add_argument('--headless')
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    # login
    driver = webdriver.Chrome(options=options)
    driver.get("http://smse.fun-master.cn/report/login")
    wait1 = WebDriverWait(driver, 120)
    print("登录")
    driver.find_element(By.ID, 'stu_no').send_keys(username)
    driver.find_element(By.ID, 'password').send_keys(password)
    driver.find_element(By.ID, 'sub').click()
    try:
        wait1.until(EC.presence_of_element_located((By.ID, "mor2")))
        print("登录成功")
    except TimeoutException as e:
        print("登录失败")
        print(e)
        return False

    print("健康申报")
    driver.find_element(By.ID, "mor2").click()
    driver.find_element(By.ID, "non2").click()
    driver.find_element(By.ID, "yes72").click()
    driver.execute_script("setLocation(121.59446978020986,38.88802522233168)") # 星海广场
    driver.find_element(By.ID, "chengnuo").click()
    driver.find_element(By.CLASS_NAME, "i-submit").click()

    wait2 = WebDriverWait(driver, 120)
    try:
        wait2.until(EC.text_to_be_present_in_element((By.CLASS_NAME, "pop-up"), "今日信息已提交"))
        print("健康申报成功")
    except TimeoutException as e:
        print("健康申报失败")
        print(e)
        return False
    return True


def send_email(result):
    s = smtplib.SMTP_SSL(mail_host, mail_port)
    s.login(sender, mail_pass)
    if result:
        content = str(datetime.date.today()) + '健康打卡成功'
    else:
        content = str(datetime.date.today()) + '健康打卡失败'
    message = MIMEText(content, 'plain', 'utf-8')
    message['Subject'] = Header(content, 'utf-8')
    message['From'] = sender
    message['To'] = receiver
    s.sendmail(sender, receiver, message.as_string())
    s.quit()


if __name__ == '__main__':
    result = upload(username, password)
    send_email(result)
