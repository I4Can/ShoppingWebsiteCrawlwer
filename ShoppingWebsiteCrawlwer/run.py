import sys
try:
    from utils  import get_config
except ModuleNotFoundError:
    from .utils import get_config
from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerProcess
from multiprocessing.context import Process
import time

# from flask import Flask
# app = Flask(__name__)

def crawl(settings, spider, name, custom_settings):
    process = CrawlerProcess(settings)  # 启动爬虫
    process.crawl(spider, **{'name': name, 'config': custom_settings})
    process.start()

def start_spider(name):
    custom_settings = get_config(name)  # 爬取使用的 Spider 名称
    spider = custom_settings.get('spider', 'aCrawler')
    project_settings = get_project_settings()
    settings = dict(project_settings.copy())  # 合并配置
    settings.update(custom_settings.get('settings'))
    process = Process(target=crawl, kwargs={'settings': settings, 'spider': spider, 'name': name,
                                            'custom_settings': custom_settings})
    return process

# @app.route('/')
def run():
    # while True:
        pro1=start_spider('jd')
        pro2=start_spider('sn')
        pro1.start()
        pro2.start()
        pro1.join()
        pro2.join()
        # time.sleep(60 * 60 * 24)    #一天运行一次

if __name__=='__main__':
    # app.run("127.0.0.1",8000,debug = True)
    run()
