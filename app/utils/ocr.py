import cv2
import numpy as np
import pytesseract

from app.config import settings
from app.utils.formatter import PlateTextFormatter


class PlateOCRProcessor:
    def __init__(self) -> None:
        if settings.TESSERACT_CMD:
            pytesseract.pytesseract.tesseract_cmd = settings.TESSERACT_CMD
        self.formatter = PlateTextFormatter()
        self.ocr_config = (
            f"--oem {settings.OCR_OEM} "
            f"--psm {settings.OCR_PSM} "
            f"-c tessedit_char_whitelist={settings.OCR_WHITELIST_CHARS}"
        )

    def extract_plate_text(self, plate_img: np.ndarray) -> str:
        processed_img = self._preprocess_image(plate_img)
        raw_text = pytesseract.image_to_string(processed_img, config=self.ocr_config)
        return self.formatter.format(raw_text)

    def _preprocess_image(self, plate_img: np.ndarray) -> np.ndarray:
        plate_img = cv2.resize(plate_img, None, fx=3, fy=3)
        gray = cv2.cvtColor(plate_img, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (3, 3), 0)
        _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        return thresh
