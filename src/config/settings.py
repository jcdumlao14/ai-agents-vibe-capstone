from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )

    app_name: str = Field(default="BusinessPilot AI")
    environment: str = Field(default="development")
    debug: bool = Field(default=False)

    openai_api_key: str | None = Field(default=None)
    google_project_id: str | None = Field(default=None)
    google_credentials_path: str | None = Field(default=None)
    google_region: str = Field(default="us-central1")
    google_adk_endpoint_id: str | None = Field(default=None)
    use_google_adk: bool = Field(default=False)
    google_antigravity_endpoint: str | None = Field(default=None)
    google_antigravity_api_key: str | None = Field(default=None)
    use_google_antigravity: bool = Field(default=False)

    log_level: str = Field(default="INFO")
    log_format: str = Field(default="%(asctime)s - %(name)s - %(levelname)s - %(message)s")


settings = AppSettings()
