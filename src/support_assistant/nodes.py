# src/support_assistant/nodes.py
import time
from typing import Any, Dict
from langchain_core.prompts import ChatPromptTemplate
from langgraph.types import Command
from langgraph.graph import END

from src.support_assistant.contracts import AgentState, AssistantResponse
from src.support_assistant.llm import get_chat_model

def security_check_node(state: AgentState) -> Command:
    """Nodo de mitigación perimetral (Filtro adversarial)."""
    question = state["question"].lower()
    adversarial_keywords = ["ignora las instrucciones", "olvida lo anterior", "system prompt", "ignore previous"]
    
    if any(kw in question for kw in adversarial_keywords):
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
    
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", (
            "Eres un asistente experto para agentes de soporte al cliente.\n"
            "Es mandatorio que utilices el campo 'reasoning' para desglosar tu lógica paso a paso (CoT) "
            "antes de completar la respuesta definitiva y los planes de acción."
        )),
        ("user", "{question}")
    ])
    
    chain = prompt_template | structured_llm
    
    start_time = time.perf_counter()
    # Invocamos la cadena (devolverá un dict con 'parsed' y 'raw' por el include_raw=True)
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