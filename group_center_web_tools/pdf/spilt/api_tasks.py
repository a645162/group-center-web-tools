# api/tasks.py

import secrets
from pathlib import Path

from .config import OUTPUT_DIR, get_output_file_name
from fastapi import UploadFile

from group_center_web_tools.pdf.spilt.spilt_color \
    import split_pdf_by_color

# 任务状态存储
task_statuses = {}


def generate_task_id():
    return secrets.token_hex(4)  # 生成一个 8 位的随机字符串


def save_uploaded_file(file: UploadFile, file_path: Path):
    with open(file_path, "wb") as buffer:
        buffer.write(file.file.read())


def split_pdf_by_color_task(input_pdf: Path, task_id: str):
    original_name = input_pdf.name

    color_pdf_name, grayscale_pdf_name = get_output_file_name(original_name)

    if not OUTPUT_DIR.exists():
        OUTPUT_DIR.mkdir(parents=True)

    color_pdf = OUTPUT_DIR / f"{color_pdf_name}"
    grayscale_pdf = OUTPUT_DIR / f"{grayscale_pdf_name}"

    def progress_func(percentage):
        if task_id not in task_statuses:
            task_statuses[task_id] = {"status": "processing"}

        task_statuses[task_id]["progress"] = percentage

    try:
        split_pdf_by_color(
            input_path=input_pdf,
            color_output_path=color_pdf,
            grayscale_output_path=grayscale_pdf,
            progress_func=progress_func
        )
    except Exception as e:
        task_statuses[task_id] = {
            "status": "failed",
            "error": "split_pdf_by_color Error:" + str(e)
        }
        return

    path_color_pdf_str = ""
    path_grayscale_pdf_str = ""

    if color_pdf.exists():
        path_color_pdf_str = color_pdf.resolve()
    if grayscale_pdf.exists():
        path_grayscale_pdf_str = grayscale_pdf.resolve()

    if not path_color_pdf_str and not path_grayscale_pdf_str:
        task_statuses[task_id] = {
            "status": "failed",
            "error": "No output file generated"
        }
        return

    task_statuses[task_id] = {
        "status": "completed",
        "color_pdf": path_color_pdf_str,
        "grayscale_pdf": path_grayscale_pdf_str
    }


def get_task_status(task_id: str):
    return task_statuses.get(task_id)
