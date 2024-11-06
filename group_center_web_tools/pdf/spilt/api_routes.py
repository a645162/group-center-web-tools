# api/pdf_routes.py

from fastapi import APIRouter, File, UploadFile, Form, BackgroundTasks, HTTPException
from fastapi.responses import FileResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path

from .api_tasks import split_pdf_by_color_task, get_task_status, save_uploaded_file, generate_task_id
from .config import UPLOAD_DIR, OUTPUT_DIR

spilt_router = APIRouter()

# 挂载模板目录
templates = Jinja2Templates(directory="../templates")


@spilt_router.post("/upload")
async def upload_file(file: UploadFile, background_tasks: BackgroundTasks):
    file_name_original = file.filename
    if not file_name_original.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")

    task_id = generate_task_id()
    file_name_new = file_name_original.replace(
        ".pdf", f"_{task_id}.pdf"
    )

    if not UPLOAD_DIR.exists():
        UPLOAD_DIR.mkdir(parents=True)

    file_path = UPLOAD_DIR / f"{file_name_new}"

    save_uploaded_file(file, file_path)

    background_tasks.add_task(split_pdf_by_color_task, file_path, task_id)

    return {"task_id": task_id}


@spilt_router.get("/status/{task_id}")
async def get_status(task_id: str):
    status = get_task_status(task_id)
    if status is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return status


@spilt_router.get("/download/{task_id}/{type}")
async def download_file(task_id: str, type: str):
    if type not in ["color", "grayscale"]:
        raise HTTPException(status_code=400, detail="Invalid file type")

    file_path = OUTPUT_DIR / f"{task_id}_{type}.pdf"
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")

    return FileResponse(file_path, filename=f"{task_id}_{type}.pdf")

# @spilt_router.get("/upload")
# async def upload_form():
#     return templates.TemplateResponse("pdf_spilt.html", {"request": {}})
