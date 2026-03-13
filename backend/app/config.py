from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = (
        "postgresql+asyncpg://pdh:changeme@localhost:5432/personal_data_hub"
    )
    database_url_sync: str = (
        "postgresql://pdh:changeme@localhost:5432/personal_data_hub"
    )
    redis_url: str = "redis://localhost:6379"
    embedding_model: str = "all-mpnet-base-v2"
    embedding_dimensions: int = 768
    chunk_size: int = 512
    chunk_overlap: int = 50
    data_mount_path: str = "/data"
    github_token: str = ""

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()
