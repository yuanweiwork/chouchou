import os
from tkinter import *
from tkinter.ttk import *
import hashlib
import time

from spider.DbManager import DbManager
from ui import *
from ui.GoodsWidget import GoodsTopLevel
from tkinter import filedialog
import utils

LOG_LINE_NUM = 0

goodTopLevel = None


class MainGui:
    def __init__(self, init_window_name):
        self.init_window_name = init_window_name

    # 设置窗口
    def set_init_window(self):
        self.init_window_name.title("工具")  # 窗口名
        sw = (self.init_window_name.winfo_screenwidth() - 320) / 2
        # 得到屏幕宽度
        sh = (self.init_window_name.winfo_screenheight() - 700) / 2
        # 宽320 高1000  居中
        self.init_window_name.geometry("%dx%d+%d+%d" % (320, 700, sw, sh))
        # 禁止改变窗口宽高
        self.init_window_name.resizable(0, 0)

        self.saveButtonPath = Button(self.init_window_name, text="文件夹", command=self._saveButtonPathCallback)
        self.saveButtonPath.pack(fill=X, ipady=10)
        
        self._1688Button = Button(self.init_window_name, text="1688抓取图片工具", command=self._1688ButtonCallback)
        self._1688Button.pack(fill=X, ipady=10)

        if not DbManager().exists("GOODS"):
            DbManager().createGoods()
        utils.setConfig("maxId", DbManager().getMaxGoodsId())


    def _1688ButtonCallback(self):
        global goodTopLevel
        if goodTopLevel is None:
            goodTopLevel = GoodsTopLevel(self.init_window_name)

    def _saveButtonPathCallback(self):
        self.init_window_name.withdraw()
        file_path = filedialog.askdirectory()
        utils.setImagePath(file_path)


def gui_start():
    init_window = Tk()  # 实例化出一个父窗口
    ZMJ_PORTAL = MainGui(init_window)
    # 设置根窗口默认属性
    ZMJ_PORTAL.set_init_window()
    init_window.mainloop()  # 父窗口进入事件循环，可以理解为保持窗口运行，否则界面不展示


gui_start()
