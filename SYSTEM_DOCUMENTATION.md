# 🌳📜 VOTSai System Documentation v2.0

[![Powered by VillageOfThousands.io](docs/assets/powered_by_villageofthousands.gif)](https://VillageOfThousands.io)

Welcome to the updated **VOTSai System Documentation**! This guide offers a detailed exploration of the enhanced VOTSai project, tailored for developers, researchers, and AI enthusiasts. VOTSai is an open-source, Streamlit-based platform integrating **Crawl4AI** for web crawling and **Ollama**'s `deepseek-r1:7b` for local AI assistance, with significant architecture improvements.

---

## 🌟 System Architecture (v2.0)

VOTSai now implements a more modular, service-oriented architecture with:

- **📦 Service Layer Pattern:** Decoupling core business logic from data access
- **⚙️ Configuration Management:** Centralized settings via YAML and environment variables
- **🔄 Model Factory & Cache:** Efficient model handling with singleton caching
- **🛡️ Validation & Security:** Enhanced input validation and rate limiting
- **📊 Progress Tracking:** Transparent operation monitoring and reporting

### Core Components

1. **Web Interface Layer (Streamlit)**
   - Provides interactive UI for querying and configuration
   - Manages user session state
   - Renders visualizations and results

2. **Orchestration Layer**
   - Coordinates request flow between components
   - Handles request routing and timeouts
   - Implements memory management

3. **Model Layer**
   - Abstracts different AI model implementations
   - Provides unified interface for queries
   - Handles model caching and resource management

4. **Memory System**
   - Short-term memory (in-memory)
   - Long-term memory (SQLite)
   - Memory service with context retrieval

5. **Analysis Components**
   - Code analyzer
   - Project analyzer
   - Directory & Git utilities

6. **Utilities**
   - Configuration management
   - Token counting & optimization
   - Input validation & sanitization
   - Progress tracking
   - Rate limiting

---

## 📂 Repository Structure (Updated)

```
VOTSai/
├── .env                  # API keys (excluded from Git)
├── .git/                 # Git repository data
├── .gitignore            # Files to exclude from Git
├── .next/                # Next.js artifact (excluded from Git)
├── README.md             # Project overview and quick start
├── SYSTEM_DOCUMENTATION.md # This detailed system guide
├── app.py                # Main Streamlit application
├── config.yaml           # Configuration file
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
│   ├── model_cache.py    # Model caching singleton
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
├── services/             # Service layer
│   ├── __init__.py
│   └── memory_service.py # Memory service
├── tests/                # Test suite
│   ├── __init__.py
│   ├── test_models.py    # Model tests
│   ├── test_memory.py    # Memory tests
│   └── test_integration.py # Integration tests
├── utils/                # Utility functions
│   ├── __init__.py
│   ├── config.py         # Configuration manager
│   ├── constants.py      # Constants (e.g., SHORT_TERM_MAX)
│   ├── helpers.py        # Helpers (e.g., format_response)
│   ├── progress_tracker.py # Progress tracking
│   ├── rate_limiter.py   # Rate limiting
│   ├── token_manager.py  # Token counting & optimization
│   └── validators.py     # Input validation
└── venv/                 # Virtual environment (excluded from Git)
```

---

## 📦 Dependencies (Updated)

Listed in the updated `requirements.txt`:

```
streamlit>=1.38.0
langchain>=0.3.0
langchain-ollama>=0.1.3
faiss-cpu>=1.9.0
pandas>=2.2.3
altair>=5.4.1
markdown>=3.7.0
requests>=2.32.3
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
pyyaml>=6.0.1
```

**Install:**
```
pip install -r requirements.txt
python -m playwright install
```

---

## 🛠️ Architectural Improvements

### 1. Configuration Management
VOTSai now uses a centralized configuration system with:
- YAML config file support
- Environment variable overrides
- Runtime configuration updates
- Type validation and conversion

Example:
```python
from utils.config import Config

# Get configuration values
timeout = Config.get("models.timeout", 60)
db_path = Config.get("memory.db_path", "vots_agi_memory.db")

# Update configuration
Config.set("models.temperature", 0.8)
```

### 2. Service Layer Pattern
Database operations are now encapsulated in service classes:
- Memory service for database operations
- Clear separation of concerns
- Improved error handling
- Connection management

Example:
```python
from services.memory_service import MemoryService

# Using memory service
memory_service = MemoryService("vots_agi_memory.db")
relevant_memories = memory_service.get_relevant_memories("quantum computing", limit=3)
memory_service.add_memory(query="What is AGI?", answer="Artificial General Intelligence...", model_used="DeepSeek API")
```

### 3. Model Caching
Efficient model handling with:
- Singleton cache implementation
- Automatic resource cleanup
- Thread-safe access
- Performance monitoring

Example:
```python
from core.model_cache import ModelCache

# Get or create a model
cache = ModelCache()
model = cache.get_model(
    "DeepSeek API",
    create_deepseek_model,  # Factory function
    api_key="your-api-key"
)

# Periodic maintenance
removed = cache.clean_cache()
print(f"Removed {removed} idle models")
```

### 4. Token Management
Optimized token handling:
- Accurate counting for different models
- Token caching for performance
- Text chunking with overlap
- Cost estimation

Example:
```python
from utils.token_manager import TokenManager

# Count tokens
input_tokens = TokenManager.count_tokens(query + context, "DeepSeek API")

# Truncate if needed
truncated_context = TokenManager.truncate_to_tokens(context, 2000, "DeepSeek API")

# Split into chunks
chunks = TokenManager.split_into_chunks(document, 1000, "DeepSeek API", overlap=100)
```

### 5. Input Validation & Security
Enhanced security with:
- Input validation for all user inputs
- Output sanitization
- URL and code validation
- Parameter validation

Example:
```python
from utils.validators import Validator

# Validate query
is_valid, error = Validator.validate_query(query)
if not is_valid:
    return {"error": error}

# Sanitize output
safe_output = Validator.sanitize_output(model_response)
```

### 6. Progress Tracking
Transparent long-running operations:
- Operation status tracking
- ETA calculation
- Result storage
- Error handling

Example:
```python
from utils.progress_tracker import ProgressTracker

# Start an operation
tracker = ProgressTracker()
op_id = tracker.start_operation("analysis", "Analyzing code...")

# Update progress
tracker.update_progress(op_id, 0.5, "Halfway through analysis")

# Complete the operation
tracker.complete_operation(op_id, {"suggestions": ["Improve error handling", "Add docstrings"]})

# Get operation status
status = tracker.get_operation(op_id)
print(f"Operation {status['id']} is {status['status']} with progress {status['progress']:.1%}")
```

### 7. Rate Limiting
Protection against abuse:
- Request rate limiting
- Token usage tracking
- Client-specific limits
- Usage statistics

Example:
```python
from utils.rate_limiter import RateLimiter

# Check rate limit
limiter = RateLimiter()
within_limit, error = limiter.check_rate_limit("user123")

if not within_limit:
    return {"error": error}

# Record a request with token usage
limiter.record_request("user123", input_tokens=500, output_tokens=200)

# Get usage statistics
stats = limiter.get_usage_stats("user123")
print(f"Requests in last hour: {stats['requests']['last_hour']}")
```

## 8. Prepare for Git

After implementing the changes, prepare for Git with:

```bash
# Create empty __init__.py files in each directory
touch utils/__init__.py
touch services/__init__.py
touch core/__init__.py
touch handlers/__init__.py
touch agents/__init__.py
touch tests/__init__.py

# Add new files to Git
git add config.yaml
git add requirements.txt
git add SYSTEM_DOCUMENTATION.md
git add utils/config.py
git add utils/token_manager.py
git add utils/validators.py
git add utils/progress_tracker.py
git add utils/rate_limiter.py
git add services/memory_service.py
git add core/model_cache.py
git add utils/__init__.py
git add services/__init__.py
git add core/__init__.py
git add handlers/__init__.py
git add agents/__init__.py
git add tests/__init__.py

# Commit the changes
git commit -m "Implement architectural improvements for VOTSai v2.0

- Add configuration management system
- Implement service layer pattern
- Add model caching
- Add token management
- Implement input validation
- Add progress tracking
- Add rate limiting
- Update documentation"

# Push changes
git push origin main
```