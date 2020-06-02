# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
import requests
from bson import binary
from base64 import b64encode
from scrapy import  Request
import os
# import redis
# Define your item pipelines here

from scrapy.exceptions import DropItem


class MongoDBPipeline(object):
    def __init__(self, host, port, db, redis_host, redis_port):
        # pool = redis.ConnectionPool(
        #     host=redis_host, port=redis_port, db=0)
        self.mongo_uri = host
        self.mongo_db = db
        # self.server = redis.Redis(connection_pool=pool)

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[spider.web_name + self.mongo_db]

    @classmethod
    def from_crawler(cls, crawler):
        return cls(host=crawler.settings.get('MONGODB_SERVER'),
                   db=crawler.settings.get('MONGODB_DB'),
                   port=crawler.settings.get('MONGODB_PORT'),
                   redis_host=crawler.settings.get("REDIS_HOST"),
                   redis_port=crawler.settings.get("REDIS_PORT"))

    def process_item(self, item, spider):
        item_id = item["id"]
        item_cat = item["category"]
        item["img"]= "http:"+item["img"]
        if spider.web_name == 'sn':
            item["img"] = item["img"].split(".jpg")[0] + ".jpg" + "_300w_300h_4e"
        item["source"] = spider.web_name
        item.pop("category")
        collection = self.db[item_cat]
        item["date_price"]={}
        item["date_price"][item.pop("date")] = [item.pop("lowest_price"), item.pop("highest_price")]
        collection.update({"id": item_id}, item,upsert=True)
        return item

    def close_spider(self, spider):
        self.client.close()
