import datetime

from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, Join, Compose


class GoodLoader(ItemLoader):
    default_output_processor = TakeFirst()
    date_out = Compose(lambda x:str(datetime.date.today()))


class JDLoader(GoodLoader):
    type_out=Compose(Join(),lambda x:x.split("：")[1].strip())
    name_out=Compose(Join(),lambda x:x.replace('\n',"").strip())
    sum_cat_out=Compose(Join(),lambda x:x.split("=")[1])

class SNLoader(GoodLoader):
    # id_out=Compose(Join(),lambda x:urlparse(x).path,lambda x:x.split("/")[1])
    name_out = Compose(Join(), lambda x: x.replace('\n', "").strip())
