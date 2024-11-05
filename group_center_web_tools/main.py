# main.py
from group_center_web_tools.net.api import app

if __name__ == '__main__':
    # 运行Flask应用
    app.run(host='::', port=15001)
