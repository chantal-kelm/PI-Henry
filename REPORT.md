# REPORTE TÉCNICO: SISTEMA OPERATIVO DE SOPORTE DESACOPLADO E INTERACTIVO MEDIANTE LANGGRAPH

## 1. Introducción y Objetivos

El presente documento detalla la arquitectura y el diseño técnico de un agente automatizado de soporte al cliente de nivel de producción.


## 2. Arquitectura del Grafo y Entorno Interactivo (REPL)

El sistema implementa una topología de orquestación basada en grafos cíclicos y acíclicos dirigidos (DAGs) utilizando **LangGraph**. A diferencia de los desarrollos monolíticos tradicionales, el flujo de ejecución se desacopla completamente en nodos funcionales aislados y se envuelve en una **interfaz de línea de comandos (CLI) interactiva en tiempo real** mediante un bucle continuo de entrada (*Read-Eval-Print Loop*):

```text
 👤 [Input Cliente en Vivo] ──► 🔄 [Bucle REPL / main.py]
                                       │
                                       ▼
                               ┌───────────────┐
                               │ security_check│
                               └───────┬───────┘
                                       │
                    ┌──────────────────┴──────────────────┐
          (Pasa Filtro) │                                     │ (Bloqueo Adversarial)
                        ▼                                     ▼
                ┌───────────────┐                     ┌───────────────┐
                │assistant_node │                     │    [ END ]    │
                └───────┬───────┘                     └───────────────┘
                        │                                     ▲
                        └─────────────────────────────────────┘

```

* **`security_check_node` (Filtro Perimetral):** Evalúa dinámicamente la consulta inyectada por el usuario en la consola mediante heurísticas de seguridad para detectar inyecciones de prompt adversariales (*Prompt Injections*). Si el sistema detecta patrones maliciosos, intercepta el control usando la primitiva `Command(goto=END)`, cortando la ejecución inmediatamente.
* **`assistant_node` (Procesamiento Inteligente):** Nodo operativo encargado de invocar al modelo de lenguaje seleccionado si la consulta supera con éxito el filtro de seguridad del perímetro.


## 3. Decisiones de Ingeniería y Optimización

### A. Factoría de Modelos Agnóstica (Abstracción del Proveedor)

Utilizando la abstracción `init_chat_model` de LangChain en el componente `llm.py`, la lógica de negocio queda completamente aislada del proveedor de infraestructura de IA (OpenAI, Anthropic, etc.).

* **Impacto:** Permite la migración inmediata entre modelos en caliente modificando únicamente las variables de entorno (`.env`), eliminando el acoplamiento técnico (*vendor lock-in*).

### B. Gestión de Costos Inteligente y Guardrail Perimetral

Para optimizar el presupuesto corporativo y proteger la infraestructura de ataques de denegación de servicio (*DoS*) o spam, la mitigación perimetral opera a costo cero.

* **Resultados Experimentales:** Como se demuestra en las métricas de ejecución, ante una consulta adversarial (*"Ignora las instrucciones anteriores..."*), el sistema responde en 0.0 ms consumiendo un total de **0 tokens**, lo que equivale a un costo exacto de **$0.000000 USD**.

### C. Selección Eficiente del Modelo (*LLM Selection*)

Se preconfiguró el modelo `gpt-4o-mini` debido a su sobresaliente balance entre latencia, capacidades multitarea y eficiencia económica. Con tarifas competitivas de $0.15 USD por millón de tokens de entrada y $0.60 USD por millón de tokens de salida, una transacción legítima promedio de soporte dentro del flujo computa un coste real insignificante de **$0.000179 USD**, maximizando el retorno de inversión corporativo.


## 4. Contratos de Datos y Validaciones Downstream

Un pilar crítico en la ingeniería de software moderna es el determinismo de los datos. Para garantizar que cualquier sistema externo (bases de datos, interfaces de usuario o ERPs) procese la información de manera segura, se implementó una estrategia de **Salidas Estructuradas Nativa** (`with_structured_output`) vinculada a modelos de validación de **Pydantic** (`AssistantResponse`).

El sistema obliga al LLM a empaquetar de manera determinista un esquema JSON estructurado que incluye obligatoriamente:

1. **`reasoning`:** Espacio aislado para que el modelo aplique *Chain of Thought* (CoT) antes de resolver.
2. **`answer`:** El mensaje final limpio orientado al usuario.
3. **`confidence`:** Un indicador decimal flotante de confianza.
4. **`actions`:** Un array plano de subtareas accionables recomendadas para el agente humano.


## 5. Telemetría, Métricas Nativas y Simulación en Vivo

El pipeline está diseñado bajo estándares de producción independientes, prescindiendo por completo de dependencias comunitarias externas no esenciales para auditar el uso. En su lugar, el sistema extrae directamente en caliente el objeto de metadatos nativo `usage_metadata` que inyecta el motor de inferencia de LangChain v0.3 en su ciclo de respuesta.

Gracias a la incorporación de la interfaz interactiva por consola, el sistema permite realizar pruebas de estrés en caliente (*ad-hoc testing*). Esto facilita la evaluación inmediata del comportamiento del agente tras cada consulta, exponiendo con total transparencia las latencias físicas del backend (`latency_ms`), el volumen granular de tokens procesados (`prompt_tokens`, `completion_tokens`) y los costos financieros reales proyectados por cada ejecución.

## 6. Estrategia de Testing Automatizado y Validación de Regresión
Para garantizar la estabilidad del sistema ante futuros cambios en el código o actualizaciones en las instrucciones del LLM, se integró una suite de pruebas automatizadas mediante **Pytest** (`test_pipeline.py`).

La prueba unitaria implementada automatiza el control de calidad ejecutando las siguientes validaciones deterministas sin intervención humana:
1. **Validación del Contrato de Rechazo:** Verifica de forma matemática que el nodo de seguridad detecte inyecciones de prompt complejas y devuelva exactamente la estructura JSON con el estado `REJECTED` y el mensaje de error correspondiente.
2. **Auditoría Estricta de Consumo de API:** Confirma mediante aserciones (`assert`) que el volumen total de tokens consumidos y el costo financiero estimado sean **estrictamente 0.0**, garantizando que el guardrail perimetral corte el flujo antes de generar gastos innecesarios.

Este enfoque permite mitigar de forma automatizada posibles regresiones de seguridad durante ciclos de integración continua (CI/CD).


## 7. Conclusión
La arquitectura presentada demuestra la viabilidad de implementar agentes de IA controlados, seguros y de costo predecible. La integración de un bucle CLI interactivo montado sobre un estado validado por Pydantic, respaldado por una suite de pruebas automatizadas, no solo soluciona los problemas clásicos de aleatoriedad en los LLMs, sino que transforma el proyecto en una herramienta auditable, resiliente a fallos y lista para su despliegue seguro en entornos corporativos reales.