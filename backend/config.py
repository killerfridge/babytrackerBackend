from pydantic import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    database_hostname: Optional[str]
    database_port: Optional[str]
    database_password: Optional[str]
    database_username: Optional[str]
    database_name: Optional[str]
    secret_key: str
    access_token_expire_minutes: int
    algorithm: str
    database_url: Optional[str]

    class Config:
        env_file = 'backend/.env'
        env_file_encoding = 'utf-8'


settings = Settings()
