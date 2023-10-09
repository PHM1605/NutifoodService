from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    ASB_CONNECTION_STRING: str
    QUEUE_NAME: str
    class Config:
        env_file = ".env"

settings = Settings()