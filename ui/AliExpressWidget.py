from tkinter import Toplevel
from tkinter.ttk import Button

from utils import getConfig


class AliExpressWidget:
    def __init__(self, tk):
        self.goodId = getConfig()["maxId"]
        sw = (tk.winfo_screenwidth() - 400) / 2 + 320
        # 得到屏幕宽度
        sh = (tk.winfo_screenheight() - 700) / 2

        self.top = Toplevel(tk)
        self.top.geometry("%dx%d+%d+%d" % (400, 700, sw, sh))
        # 禁止改变窗口宽高
        self.top.resizable(0, 0)
        # self.top.attributes("-toolwindow", True)
        # self.top.wm_attributes("-topmost", True)
        self.top.title("抓图工具")
        self.initViews()

    def initViews(self):
        self.sendGoodbutton = Button(self.top, text="打开浏览器", command=self.sendGoodCallback)

    def sendGoodCallback(self):
        self.eidtInfo()
        self.editPrice()
        self.editDetails()
        self.editpacking()
        pass

    def eidtInfo(self):
        pass

    def editPrice(self):
        pass

    def editDetails(self):
        pass

    def editpacking(self):
        pass
