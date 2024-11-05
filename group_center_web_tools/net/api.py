# app.py
from flask import Flask, request

app = Flask(__name__)


@app.route('/get-ip', methods=['GET'])
def get_ip():
    # 获取客户端IP地址
    if request.headers.getlist("X-Forwarded-For"):
        # 如果存在代理，则使用代理的IP
        ip = request.headers.getlist("X-Forwarded-For")[0]
    else:
        # 否则直接使用请求的IP
        ip = request.remote_addr
    return {'client_ip': ip}


@app.route('/ip_addr', methods=['GET'])
def ip_addr():
    return request.remote_addr


@app.route('/', methods=['GET'])
def index():
    return request.remote_addr
