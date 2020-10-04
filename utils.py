import json
import os

base_dir = os.path.dirname(os.path.dirname(__file__))


def getBaseDir():
    dirs = base_dir + "\config"
    if not os.path.exists(dirs):
        os.makedirs(dirs)
    return dirs


def getDbDir():
    dirs = getBaseDir() + "\chouchou.db"
    return dirs


def getConfig():
    path = getBaseDir() + "\config.json"
    checkFile(path)
    if os.path.getsize(path) == 0:
        return None
    with open(path, 'r', encoding='utf8')as fp:
        json_data = json.load(fp)
        return json_data


def checkFile(file):
    try:
        f = open(file, 'r')
        f.close()
    except IOError:
        f = open(file, 'w')
        f.close()


def setConfig(key, value):
    global dict1
    path = getBaseDir() + "\config.json"
    checkFile(path)
    dict = {}
    temp = getConfig()
    if temp is not None:
        dict = getConfig()
    dict[key] = value
    with open(path, 'w', encoding='utf8')as fp:
        jsonstr = json.dumps(dict)
        fp.write(jsonstr)


def getImagePath():
    return getConfig()['images']


def setImagePath(path):
    return setConfig('images', path)
