import fitz
from PIL import Image
from io import BytesIO


def convert_pdf_to_images(pdf_bytes, quality=50):
    """
    Конвертирует страницы PDF в список байтов изображений с пониженным качеством (JPEG).
    :param pdf_bytes: Байтовые данные PDF-файла.
    :param quality: Уровень качества JPEG (0–100).
    """
    pdf_document = fitz.open(stream=BytesIO(pdf_bytes))
    images = []
    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)
        pixmap = page.get_pixmap()
        img = Image.frombytes("RGB", [pixmap.width, pixmap.height], pixmap.samples)
        
        # Создаем JPEG с заданным уровнем качества
        image_buffer = BytesIO()
        img.save(image_buffer, format='JPEG', quality=quality, optimize=True)
        images.append(image_buffer.getvalue())
    return images