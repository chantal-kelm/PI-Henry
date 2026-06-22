## Support Assistant Agent 🤖 (LangGraph Pipeline)

This project implements an automated and interactive customer support agent utilizing a node-oriented graph architecture with LangGraph and strict data validation via Pydantic contracts.

The system features a zero-cost perimetral security guardrail to intercept malicious prompt injections and native telemetry to persistently audit exact API token usage and cost.

### 🏗️ System Architecture

The execution control flow is decoupled into isolated functional nodes operating within a continuous interactive Command Line Interface (CLI) loop:

security_check_node: Heuristically analyzes customer input for adversarial phrases using the independent safety.py module. If an attack is detected, it immediately reroutes the flow to the end (END) without invoking the paid model API.

assistant_node: Structurally invokes the gpt-4o-mini model, parsing the external prompt template, applying Chain-of-Thought (CoT) reasoning, and calculating native usage metrics.

### 🧪 Automated Tests

The project includes automated unit tests using pytest to validate the integrity of JSON contracts and the behavior of the perimetral guardrail (ensuring zero token consumption during attacks).

To run the official automated test suite, execute the following command from the project root:

uv run pytest tests/test_core.py


### 🚀 Setup & Installation

This project manages its dependencies using uv, the ultra-fast Python package installer and resolver.

1. Clone the Repository and Navigate to the Root

```bash
cd PI-Henry
```

2. Configure Environment Variables

Create a .env file in the root directory of the project with your official OpenAI API credentials:

```bash
OPENAI_API_KEY=your_api_key_here
```

3. Install Dependencies

Synchronize the isolated virtual environment by executing:

```bash
uv sync
```

💻 Running the Interactive Assistant

To launch the main executable application (CLI) in real-time interactive mode, execute the following command from the root directory:

```bash
uv run python src/run_query.py
```

### 🎮 Console Simulation Example

🤖 [SUPPORT SYSTEM INITIALIZED]
Type your support query below or type 'salir' to exit.

👤 Client (enter your question): compre una suscripcion ayer y quiero saber cuanto dura?

📥 [QUERY PROCESSED]: compre una suscripcion ayer y quiero saber cuanto dura?
🚀 [DOWNSTREAM JSON CONTRACT OUTPUT]
{
  "reasoning": "The customer is asking about their subscription duration...",
  "answer": "Hello! I would be happy to help you verify your subscription duration...",
  "confidence": 0.95,
  "actions": ["Check user database", "Validate plan validity"]
}
📊 [METRICS REGISTERED]
{
  "latency_ms": 3210.45,
  "prompt_tokens": 235,
  "completion_tokens": 180,
  "total_tokens": 415,
  "estimated_cost_usd": 0.000143
}


### 📊 Tracking & Reproducing Metrics

Every successful query automatically appends structured usage telemetry to a persistent audit log. To reproduce and check the records:

Interact with the assistant by submitting a valid query using src/run_query.py.

Type salir to safely terminate the session.

Inspect the consolidated JSON report containing timestamps, token counts, latencies, and estimated costs at:

```bash
cat metrics/metrics.json
```

### ⚠️ Known Limitations

External API Dependency: Requires an active internet connection and available credit on the OpenAI API Key to process queries in the assistant nodes.

Static Security Heuristics: The local guardrail intercepts common attack vectors at zero cost, but highly complex, multi-layered prompt injections might require a dedicated LLM-based moderation endpoint.

Simple Local Persistence: Telemetry is stored locally as a flat JSON file, which limits concurrent access in multi-user distributed environments.

### 📂 Project Structure

```bash
pi-henry/
├── .venv/                 # Python virtual environment (uv)
├── src/                   # Main source code directory
│   ├── support_assistant/ # Agent logical module
│   │   ├── __init__.py
│   │   ├── config.py      # Environment (.env) loader and config
│   │   ├── contracts.py   # Pydantic data schemas and contracts
│   │   ├── llm.py         # Agnostic LLM model factory
│   │   ├── main.py        # LangGraph definition & CLI loop
│   │   └── nodes.py       # Execution nodes (security and assistant)
│   ├── run_query.py       # Official entrypoint script (M1 Requirement)
│   └── safety.py          # Perimetral security validation module
├── prompts/               # Required folder for prompt templates
│   └── main_prompt.txt    # Structured system prompt with Few-Shot examples
├── metrics/               # Persistent analytics data directory
│   └── metrics.json       # Telemetry execution logs (JSON format)
├── reports/               # Technical reports and documentation
│   └── PI_report_en.md    # Brief technical architecture report
├── tests/                 # Automated test suite
│   └── test_core.py       # Token count and contract validation tests
├── .env                   # Private OpenAI credentials (git-ignored)
├── .gitignore             # Files and patterns excluded from Git
├── .python-version        # Active local Python version specifier
├── pyproject.toml         # Project dependencies and configurations
└── uv.lock                # Deterministic dependency lock file
```

### Additional Technical Documentation

The comprehensive engineering report covering architectural decisions, prompt engineering techniques (Few-Shot), metrics formulas, and solved technical challenges can be found in the reports folder:

👉 PI_report_en.md