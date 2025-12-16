from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = 'Phonebook API Service'
    redis_host: str = 'localhost'
    redis_port: int = 6379
    redis_db: int = 0
    log_level: str = 'INFO'
    api_version: str = 'v1'

    class Config:
        env_file = '.env'


settings = Settings()
