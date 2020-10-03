# 浏览器控制类
import time

from selenium import webdriver


class DeviceManager:
    """这是一种简单的单例设计模式的实现方式"""
    __obj = None
    __flag_init = True

    def __new__(cls, *args, **kwargs):
        if cls.__obj is None:
            cls.__obj = object.__new__(cls)

        return cls.__obj

    def __init__(self):
        if DeviceManager.__flag_init:
            self.driver = webdriver.Chrome()
            DeviceManager.__flag_init = False

    def getDevice(self):
        return self.driver

    def getUrl(self, url):
        self.driver.get(url)
        return self.driver

    def openUrl(self, url):
        js = "window.open('" + url + "')"
        self.driver.execute_script(js)
        time.sleep(5)
        return self.driver
