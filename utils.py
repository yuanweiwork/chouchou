import json
import os

base_dir = os.path.dirname(os.path.dirname(__file__))


def getConfig():
    path = base_dir + "/config.json"
    if not os.path.exists(path):
        open(path, 'w')
    if os.path.getsize(path) == 0:
        return None
    with open(path, 'r', encoding='utf8')as fp:
        json_data = json.load(fp)
        return json_data


def setConfig(key, value):
    global dict1
    path = base_dir + "/config.json"
    if not os.path.exists(path):
        open(path, 'w')
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
