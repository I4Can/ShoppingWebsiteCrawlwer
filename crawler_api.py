# -*- coding: utf-8 -*-
import sys
import re
from scrapy.utils.project import get_project_settings
import requests
import re
from lxml import etree
try:
    from .ShoppingWebsiteCrawlwer.utils import get_config
except ImportError:
    from ShoppingWebsiteCrawlwer.utils import get_config
from scrapy.crawler import CrawlerProcess
from multiprocessing.context import Process
from multiprocessing import Manager
from urllib.parse import urlparse
import os
from collections import defaultdict
from ShoppingWebsiteCrawlwer.settings import MONGODB_SERVER,MONGODB_PORT
import pymongo
item_num = 2
url_pattern = "http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"
jd_url = "https://item.jd.com/{}.html"
sn_url = "https://product.suning.com/{}/{}.html"
jd_cat_xpath="//div[@class='crumb fl clearfix']/div[5]/a/text()"
sn_cat_xpath="//div[@class='breadcrumb']/div[@class='dropdown'][2]/span[@class='dropdown-text']/a/text()"
sku_id=None
client = pymongo.MongoClient(MONGODB_SERVER)
headers={"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36 Edg/83.0.478.37"}

def crawl(settings, spider, name=None, custom_settings=None, result=None, url=None, keyword=None, item_num=None):
    process = CrawlerProcess(settings)
    process.crawl(spider, **{'name': name, 'config': custom_settings, 'keyword': keyword,
                             'item_num': item_num, 'url': url, 'result': result})
    process.start()


def spider_process(name, keyword=None, item_num=None, url=None, spider=None, result=None):
    project_settings = get_project_settings()
    settings = dict(project_settings.copy())
    custom_settings=None
    if name!='tb':
        custom_settings = get_config(name)
        custom_settings["start_urls"][0]["args"][1]=1
        if not spider:
            spider = custom_settings.get('spider', 'aCrawler')
        settings.update(custom_settings.get('settings'))
    else:
        spider='taobao'
    if item_num is not None:
        item_num = int(item_num)
        assert (item_num>0),"item_num must > 0"
        # 关键字模式下，C_R参数设置同时请求个数
        # 防止终止爬虫时其他请求继续异步进行
        # 但是可能会造成请求较慢
        # settings["CONCURRENT_REQUESTS"] = 1
    process = Process(target=crawl, kwargs={'settings': settings, 'spider': spider, 'name': name,
                                            'custom_settings': custom_settings, 'keyword': keyword,
                                            'item_num': item_num, 'url': url, 'result': result})
    return process


def search_with_url_or_keyword(url_or_keyword, item_num=None):
    assert (isinstance(url_or_keyword,str) and url_or_keyword!=""),"illegal input for url_or_keyword"
    manager = Manager()
    return_list = manager.list()
    if  re.match(url_pattern, url_or_keyword):  # url
        url_result = urlparse(url_or_keyword)
        if 'jd.com' in url_or_keyword:
            name = 'jd'
            xp = jd_cat_xpath
            url = url_or_keyword
            if "item.m.jd.com" in url_or_keyword:
                sku_id = url_result.path.split("/")[2].split(".")[0]
                try:
                    int(sku_id)
                except ValueError:
                    try:
                        sku_id=re.search(".*?wareId=(.*?)&.*",url).group(1)
                    except AttributeError:
                        raise ValueError("Unexpected value for url_or_keyword")
                url = jd_url.format(sku_id)
            else:
                sku_id=url.split("/")[3].split(".")[0]

        elif 'suning.com' in url_or_keyword:
            xp = sn_cat_xpath
            name = 'sn'
            url = url_or_keyword
            if "m.suning.com" in url_or_keyword:

                sup_id = url_result.path.split("/")[2]
                sku_id = url_result.path.split("/")[3].split(".")[0]
                try:
                    int(sku_id)
                    int(sup_id)
                except ValueError:
                    raise ValueError("Unexpected value for args")
                url = sn_url.format(sup_id, sku_id)
            else:
                sku_id=url.split("/")[4].split(".")[0]

        else:
            raise NotImplementedError("This Website has not been implemented.")

        db=client[name+"Good"]
        text=requests.get(url,headers=headers).text
        page=etree.HTML(text)
        cat=page.xpath(xp)[0]
        r=[dict(db[cat].find_one({"id":{'$regex':'.*'+sku_id+'.*'}}))]
        for i in r:
            i.pop("_id")
        return r

    else:  # keyword
        if item_num is None:
            raise RuntimeError("must specify a value for item_num")
        # for name in ['jd', 'sn']:
        pro1 = spider_process(name='jd', keyword=url_or_keyword, item_num=item_num, result=return_list)
        pro2 = spider_process(name='sn', keyword=url_or_keyword, item_num=item_num, result=return_list)
        # pro3 = spider_process(name='tb', keyword=url_or_keyword, item_num=item_num, result=return_list)
        pro1.start()
        pro2.start()
        # pro3.start()
        pro1.join()
        pro2.join()
        # pro3.join()
    return return_list


if __name__ == "__main__":
    import time
    t = time.time()
    # r1 = search_with_url_or_keyword(url_or_keyword="https://item.taobao.com/item.htm?spm=a217m.12005862.1223185.2.2ddf1296YjHNEB&id=606930801180")

    # r1=search_with_url_or_keyword(url_or_keyword="https://item.jd.com/100005182618.html")
    # print(r1)
    r1=search_with_url_or_keyword(url_or_keyword="手机",item_num=4)
    print(r1)
    print(time.time() - t)
