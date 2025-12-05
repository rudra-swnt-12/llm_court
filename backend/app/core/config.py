import os
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    GROQ_API_KEY: str
    DATABASE_URL: str
    
    MODEL_JUDGE: str = "openai/gpt-oss-120b"  
    MODEL_PROSECUTOR: str = "llama-3.3-70b-versatile" 
    MODEL_DEFENSE: str = "openai/gpt-oss-20b"
    MODEL_EVIDENCE_ANALYZER: str = "meta-llama/llama-4-scout-17b-16e-instruct"

    PROJECT_NAME: str = "LLM Court"
    API_V1_STR: str = "/api/v1"
    
    model_config = SettingsConfigDict(
        env_file=".env", 
        env_ignore_empty=True,
        extra="ignore"
    )

settings = Settings()