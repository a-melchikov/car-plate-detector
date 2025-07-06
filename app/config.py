from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):  # type: ignore
    BASE_DIR: Path = Path(__file__).resolve().parent.parent

    model_config = SettingsConfigDict(env_file=BASE_DIR / "app" / ".env")

    MODEL_PATH: str = str(BASE_DIR / "models" / "russian_license_plate.pt")

    TESSERACT_CMD: str | None = None
    OCR_PSM: int = 6
    OCR_OEM: int = 3
    OCR_WHITELIST_CHARS: str = "ABEKMHOPCTYX0123456789"

    VISUALIZE: bool = True

    RESULTS_DIR: Path = BASE_DIR / "data" / "results"


settings = Settings()
