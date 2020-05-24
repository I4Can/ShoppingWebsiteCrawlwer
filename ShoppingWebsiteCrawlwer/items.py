# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field,Item


class Good(Item):
    _id = Field()   #
    category=Field()    #
    shop=Field()    #
    url=Field()#
    name = Field()#
    id = Field()#
    lowest_price = Field()
    highest_price=Field()
    brand = Field()#
    date=Field()    #爬取时间，用来描述价格曲线  #
    type=Field()    #商品型号，用来对齐不同电商直接的商品 #
    img=Field() #
    coupons=Field() #
