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
    date_price=Field()
    type=Field()    #商品型号，用来对齐不同电商直接的商品 #
    img=Field() #
    coupons=Field() #
    source=Field()
    sale_volume=Field()

class ScrapyseleniumItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    collection='taobao'
    price =scrapy.Field()
    store_url = scrapy.Field()
    store_name = scrapy.Field()
    item_url = scrapy.Field()
    image_url=scrapy.Field()
    title = scrapy.Field()
    sale_volume=scrapy.Field()
    where_produce=scrapy.Field()