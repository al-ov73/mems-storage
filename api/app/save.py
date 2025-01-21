from pathlib import Path

from utils.os_utils import compress_image


def make_preview_for_existing_images():
    folder_path = Path("static/photos/")
    for file_path in folder_path.rglob("*"):
        filename = file_path.stem
        out_path = f"static/previews/{filename}.jpeg"
        if file_path.is_file():
            compress_image(file_path, out_path)


if __name__ == "__main__":
    make_preview_for_existing_images()
