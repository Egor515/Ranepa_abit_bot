from functools import cached_property

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    BOT_TOKEN: str

    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 8000
    DEBUG: bool = True

    GEMINI_API_KEY: str | None = None
    GEMINI_MODEL: str = "gemini-2.5-flash"

    FAQ_TOP_K: int = 5
    FAQ_SCORE_THRESHOLD: float = 0.75

    FAQ_SOURCE_PATH: str = "data/Database.xlsx"
    FAQ_QUESTION_COLUMN: str = "Question"
    FAQ_ANSWER_COLUMN: str = "Answer"

    MILVUS_URI: str = "./milvus_faq.db"
    MILVUS_COLLECTION_NAME: str = "faq_collection"

    STOPWORDS_FILES: list[str] = Field(
        default_factory=lambda: [
            "data/ru_abusive_words.txt",
            "data/ru_curse_words.txt",
        ]
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @field_validator("STOPWORDS_FILES", mode="before")
    @classmethod
    def parse_stopwords_files(cls, value: str | list[str]) -> list[str]:
        if isinstance(value, str):
            return [item.strip() for item in value.split(",") if item.strip()]
        return value

    @cached_property
    def faq_source_columns(self) -> tuple[str, str]:
        return (self.FAQ_QUESTION_COLUMN, self.FAQ_ANSWER_COLUMN)


settings = Settings()
