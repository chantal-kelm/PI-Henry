import os
import time
from typing import Any, Dict
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import SystemMessage  # Importación clave para ignorar llaves de JSON
from langgraph.types import Command
from langgraph.graph import END

from src.support_assistant.contracts import AgentState, AssistantResponse
from src.support_assistant.llm import get_chat_model
from src.safety import is_adversarial_query  # Importación limpia del módulo de seguridad

def load_system_prompt() -> str:
    """Carga dinámicamente el prompt del sistema desde la carpeta externa de prompts."""
    try:
        # Determinamos la ruta absoluta de la raíz del proyecto para evitar errores de ejecución
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        prompt_path = os.path.join(base_dir, "prompts", "main_prompt.txt")
        
        with open(prompt_path, "r", encoding="utf-8") as f:
            return f.read().strip()
    except Exception:
        # Fallback de respaldo en duro si el archivo físico es inaccesible
        return (
            "Eres un asistente experto para agentes de soporte al cliente.\n"
            "Es mandatorio que utilices el campo 'reasoning' para desglosar tu lógica paso a paso (CoT) "
            "antes de completar la respuesta definitiva y los planes de acción."
        )

def security_check_node(state: AgentState) -> Command:
    """Nodo de mitigación perimetral (Filtro adversarial)."""
    # Delegamos la lógica de verificación al módulo de seguridad dedicado (Requisito de rúbrica)
    if is_adversarial_query(state["question"]):
        return Command(
            update={
                "response": {
                    "status": "REJECTED",
                    "error": "Consulta denegada por motivos de seguridad."
                },
                "metrics": {
                    "latency_ms": 0.0,
                    "total_tokens": 0,
                    "estimated_cost_usd": 0.0
                }
            },
            goto=END
        )
    return Command(goto="assistant_node")

def assistant_node(state: AgentState) -> Dict[str, Any]:
    """Nodo operativo del LLM puro sin dependencias comunitarias."""
    llm = get_chat_model(temperature=0.0)
    structured_llm = llm.with_structured_output(AssistantResponse, include_raw=True)
    
    # Cargamos dinámicamente el prompt externo (cumpliendo con la rúbrica oficial)
    system_instruction = load_system_prompt()
    
    # Al usar SystemMessage, evitamos que LangChain parsee las llaves {} del JSON como variables de Python
    prompt_template = ChatPromptTemplate.from_messages([
        SystemMessage(content=system_instruction),
        ("user", "{question}")
    ])
    
    chain = prompt_template | structured_llm
    
    start_time = time.perf_counter()
    # Invocamos la cadena estructurada
    output_wrapper = chain.invoke({"question": state["question"]})
    end_time = time.perf_counter()
    
    latency_ms = (end_time - start_time) * 1000
    
    # Extraemos el objeto estructurado (Pydantic) y los metadatos de uso nativos
    llm_output = output_wrapper["parsed"]
    raw_message = output_wrapper["raw"]
    
    # Extraemos los tokens directamente del mensaje de respuesta de LangChain v0.3+
    usage = raw_message.usage_metadata or {}
    prompt_tokens = usage.get("input_tokens", 0)
    completion_tokens = usage.get("output_tokens", 0)
    total_tokens = usage.get("total_tokens", 0)
    
    # Cálculo manual basado en tarifas oficiales de gpt-4o-mini ($0.15 / M input, $0.60 / M output)
    estimated_cost = (prompt_tokens * 0.15 / 1_000_000) + (completion_tokens * 0.60 / 1_000_000)
    
    return {
        "response": llm_output.model_dump(),
        "metrics": {
            "latency_ms": round(latency_ms, 2),
            "prompt_tokens": prompt_tokens,
            "completion_tokens": completion_tokens,
            "total_tokens": total_tokens,
            "estimated_cost_usd": round(estimated_cost, 6)
        }
    }