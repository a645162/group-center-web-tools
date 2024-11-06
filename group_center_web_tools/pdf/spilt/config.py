from pathlib import Path

# 存储上传文件的目录
UPLOAD_DIR = Path("data/upload/pdf")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

# 存储处理后文件的目录
OUTPUT_DIR = Path("data/output/pdf")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
