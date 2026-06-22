# src/support_assistant/llm.py
from __future__ import annotations
from langchain.chat_models import init_chat_model
from langchain_core.language_models.chat_models import BaseChatModel
# Agregamos "src."
from src.support_assistant.config import get_settings

def get_chat_model(temperature: float = 0.0) -> BaseChatModel:
    """Fábrica única de modelos de chat — provider-agnostic."""
    s = get_settings()
    
    # El chequeo seguro se realiza en caliente antes de llamar a la API
    if s.openai_api_key is None:
        raise RuntimeError("OPENAI_API_KEY no está configurada en tu archivo .env")
        
    return init_chat_model(
        s.llm_model,
        model_provider=s.llm_provider,
        temperature=temperature,
        api_key=s.openai_api_key.get_secret_value(),
    )