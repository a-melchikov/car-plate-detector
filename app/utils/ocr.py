import cv2
import numpy as np
import pytesseract

from app.config import settings
from app.utils.formatter import format_plate_text

if settings.TESSERACT_CMD:
    pytesseract.pytesseract.tesseract_cmd = settings.TESSERACT_CMD


def extract_plate_text(plate_img: np.ndarray) -> str:
    plate_img = cv2.resize(plate_img, None, fx=3, fy=3)
    gray = cv2.cvtColor(plate_img, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (3, 3), 0)
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    config = f"--oem {settings.OCR_OEM} --psm {settings.OCR_PSM} -c tessedit_char_whitelist={settings.OCR_WHITELIST_CHARS}"
    text = pytesseract.image_to_string(thresh, config=config)
    return format_plate_text(text)
