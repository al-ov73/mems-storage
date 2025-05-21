import zipfile
from io import BytesIO
from typing import Dict

import fitz
from fastapi import HTTPException, Request
from PIL import Image
from PyPDF2 import PdfMerger, PdfReader, PdfWriter


def convert_pdf_to_images(pdf_bytes: bytes, quality: int = 50) -> list[bytes]:
    """
    Конвертирует страницы PDF в список байтов изображений JPEG.
    :param pdf_bytes: Байтовые данные PDF-файла
    :param quality: Уровень качества JPEG (0-100)
    :return: Список байтовых строк с изображениями
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


def parse_page_ranges(pages: str) -> list[int]:
    """Парсит строку с диапазонами страниц в список номеров страниц"""
    page_ranges = []
    for part in pages.split(","):
        part = part.strip()
        if "-" in part:
            start, end = map(int, part.split("-"))
            page_ranges.extend(range(start - 1, end))  # -1 для 0-based индекса
        else:
            page_ranges.append(int(part) - 1)
    return sorted(list(set(page_ranges)))  # Удаляем дубликаты и сортируем


def split_pdf(file_content: bytes, pages: str) -> BytesIO:
    """
    Разделяет PDF по заданным страницам
    :param file_content: Байтовое содержимое PDF
    :param pages: Строка с номерами страниц (например, "1-3,5,7-9")
    :return: BytesIO поток с результирующим PDF
    :raises HTTPException: При ошибках обработки
    """
    try:
        page_numbers = parse_page_ranges(pages)
    except ValueError:
        raise HTTPException(status_code=400, detail="Некорректный формат номеров страниц")

    try:
        pdf_reader = PdfReader(BytesIO(file_content))
        pdf_writer = PdfWriter()

        for page_num in page_numbers:
            if 0 <= page_num < len(pdf_reader.pages):
                pdf_writer.add_page(pdf_reader.pages[page_num])
            else:
                raise HTTPException(
                    status_code=400,
                    detail=f"Страница {page_num + 1} не существует в документе"
                )

        output_stream = BytesIO()
        pdf_writer.write(output_stream)
        output_stream.seek(0)
        return output_stream
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Ошибка при обработке PDF: {str(e)}"
        )


def merge_pdfs(filenames: list[str], session_files: dict) -> BytesIO:
    """
    Объединяет несколько PDF из сессии в один
    :param filenames: Список имен файлов для объединения
    :param session_files: Словарь файлов из сессии {filename: file_data}
    :return: BytesIO поток с объединенным PDF
    :raises HTTPException: Если файлы не найдены
    """
    merger = PdfMerger()
    output = BytesIO()

    try:
        # Проверяем наличие всех файлов
        missing_files = [f for f in filenames if f not in session_files]
        if missing_files:
            raise HTTPException(
                status_code=404,
                detail=f"Файлы не найдены: {', '.join(missing_files)}"
            )

        # Добавляем файлы в merger
        for filename in filenames:
            file_data = session_files[filename]
            merger.append(BytesIO(file_data["file_content"]))

        merger.write(output)
        output.seek(0)
        return output
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Ошибка при объединении PDF: {str(e)}"
        )
    finally:
        merger.close()


def get_files_from_session(request: Request, filenames: list[str]) -> Dict[str, bytes]:
    """
    Получает файлы из сессии по именам
    :param request: FastAPI Request объект
    :param filenames: Список имен файлов
    :return: Словарь {имя_файла: содержимое_файла}
    :raises HTTPException: Если файлы не найдены
    """
    session_files = request.state.session.get("files", {})
    result = {}

    for filename in filenames:
        if filename not in session_files:
            raise HTTPException(
                status_code=404,
                detail=f"Файл '{filename}' не найден в сессии"
            )

        file_content = session_files[filename].get("file_content")
        if not file_content:
            raise HTTPException(
                status_code=400,
                detail=f"Отсутствует содержимое файла '{filename}'"
            )

        result[filename] = file_content

    return result


def convert_pdf_to_jpeg(file_content: bytes, dpi: int = 300) -> list[Image.Image]:
    """
    Конвертирует PDF в список изображений JPEG
    :param file_content: Байтовое содержимое PDF
    :param dpi: Разрешение изображений
    :return: Список объектов PIL.Image
    """
    doc = fitz.open(stream=BytesIO(file_content))
    images = []
    for page_num in range(doc.page_count):
        page = doc.load_page(page_num)
        pixmap = page.get_pixmap(dpi=dpi)
        img = Image.frombytes("RGB", [pixmap.width, pixmap.height], pixmap.samples)
        images.append(img)
    return images


def pack_images_into_zip(images: list[Image.Image], prefix: str) -> BytesIO:
    """
    Упаковывает изображения в ZIP-архив
    :param images: Список изображений PIL.Image
    :param prefix: Префикс для имен файлов
    :return: BytesIO поток с ZIP-архивом
    """
    buffer = BytesIO()
    with zipfile.ZipFile(buffer, "w") as zf:
        for idx, img in enumerate(images, start=1):
            img_bytes = BytesIO()
            img.save(img_bytes, format="JPEG", quality=85)
            zf.writestr(f"{prefix}_page_{idx}.jpg", img_bytes.getvalue())
    buffer.seek(0)
    return buffer


def convert_and_pack(filename: str, file_content: bytes, dpi: int = 300) -> BytesIO:
    """
    Конвертирует PDF в JPEG и упаковывает в ZIP
    :param filename: Имя исходного файла
    :param file_content: Байтовое содержимое PDF
    :param dpi: Разрешение изображений
    :return: BytesIO поток с ZIP-архивом
    """
    images = convert_pdf_to_jpeg(file_content, dpi)
    prefix = filename.rsplit(".", 1)[0]  # Удаляем расширение
    return pack_images_into_zip(images, prefix)


def combine_archives(individual_archives: list[BytesIO]) -> BytesIO:
    """
    Объединяет несколько ZIP-архивов в один
    :param individual_archives: Список BytesIO потоков с ZIP-архивами
    :return: BytesIO поток с объединенным ZIP-архивом
    """
    buffer = BytesIO()
    with zipfile.ZipFile(buffer, "w") as zf:
        for idx, archive in enumerate(individual_archives, start=1):
            archive.seek(0)
            with zipfile.ZipFile(archive) as src_zip:
                for name in src_zip.namelist():
                    zf.writestr(f"file_{idx}/{name}", src_zip.read(name))
    buffer.seek(0)
    return buffer