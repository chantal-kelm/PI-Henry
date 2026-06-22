# Support Assistant Agent 🤖 (LangGraph Pipeline)

Este proyecto implementa un agente automatizado e interactivo de soporte al cliente utilizando una arquitectura de grafos orientada a nodos con **LangGraph** y validación estricta de datos mediante contratos **Pydantic**. El diseño toma como referencia los patrones desacoplados y limpios del framework corporativo `cop-fx-intelligence`.

El sistema incluye mitigación perimetral de seguridad para interceptar inyecciones de prompt maliciosas a costo cero y telemetría nativa para auditar el consumo exacto de la API.

---

## 🏗️ Arquitectura del Sistema

El flujo de control se desacopla en nodos funcionales aislados dentro de un bucle interactivo continuo por consola (CLI):

1. **`security_check_node`**: Analiza heurísticamente el input del cliente en busca de frases adversariales. Si detecta un ataque, desvía el flujo inmediatamente al final (`END`) sin tocar la API de pago.

2. **`assistant_node`**: Invoca de manera estructurada al modelo `gpt-4o-mini` para procesar consultas legítimas, aplicando *Chain of Thought* (CoT) y calculando las métricas nativas de uso.


## 🚀 Requisitos e Instalación

Este proyecto gestiona sus dependencias mediante **`uv`**, el instalador y gestor de entornos ultra-rápido para Python.

### 1. Clonar el repositorio y posicionarse en la raíz
```bash
cd pi-henry

2. Configurar las Variables de Entorno

Crea un archivo .env en la raíz del proyecto (basándote en tu archivo de configuración) con tus credenciales oficiales de OpenAI:

OPENAI_API_KEY=tu_api_key_aqui

3. Instalar Dependencias
Sincroniza el entorno virtual aislado ejecutando:

uv sync

💻 Ejecución del Asistente Interactivo

Para lanzar el asistente de soporte en modo interactivo en tiempo real (CLI), ejecuta el comando modular absoluto desde la raíz:

uv run python -m src.support_assistant.main

🎮 Simulación de Uso en Consola

🤖 [SISTEMA DE SOPORTE INICIADO]
Escribe tu consulta de soporte abajo (o escribe 'salir' para terminar).

👤 Cliente (ingresa tu pregunta): compre una suscripcion ayer y quiero saber cuanto dura?

📥 [CONSULTA PROCESADA]: compre una suscripcion ayer y quiero saber cuanto dura?
🚀 [OUTPUT CONTRATO JSON DOWNSTREAM]
{
  "reasoning": "El cliente consulta por la duración de su suscripción...",
  "answer": "Hola, con gusto verifico los detalles de tu plan...",
  "confidence": 0.95,
  "actions": ["Revisar base de datos de usuarios", "Validar vigencia del plan"]
}
📊 [MÉTRICAS REGISTRADAS]
{
  "latency_ms": 3210.45,
  "prompt_tokens": 235,
  "completion_tokens": 180,
  "total_tokens": 415,
  "estimated_cost_usd": 0.000143
}
============================================================


Estructura del proyecto

## 📂 Estructura del Proyecto

```text
pi-henry/
├── .venv/                 # Entorno virtual aislado gestionado por uv
├── src/
│   └── support_assistant/
│       ├── __pycache__/
│       ├── __init__.py    # Inicializador del paquete modular
│       ├── config.py      # Orquestador de entornos y variables (.env)
│       ├── contracts.py   # Contratos de datos y esquemas rígidos de Pydantic
│       ├── llm.py         # Factoría agnóstica para conmutación de modelos
│       ├── main.py        # Grafo de LangGraph y CLI de simulación interactiva
│       └── nodes.py       # Lógica funcional de seguridad y llamados al LLM
├── .env                   # Variables críticas de entorno (API Keys)
├── .gitignore             # Exclusiones de Git (vicios de compilación y caché)
├── .python-version        # Especificación de versión del intérprete
├── pyproject.toml         # Manifiesto global de dependencias del proyecto
├── README.md              # Guía de inicio rápido y uso del sistema
├── REPORT.md              # Reporte técnico y justificación de arquitectura
└── uv.lock                # Archivo de bloqueo determinista de dependencias


📄 Documentación Técnica Adicional
Para un análisis detallado sobre las decisiones de ingeniería, el control de presupuesto con mitigación adversarial y la justificación técnica de la arquitectura de grafos, consulta el documento de diseño en la raíz del proyecto:

👉 REPORT.md