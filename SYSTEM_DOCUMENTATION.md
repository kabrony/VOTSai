#### Updated `SYSTEM_DOCUMENTATION.md`
Incorporating the same badge and ensuring consistency:

```bash
cat << 'EOF' > ~/VOTSai/SYSTEM_DOCUMENTATION.md
# 🌳📜 VOTSai System Documentation

Welcome to the **VOTSai System Documentation**! This guide offers a detailed exploration of the VOTSai project, tailored for developers, researchers, and AI enthusiasts. VOTSai is an open-source, Streamlit-based platform integrating **Crawl4AI** for web crawling and **Ollama**’s `deepseek-r1:7b` for local AI assistance. It’s designed to empower users with robust research tools, code analysis, and project management capabilities.

![Powered by VillageOfThounds.io](https://img.shields.io/badge/Powered%20by-VillageOfThounds.io-blueviolet?style=flat&logo=data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjAwIiBoZWlnaHQ9IjUwIiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciPjx0ZXh0IHg9IjUwJSIgeT0iNTAlIiBkb21pbmFudC1iYXNlbGluZT0ibWlkZGxlIiB0ZXh0LWFuY2hvcj0ibWlkZGxlIiBmaWxsPSIjZmZmZmZmIj5Qb3dlcmVkIGJ5IFZpbGxhZ2VPZlRob3VuZHMuaW88L3RleHQ+PC9zdmc+)

---

## 🌟 System Overview (High-Level)

### What is VOTSai?
VOTSai is built for developers, researchers, and AI enthusiasts, providing:
- **🔍 Web Crawling:** Fetch static and dynamic content with Crawl4AI.
- **🧠 AI Queries:** Leverage Perplexity API, DeepSeek API, or local `deepseek-r1:7b`.
- **💻 Code Analysis:** Enhance scripts with AI-driven insights.
- **📚 Memory Management:** Store and recall research via SQLite and in-memory deque.
- **📂 Project Assistance:** Local model access to directory contents for Git and improvements.

### Purpose
Enable seamless research, project optimization, and local AI assistance through an intuitive, extensible interface—runnable locally or hosted on the cloud.

### Key Technologies
- **Streamlit:** Interactive web UI.
- **Crawl4AI:** Advanced crawling with Playwright.
- **Ollama:** Hosts `deepseek-r1:7b` locally.
- **SQLite:** Persistent storage for long-term memory.

---

## 📂 Repository Structure (Tree)

Here’s the full tree of `~/VOTSai/`:

```plaintext
VOTSai/
├── .env                  # API keys (excluded from Git)
├── .git/                 # Git repository data
├── .gitignore            # Files to exclude from Git
├── .next/                # Next.js artifact (excluded from Git)
├── README.md             # Project overview and quick start
├── SYSTEM_DOCUMENTATION.md # This detailed system guide
├── app.py                # Main Streamlit application
├── mkdocs.yml            # MkDocs configuration
├── requirements.txt      # Python dependencies
├── vots_agi.log          # Runtime logs (excluded from Git)
├── vots_agi_memory.db    # SQLite database (excluded from Git)
├── votsai-backup-*.tar.gz # Backup file (excluded from Git)
├── agents/               # Agent scripts
│   └── codeAgent.py      # Code analysis with DeepSeek
├── core/                 # Core functionality
│   ├── __init__.py
│   ├── classifier.py     # Intent classifier for model selection
│   ├── memory.py         # Memory management (SQLite)
│   └── models.py         # Model factory and implementations
├── docs/                 # MkDocs documentation pages
│   ├── index.md          # Home page
│   ├── quickstart.md     # Quick start guide
│   ├── core/             # Core features
│   │   ├── crawling.md
│   │   ├── queries.md
│   │   ├── memory.md
│   │   ├── code_analysis.md
│   │   └── directory_git.md
│   ├── advanced/         # Advanced usage
│   │   ├── config.md
│   │   └── examples.md
│   ├── deployment.md     # Deployment instructions
│   └── contributing.md   # Contributing guide
├── handlers/             # Query and web handling
│   ├── __init__.py
│   ├── query.py          # Query orchestration
│   └── web.py            # Web crawling with Crawl4AI
├── utils/                # Utility functions
│   ├── __init__.py
│   ├── constants.py      # Constants (e.g., SHORT_TERM_MAX)
│   └── helpers.py        # Helpers (e.g., format_response)
└── venv/                 # Virtual environment (excluded from Git)

📦 Dependencies
VOTSai relies on these Python packages, listed in requirements.txt:
plaintext

