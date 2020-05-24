# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
import os
import redis
# Define your item pipelines here

from scrapy.exceptions import DropItem
class MongoDBPipeline(object):
    def __init__(self, host, port, db,redis_host,redis_port):
        pool = redis.ConnectionPool(
            host=redis_host, port=redis_port, db=0)
        self.mongo_uri = host
        self.mongo_db = db
        self.server = redis.Redis(connection_pool=pool)


    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[spider.web_name+self.mongo_db]

    @classmethod
    def from_crawler(cls, crawler):
        return cls(host=crawler.settings.get('MONGODB_SERVER'),
                   db=crawler.settings.get('MONGODB_DB'),
                   port=crawler.settings.get('MONGODB_PORT'),
                   redis_host=crawler.settings.get("REDIS_HOST"),
                   redis_port=crawler.settings.get("REDIS_PORT"))

    def process_item(self, item, spider):
        # item_id=item["id"]
        item_cat=item["category"]
        item.pop("category")
        collection=self.db[item_cat]
        # find_result=collection.find_one({"id":item_id})
        # if find_result:
        #     collection.update(find_result,item)
        # else:    
        collection.insert_one(item)
        return item

    def close_spider(self, spider):
        self.client.close()
