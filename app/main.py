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

    except Exception as e:
        print(f"Ошибка загрузки изображений: {e}")


if __name__ == "__main__":
    main()
