# TRILOGY Brain

<div align="center">
  <img src="docs/images/trilogy_logo.png" alt="TRILOGY Brain Logo" width="300px">
  <br>
  <h3>Advanced AI Orchestration System</h3>
  <p>Seamlessly integrate multiple AI models with chain-of-thought reasoning</p>
  
  [![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
  [![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/downloads/)
  [![Powered by VillageOfThousands](https://img.shields.io/badge/Powered%20by-VillageOfThousands-purple)](https://villageofthousands.io)
</div>

## 🚀 Features

- **Multi-Model Orchestration**: Seamlessly use local and API-based models
- **Intelligent Router**: Auto-selects the optimal model based on query characteristics
- **Chain of Thought Reasoning**: Step-by-step reasoning process visualization
- **Matrix-inspired UI**: Cyberpunk-styled terminal interface
- **Advanced Memory System**: Vector-based semantic memory with visualization
- **Plugin Architecture**: Extend functionality with custom plugins
- **Analytics Dashboard**: Track model performance across different domains

## 🧠 Supported Models

TRILOGY Brain supports a variety of AI models:

- **Local Models** via [Ollama](https://ollama.ai/)
  - Llama 2/3
  - CodeLlama
  - Mistral
  - And any other models available in Ollama

- **API Models**
  - Claude (via Anthropic API)
  - DeepSeek (via DeepSeek API)
  - Perplexity Sonar (with web search capabilities)

## 📋 Requirements

- Python 3.8+
- [Ollama](https://ollama.ai/) (for local model integration)
- API keys for Claude, DeepSeek, or Perplexity (optional)

## 🔧 Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/trilogy-brain.git
cd trilogy-brain

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables (optional for API models)
export ANTHROPIC_API_KEY="your_claude_api_key"
export DEEPSEEK_API_KEY="your_deepseek_api_key"
export PERPLEXITY_API_KEY="your_perplexity_api_key"
```

## 🏃‍♂️ Getting Started

```bash
# Start the UI
streamlit run trilogy_app.py

# Or use the CLI example
python examples/basic_usage.py
```

## 🧩 Architecture

TRILOGY Brain follows a modular architecture:

```
trilogy-brain/
├── core/           # Core orchestration components
│   ├── memory/     # Memory systems
│   ├── reasoning/  # Reasoning systems
│   └── plugins/    # Plugin system
├── models/         # Model integrations
├── ui/             # User interface components
│   └── components/ # Reusable UI components
├── utils/          # Utility functions
├── plugins/        # Plugin implementations
├── docs/           # Documentation
└── api/            # API endpoints
```

The system uses:
- **Chain of Thought Processing**: Advanced reasoning capabilities
- **Intelligent Router**: Optimal model selection
- **Vector Memory System**: Semantic search for conversation history
- **Terminal UI**: Matrix-inspired interface
- **Plugin Architecture**: Extensible functionality

## 🔌 Using Plugins

TRILOGY Brain comes with several built-in plugins:

- **Calculator**: Perform mathematical calculations
- **Translator**: Translate text between languages

You can activate plugins from the Plugins tab in the UI. To create your own plugin:

1. Create a new folder in the `plugins/` directory
2. Implement a class that inherits from one of the plugin base classes
3. Restart the application

See the [Plugin Development Guide](docs/plugin_development_guide.md) for details.

## 📚 Documentation

For full documentation, see the [docs folder](docs/) or visit our [Documentation Site](https://yourusername.github.io/trilogy-brain).

## 🤝 Contributing

Contributions are welcome! Please check out our [Contributing Guidelines](CONTRIBUTING.md).

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgements

- Powered by [VillageOfThousands.io](https://villageofthousands.io)
- Chain of Thought implementation inspired by [Google Research](https://research.google/blog/language-models-perform-reasoning-via-chain-of-thought/)
- Matrix UI inspired by the Matrix film series