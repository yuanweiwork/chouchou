import os

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from ConstantURL import *
import time

# driver = webdriver.Chrome()
username = os.getenv("USERNAME")
userProfile = "\\Users\\yuanwei\\Documents\\video\\Default"
options = webdriver.ChromeOptions()
options.add_argument("user-data-dir={}".format(userProfile))
# add here any tag you want.
options.add_experimental_option("excludeSwitches",
                                ["ignore-certificate-errors", "safebrowsing-disable-download-protection",
                                 "safebrowsing-disable-auto-update", "disable-client-side-phishing-detection"])
driver = webdriver.Chrome(options=options)


def init():
    try:
        driver.get(login_url)
        input = driver.find_element_by_id("fm-login-id")
        input.send_keys("Python")
        input.send_keys(Keys.ENTER)
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.ID, "content_left")))
    finally:
        driver.close()


def login(username, password):
    # try:
    driver.get("https://www.1688.com/")
    driver.implicitly_wait(3)
    driver.find_element_by_xpath("//li[@class='account-signin redPackageInfoBox']").click()
    driver.implicitly_wait(2)
    frame = driver.find_element_by_xpath("//div[@id='loginchina']/iframe")
    driver.switch_to.frame(frame)
    time.sleep(2)
    driver.find_element_by_name("fm-login-id").send_keys(username)
    time.sleep(3)
    passwordInput = driver.find_element_by_id("fm-login-password")
    passwordInput.send_keys(password)
    time.sleep(1)
    passwordInput.send_keys(Keys.ENTER)
    print(driver.page_source)


# finally:
# browser.close()


login("13673921628", "a2916893")
