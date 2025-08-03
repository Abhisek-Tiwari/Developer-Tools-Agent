# Developer-Tools-Agent 🛠️🤖

An intelligent, LLM-powered assistant that helps developers choose and compare the best tools for their workflows — from CI/CD to testing frameworks and beyond. This agent uses OpenAI and Firecrawl APIs to generate real-time, reasoned recommendations based on context.

---

## ✨ Features

- ✅ Compare tools: “Which is better — Jest or Mocha?”
- ✅ Make tool recommendations based on use case
- ✅ Uses OpenAI and Firecrawl for dynamic, intelligent responses
- ✅ Modular code structure, easy to extend and customize

---

## 🧰 Tech Stack

**Core Language:** Python  
**Agent Frameworks:**  
- [LangChain](https://www.langchain.com/)
- [LangGraph](https://github.com/langchain-ai/langgraph)

**APIs Used:**  
- [OpenAI](https://openai.com/)
- [Firecrawl](https://www.firecrawl.dev/)

**Environment Management:**  
- [`python-dotenv`](https://pypi.org/project/python-dotenv/)  
- [uv](https://github.com/astral-sh/uv) (instead of pip/venv)

**Dependencies (from `pyproject.toml`):**
```toml
firecrawl-py >= 2.15.0
langchain >= 0.3.26
langchain-openai >= 0.3.27
langgraph >= 0.5.2
pydantic >= 2.11.7
python-dotenv >= 1.1.1
```

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/Abhisek-Tiwari/Developer-Tools-Agent.git
cd Developer-Tools-Agent
```

### 2. Set Up Environment

Create a `.env` file in the project root with the following keys:

```env
FIRECRAWL_API_KEY=your_firecrawl_api_key
OPENAI_API_KEY=your_openai_api_key
```

Make sure the file is located at:

```
.env
```

### 3. Create Virtual Environment (with `uv`)

This project uses [`uv`](https://github.com/astral-sh/uv), not `pip`:

```bash
uv venv
source .venv/bin/activate
uv pip install -e .
```

> Make sure to activate the `.venv/` environment for all development work.

---

## 📁 Project Structure

```
Developer-Tools-Agent/
├── .venv/                  # Virtual environment (created via uv)
├── .env                    # API keys for Firecrawl and OpenAI
├── .python-version         # Python version pinning
├── main.py                 # Entry point to run the agent
├── pyproject.toml          # Project metadata & dependencies
├── README.md
└── src/
    ├── __init__.py
    ├── agent.py            # Main LangGraph agent logic
    ├── firecrawl.py        # Integration with Firecrawl API
    ├── model.py            # Model configuration & setup
    └── prompt_handling.py  # Prompt parsing and formatting
```

---

## ▶️ Running the Agent

After setup, you can run the agent via:

```bash
uv run main.py
```

Then interact with it like:

> "Which CI/CD tool should I use for my Python project?"

> "Should I use ESLint or Rome for linting in a React app?"

---

## 🧪 Example Query

```text
> Which JavaScript testing framework is better: Jest or Mocha?
Answer:
Jest is typically preferred for modern JS apps due to its built-in mocking, snapshot testing, and integration with React. Mocha is more flexible but requires more configuration...
```

---

## 🧠 Extending the Agent

- Add new capabilities in `src/agent.py`
- Define additional Firecrawl utilities in `src/firecrawl.py`
- Modify prompt handling in `src/prompt_handling.py`
- Customize model behavior in `src/model.py`

---

## 🤝 Contributing

Pull requests are welcome! Open issues, submit fixes, or create your own tools logic.

---

## 📄 License

MIT