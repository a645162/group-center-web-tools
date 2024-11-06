# fastapi_main.py

from fastapi import FastAPI
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

from net.api_ip import ip_router
from pdf.spilt.api_routes import spilt_router

app = FastAPI()

# 注册路由
app.include_router(ip_router, prefix="/api/net")

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
app.include_router(spilt_router, prefix="/api/pdf/split")


@app.get("/")
async def home():
    return templates.TemplateResponse("index.html", {"request": {}})


@app.get("/pdf/spilt")
async def pdf_spilt():
    return templates.TemplateResponse("pdf_spilt.html", {"request": {}})
