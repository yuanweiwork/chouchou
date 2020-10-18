# -*- coding: UTF-8 -*-
import json

import xlrd

from Model import Country

# book = xlrd.open_workbook('./简易类.xlsx')
book = xlrd.open_workbook('./标准类.xlsx')
f = open("out.txt", "w")

# for sheet in book.sheets():
#     print(sheet.name)
# 重量合适的列
# column = 0

# 重量
weight = 100
# 运费差距间隔
IntervalPrice = 10.2


# 第一张表的俄罗斯的运费作为基准 之后的增减

def ergodicTable():
    targetPrice = 0
    for sheet in book.sheets():
        list = []
        column = 0
        tableName = sheet.name
        row = sheet.row_values(0)
        for index, value in enumerate(row):
            try:
                section = str(value).split("-")
                if int(section[1]) >= weight >= int(section[0]):
                    column = index
            except Exception as e:
                # column = 0
                pass
        for index in range(1, sheet.nrows):
            try:
                row = sheet.row_values(index)
                if row[column] is not None and row[column] != "-" and row[column] != "无服务":
                    kgPrice = row[column]
                    item = row[column + 1]
                    price = kgPrice / 1000 * weight + item
                    print(str(row[0]) + str(price) + "==" + str(kgPrice) + "==" + str(item))
                    list.append(Country(row[0], price))
            except Exception as e:
                print(e)
                pass
        list.sort(key=lambda x: x.price, reverse=False)
        # for model in list:
        #     print(model.name + str(model.price))
        if targetPrice == 0:
            # 临时对比价格
            tempPrice = 0
            indexTemp = 1
            jsonobj = {}
            start = True
            for index, bean in enumerate(list):
                if not start:
                    # 和包邮俄罗斯的邮费差
                    temp = (bean.price - targetPrice)
                    if (temp - tempPrice) > IntervalPrice:
                        temparray = []
                        for beanTemp in list[indexTemp + 1:index + 1]:
                            temparray.append(beanTemp.name)
                        jsonobj[round(temp / 6.8, 2)] = temparray
                        tempPrice = temp
                        indexTemp = index
                    if (temp - tempPrice) > IntervalPrice:
                        try:
                            model = list[index + 1]
                            if (model.price - targetPrice) > IntervalPrice:
                                temparray = []
                                for beanTemp in list[indexTemp + 1:index + 1]:
                                    temparray.append(beanTemp.name)
                                jsonobj[round(temp / 6.8, 2)] = temparray
                                indexTemp = index
                        except Exception as e:
                            temp = (bean.price - targetPrice)
                            temparray = []
                            for beanTemp in list[index:]:
                                temparray.append(beanTemp.name)
                            jsonobj[round(temp / 6.8, 2)] = temparray
                if bean.name == "俄罗斯" and start:
                    start = False
                    temparray = []
                    indexTemp = index
                    for beanTemp in list[0:index + 1]:
                        name = str(beanTemp.name)
                        temparray.append(name)
                    targetPrice = bean.price
                    jsonobj["包邮" + str(round(bean.price / 6.8, 2))] = temparray
        else:
            # 临时对比价格
            tempPrice = 0
            indexTemp = 1
            jsonobj = {}
            start = True
            for index, bean in enumerate(list):
                if bean.price > targetPrice:
                    if start:
                        temparray = []
                        indexTemp = index
                        for beanTemp in list[0:index + 1]:
                            name = str(beanTemp.name)
                            temparray.append(name)
                        jsonobj["包邮地区:"] = temparray
                        start = False
                    else:
                        temp = (bean.price - targetPrice)
                        if (temp - tempPrice) > IntervalPrice:
                            temparray = []
                            for beanTemp in list[indexTemp + 1:index + 1]:
                                temparray.append(beanTemp.name)
                            jsonobj[round(temp / 6.8, 2)] = temparray
                            tempPrice = temp
                            indexTemp = index
                        if (temp - tempPrice) > IntervalPrice:
                            try:
                                model = list[index + 1]
                                if (model.price - targetPrice) > IntervalPrice:
                                    temparray = []
                                    for beanTemp in list[indexTemp + 1:index + 1]:
                                        temparray.append(beanTemp.name)
                                    jsonobj[round(temp / 6.8, 2)] = temparray
                                    indexTemp = index
                            except Exception as e:
                                temp = (bean.price - targetPrice)
                                temparray = []
                                for beanTemp in list[index:]:
                                    temparray.append(beanTemp.name)
                                jsonobj[round(temp / 6.8, 2)] = temparray
                else:
                    try:
                        model = list[index + 1]
                    except Exception as e:
                        temp = (bean.price - targetPrice)
                        temparray = []
                        for beanTemp in list:
                            temparray.append(beanTemp.name)
                        jsonobj[round(temp / 6.8, 2)] = temparray

        print(json.dumps(jsonobj).encode('utf-8').decode("unicode_escape"))
        f.write(
            "%1s=================================================================================================================\n" % tableName)
        for key, value in jsonobj.items():
            f.write("%1s\n" % key)
            for name in value:
                f.write("%1s," % name)
            f.write("  \n")
        f.write("  \n\n")
    f.write("基准价格为：%1s" % str(targetPrice))
    f.close()


ergodicTable()
