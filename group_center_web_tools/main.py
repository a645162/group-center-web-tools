# main.py
import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

import uvicorn
from fastapi_main import app

if __name__ == "__main__":
    host = "0.0.0.0"
    port = 15000
    reload = True

    if reload:
        uvicorn.run("fastapi_main:app", host=host, port=port, reload=True)
    else:
        uvicorn.run(app, host=host, port=port, reload=False)
