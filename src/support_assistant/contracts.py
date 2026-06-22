# src/support_assistant/contracts.py
from __future__ import annotations
from typing import List, Optional, Any, TypedDict
from pydantic import BaseModel, Field

# Esquema para el caso exitoso (Downstream)
class AssistantResponse(BaseModel):
    reasoning: str = Field(description="Análisis secuencial detallado usando Chain of Thought (CoT).")
    answer: str = Field(description="Respuesta directa y estructurada destinada al cliente.")
    confidence: float = Field(description="Estimación del nivel de confianza, de 0.0 a 1.0.")
    actions: List[str] = Field(description="Lista de acciones recomendadas sugeridas para el agente.")

# Esquema para el caso bloqueado de seguridad
class SecurityRejection(BaseModel):
    status: str = "REJECTED"
    error: str = "Consulta denegada por motivos de seguridad del sistema."

class AgentState(TypedDict):
    question: str
    # Usar Any permite que LangGraph reemplace el objeto entero sin buscar reducers de diccionarios
    response: Any
    metrics: Any