from pathlib import Path

from PIL.Image import Image

from app.utils.detector import PlateDetector
from app.utils.image_loader import load_images_from_path


class PlateDetectorApp:
    def __init__(self, input_path: str):
        self.input_path = Path(input_path).expanduser().resolve()
        self.detector = PlateDetector()

    def run(self) -> None:
        images = self._load_images()
        if not images:
            print("Изображения не найдены.")
            return

        self._print_summary(images)
        self._process_images(images)

    def _load_images(self) -> list[tuple[str, Image]]:
        try:
            return load_images_from_path(str(self.input_path))
        except Exception as e:
            raise RuntimeError(f"Ошибка загрузки изображений: {e}")

    def _print_summary(self, images: list[tuple[str, Image]]) -> None:
        print(f"\nЗагружено изображений: {len(images)}")
        for filename, _ in images:
            print(f"- {filename}")

    def _process_images(self, images: list[tuple[str, Image]]) -> None:
        for filename, image in images:
            print(f"\n[Обработка] {filename}")
            image_path = image.filename

            detection_result = self.detector.detect_from_image_path(image_path)

            for result in detection_result:
                print(f"Файл: {result['filename']}")
                for i, plate in enumerate(result["plates"]):
                    print(f"  Номерной знак {i + 1}: {plate['text']}")
                    print(f"  Координаты: {plate['box']}")
