# main.py

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
