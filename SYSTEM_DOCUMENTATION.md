# 🌳📜 VOTSai System Documentation

[![Powered by VillageOfThousands.io](docs/assets/powered_by_villageofthousands.gif)](https://VillageOfThousands.io)

Welcome to the **VOTSai System Documentation**! This guide offers a detailed exploration of the VOTSai project, tailored for developers, researchers, and AI enthusiasts. VOTSai is an open-source, Streamlit-based platform integrating **Crawl4AI** for web crawling and **Ollama**'s `deepseek-r1:7b` for local AI assistance. It's designed to empower users with robust research tools, code analysis, and project management capabilities.

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
│   ├── init.py
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
│   ├── init.py
│   ├── query.py          # Query orchestration
│   └── web.py            # Web crawling with Crawl4AI
├── utils/                # Utility functions
│   ├── init.py
│   ├── constants.py      # Constants (e.g., SHORT_TERM_MAX)
│   └── helpers.py        # Helpers (e.g., format_response)
└── venv/                 # Virtual environment (excluded from Git)


---

## 📦 Dependencies
Listed in `requirements.txt`:

streamlit>=1.32.0
crawl4ai>=0.4.3
playwright>=1.50.0
openai>=1.12.0
ollama>=0.1.6
tenacity>=8.2.3
tiktoken>=0.6.0
scikit-learn>=1.4.0
numpy>=1.26.0
mkdocs>=1.6.0
mkdocs-material>=9.5.0

**Install:**
```bash
pip install -r requirements.txt
python -m playwright install

🛠️ How It Works
High-Level Overview
VOTSai is a Streamlit-based web app (app.py) with three tabs:

    Query: Processes web crawls, AI queries, and memory recalls.
    Code Analysis: Offers code review via deepseek-r1:7b.
    Directory & Git: Feeds directory context to the local model.

Workflow:

    User submits a query/code/Git request via UI.
    Intent classifier (core/classifier.py) selects the model.
    Query orchestrator (handlers/query.py) routes the request.
    Results are formatted (utils/helpers.py) and displayed.

🚀 Usage Examples

    Crawl: crawl https://example.com → Summarized HTML.
    Query: how does quantization work? → Explanation from DeepSeek.
    Recall: recall quantum → Past results from SQLite.
    Code: def add(a, b): return a + b → Optimization suggestions.
    Git: suggest a commit message → "Enhance VOTSai with feature X".

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


Update the file using:
```bash
cat << 'EOF' > ~/VOTSai/SYSTEM_DOCUMENTATION.md
# ... (paste the content above) ...
EOF

Step 3: Update MkDocs Pages
You need to add the clickable animated badge to all MkDocs pages under the docs/ directory. The image path depends on the file's location:

    For files in docs/ (e.g., index.md, quickstart.md):
    markdown

[![Powered by VillageOfThousands.io](assets/powered_by_villageofthousands.gif)](https://VillageOfThousands.io)

For files in subdirectories (e.g., docs/core/crawling.md, docs/advanced/config.md):
markdown

    [![Powered by VillageOfThousands.io](../assets/powered_by_villageofthousands.gif)](https://VillageOfThousands.io)

As an example, update docs/index.md:
markdown

# 🚀🤖 Welcome to VOTSai Documentation

[![Powered by VillageOfThousands.io](assets/powered_by_villageofthousands.gif)](https://VillageOfThousands.io)

**VOTSai** is a cutting-edge, open-source platform for AI-driven research, seamlessly integrating **Crawl4AI** for powerful web crawling and local model support with Ollama's `deepseek-r1:7b`.

## 🌟 Why VOTSai?
- **🔍 Advanced Crawling:** Fetch static and dynamic content with Crawl4AI.
- **🧠 Flexible AI:** Choose between Perplexity, DeepSeek, or local models.
- **📚 Smart Memory:** Retain and recall research with SQLite.
- **💻 Code Insights:** Optimize your scripts with AI assistance.
- **📂 Project Awareness:** Local model sees your directory for Git and improvements.

Dive into the [Quick Start](#quick-start) to get up and running in minutes!