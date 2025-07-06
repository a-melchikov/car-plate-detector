from app.cli import PlateDetectorApp


def main() -> None:
    path = input("Введите путь к изображению или папке: ").strip()
    try:
        app = PlateDetectorApp(path)
        app.run()
    except Exception as e:
        print(f"Ошибка выполнения программы: {e}")


if __name__ == "__main__":
    main()
