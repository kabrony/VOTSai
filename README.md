# 🚀🤖 VOTSai: Advanced AI Research Platform with Crawl4AI Integration

**VOTSai** is a powerful, open-source, Streamlit-based platform designed for AI-driven research, enhanced with **Crawl4AI** for robust web crawling and local model support via Ollama’s `deepseek-r1:7b`. Explore the web, analyze code, and leverage memory with a sleek, user-friendly interface.

![Powered by VillageOfThounds.io](https://img.shields.io/badge/Powered%20by-VillageOfThounds.io-blueviolet?style=flat&logo=data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjAwIiBoZWlnaHQ9IjUwIiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciPjx0ZXh0IHg9IjUwJSIgeT0iNTAlIiBkb21pbmFudC1iYXNlbGluZT0ibWlkZGxlIiB0ZXh0LWFuY2hvcj0ibWlkZGxlIiBmaWxsPSIjZmZmZmZmIj5Qb3dlcmVkIGJ5IFZpbGxhZ2VPZlRob3VuZHMuaW88L3RleHQ+PC9zdmc+)

---

## 🌟 Features

- **🔍 Robust Web Crawling:** Powered by Crawl4AI, crawl static and dynamic pages with JavaScript rendering.
- **🧠 Multi-Model Support:** Query Perplexity API, DeepSeek API, or local `deepseek-r1:7b` with intent-based selection.
- **📚 Memory System:** Persistent SQLite database for long-term memory, paired with short-term deque tracking.
- **💻 Code Analysis:** DeepSeek-powered code review and improvement suggestions.
- **📂 Directory Insights:** Local model access to project files for Git and optimization help.
- **📜 Structured Output:** Responses in Text, Markdown, or JSON with shareable links.

---

## 📦 Quick Start

### Prerequisites
- **Python 3.12+**
- **Git**
- **Virtual Environment** (`venv`)
- **Ollama** (for local `deepseek-r1:7b`)

### Installation
```bash
git clone https://github.com/kabrony/VOTSai.git
cd VOTSai
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python -m playwright install  # Install Crawl4AI browser dependencies

Running Locally

    Start Ollama (if using local model):
    bash

ollama run deepseek-r1:7b

Launch VOTSai:
bash

    streamlit run app.py

        Open http://localhost:8501 in your browser.

Configuration
Set API keys in .env:
plaintext

PERPLEXITY_API_KEY=your_perplexity_key
DEEPSEEK_API_KEY=your_deepseek_key

🛠️ Core Features
Web Crawling with Crawl4AI
Crawl any URL with advanced JavaScript rendering:

    Query: crawl https://example.com
    Result: Summarized content in your chosen format (Text, Markdown, JSON).

Multi-Model Queries

    General/Web: Perplexity API (e.g., "what is quantum AGI?").
    Technical/Conceptual: DeepSeek API or local deepseek-r1:7b (e.g., "how does quantization work?").
    Auto Selection: Intent-based model choice via Naive Bayes classifier.

Memory Management

    Short-Term: Tracks last 15 queries in-memory.
    Long-Term: Stores queries and answers in vots_agi_memory.db.
    Recall: Use recall <query> to retrieve past results.

Code Analysis
Analyze code snippets with deepseek-r1:7b:

    Input: def add(a, b): return a + b
    Output: Suggestions for optimization or error handling.

Directory & Git Assistance

    Directory View: See ~/VOTSai/ contents in the app.
    Git Help: Query "suggest a commit message" or "how to push to GitHub" for local model advice.

📈 Advanced Usage
Customizing Queries

    Timeout: Adjust crawl/query timeout (10-120s) in the sidebar.
    Creativity: Tune model temperature (0-100) for creative responses.
    Web Priority: Toggle web integration for Perplexity API usage.

Example Queries

    Crawl: crawl https://news.ycombinator.com
    General: explain quantum computing
    Recall: recall quantum
    Git: suggest a commit message for adding crawl4ai

Local Model Enhancements
Feed directory contents to deepseek-r1:7b:

    Query: "improve app.py"
    Response: Tailored suggestions based on your codebase.

📝 Documentation
Quick Start
Basic setup instructions (see above).
Core Features
Detailed guides for each capability (Crawling, Queries, Memory, etc.).
Advanced Usage
Tips for power users (custom timeouts, creativity tuning).
API Reference

    Coming Soon: Full code-level docs for developers.

🌐 Deployment
Hosted on Streamlit Community Cloud:
bash

# Deploy Steps
1. Push to GitHub: `git push origin main`
2. Configure on Streamlit Cloud:
   - Repo: kabrony/VOTSai
   - Branch: main
   - File: app.py
3. Add Secrets: PERPLEXITY_API_KEY, DEEPSEEK_API_KEY

    Note: SQLite memory is ephemeral on Cloud; use locally for persistence.

🤝 Contributing

    Star Us: Show support on GitHub!
    Fork & PR: Add features, fix bugs, or enhance docs.
    Issues: Report problems or suggest ideas.

🙌 Thanks
Built with ❤️ by kabrony, powered by Crawl4AI’s awesome community and Ollama’s local model magic.