from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_name: str = "RAG Document Q&A"
    upload_dir: Path = Path("data/uploads")
    chroma_dir: Path = Path("chroma_db")
    registry_path: Path = Path("data/documents.json")
    embedding_model: str = "all-MiniLM-L6-v2"
    chunk_size: int = 1800
    chunk_overlap: int = 250
    top_k: int = 5
    llm_provider: str = "openai"
    openai_api_key: str | None = None
    openai_model: str = "gpt-4.1-mini"

    def ensure_directories(self) -> None:
        self.upload_dir.mkdir(parents=True, exist_ok=True)
        self.chroma_dir.mkdir(parents=True, exist_ok=True)
        self.registry_path.parent.mkdir(parents=True, exist_ok=True)


settings = Settings()
settings.ensure_directories()
