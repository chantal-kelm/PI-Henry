# Support Assistant Agent 🤖 (LangGraph Pipeline)

Este proyecto implementa un agente automatizado e interactivo de soporte al cliente utilizando una arquitectura de grafos orientada a nodos con **LangGraph** y validación estricta de datos mediante contratos **Pydantic**.

El sistema incluye mitigación perimetral de seguridad para interceptar inyecciones de prompt maliciosas a costo cero y telemetría nativa para auditar el consumo exacto de la API.


## 🏗️ Arquitectura del Sistema

El flujo de control se desacopla en nodos funcionales aislados dentro de un bucle interactivo continuo por consola (CLI):

1. **`security_check_node`**: Analiza heurísticamente el input del cliente en busca de frases adversariales. Si detecta un ataque, desvía el flujo inmediatamente al final (`END`) sin tocar la API de pago.

2. **`assistant_node`**: Invoca de manera estructurada al modelo `gpt-4o-mini` para procesar consultas legítimas, aplicando *Chain of Thought* (CoT) y calculando las métricas nativas de uso.

## 🧪 Tests Automatizados

El proyecto incluye pruebas unitarias automatizadas mediante `pytest` para validar la integridad de los contratos JSON y el comportamiento del guardrail perimetral (conteo de tokens a cero en ataques).

Para ejecutar la suite de pruebas de forma automática, corre:

```bash
uv run pytest src/support_assistant/test_pipeline.py
```

## 🚀 Requisitos e Instalación

Este proyecto gestiona sus dependencias mediante **`uv`**, el instalador y gestor de entornos ultra-rápido para Python.

### 1. Clonar el repositorio y posicionarse en la raíz

```bash
cd PI-Henry
```

2. Configurar las Variables de Entorno

Crea un archivo .env en la raíz del proyecto (basándote en tu archivo de configuración) con tus credenciales oficiales de OpenAI:

```bash
OPENAI_API_KEY=tu_api_key_aqui
```

3. Instalar Dependencias
Sincroniza el entorno virtual aislado ejecutando:

```bash
uv sync
```


💻 Ejecución del Asistente Interactivo

Para lanzar el asistente de soporte en modo interactivo en tiempo real (CLI), ejecuta el comando modular absoluto desde la raíz:

```bash
uv run python -m src.support_assistant.main
```

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



## 📂 Estructura del Proyecto

```text
pi-henry/
├── .venv/                 # Entorno virtual de Python (uv)
├── src/                   # Directorio de código fuente
│   └── support_assistant/ # Módulo principal del agente
│       ├── __pycache__/
│       ├── __init__.py    # Inicializador de paquete
│       ├── config.py      # Carga de entornos (.env)
│       ├── contracts.py   # Modelos y contratos Pydantic
│       ├── llm.py         # Factoría de conmutación de LLM
│       ├── main.py        # Grafo LangGraph y CLI interactiva
│       ├── nodes.py       # Nodos de seguridad y asistente
│       └── test_pipeline.py # Tests automatizados con Pytest
├── .env                   # Credenciales privadas de OpenAI
├── .gitignore             # Archivos excluidos de Git
├── .python-version        # Versión local activa de Python
├── pyproject.toml         # Dependencias y configuraciones
├── README.md              # Guía de inicio rápido (este archivo)
├── REPORT.md              # Reporte de arquitectura técnica
└── uv.lock                # Bloqueo de dependencias de uv
```

## Documentación Técnica Adicional
Para un análisis detallado sobre las decisiones de ingeniería, el control de presupuesto con mitigación adversarial y la justificación técnica de la arquitectura de grafos, consulta el documento de diseño en la raíz del proyecto:

👉 REPORT.md