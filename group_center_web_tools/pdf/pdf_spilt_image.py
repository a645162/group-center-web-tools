import fitz  # PyMuPDF


def split_pdf_by_images(input_pdf_path, output_pdf_with_images, output_pdf_without_images):
    # 打开PDF文件
    pdf = fitz.open(input_pdf_path)

    # 创建两个新的PDF文档
    pdf_with_images = fitz.open()
    pdf_without_images = fitz.open()

    # 遍历PDF中的每一页
    for page in pdf:
        # 检查页面是否包含图片
        if len(page.get_images(full=True)) > 0:
            # 如果页面包含图片，则将其添加到带图片的PDF
            pdf_with_images.insert_pdf(pdf, from_page=page.number, to_page=page.number)
        else:
            # 如果页面不包含图片，则将其添加到不带图片的PDF
            pdf_without_images.insert_pdf(pdf, from_page=page.number, to_page=page.number)

    # 保存两个新的PDF文件
    pdf_with_images.save(output_pdf_with_images)
    pdf_without_images.save(output_pdf_without_images)

    # 关闭所有PDF文档
    pdf_with_images.close()
    pdf_without_images.close()
    pdf.close()


split_pdf_by_images(
    'input.pdf',
    'output_with_images.pdf',
    'output_without_images.pdf'
)
