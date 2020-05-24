from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule

rules = {
    'jd': (
        Rule(LinkExtractor(allow='item\.jd\.com\/.*\.html', restrict_xpaths='//div[@class="p-img"]/a'),
             callback='parse_item',cb_kwargs={}),
    ),
    'tb': (
        Rule(LinkExtractor(allow='item.jd.com\/.*\.html', restrict_xpaths='//div[@class="p-img"]/a'),
             callback='parse_item'),
    ),
    'tm': (
        Rule(LinkExtractor(allow='detail\.tmall\.com\/item\.htm\?.*', restrict_xpaths='//div[@class="img-block"]/a/[@class="sellPoint"]'),
             callback='parse_item'),
    ),
    'sn': (
        Rule(LinkExtractor(allow='product\.suning\.com\/.*\/.*\.html\??.?', restrict_xpaths='//div[@class="img-block"]/a'),
             callback='parse_item'),
    )
}
