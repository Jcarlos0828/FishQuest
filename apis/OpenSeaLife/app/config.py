from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    hf_base: str = "https://huggingface.co"
    hf_repo: str = "datasets/cboettig/fishbase"
    hf_branch: str = "main"
    default_version: str = "v25.04"


settings = Settings()
