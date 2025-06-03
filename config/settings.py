import enum
from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

load_dotenv(override=True)


class LogLevel(str, enum.Enum):
    NOTSET = "NOTSET"
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    FATAL = "FATAL"


class AppSettings(BaseSettings):
    host: str = "0.0.0.0"
    port: int = 8000
    workers_count: int = 2
    environment: str = os.getenv("ENVIRONMENT", "development")
    reload: bool = True if environment == "development" else False
    log_level: LogLevel = LogLevel.INFO
    weather_api_key: str
    openai_api_key: str
    redis_url: str

    class Config:
        env_file = ".env"
