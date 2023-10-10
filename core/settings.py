from pydantic import BaseSettings
import os
from starlette.config import Config

class Settings(BaseSettings):
    environment: str = os.getenv("BUILD_ENVIRONMENT", "prod")
    ASB_CONNECTION_STRING: str = ""
    AZURE_STORAGE_CONNECTION_STRING: str = ""
    config = Config(f"./environment/environment.{environment}.env")
    ASB_CONNECTION_STRING = config('ASB_CONNECTION_STRING', default="")
    AZURE_STORAGE_CONNECTION_STRING = config('AZURE_STORAGE_CONNECTION_STRING', default="")
    DATABASE_CONNECTION_STRING = config('DATABASE_CONNECTION_STRING', default="")
    QUEUE_NAME_INPUT = config('QUEUE_NAME_INPUT', default="")
    QUEUE_NAME_OUTPUT = config('QUEUE_NAME_OUTPUT', default="")
    URL_DETECTION_API = config('URL_DETECTION_API', default="")
    AZURE_STORAGE_CONNECTION_STRING_2 = config('AZURE_STORAGE_CONNECTION_STRING_2', default="")
    QUEUE_NAME_INSERT = config('QUEUE_NAME_INSERT', default="")
    MODEL_NAME = config('MODEL_NAME', default='')
    CLASS_NAME = config('CLASS_NAME', default='')
    