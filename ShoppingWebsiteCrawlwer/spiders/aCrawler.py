# -*- coding: utf-8 -*-
import re
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..items import *
from ..loaders import *
from ..utils import get_config
from .. import urls
from ..rules import rules
import json
import os
import random
import requests
from bson import binary
from scrapy.crawler import Crawler
from urllib.parse import urlparse
from ..utils import get_config


class AcrawlerSpider(CrawlSpider):
    name = 'aCrawler'

    def __init__(self, name=None, config=None, keyword=None, item_num=None, result=None, config_file=None, *args,
                 **kwargs):
        self.web_name = name
        if config_file is not None:
            self.config = get_config(config_file)
        else:
            self.config = config
        self.item_num = item_num
        self.current_num = 0
        self.items = result
        self.rules = rules.get(config.get('rules'))
        self.price_url = self.config.get("price_url")
        self.price_url2 = self.config.get("price_url2")
        self.price_url3 = self.config.get("price_url3")
        self.price_url4 = self.config.get("price_url4")
        self.price_url5 = self.config.get("price_url5")
        self.coupons_url = self.config.get("coupons_url")
        start_urls = config.get('start_urls')
        if keyword is not None:
            keywords = [keyword]
        else:
            keywords = self.config.get('keywords')
        self.start_urls = []
        if start_urls:
            for k in keywords:
                self.keyword = k
                for start_url in start_urls:
                    if start_url.get('type') == 'static':
                        self.start_urls += start_url.get('value')
                    elif start_url.get('type') == 'dynamic':
                        self.start_urls += list(
                            eval('urls.' + start_url.get('method'))(*start_url.get('args', []), keyword=k))

        self.allowed_domains = config.get('allowed_domains')
        super(AcrawlerSpider, self).__init__(*args, **kwargs)  # 得到父类--CrawlSpider的__init__()结果

    def parse_jd_skus(self, response):

        text = response.text
        try:
            color_size = eval(re.search("colorSize: (\[.*?]),", text).group(1))
        except AttributeError:  # 找不懂colorSize，即没有不同型号
            return [response.url.split("/")[3].split(".")[0]]

        return [str(sku["skuId"]) for sku in color_size]

    def parse_jd_price(self, sku_id):
        """获取商品价格
        """
        # import json
        # import random
        # import requests
        try:
            price = json.loads(requests.get(self.price_url3.format(sku_id)).text)
            return price[0].get("p")
        except KeyError as err:
            if price['error'] == 'pdos_captcha':
                print("触发验证码")
            print("Price parse error, parse is {}".format(price))
        except json.decoder.JSONDecodeError as err:
            print('prase price failed, try backup price url')
            price = json.loads(requests.get(self.price_url2.format(random.randint(1, 100000000), sku_id)).text)
            return price[0].get("p")

    def parse_item(self, response):
        item = self.config.get('item')
        if item:
            cls = eval(item.get('class'))()
            loader = eval(item.get('loader'))(cls, response=response)
            # 动态获取属性配置
            for key, value in item.get('attrs').items():
                for extractor in value:
                    if extractor.get('method') == 'xpath':
                        loader.add_xpath(key, *extractor.get('args'), **{'re': extractor.get('re')})
                    if extractor.get('method') == 'css':
                        loader.add_css(key, *extractor.get('args'), **{'re': extractor.get('re')})
                    if extractor.get('method') == 'value':
                        loader.add_value(key, *extractor.get('args'), **{'re': extractor.get('re')})
                    if extractor.get('method') == 'attr':
                        loader.add_value(key, getattr(response, *extractor.get('args')))
                    if extractor.get('method') == 'func':
                        loader.add_value(key, "")
                        if key == "id" and self.web_name == "jd":
                            loader.add_value(key, ";".join(self.parse_jd_skus(response)))
                        if key == "coupons" and self.web_name == 'jd':
                            coupons = self.jd_get_coupons(response)
                            loader.add_value(key, coupons)
                        elif self.web_name == "sn" and key == "coupons":
                            coupons = self.sn_get_couponse(response)
                            loader.add_value(key, coupons)
                        if key == "sale_volume" and self.web_name == "jd":
                            pass
                        elif self.web_name == "sn" and key == "sale_volume":
                            continue
                            coupons = self.sn_get_couponse(response)
                            loader.add_value(key, coupons)
            if self.web_name == "jd":
                highest_price, lowest_price = self.get_low_or_highest_price(response)
            elif self.web_name == "sn":
                highest_price, lowest_price, ids = self.sn_get_low_or_highest_price(response)
                loader.add_value("id", ids)
            loader.add_value("highest_price", highest_price)
            loader.add_value("lowest_price", lowest_price)
            yield loader.load_item()

    def get_sale_volume(self, response):

        if self.web_name == "jd":
            sku_id = response.url.split("/")[3].split(".")[0]
            return json.loads(requests.get(
                "https://club.jd.com/comment/productCommentSummaries.action?referenceIds=" + sku_id).text())[0].get("CommentCount")

        else:
            sku_id = urlparse(response.url).path.split("/")[2].split(".")[0]
            pass

    def sn_get_couponse(self, response):
        coupons = []
        cat = urlparse(response.url).path.split("/")[1]
        sku_id = urlparse(response.url).path.split("/")[2].split(".")[0]
        try:
            coupons_page = json.loads(requests.get(self.coupons_url.format(cat=cat, sku_id=sku_id),
                                                   headers={
                                                       "USER_AGENT": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36"}).text[
                                      17:-2])
        except Exception as e:
            # print(requests.get(self.coupons_url.format(cat=cat, sku_id=sku_id)).text)
            raise e
        for promotion in coupons_page["promotions"]:
            if promotion["activityType"] == "7":
                quota = promotion["activityDesc"].split("用")[1]
                discount = promotion["activityDesc"].split("用")[0][1:]
                coupons.append({"quota": quota, "discount": discount})
        return coupons

    def jd_get_coupons(self, response):
        vender_id = re.search("venderId:(.*?),", response.text).group(1)
        shop_id = re.search("shopId:(.*?),", response.text).group(1)
        cat = ",".join(str(i) for i in eval(re.search("cat:(.*?\]),", response.text).group(1)))
        sku_id = response.url.split("/")[3].split(".")[0]
        coupons_page = json.loads(requests.get(
            self.coupons_url.format(shopId=shop_id, venderId=vender_id, cat=cat,
                                    sku_id=sku_id)).text)
        # print(self.coupons_url.format(shopId=shop_id, venderId=vender_id, cat=cat,
        #                             sku_id=sku_id))
        coupons = []
        for coupon in coupons_page["skuCoupon"]:
            discount = str(coupon["discount"])
            quota = str(coupon["quota"])
            url = str(coupon["url"])
            coupons.append({"quota": quota, "discount": discount, "url": url})
        try:
            for item in coupons_page['prom']['pickOneTag']:
                coupons.append(item['content'])
        except KeyError:
            pass
        except Exception as  e:
            raise e
        return coupons

    def sn_get_low_or_highest_price(self, response):
        sku_ids = ["0000000" + response.url.split("/")[4].split(".")[0]]
        try:
            clusterMap = eval(re.search('"clusterMap":(.*"itemCuPartNumber".*?].*?])', response.text).group(1))
            for map in clusterMap:
                for part_number in map["itemCuPartNumber"]:
                    sku_ids.append(part_number["partNumber"])
        except AttributeError:
            try:
                colorList = eval(re.search('"colorList":(.*?\])', response.text).group(1))
                for i in colorList:
                    if i["partNumber"] in sku_ids:
                        continue
                    sku_ids.append(i["partNumber"])
            except AttributeError:
                pass
        ids = ",".join(sid[7:] for sid in sku_ids)
        sup_id = urlparse(response.url).path.split("/")[1]
        if len(sku_ids) > 1:
            prices = []
            for i in range(len(sku_ids) // 20 + 1):
                if i * 20 + 20 < len(sku_ids):
                    end = i * 20 + 20
                else:
                    end = len(sku_ids)
                ids1 = ",".join(sku_id for sku_id in sku_ids[i * 20:end])
                ids2 = ",".join([str(sup_id)] * (end - i * 20))
                url = self.price_url.format(ids1, ids2)

                price_page = eval(requests.get(url).text.replace("null", "\"null\"")[16:-2])
                for item_info in price_page:
                    if item_info["price"] == "null" or item_info["price"] == "":
                        continue
                    prices.append(item_info["snPrice"])
            if len(prices) > 0:
                return max(float(price) for price in prices), min(float(price) for price in prices), ids
            else:
                sku_id = sku_ids[0][7:]
                url = self.price_url4.format(sku_id, sku_id, sup_id)
                data = re.search("pcData\((.*)\)", requests.get(url).text).group(1)
                price = eval(data)["data"]["price"]["saleInfo"][0]["promotionPrice"]
                return price, price, ids
        else:
            sku_id = sku_ids[0][7:]
            if len(set(sup_id)) == 1:
                url = self.price_url2.format(sku_id, sku_id, sup_id)
            else:
                url = self.price_url3.format(sku_id, sku_id, sup_id)
            try:
                data = re.search("pcData\((.*)\)", requests.get(url).text).group(1)
            except AttributeError:
                try:
                    url = self.price_url3.format(sku_id, sku_id, sup_id)
                    data = re.search("pcData\((.*)\)", requests.get(url).text).group(1)
                except AttributeError:
                    url = self.price_url5.format(sku_id, sup_id)
                    # print(url)
                    # import time;time.sleep(2)
                    data = re.search("pcData\((.*)\)", requests.get(url).text).group(1)
            price = eval(data)["data"]["price"]["saleInfo"][0]["promotionPrice"]
            if price:
                hprice = lprice = price
                if "-" in price:
                    lprice, hprice = price.split("-")
                return hprice, lprice, ids
            else:
                url = self.price_url4.format(sku_id, sku_id, sup_id)
                try:
                    data = re.search("pcData\((.*)\)", requests.get(url).text).group(1)
                except Exception as e:
                    pass
                    # print(response.url)
                    # print(url)
                    # print(e)
                    # print(requests.get(url).text)
                    # os._exit(2)
                price = eval(data)["data"]["price"]["saleInfo"][0]["promotionPrice"]
                hprice = lprice = price
                if "-" in price:
                    lprice, hprice = price.split("-")
                return hprice, lprice, ids

    def get_low_or_highest_price(self, response):
        sku_ids = ["J_" + sku for sku in self.parse_jd_skus(response)]
        skus = ",".join(sku_ids)
        price_page = re.search("jQuery1683353\((.*)\)", requests.get(self.price_url3.format(skus)).text).group(1)
        prices = [info["p"] for info in eval(price_page)]
        # prices = [float(self.parse_jd_price(sku_id)) for sku_id in self.parse_jd_skus(response)]
        return max(float(price) for price in prices), min(float(price) for price in prices)
