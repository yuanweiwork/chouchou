# 图片下载器
import os

import requests

#
import utils

sizeArray = [".1200x1200.jpg", ".1000x1000.jpg", ".800x800.jpg", ".jpg", ".png"]


def downloadImageSize(imgUrl, saveFileDir, name):
    for size in sizeArray:
        if downloadImage(imgUrl + size, saveFileDir, name):
            return name + ".jpg"


def downloadImage(imgUrl, saveFileDir, name):
    try:
        path = saveFileDir + name + ".jpg"
        print(imgUrl)
        if not os.path.exists(saveFileDir):
            os.mkdir(saveFileDir)
        if not os.path.exists(path):
            r = requests.get(imgUrl)
            r.raise_for_status()
            with open(path, 'wb') as f:
                f.write(r.content)
                f.close()
            print(path)
        else:
            return True
    except Exception as e:
        return False


def formatIndex(index):
    if int(index) < 100:
        if index < 10:
            index = '0' + str(index)
        index = '0' + str(index)
    return str(index)
