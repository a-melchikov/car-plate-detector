from pathlib import Path

from PIL import Image


def is_image_file(path: Path) -> bool:
    available_extensions = {".jpg", ".jpeg", ".png"}
    return path.suffix.lower() in available_extensions


def process_file(path: Path) -> tuple[str, Image.Image] | None:
    """
    Обрабатывает один файл: если это изображение, открывает его.
    """
    if is_image_file(path):
        img = Image.open(path)
        return path.name, img
    return None


def load_images_from_path(path_str: str) -> list[tuple[str, Image.Image]]:
    """
    Загружает изображения из файла или папки.
    Возвращает список кортежей (имя файла, объект Image).
    """
    path = Path(path_str)
    images = []

    if path.is_file():
        if result := process_file(path):
            images.append(result)
    elif path.is_dir():
        for file_path in path.iterdir():
            if file_path.is_file():
                if result := process_file(file_path):
                    images.append(result)
    else:
        raise ValueError(f"Путь {path} не является изображением или директорией.")

    return images
