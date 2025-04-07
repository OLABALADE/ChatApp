from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_HOST: str
    DATABASE_PORT: int
    DATABASE_NAME: str
    DATABASE_USER: str
    DATABASE_PASSWORD: str

    SECRET_KEY: str

    class Config:
        env_file = "../../../.env"
        env_file_encoding = "utf-8"
        case_sensitive = True


settings = Settings()
