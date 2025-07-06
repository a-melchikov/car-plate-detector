from app.utils.detector import detect_plates
from app.utils.image_loader import load_images_from_path


def main() -> None:
    path = input("Введите путь к изображению или папке: ").strip()

    try:
        images = load_images_from_path(path)
        if not images:
            print("Изображения не найдены.")
            return

        print(f"\nЗагружено изображений: {len(images)}")
        for filename, _ in images:
            print(f"- {filename}")

        for filename, image in images:
            print(f"\n[Обработка] {filename}")
            image_path = image.filename

            detection_result = detect_plates(image_path)

            for result in detection_result:
                print(f"Файл: {result['filename']}")
                for i, plate in enumerate(result["plates"]):
                    print(f"  Номерной знак {i + 1}: {plate['text']}")
                    print(f"  Координаты: {plate['box']}")

    except Exception as e:
        print(f"Ошибка загрузки или обработки изображений: {e}")


if __name__ == "__main__":
    main()
