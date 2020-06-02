import datetime
import random
import copy


def inc_date(date_str,time):
    return datetime.datetime.fromtimestamp(datetime.datetime.strptime('2020-05-27', '%Y-%m-%d').timestamp() + time).strftime('%Y-%m-%d')

with open("test1.txt","r") as f:
    item_list=[]
    for item in eval(f.read()):
        item_history = [item]
        cp=copy.deepcopy(item)
        _date=item.get("date")
        h_price=item.get("highest_price")
        l_price = item.get("lowest_price")
        for i in range(4):
            _date=inc_date(_date,60*60*24*(i+1))
            r_p=random.randint(-200,200)
            cp["highest_price"]=h_price+r_p
            cp["lowest_price"] = l_price + r_p
            cp["date"]=_date
            item_history.append(copy.deepcopy(cp))
        item_list+=item_history
    with open("test2.txt","w") as f:
        f.write(str(item_list))
