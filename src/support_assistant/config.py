# src/support_assistant/config.py
from typing import Optional
from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict
from datetime import datetime
from dotenv import load_dotenv

# Forzamos la carga del archivo .env ANTES de que Pydantic intente validar nada
load_dotenv()

class Settings(BaseSettings):
    # Al asignarle None por defecto, Pydantic NO tirará "Field required" si el entorno tarda en leerse
    openai_api_key: Optional[SecretStr] = None
    llm_provider: str = "openai"
    llm_model: str = "gpt-4o-mini"
    
    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding="utf-8", 
        case_sensitive=False,
        extra="ignore"
    )

def get_settings() -> Settings:
    return Settings(_env_file=".env")