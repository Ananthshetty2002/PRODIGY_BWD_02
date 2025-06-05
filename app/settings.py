# app/settings.py

import os
print(">>> CWD in settings.py:", os.getcwd())
print(">>> Files here:", os.listdir(os.getcwd()))

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
print(">>> Loaded DATABASE_URL:", settings.DATABASE_URL)
