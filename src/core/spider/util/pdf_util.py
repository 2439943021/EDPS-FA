import os
import fitz


def convert_pdf_to_image(pdf_path, image_folder_path):
    """
    将pdf转换为img
    @param pdf_path:pdf路径
    @param image_folder_path: 图片文件夹存储路径
    """
    print("imagePath=" + image_folder_path)
    if not os.path.exists(image_folder_path):
        os.makedirs(image_folder_path)
    pdf_doc = fitz.open(pdf_path)
    # metaData = pdfDoc.metadata
    # print("pdf 元数据: ", metaData)
    # toc = pdfDoc.get_toc()

    total = pdf_doc.page_count
    image_path_list = []
    for pg in range(total):
        page = pdf_doc[pg]
        # str = page.get_text()
        # paras = split_paragraphs(str)
        # print(page.get_text())
        zoom = int(1024)  # 值越大，分辨率越高，文件越清晰
        rotate = int(0)

        trans = fitz.Matrix(zoom / 100.0, zoom / 100.0).prerotate(rotate)
        pm = page.get_pixmap(matrix=trans, alpha=False)
        if not os.path.exists(image_folder_path):
            os.mkdir(image_folder_path)
        save = os.path.join(image_folder_path, '%s.png' % (pg + 1))
        image_path_list.append(save)
        # if os.path.exists(save):
        #     os.remove(save)
        pm.save(save)
    pdf_doc.close()
    return image_path_list
