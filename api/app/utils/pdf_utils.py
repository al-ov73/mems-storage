import zipfile
from io import BytesIO

import fitz
from fastapi import HTTPException, Request
from PIL import Image
from PyPDF2 import PdfMerger, PdfReader, PdfWriter


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

        image_buffer = BytesIO()
        img.save(image_buffer, format="JPEG", quality=quality, optimize=True)
        images.append(image_buffer.getvalue())
    return images


def split_pdf(file_content: bytes, pages: str) -> BytesIO:
    page_ranges = []
    for part in pages.split(","):
        if "-" in part:
            start, end = map(int, part.split("-"))
            page_ranges.extend(range(start - 1, end))
        else:
            page_ranges.append(int(part) - 1)

    pdf_reader = PdfReader(BytesIO(file_content))
    pdf_writer = PdfWriter()

    for page_num in page_ranges:
        if 0 <= page_num < len(pdf_reader.pages):
            pdf_writer.add_page(pdf_reader.pages[page_num])
        else:
            raise HTTPException(status_code=400, detail=f"Список страниц некорректен ({page_num+1}).")

    output_stream = BytesIO()
    pdf_writer.write(output_stream)
    output_stream.seek(0)
    return output_stream


def merge_pdfs(filenames: list[str], session_files: dict) -> BytesIO:
    requested_files = {}
    for filename in filenames:
        found = next((f for f in session_files if f["filename"] == filename), None)
        if found:
            requested_files[filename] = found["file_content"]
        else:
            raise HTTPException(status_code=404, detail=f"Файл '{filename}' не найден!")

    merger = PdfMerger()
    for filename, file_content in requested_files.items():
        reader = PdfReader(BytesIO(file_content))
        merger.append(reader)

    # Генерируем выходной поток байтов
    merged_bytes = BytesIO()
    merger.write(merged_bytes)
    merged_bytes.seek(0)
    return merged_bytes


def get_files_from_session(request: Request, filenames: list) -> dict[str, bytes]:
    """
    Получает файлы из сессии по указанным именам.
    """
    session_files = request.state.session.get("files", [])
    requested_files = {}
    for filename in filenames:
        found = next((f for f in session_files if f["filename"] == filename), None)
        if found:
            requested_files[filename] = found["file_content"]
        else:
            raise HTTPException(status_code=404, detail=f"Файл '{filename}' не найден!")
    return requested_files


def convert_pdf_to_jpeg(file_content: bytes, dpi: int = 300) -> list[Image.Image]:
    """
    Конвертирует PDF-файл в список изображений JPEG.
    """
    doc = fitz.open(stream=file_content)
    images = []
    for page_num in range(doc.page_count):
        page = doc.load_page(page_num)
        pixmap = page.get_pixmap(dpi=dpi)
        img = Image.frombytes("RGB", [pixmap.width, pixmap.height], pixmap.samples)
        images.append(img)
    return images


def pack_images_into_zip(images: list[Image.Image], prefix: str) -> BytesIO:
    """
    Пакует изображения в ZIP-архив с префиксом для имен файлов.
    """
    buffer = BytesIO()
    with zipfile.ZipFile(buffer, mode="w") as zf:
        for idx, img in enumerate(images):
            img_byte_arr = BytesIO()
            img.save(img_byte_arr, format="JPEG")
            zf.writestr(f"{prefix}_{idx}.jpg", img_byte_arr.getvalue())
    buffer.seek(0)
    return buffer


def convert_and_pack(filename: str, file_content: bytes, dpi: int = 300) -> BytesIO:
    """
    Конвертирует PDF-файл в JPEG и упаковывает в ZIP-архив.
    """
    doc = fitz.open(stream=file_content)
    images = []
    for page_num in range(doc.page_count):
        page = doc.load_page(page_num)
        pixmap = page.get_pixmap(dpi=dpi)
        img = Image.frombytes("RGB", [pixmap.width, pixmap.height], pixmap.samples)
        images.append(img)
    return pack_images_into_zip(images, filename.split(".")[0])


def combine_archives(individual_archives: list[BytesIO]) -> BytesIO:
    """
    Объединяет отдельные ZIP-архивы в один общий архив.
    """
    buffer = BytesIO()
    with zipfile.ZipFile(buffer, mode="w") as zf:
        for idx, archive in enumerate(individual_archives):
            zf.writestr(f"archive_{idx}.zip", archive.getvalue())
    buffer.seek(0)
    return buffer
