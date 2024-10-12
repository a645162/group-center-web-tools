# main.py
from api import app

if __name__ == '__main__':
    # 运行Flask应用
    app.run(host='::', port=15001)
