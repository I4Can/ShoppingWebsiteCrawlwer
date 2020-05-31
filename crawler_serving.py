from flask import Flask,jsonify,request
from flask_cors import CORS
from gevent.pywsgi import WSGIServer
from geventwebsocket.handler import WebSocketHandler
from ShoppingWebsiteCrawlwer.crawler_api import search_with_url_or_keyword

app = Flask(__name__)

app.config.update(
    DEBUG=True
)
#跨域问题
CORS(app,supports_credentials=True)

@app.route('/get_serving',methods=["post","get"])
def get_serving():
    keys = request.args.to_dict()
    url_or_keyword=keys.get("url_or_keyword")
    item_num=keys.get("item_num")
    r=search_with_url_or_keyword(url_or_keyword,item_num)
    return jsonify({'data': str(r)})

@app.route('/')
def index():
    return "Hello"

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5555)
    http_server = WSGIServer(('0.0.0.0', 5555), app, handler_class=WebSocketHandler)
    http_server.serve_forever()