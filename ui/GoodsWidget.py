import random
import time
from tkinter import *
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
from tkinter.ttk import *
import html
from urllib import request

import utils
from Model import Goods, GoodsSku
from spider.DbManager import DbManager
from spider.DeviceManager import DeviceManager
from spider.ImageLoader import formatIndex, downloadImageSize
from utils import getConfig

clickid = "&clickid=459c155c54f04734a21a6792f8dd45a7&sessionid=926b47fef14071a20b10b291c4c8db99"


class GoodsTopLevel:
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
        # self.init_open_device_button = Button(self.top, text="打开浏览器", command=self.openDeviceCallBack)
        # self.init_open_device_button.pack(fill=X, ipady=10)
        #
        # self.search_user_sid = Button(self.top, text="抓取身份信息", command=self.search_user_sid_callback)
        # self.search_user_sid.pack(fill=X, ipady=10)
        # text = getConfig()["sid"]
        # if text == "":
        #     text = "请打开浏览器,登录后 点击抓取身份信息！"
        # self.init_sid_lib = Label(self.top, text=text)
        # self.init_sid_lib.pack(fill=X, ipady=10)

        self.init_edit_goods_url = Text(self.top, width=70, height=5)
        self.init_edit_goods_url.config(highlightbackground="black")
        self.init_edit_goods_url.pack()
        self.tip_lab = ttk.Label(self.top, text="在上面输入想要的网址").pack(fill=X)
        self.checkBox = ttk.Checkbutton(self.top, text="是否加入到数据库中").pack()

        self.init_search_good_button = Button(self.top, text="开始搜索", command=self.startSearchCallback)
        self.init_search_good_button.pack(fill=X, ipady=10)

        self.layout = ScrolledText(self.top, wrap=WORD)
        self.layout.config(highlightbackground="black")
        self.layout.pack(fill=X, ipady=40, sid=BOTTOM)

    def openDeviceCallBack(self):
        # 打开浏览器
        DeviceManager().getUrl("https://www.1688.com/")

    def addLogMessage(self, message):
        self.layout.insert(INSERT, chars=message + '\n')
        self.layout.see(END)

    # 开始搜索页面
    def startSearchCallback(self):
        goodsUrlList = []
        urls = self.init_edit_goods_url.get('0.0', 'end')
        if urls == '':
            self.addLogMessage("输入框网址为空！！！！！")
            return

        for line in str(urls).split("\n"):
            if line == "":
                break
            goodsUrlList.append(line)
        self.addLogMessage("检测到网址" + str(len(goodsUrlList)))
        for url in goodsUrlList:
            url_device = DeviceManager().getUrl(url + clickid)
            time.sleep(random.randint(2, 6))
            htmlstr = url_device.page_source
            htmlstr = html.unescape(htmlstr)
            title = url_device.title

            goods = Goods()
            goods.url = url
            goods.title = title
            goods.id = self.goodId
            bannerImage = self.search_and_download_banner_imageUrl(htmlstr)
            bannerArray = self.downloadBannerImgUrl(bannerImage)

            detailsImage = self.search_and_download_details_imageUrl(htmlstr)
            detailsArray = self.downloadDetailsImgUrl(detailsImage)

            skuImage = self.search_and_download_sku_imageUrl(htmlstr, url_device)
            goods.banner = str(bannerArray)
            goods.details = str(detailsArray)

            DbManager().installGoods(goods)
            DbManager().installSku(skuImage)

    def downloadBannerImgUrl(self, images):
        saveFileDir = utils.getImagePath() + "/" + str(self.goodId) + "/"
        downloadImageSuccess = []
        self.addLogMessage("共有banner图：" + str(len(images)) + "张")
        for index, img in enumerate(images):
            name = "banner" + str(self.goodId) + formatIndex(index)
            successName = downloadImageSize(img, saveFileDir, name)
            downloadImageSuccess.append(successName)
            self.addLogMessage("已下载：" + str(index + 1) + "/" + str(len(images)) + "张")
        return downloadImageSuccess

    def downloadDetailsImgUrl(self, images):
        saveFileDir = utils.getImagePath() + "/" + str(self.goodId) + "/"
        downloadImageSuccess = []
        self.addLogMessage("共有details图：" + str(len(images)) + "张")
        for index, img in enumerate(images):
            name = "details" + str(self.goodId) + formatIndex(index)
            successName = downloadImageSize(img, saveFileDir, name)
            downloadImageSuccess.append(successName)
            self.addLogMessage("已下载：" + str(index + 1) + "/" + str(len(images)) + "张")
        return downloadImageSuccess

    def downloadSkuImageUrl(self, skuImage):
        saveFileDir = utils.getImagePath() + "/" + str(self.goodId) + "/"
        downloadImageSuccess = []
        self.addLogMessage("共有sku图：" + str(len(skuImage)) + "张")
        for index, img in enumerate(skuImage):
            name = str(self.goodId) + formatIndex(index)
            successName = downloadImageSize(img, saveFileDir, name)
            downloadImageSuccess.append(successName)
            self.addLogMessage("已下载：" + str(index + 1) + "/" + str(len(skuImage)) + "张")
        return downloadImageSuccess

    # 搜索详情图
    def search_and_download_details_imageUrl(self, htmlstr):
        # 搜索图片
        detailsStr = re.findall('data-tfs-url="(.*)" data-enable', htmlstr, flags=re.DOTALL)
        resp = request.urlopen(detailsStr[0])
        page = str(resp.read()).replace("\\", "")
        detailsimages = re.findall('src="(.*?).jpg', page, flags=re.DOTALL)
        return detailsimages

    # 搜索banner图
    def search_and_download_banner_imageUrl(self, htmlstr):
        # 搜索图片
        bannerStr = re.findall('<div class="tab-content-container">(.*)<div class="obj-fav">', htmlstr, flags=re.DOTALL)
        array = []
        banners = re.findall('<img src="(http.*).60x60.jpg', bannerStr[0])
        tip = "data-lazy-src"
        for banner in banners:
            if tip not in banner:
                array.append(banner)
            else:
                url = re.findall('data-lazy-src="(http.*)', banner)
                if len(url) != 0:
                    array.append(url[0])
        return array

    # 搜索sku
    def search_and_download_sku_imageUrl(self, htmlstr, url_device):
        htmlstr = htmlstr.replace(" ", "").replace("\n", "")
        skus = []
        # 搜索sku  图片  价格  尺码 等信息
        skubodystr = re.findall('list-leading">(.*?)</ul>', htmlstr, flags=re.DOTALL)
        if len(skubodystr) == 0:
            skusizeStr = re.findall('<tableclass="table-sku">(.*)</table>', htmlstr, flags=re.DOTALL)
            searchsku = self.search_good_sku(str=skusizeStr[0], code=0)
            skus.append(searchsku)
        else:
            ul = url_device.find_element_by_xpath("//ul[@class='list-leading']")
            lis = ul.find_elements_by_xpath('li')
            skuimg = re.findall('src="(.*?).32x32.jpg', skubodystr[0], flags=re.DOTALL)
            skuimgPath = self.downloadSkuImageUrl(skuimg)
            for index, li in enumerate(lis):
                li.click()
                skusizeStr = re.findall('<tableclass="table-sku">(.*)</table>', htmlstr, flags=re.DOTALL)
                searchsku = self.search_good_sku(skusizeStr[0], skuimg[index], skuimgPath[index], index)
                for sku in searchsku:
                    skus.append(sku)
        return skus

        # 下载图片
        # 存入数据库

    def search_good_sku(self, str, image="", imagePath="", code=0):
        skus = []
        size = re.findall('data-sku-config(.*?)</tr>', str, flags=re.DOTALL)
        for index, i in enumerate(size):
            sku = GoodsSku()
            if "" == image:
                arrayImg = re.findall('data-lazy-src="(.*).32x32.jpg', i)
                sku.imageUrl = arrayImg[0]
                sku.path = self.downloadSkuImageUrl([sku.imageUrl])[0]
            else:
                sku.imageUrl = image
                sku.path = imagePath
            price = re.findall('class="value">(.*)</em><emclass="price-unit">', i)
            name = re.findall('skuName":"(.*)","isMix', i)
            sku.price = price[0]
            sku.skuname = name[0]
            sku.goodid = self.goodId
            goodidStr = formatIndex(self.goodId)
            codestr = formatIndex(code)
            indexStr = formatIndex(index)
            sku.goodskuId = goodidStr + codestr + indexStr
            skus.append(sku)
        return skus
