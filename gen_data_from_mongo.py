import pymongo
from ShoppingWebsiteCrawlwer.settings import MONGODB_SERVER
import random
client = pymongo.MongoClient(MONGODB_SERVER)
import uuid

def del_dumply():
    for name in ['jd', 'sn']:
        db = client[name + 'Good']
        for c_name in db.list_collection_names():
            collect = db[c_name]
            datas = collect.aggregate([{'$group': {'_id': {'id': '$id', 'date': '$date'},
                                                   'count': {'$sum': 1},
                                                   'dups': {'$addToSet': '$_id'}}}, {
                                           '$match': {'count': {'$gt': 1}}
                                       }])
            for data in datas:
                if data["count"]>1:
                    collect.remove({"_id":{'$in':data['dups']}})
import datetime
def inc_date(date_str,time):
    return datetime.datetime.fromtimestamp(datetime.datetime.strptime(date_str, '%Y-%m-%d').timestamp() + time).strftime('%Y-%m-%d')

def gen_date_price():
    for name in ['jd', 'sn']:
        db = client[name + 'Good']
        for c_name in db.list_collection_names():
            collect = db[c_name]
            item_dates=collect.find()
            for item_data in item_dates:
                item=dict(item_data)
                if "date_price" not  in item_data.keys():
                    continue
                prices=list(item["date_price"].values())[0]
                try:
                    h_price=float(prices[1])
                    l_price=float(prices[0])
                except Exception:
                    print(collect.name)
                    print(item["_id"])
                for i in range(62):
                    date=inc_date('2020-4-1',60*60*24*i)
                    if date in item["date_price"].keys():
                        continue
                    prob=random.random()
                    price_range = int((float(h_price) + float(l_price)) / 2 * 0.05)
                    if prob>24/25:
                        h_price+=price_range
                        l_price+=price_range
                    elif prob<1/25:
                        h_price -= price_range
                        l_price -= price_range
                    item["date_price"][date]=[l_price,h_price]
                collect.update_one({'_id':item["_id"]},{ "$set": item })

def convert_pre_to_now():
    for name in ['jd', 'sn']:
        db = client[name + 'Good']
        for c_name in db.list_collection_names():
            collect = db[c_name]
            item_dates = collect.aggregate([{'$group': {'_id': {'id': '$id'},
                                                   'ids': {'$addToSet': '$_id'},'id':{'$addToSet': '$id'}}}])
            for item_date in item_dates:
                item_info = dict(collect.find_one({"_id": item_date["ids"][0]}))
                item_info.pop("highest_price")
                item_info.pop("lowest_price")
                item_info.pop("date")
                items=collect.find({'id':item_date['id'][0]})
                for item in items:
                    h_price = float(item.pop("highest_price"))
                    l_price=float(item.pop("lowest_price"))
                    date=item.pop("date")
                    item.pop('_id')
                    item_info["_id"]=uuid.uuid4()
                    if "date_price" not in item_info.keys():
                        item_info["date_price"]={}
                    item_info["date_price"][date]=[l_price,h_price]
                    collect.insert_one(item_info)

# convert_pre_to_now()


def del_info():
    for name in ['jd', 'sn']:
        db = client[name + 'Good']
        for c_name in db.list_collection_names():
            collect = db[c_name]
            items = collect.find()
            for item in items:
                if item.get("date") is not None:
                    _id=item.get("_id")
                    collect.delete_one({"_id":_id})

# gen_date_price()

def del_dup_by_id():
    for name in ['jd', 'sn']:
        db = client[name + 'Good']
        for c_name in db.list_collection_names():
            collect = db[c_name]
            datas = collect.aggregate([{'$group': {'_id': {'id': '$id'},
                                                   'count': {'$sum': 1},
                                                   'dups': {'$addToSet': '$_id'}}}, {
                                           '$match': {'count': {'$gt': 1}}
                                       }])
            for data in datas:
                if data["count"] > 1:
                    collect.delete_one({"_id": {'$in': data['dups']}})

def show_data():
    for name in ['jd', 'sn']:
        db = client[name + 'Good']
        for c_name in db.list_collection_names():
            collect = db[c_name]
            for item in collect.find():
                print(item["date_price"])
gen_date_price()