streamlit>=1.32.0         # Web app framework
crawl4ai>=0.4.3           # Web crawling with Playwright
playwright>=1.50.0        # Browser automation for Crawl4AI
openai>=1.12.0            # API client for Perplexity/DeepSeek
ollama>=0.1.6             # Local model hosting
tenacity>=8.2.3           # Retry logic
tiktoken>=0.6.0           # Token counting
scikit-learn>=1.4.0       # Intent classification
numpy>=1.26.0             # Numerical operations
mkdocs>=1.6.0             # Documentation generator
mkdocs-material>=9.5.0    # Material theme for MkDocs

Installation
bash

pip install -r requirements.txt
python -m playwright install

🛠️ How It Works
High-Level Overview
VOTSai is a Streamlit-based web application (app.py) with three interactive tabs:

    Query: Processes web crawls, AI queries, and memory recalls.
    Code Analysis: Offers code review via deepseek-r1:7b.
    Directory & Git: Feeds directory context to the local model for project assistance.

Workflow:

    User submits a query, code, or Git request via the UI.
    Intent classifier (core/classifier.py) determines the model.
    Query orchestrator (handlers/query.py) routes the request:
        Crawls via Crawl4AI (handlers/web.py).
        Queries models (core/models.py).
        Manages memory (core/memory.py).
    Results are formatted (utils/helpers.py) and displayed with metadata.

Mid-Level Components

    Frontend (app.py):
        Purpose: Streamlit UI with tabs and sidebar for configuration.
        Inputs: Queries (e.g., "crawl https://example.com"), code snippets, Git requests.
        Outputs: Formatted responses (Text/Markdown/JSON) with latency and reasoning.
    Crawling (handlers/web.py):
        Purpose: Fetches web content using Crawl4AI’s AsyncWebCrawler.
        Details: Handles timeouts, logs errors, returns HTML for summarization.
    Model Management (core/models.py):
        Purpose: Manages model selection and querying.
        Details: ModelFactory uses IntentClassifier to pick Perplexity, DeepSeek, or local deepseek-r1:7b.
    Memory System (core/memory.py):
        Purpose: Stores and retrieves queries/results.
        Details: SQLite for long-term, deque (max 15) for short-term.
    Code Analysis (agents/codeAgent.py):
        Purpose: Analyzes code with deepseek-r1:7b.
        Details: Async queries via Ollama API.
    Utilities (utils/):
        Purpose: Supports constants and formatting.
        Details: constants.py (e.g., SHORT_TERM_MAX=15), helpers.py (e.g., format_response).

Low-Level Details

    Crawling Implementation:
    python

# handlers/web.py
async def crawl_url(url: str, timeout: int) -> str:
    async with AsyncWebCrawler(verbose=True) as crawler:
        result = await crawler.arun(url=url, timeout=timeout * 1000)
        return result.html if result.success else raise Exception(result.error_message)

Model Selection Logic:
python

# core/models.py
def select_model(self, query: str, user_selected: str, web_priority: bool, classifier):
    if user_selected != "Auto":
        return self.create_model(user_selected)
    intent = classifier.predict(query)
    if web_priority or intent == "web_search":
        return self.create_model("Perplexity API")
    elif intent in ["technical", "conceptual"]:
        return self.create_model("DeepSeek API")
    return self.create_model("Local DeepSeek")

Memory Management:
python

# core/memory.py
def update_memory(conn, query, result, short_term_memory):
    short_term_memory.append({"query": query, "answer": result['answer'], "model": result['model_name']})
    if len(short_term_memory) > SHORT_TERM_MAX:
        oldest = short_term_memory.popleft()
        c = conn.cursor()
        c.execute("INSERT INTO long_term_memory VALUES (?, ?, ?, ?, ?, ?)", 
                  (None, oldest["query"], oldest["answer"], datetime.now().isoformat(), None, oldest["model"]))
        conn.commit()

Directory Access:
python

    # app.py
    def get_directory_contents():
        dir_path = os.getcwd()
        contents = os.listdir(dir_path)
        return "\n".join([f"- {item}" + (" (dir)" if os.path.isdir(os.path.join(dir_path, item)) else "") for item in contents])

🚀 Usage Examples

    Crawl: crawl https://example.com → Summarized HTML content.
    Query: how does quantization work? → Detailed explanation from DeepSeek.
    Recall: recall quantum → Past query results from SQLite.
    Code: def add(a, b): return a + b → Optimization suggestions.
    Git: suggest a commit message → "Enhance VOTSai with new feature X".

📋 Deployment
Local
bash

streamlit run app.py

Streamlit Cloud

    Push to GitHub: git push origin main
    Configure at streamlit.io/cloud:
        Repo: kabrony/VOTSai
        Branch: main
        File: app.py
    Add secrets: .env contents.

GitHub Pages (Docs)
bash

mkdocs gh-deploy

    Visit https://kabrony.github.io/VOTSai.