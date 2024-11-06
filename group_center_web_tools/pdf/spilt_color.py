# PyMuPDF
import fitz
import tqdm


def check_picture_color(fitz_image) -> bool:
    # Check if the image is grayscale
    channel_count = fitz_image.n
    if channel_count < 3:
        return False

    height, width = fitz_image.height, fitz_image.width
    height, width = (
        int(str(height)),
        int(str(width))
    )

    # Check if the image is color
    for y in range(height):
        for x in range(width):
            if channel_count == 3:
                r, g, b = fitz_image.pixel(x, y)
            else:
                r, g, b, _ = fitz_image.pixel(x, y)

            if r != g or g != b:
                return True

    return False


def check_text_color(page) -> bool:
    text_dict = page.get_text("dict")
    for block in text_dict.get("blocks", []):
        if "lines" in block:
            for line in block["lines"]:
                for span in line.get("spans", []):
                    if "color" in span and span["color"] != 0:
                        r = (span["color"] >> 16) & 0xFF
                        g = (span["color"] >> 8) & 0xFF
                        b = span["color"] & 0xFF
                        if r != g or g != b:
                            return True

    return False


def is_page_color(page, check_text=False) -> bool:
    """Check if a PDF page is color or grayscale"""

    # Check Image
    all_picture = page.get_images(full=True)
    have_picture = len(all_picture) > 0
    if have_picture:
        for image_data in all_picture:
            xref = image_data[0]
            fitz_image = fitz.Pixmap(page.parent.extract_image(xref)["image"])

            if check_picture_color(fitz_image):
                return True

    # Check text color
    if check_text and check_text_color(page):
        return True

    return False


def split_pdf_by_color(input_path, color_output_path, grayscale_output_path):
    """Split a PDF into color and grayscale pages"""
    doc = fitz.open(input_path)
    color_doc = fitz.open()
    grayscale_doc = fitz.open()

    # for page_num in range(len(doc)):
    for page_num in tqdm.tqdm(range(len(doc))):
        page = doc.load_page(page_num)
        is_color = is_page_color(
            page,
            check_text=True
        )
        # print(page_num, is_color)
        if is_color:
            color_doc.insert_pdf(doc, from_page=page_num, to_page=page_num)
        else:
            grayscale_doc.insert_pdf(doc, from_page=page_num, to_page=page_num)

    color_doc.save(color_output_path)
    grayscale_doc.save(grayscale_output_path)


if __name__ == "__main__":
    input_pdf = "input.pdf"
    color_pdf = "color_pages.pdf"
    grayscale_pdf = "grayscale_pages.pdf"

    print("正在分割 PDF...")
    print(f"输入 PDF 路径: {input_pdf}")
    split_pdf_by_color(input_pdf, color_pdf, grayscale_pdf)
    print(f"彩色页面已保存到 {color_pdf}")
    print(f"黑白页面已保存到 {grayscale_pdf}")
