from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    BOT_TOKEN: str
    OPENAI_API_KEY: str
    ASSISTANT_ID: str
    DB_FILENAME: str
    WEBHOOK_URL: str
    @property
    def DATABASE_URL(self):
        return f"sqlite+aiosqlite:///{self.DB_FILENAME}"

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
