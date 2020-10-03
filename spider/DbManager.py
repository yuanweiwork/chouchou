# 数据库管理
import os
import sqlite3

from Model import Goods


class DbManager:
    """这是一种简单的单例设计模式的实现方式"""
    __obj = None
    __flag_init = True

    def __new__(cls, *args, **kwargs):
        if cls.__obj is None:
            cls.__obj = object.__new__(cls)
        return cls.__obj

    def __init__(self):
        if DbManager.__flag_init:
            path = os.path.dirname(os.path.dirname(__file__)) + "/chouchou.db"
            self.conn = sqlite3.connect(path)
            DbManager.__flag_init = False

    def exists(self, tableName):
        try:
            c = self.conn.cursor()
            select_cmd = '''SELECT * FROM "%s"''' % tableName
            c.execute(select_cmd)
            self.conn.commit()
            return True
        except:
            return False

    def createGoods(self):
        c = self.conn.cursor()
        sql = '''CREATE TABLE GOODS (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        GOOD_ID INT ,
        GOOD_NAME TEXT ,
        URL TEXT ,
        BANNER TEXT ,
        DETAILS TEXT );'''
        c.execute(sql)
        self.conn.commit()
        c = self.conn.cursor()
        skusql = '''CREATE TABLE GOODS_SKU(
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        GOOD_SKU_ID TEXT ,
        GOOD_ID INT ,
        SKU_NAME TEXT ,
        IMAGE_URL TEXT ,
        PRICE FLOAT, 
        PATH TEXT );'''
        c.execute(skusql)
        self.conn.commit()

    def installGoods(self, good):
        c = self.conn.cursor()
        sql = '''INSERT INTO GOODS(GOOD_ID,GOOD_NAME,URL,BANNER,DETAILS)  VALUES ("%s","%s","%s","%s","%s");''' % (
            good.id, good.title, good.url, good.banner, good.details)
        c.execute(sql)
        self.conn.commit()

    def installSku(self, skus):
        for sku in skus:
            c = self.conn.cursor()
            sql = '''INSERT INTO GOODS_SKU(GOOD_SKU_ID,GOOD_ID,SKU_NAME,IMAGE_URL,PRICE,PATH) VALUES ("%s","%s","%s","%s","%s","%s");''' % (
                sku.goodskuId, sku.goodid, sku.skuname, sku.imageUrl, sku.price, sku.path)
            c.execute(sql)
            self.conn.commit()
