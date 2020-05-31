import requests
import json
import time
t=time.time()
r=requests.get("http://127.0.0.1:5555/get_serving?url_or_keyword=https://item.jd.com/100005182618.html").text
print("用时",time.time()-t)
print(r)
r2=requests.get("http://127.0.0.1:5555/get_serving?url_or_keyword=手机&item_num=6").text
print("用时",time.time()-t)
print(r2)
