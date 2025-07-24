from pydantic import BaseSettings

class Settings(BaseSettings):
    DB_USERNAME: str
    DB_PASSWORD: str
    DB_HOST: str = 'localhost'
    DB_PORT: int = 5432
    DB_NAME: str

    class Config:
        env_file = '.env'

settings = Settings()
