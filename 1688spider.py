from selenium import webdriver
import random
import time
import re
import requests
import os

textfile = "/Users/yuanwei/Documents/study/pythone/chouchou/"
goodsList = []
goodname = ""

detailsImgPattern = '"imageUrl":"(http.*?).jpg'
bannerImgPattern = '<img src="(http.*?).60x60.jpg"'
sizeImgPattern = 'data-lazy-src="(https.*?).60x60.jpg" alt='


# bannerImgPattern = 'src="(http.*?).32x32.jpg"'


# 1. 打开页面
# 2.抓取页面元素  用正则拿到所有图片链接
# 3.下载所有图片

def getHtml(url):
    driver = webdriver.Chrome(executable_path='/usr/local/bin/chromedriver')
    driver.get(url)
    driver.name
    sleeptime = random.randint(2, 10)
    print('time--' + str(sleeptime))
    time.sleep(sleeptime)
    content = driver.page_source
    driver.close()
    return content


def filterImgUrl(html, pattern):
    arrayimages = re.findall(pattern, html)
    return arrayimages


def downloadImgUrl(images, goodname, type, size):
    file = textfile + goodname + "/"
    print(file)
    for index, img in enumerate(images):
        if index < 10:
            index = '0' + str(index)
        else:
            index = str(index)
        path = file + type + "_" + index + '.jpg'
        imageUrl = str(img) + str(size) + '.jpg'

        try:
            if not os.path.exists(file):
                os.mkdir(file)
            if not os.path.exists(path):
                r = requests.get(imageUrl)
                r.raise_for_status()
                with open(path, 'wb') as f:
                    f.write(r.content)
                    f.close()
            else:
                print("图片已存在")
        except Exception as e:
            print("图片获取失败" + imageUrl)


def readTxt(filename):
    with open(filename + "config.txt", 'r') as file_to_read:
        lines = file_to_read.read()  # 整行读取数据
        for line in str(lines).split("\n"):
            if line == "":
                break
            goodsList.append(line)


if __name__ == '__main__':
    # 解析txt文档 第一行 存储路径   第二行 详情页连接
    readTxt(textfile)
    # 1.获取网页源码
    for good in goodsList:
        htmlstr = getHtml(good)
        goodname = re.findall(r'<title>(.*?)</title>', htmlstr)
        detailsImgs = filterImgUrl(htmlstr, detailsImgPattern)
        bannerImgs = filterImgUrl(htmlstr, bannerImgPattern)
        sizeImgs = filterImgUrl(htmlstr, sizeImgPattern)
        downloadImgUrl(detailsImgs, goodname[0], "details", "")
        downloadImgUrl(bannerImgs, goodname[0], "banner", ".800x800")
        downloadImgUrl(sizeImgs, goodname[0], "size", ".800x800")

    # 2.获取轮播图 url
    # 3.获取详情图url
    # 4.下载轮播图url
    # 5.下载详情图
    # localFile = cur_path = os.path.abspath(os.path.dirname(__file__))
    # htmlstr = getHtml(url)
    # arrayimages = filterImgUrl(htmlstr)
    # downloadImgUrl(arrayimages, localFile, "")
