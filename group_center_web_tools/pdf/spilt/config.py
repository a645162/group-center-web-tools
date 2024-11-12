from pathlib import Path

# 存储上传文件的目录
UPLOAD_DIR = Path("data/upload/pdf")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

# 存储处理后文件的目录
OUTPUT_DIR = Path("data/output/pdf")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def get_output_file_name(original_name: Path | str, type: str = ""):
    type = type.lower().strip()

    if type == "":
        if isinstance(original_name, Path):
            original_name = original_name.name

        color_pdf_name = original_name.replace(
            ".pdf", "_color.pdf"
        )
        grayscale_pdf_name = original_name.replace(
            ".pdf", "_grayscale.pdf"
        )

        return color_pdf_name, grayscale_pdf_name
    else:
        if type not in ["color", "grayscale"]:
            raise ValueError("Invalid file type")
        else:
            if type == "color":
                new_name = original_name.replace(
                    ".pdf", "_color.pdf"
                )
            else:
                new_name = original_name.replace(
                    ".pdf", "_grayscale.pdf"
                )
            return new_name
