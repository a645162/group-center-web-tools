import fitz  # PyMuPDF


def is_page_color(page):
    """检查页面是否包含彩色内容"""
    # 检查图像
    for image in page.get_images(full=True):
        xref = image[0]
        base_image = fitz.Pixmap(page.parent.extract_image(xref)["image"])

        # 检查图像是否为灰度图像
        if base_image.n < 3:
            continue

        # 检查图像是否有彩色像素
        for y in range(base_image.height):
            for x in range(base_image.width):
                r, g, b = base_image.pixel(x, y)
                if r != g or g != b:
                    return True

    # 检查文本
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


def split_pdf_by_color(input_path, color_output_path, grayscale_output_path):
    """将 PDF 分割为彩色和黑白页面"""
    doc = fitz.open(input_path)
    color_doc = fitz.open()
    grayscale_doc = fitz.open()

    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        if is_page_color(page):
            color_doc.insert_pdf(doc, from_page=page_num, to_page=page_num)
        else:
            grayscale_doc.insert_pdf(doc, from_page=page_num, to_page=page_num)

    color_doc.save(color_output_path)
    grayscale_doc.save(grayscale_output_path)


if __name__ == "__main__":
    input_pdf = "input.pdf"
    color_pdf = "color_pages.pdf"
    grayscale_pdf = "grayscale_pages.pdf"

    split_pdf_by_color(input_pdf, color_pdf, grayscale_pdf)
    print(f"彩色页面已保存到 {color_pdf}")
    print(f"黑白页面已保存到 {grayscale_pdf}")
