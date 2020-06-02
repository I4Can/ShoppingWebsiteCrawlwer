import pymongo
from ShoppingWebsiteCrawlwer.settings import MONGODB_SERVER
import datetime

import datetime
import time
date=datetime.date.today()
date_stamp=time.mktime(date.timetuple())-24*60*60
thirty_ago_stamp=date_stamp-30*24*60*60
thirty_ago_date=str(datetime.date.fromtimestamp(thirty_ago_stamp))
client = pymongo.MongoClient(MONGODB_SERVER)

for name in ['jd', 'sn']:
    db = client[name + 'Good']
    recomm_ist=[]
    if db["30_days"]:
        db.drop_collection("30_days")
    for c_name in db.list_collection_names():
        collect = db[c_name]
        items=collect.find()
        for item in items:
            try:
                current_price=float(item["date_price"][str(date)][0])+float(item["date_price"][str(date)][1])
                thirty_ago=float(item["date_price"][thirty_ago_date][0])+float(item["date_price"][str(date)][1])
            except Exception:
                print(item["_id"])
                continue
            if current_price>=thirty_ago:
                continue
            recomm_ist.append({"id":item["_id"],"rank":(thirty_ago-current_price)/thirty_ago,"collect":collect.name})
    recomm_ist.sort(key=lambda x:x["rank"])
    for item in recomm_ist[:50]:
        _id=item["id"]
        collect=db[item["collect"]]
        detail_item=collect.find_one({"_id":_id})
        detail_item["rank"]=item["rank"]
        detail_item.pop("_id")
        recomm_db=db["30_days"]
        recomm_db.insert_one(detail_item)
