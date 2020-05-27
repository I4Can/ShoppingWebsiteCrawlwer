from ..spiders.aCrawler import AcrawlerSpider
from ..utils import get_config
from scrapy import Request

class LinkCrawler(AcrawlerSpider):
    name = 'LCrawler'
    def __init__(self,url,name,config,keyword=None,item_num=None ,*args, **kwargs):
        self.url=url
        self.config = config
        self.price_url = self.config.get("price_url")
        self.price_url2 = self.config.get("price_url2")
        self.price_url3 = self.config.get("price_url3")
        self.price_url4 = self.config.get("price_url4")
        self.coupons_url = self.config.get("coupons_url")
        super(LinkCrawler, self).__init__(name, config,*args,**kwargs)

    def parse(self, response):
        return Request(self.url,self.parse_item)