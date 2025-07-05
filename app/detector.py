import json
import os
from typing import Any

import cv2
import pytesseract
from config import settings
from ultralytics import YOLO

model = YOLO(settings.MODEL_PATH)

if settings.TESSERACT_CMD:
    pytesseract.pytesseract.tesseract_cmd = settings.TESSERACT_CMD

PLATE_CLASS_NAMES = {"IndividualPlateStandart"}


def format_plate_text(text: str) -> str:
    valid_letters = set("ABEKMHOPCTYX")
    valid_digits = set("0123456789")

    replacements = {
        "0": "O",
        "O": "0",
        "1": "Y",
        "Y": "1",
        "3": "E",
        "E": "3",
        "4": "A",
        "A": "4",
        "5": "S",
        "S": "5",
        "7": "T",
        "T": "7",
        "8": "B",
        "B": "8",
        "9": "P",
        "P": "9",
    }

    text = text.replace(" ", "")
    cleaned = [
        c.upper() for c in text if c.upper() in valid_letters or c in valid_digits
    ]

    if len(cleaned) < 6:
        return "".join(cleaned)

    expected_types = [
        valid_letters,
        valid_digits,
        valid_digits,
        valid_digits,
        valid_letters,
        valid_letters,
    ]

    for i in range(6, len(cleaned)):
        expected_types.append(valid_digits)

    corrected = []
    for i, char in enumerate(cleaned):
        if i >= len(expected_types):
            break

        expected = expected_types[i]
        if char in expected:
            corrected.append(char)
        else:
            corrected_char = replacements.get(char, None)
            if corrected_char and corrected_char in expected:
                corrected.append(corrected_char)
            else:
                corrected.append("?")

    corrected_text = "".join(corrected)

    base = corrected_text[:6]
    region = corrected_text[6:]
    formatted_text = base + " " + region[:3]
    return formatted_text


def extract_plate_text(plate_img) -> str:
    plate_img = cv2.resize(plate_img, None, fx=3, fy=3)
    gray = cv2.cvtColor(plate_img, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (3, 3), 0)
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    config = f"--oem {settings.OCR_OEM} --psm {settings.OCR_PSM} -c tessedit_char_whitelist={settings.OCR_WHITELIST_CHARS}"
    text = pytesseract.image_to_string(thresh, config=config)
    return format_plate_text(text)


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

    if settings.VISUALIZE:
        output_path = "output_with_boxes.jpg"
        cv2.imwrite(output_path, original_img)
        print(f"Изображение с рамками сохранено: {output_path}")

    return [output]


if __name__ == "__main__":
    result = detect_plates("../data/images/combined.png")
    print(json.dumps(result, indent=2, ensure_ascii=False))

    with open("output.json", "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
