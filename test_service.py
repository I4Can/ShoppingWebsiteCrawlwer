import requests
import json
import time
import json
t=time.time()
r2=requests.get("http://127.0.0.1:5555/get_serving?url_or_keyword=https://product.suning.com/0070074453/10790216232.html").text
print("用时",time.time()-t)
r2=requests.get("http://127.0.0.1:5555/get_serving?url_or_keyword=手机&item_num=8").text
r2=json.loads(requests.get("http://127.0.0.1:5555/30_days_recomment").text)
with open("test.json","w",encoding="utf8") as f:
    f.write(r2)
print(r2)
print("用时",time.time()-t)
