from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    MONGODB_URL: str
    MONGODB_DB_NAME: str
    PORT: int = 8080
    SCOREME_USERNAME: str
    SCOREME_PASSWORD: str
    SCOREME_BASE_URL: str

    class Config:
        env_file = ".env"

settings = Settings()