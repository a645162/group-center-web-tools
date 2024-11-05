# fastapi_main.py

from fastapi import FastAPI

from net.api_ip import ip_router

app = FastAPI()

# 注册路由
app.include_router(ip_router, prefix="/net")
