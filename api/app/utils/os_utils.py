import os
import shutil
from urllib.parse import urljoin
import logging

from ..config import config
from PIL import Image, UnidentifiedImageError

logger = logging.getLogger(__name__)


def clean_dir(dir_path: str) -> None:
    for filename in os.listdir(dir_path):
        file_path = os.path.join(dir_path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print("Failed to delete %s. Reason: %s" % (file_path, e))


def get_folder_size(path: str) -> int:
    """return folder size im MB"""
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(path):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            try:
                total_size += os.path.getsize(file_path)
            except OSError as e:
                print(f"Ошибка при получении размера файла {file_path}: {e}")
    return round(total_size / 10**6, 1)


def compress_image(
    input_path: str,
    quality: int = 20,
    resize_factor: bool = None,
) -> str:
    """
    :param input_path: Путь к исходному изображению.
    :param output_path: Путь для сохранения сжатого изображения.
    :param quality: Качество сохранения (от 1 до 95, чем меньше, тем сильнее сжатие).
    :param resize_factor: Коэффициент уменьшения размеров (например, 0.5 для уменьшения в 2 раза).
    """
    img_path = f"{input_path}.jpg"
    preview_path = os.path.join(config.STATIC_DIR, "previews", f"{os.path.basename(input_path)}.jpeg")
    try:
        with Image.open(img_path) as img:
            if resize_factor:
                new_width = int(img.width * resize_factor)
                new_height = int(img.height * resize_factor)
                img = img.resize((new_width, new_height), Image.LANCZOS)

            img.save(preview_path, "JPEG", quality=quality, optimize=True)
            logger.info(f"Файл {preview_path} сохранен")
            preview_link = urljoin(config.API_URL, f"{config.STATIC_URL}/previews/{os.path.basename(input_path)}.jpeg")
            return preview_link
    except UnidentifiedImageError as e:
        logger.info(f"Ошибка обработки файла {img_path}: {e}")
        return urljoin(config.API_URL, f"{config.STATIC_URL}/photos/{os.path.basename(img_path)}.jpg")
