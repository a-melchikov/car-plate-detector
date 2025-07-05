import os

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
    )

    MODEL_PATH: str = "../models/russian_license_plate.pt"

    TESSERACT_CMD: str | None = None
    OCR_PSM: int = 6
    OCR_OEM: int = 3
    OCR_WHITELIST_CHARS: str = "ABEKMHOPCTYX0123456789"

    VISUALIZE: bool = True


settings = Settings()
