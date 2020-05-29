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


def crawl(settings, spider, name, custom_settings, result=None, url=None, keyword=None, item_num=None):
    process = CrawlerProcess(settings)
    process.crawl(spider, **{'name': name, 'config': custom_settings, 'keyword': keyword,
                             'item_num': item_num, 'url': url, 'result': result})
    process.start()


def spider_process(name, keyword=None, item_num=None, url=None, spider=None, result=None):
    custom_settings = get_config(name)
    if not spider:
        spider = custom_settings.get('spider', 'aCrawler')
    project_settings = get_project_settings()
    settings = dict(project_settings.copy())
    settings.update(custom_settings.get('settings'))
    if item_num is not None:
        assert (item_num>0),"item_num must > 0"
        # 关键字模式下，C_R参数设置同时请求个数
        # 防止终止爬虫时其他请求继续异步进行
        # 但是可能会造成请求较慢
        settings["CONCURRENT_REQUESTS"] = 1
    process = Process(target=crawl, kwargs={'settings': settings, 'spider': spider, 'name': name,
                                            'custom_settings': custom_settings, 'keyword': keyword,
                                            'item_num': item_num, 'url': url, 'result': result})
    return process


def search_with_url_or_keyword(url_or_keyword, item_num=None):
    assert (isinstance(url_or_keyword,str) and url_or_keyword!=""),"illegal input for url_or_keyword"
    manager = Manager()
    return_list = manager.list()
    if item_num is None and  re.match(url_pattern, url_or_keyword):  # url
        url_result = urlparse(url_or_keyword)
        if 'jd.com' in url_or_keyword:
            name = 'jd'
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
        elif 'suning.com' in url_or_keyword:
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
            raise NotImplementedError("This Website has not been implemented.")
        spider = "LCrawler"
        process = spider_process(name=name, url=url, spider=spider, result=return_list)
        process.start()
        process.join()

    else:  # keyword
        for name in ['jd', 'sn']:
            pro = spider_process(name=name, keyword=url_or_keyword, item_num=item_num, result=return_list)
            pro.start()
            pro.join()
    return return_list


if __name__ == "__main__":

    # r1 = search_with_url_or_keyword(url_or_keyword="https://item.taobao.com/item.htm?spm=a217m.12005862.1223185.2.2ddf1296YjHNEB&id=606930801180")
    #
    r1=search_with_url_or_keyword(url_or_keyword="手机",item_num=1)
    # with open("test1.txt", "w", encoding="utf8") as f:
    #     f.write(str(r2))
    print("r1:",len(r1), r1)
