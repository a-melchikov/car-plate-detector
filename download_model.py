import os

from dotenv import load_dotenv
from roboflow import Roboflow

load_dotenv()

api_key = os.getenv("ROBOFLOW_API_KEY")
if not api_key:
    raise ValueError("ROBOFLOW_API_KEY не найден в .env или переменных окружения")

rf = Roboflow(api_key=api_key)
project = rf.workspace("work-cqtt7").project("autoplate")
version = project.version(4)
dataset = version.download("yolov8")

print("Модель и датасет успешно скачаны!")
