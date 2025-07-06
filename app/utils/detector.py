import json
import os
from typing import Any

import cv2
from ultralytics import YOLO

from app.config import settings
from app.utils.ocr import extract_plate_text

model = YOLO(settings.MODEL_PATH)
PLATE_CLASS_NAMES = {"IndividualPlateStandart"}


def detect_plates(image_path: str) -> list[dict[str, Any]]:
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Изображение не найдено: {image_path}")

    img = cv2.imread(image_path)
    original_img = img.copy()

    results = model(image_path)
    filename = os.path.basename(image_path)

    output = {"filename": filename, "plates": []}

    for result in results:
        for box in result.boxes:
            class_id = int(box.cls[0])
            class_name = model.names[class_id]

            if class_name not in PLATE_CLASS_NAMES:
                continue

            x1, y1, x2, y2 = map(int, box.xyxy[0])
            width, height = x2 - x1, y2 - y1

            plate_img = img[y1:y2, x1:x2]
            text = extract_plate_text(plate_img)

            output["plates"].append({"box": [x1, y1, width, height], "text": text})

            if settings.VISUALIZE:
                cv2.rectangle(original_img, (x1, y1), (x2, y2), (0, 255, 0), 2)

                font_scale = max(0.5, min(1.5, height / 40))
                text_x = x1
                text_y = y1 - 10

                cv2.putText(
                    original_img,
                    text,
                    (text_x, text_y),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    font_scale,
                    (0, 255, 0),
                    2,
                )

    results_dir = settings.RESULTS_DIR
    os.makedirs(results_dir, exist_ok=True)

    base_filename = os.path.splitext(filename)[0]
    output_json_path = results_dir / f"{base_filename}.json"

    with open(output_json_path, "w", encoding="utf-8") as f:
        json.dump([output], f, ensure_ascii=False, indent=2)
        print(f"Результаты сохранены в файл: {output_json_path}")

    if settings.VISUALIZE:
        output_image_path = os.path.join(results_dir, f"{base_filename}_boxes.jpg")
        cv2.imwrite(output_image_path, original_img)
        print(f"Изображение с рамками сохранено: {output_image_path}")

    return [output]


if __name__ == "__main__":
    image_path = "../data/images/combined.png"
    result = detect_plates(image_path)

    print(json.dumps(result, indent=2, ensure_ascii=False))
