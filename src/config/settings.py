from pydantic import BaseSettings, Field


class AppSettings(BaseSettings):
    app_name: str = Field("BusinessPilot AI", env="APP_NAME")
    environment: str = Field("development", env="ENVIRONMENT")
    debug: bool = Field(False, env="DEBUG")

    openai_api_key: str = Field(..., env="OPENAI_API_KEY")
    google_project_id: str = Field(..., env="PROJECT_ID")
    google_credentials_path: str = Field(..., env="GOOGLE_APPLICATION_CREDENTIALS")
    google_region: str = Field("us-central1", env="GOOGLE_REGION")
    google_adk_endpoint_id: str | None = Field(None, env="GOOGLE_ADK_ENDPOINT_ID")
    use_google_adk: bool = Field(False, env="USE_GOOGLE_ADK")
    google_antigravity_endpoint: str | None = Field(None, env="GOOGLE_ANTIGRAVITY_ENDPOINT")
    google_antigravity_api_key: str | None = Field(None, env="GOOGLE_ANTIGRAVITY_API_KEY")
    use_google_antigravity: bool = Field(False, env="USE_GOOGLE_ANTIGRAVITY")

    log_level: str = Field("INFO", env="LOG_LEVEL")
    log_format: str = Field("%(asctime)s - %(name)s - %(levelname)s - %(message)s", env="LOG_FORMAT")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = AppSettings()
