# -*- coding: utf-8 -*-
import sys
import re
from scrapy.utils.project import get_project_settings
from utils import get_config
from scrapy.crawler import CrawlerProcess
from multiprocessing.context import Process
from multiprocessing import Manager
from urllib.parse import urlparse
import os

item_num = 2
url_pattern = "http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"
jd_url = "https://item.jd.com/{}.html"
sn_url = "https://product.suning.com/{}/{}.html"


def crawl(settings, spider, name, custom_settings,result=None, url=None, keyword=None, item_num=None):
    process = CrawlerProcess(settings)
    process.crawl(spider, **{'name': name, 'config': custom_settings, 'keyword': keyword,
                             'item_num': item_num, 'url': url,'result':result})
    process.start()


def spider_process(name, keyword=None, item_num=None, url=None, spider=None,result=None):
    custom_settings = get_config(name)
    if not spider:
        spider = custom_settings.get('spider', 'aCrawler')
    project_settings = get_project_settings()
    settings = dict(project_settings.copy())
    settings.update(custom_settings.get('settings'))
    print(item_num)
    if item_num is not None:
        # 关键字模式下，C_R参数设置同时请求个数
        # 防止终止爬虫时其他请求继续异步进行
        # 但是可能会造成请求较慢
        settings["CONCURRENT_REQUESTS"]=1
    print(settings)
    process = Process(target=crawl, kwargs={'settings': settings, 'spider': spider, 'name': name,
                                            'custom_settings': custom_settings, 'keyword': keyword,
                                            'item_num': item_num, 'url': url,'result':result})
    return process


def search_with_url_or_keyword(url_or_keyword,item_num=None):
    manager = Manager()
    return_list = manager.list()
    if re.match(url_pattern, url_or_keyword):  # url
        url_result = urlparse(url_or_keyword)
        if 'jd.com' in url_or_keyword:
            name = 'jd'
            url = url_or_keyword
            if "item.m.jd.com" in url_or_keyword:
                sku_id = url_result.path.split("/")[2].split(".")[0]
                url = jd_url.format(sku_id)
        elif 'product.suning.com' in url_result:
            name = 'sn'
            url = url_or_keyword
            if "m.suning.com" in url_or_keyword:
                sup_id = url_result.path.split("/")[2]
                sku_id = url_result.path.split("/")[3].split(".")[0]
                url = sn_url.format(sup_id, sku_id)
        spider = "LCrawler"
        process = spider_process(name=name, url=url,spider=spider,result=return_list)
        process.start()
        process.join()

    else:  # keyword
        for name in ['jd', 'sn']:
            pro = spider_process(name=name, keyword=url_or_keyword, item_num=item_num,result=return_list)
            pro.start()
            pro.join()
    return return_list

if __name__ == "__main__":
    r1=search_with_url_or_keyword(url_or_keyword="https://product.suning.com/0070142956/11765498415.html")
    r2=search_with_url_or_keyword(url_or_keyword="手机",item_num=3)
    print("r1:",r1)
    print("r2:",r2)









