import datetime

from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, Join, Compose
import uuid

class GoodLoader(ItemLoader):
    default_output_processor = TakeFirst()
    date_out = Compose(lambda x:str(datetime.date.today()))


class JDLoader(GoodLoader):
    _id_out=Compose(lambda x:str(uuid.uuid4()))
    type_out=Compose(Join(),lambda x:x.split("：")[1].strip())
    name_out=Compose(Join(),lambda x:x.replace('\n',"").strip())
    sum_cat_out=Compose(Join(),lambda x:x.split("=")[1])

class SNLoader(GoodLoader):
    _id_out=Compose(lambda x:str(uuid.uuid4()))
    # id_out=Compose(Join(),lambda x:urlparse(x).path,lambda x:x.split("/")[1])
    name_out = Compose(Join(), lambda x: x.replace('\n', "").strip())
