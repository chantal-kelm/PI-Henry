import os
import json
import sys
from datetime import datetime

# Añadimos la raíz al path de ejecución para evitar errores de importación
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.support_assistant.main import build_graph

def persist_execution_metrics(metrics: dict):
    """Guarda y acumula las métricas de uso con timestamps de forma persistente en metrics/metrics.json"""
    os.makedirs("metrics", exist_ok=True)
    metrics_path = "metrics/metrics.json"
    
    # Estructura requerida estrictamente por la rúbrica
    metrics_record = {
        "timestamp": datetime.now().isoformat(),
        "tokens_prompt": metrics.get("prompt_tokens", 0),
        "tokens_completion": metrics.get("completion_tokens", 0),
        "total_tokens": metrics.get("total_tokens", 0),
        "latency_ms": metrics.get("latency_ms", 0.0),
        "estimated_cost_usd": metrics.get("estimated_cost_usd", 0.0)
    }
    
    # Cargamos el historial existente si el archivo ya existe
    try:
        if os.path.exists(metrics_path):
            with open(metrics_path, "r", encoding="utf-8") as f:
                history = json.load(f)
                if not isinstance(history, list):
                    history = []
        else:
            history = []
    except Exception:
        history = []
        
    history.append(metrics_record)
    
    # Escribimos los datos de manera estructurada e indentada
    with open(metrics_path, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2, ensure_ascii=False)

def run_interactive_assistant():
    """Ejecuta el asistente interactivo y procesa las consultas."""
    print("🤖 [SISTEMA DE SOPORTE INICIADO]")
    print("Escribe tu consulta de soporte abajo o escribe 'salir' para terminar.\n")
    
    app = build_graph()
    
    while True:
        try:
            user_input = input("👤 Cliente (ingresa tu pregunta): ")
            if user_input.strip().lower() == "salir":
                print("👋 ¡Gracias por usar el asistente de soporte!")
                break
                
            if not user_input.strip():
                continue
                
            print(f"\n📥 [CONSULTA PROCESADA]: {user_input}")
            
            # Ejecutamos el flujo de LangGraph
            state = app.invoke({"question": user_input})
            
            # Imprimimos la respuesta en formato JSON válido en consola (Requisito de rúbrica)
            print("🚀 [OUTPUT CONTRATO JSON DOWNSTREAM]")
            print(json.dumps(state["response"], indent=2, ensure_ascii=False))
            
            print("📊 [MÉTRICAS REGISTRADAS]")
            print(json.dumps(state["metrics"], indent=2, ensure_ascii=False))
            print("=" * 60 + "\n")
            
            # Persistimos las métricas nativas directamente en el archivo JSON
            persist_execution_metrics(state["metrics"])
            
        except KeyboardInterrupt:
            print("\n👋 Sesión interrumpida. Saliendo de forma segura...")
            break
        except Exception as e:
            print(f"❌ Ocurrió un error inesperado en la ejecución: {str(e)}\n")

if __name__ == "__main__":
    run_interactive_assistant()