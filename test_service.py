import requests
import json
import time
t=time.time()
r=requests.get("http://127.0.0.1:5555/get_serving?url_or_keyword=%E5%B0%8F%E7%B1%B310&item_num=6").text
t=time.time()-t
print("用时:",t)
print(r)

import scrapyrt.core