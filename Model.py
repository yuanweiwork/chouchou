class Goods:
    def __init__(self, goodid="", title="", url="", banner="", details=""):
        self.id = goodid
        self.title = title
        self.url = url
        self.banner = banner
        self.details = details


class GoodsSku:
    def __init__(self, goodid="", goodskuId="", skuname="", imageUrl="", price="", path=""):
        self.goodid = goodid
        self.skuname = skuname
        self.goodskuId = goodskuId
        self.imageUrl = imageUrl
        self.price = price
        self.path = path


class Country:
    def __init__(self, name, price):
        self.name = name
        self.price = price
