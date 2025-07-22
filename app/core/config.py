from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    mongodb_uri: str
    mongodb_db: str

    class Config:
        env_file = ".env"

settings = Settings()
