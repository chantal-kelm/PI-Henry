# src/support_assistant/main.py
import json
from langgraph.graph import StateGraph, START
from src.support_assistant.contracts import AgentState
from src.support_assistant.nodes import security_check_node, assistant_node

def build_graph():
    """Construye e interconecta la topología del flujo."""
    # Le pasamos AgentState (Pydantic) para que el grafo valide la estructura de entrada
    graph = StateGraph(AgentState)

    graph.add_node("security_check", security_check_node)
    graph.add_node("assistant_node", assistant_node)

    graph.add_edge(START, "security_check")

    return graph.compile()

def run_pipeline(user_query: str) -> None:
    app = build_graph()
    
    # Invocamos pasando el diccionario inicial esperado por el esquema
    final_state = app.invoke({"question": user_query})
    
    print(f"\n📥 [CONSULTA PROCESADA]: {user_query}")
    print("🚀 [OUTPUT CONTRATO JSON DOWNSTREAM]")
    # Usamos .get() o acceso a dict ya que LangGraph devuelve el estado final como diccionario
    print(json.dumps(final_state.get("response", {}), indent=2, ensure_ascii=False))
    
    print("📊 [MÉTRICAS REGISTRADAS]")
    print(json.dumps(final_state.get("metrics", {}), indent=2))
    print("=" * 60)

if __name__ == "__main__":
    print("🤖 [SISTEMA DE SOPORTE INICIADO]")
    print("Escribe tu consulta de soporte abajo (o escribe 'salir' para terminar).\n")
    
    while True:
        user_input = input("👤 Cliente (ingresa tu pregunta): ")
        
        if user_input.lower().strip() == "salir":
            print("Cerrando el asistente de soporte. ¡Adiós!")
            break
            
        if not user_input.strip():
            continue
            
        run_pipeline(user_input)