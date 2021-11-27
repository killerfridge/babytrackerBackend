from pydantic import BaseSettings


class Settings(BaseSettings):
    database_hostname: str
    database_port: str
    database_password: str
    database_username: str
    database_name: str
    secret_key: str
    access_token_expire_minutes: str
    algorithm: str

    class Config:
        env_file = 'backend/.env'
        env_file_encoding = 'utf-8'


settings = Settings()
