from flask import Flask,jsonify,request
from flask_cors import CORS
from gevent.pywsgi import WSGIServer
from geventwebsocket.handler import WebSocketHandler
from crawler_api import search_with_url_or_keyword
import pymongo
from ShoppingWebsiteCrawlwer.settings import MONGODB_SERVER,MONGODB_PORT

client = pymongo.MongoClient(MONGODB_SERVER)
app = Flask(__name__)

app.config.update(
    DEBUG=True
)
#跨域问题
CORS(app,supports_credentials=True)
import json
@app.route('/get_serving',methods=["post","get"])
def get_serving():
    keys = request.args.to_dict()
    url_or_keyword=keys.get("url_or_keyword")
    item_num=keys.get("item_num",None)
    r=[dict(i) for i in search_with_url_or_keyword(url_or_keyword,item_num)]
    for i in r:
        i.pop("id")
    return jsonify(r)

@app.route('/30_days_recomment')
def thirty_recomm():
    result=[]
    for name in ['jd','sn']:
        db=client[name+"Good"]
        data=db["30_days"].find()
        result.extend(data)
    result=sorted([dict(i) for i in result], key=lambda x:x["rank"],reverse=True)[:50]
    for i in result:
        i.pop("id")
        i.pop("_id")
    return jsonify(result)



@app.route('/')
def index():
    return "Hello"

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5555)
    http_server = WSGIServer(('0.0.0.0', 5555), app, handler_class=WebSocketHandler)
    http_server.serve_forever()