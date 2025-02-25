# Getting Started with TRILOGY Brain

This guide will walk you through the process of setting up and using TRILOGY Brain, the advanced AI orchestration system.

## Prerequisites

- Python 3.8 or later
- Streamlit 1.28.0 or later
- Ollama (for local model integration)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/villageofthousands/trilogy-brain.git
   cd trilogy-brain
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up Ollama (for local model integration):
   ```bash
   # Install Ollama
   curl -fsSL https://ollama.com/install.sh | sh
   
   # Pull a model
   ollama pull llama2
   ```

## Running TRILOGY Brain

1. Start the application:
   ```bash
   streamlit run trilogy_app.py
   ```

2. Access the UI in your browser at `http://localhost:8501`

## Using TRILOGY Brain

### Neural Interface

The Neural Interface is where you can interact with TRILOGY Brain through a chat interface. Simply type your query and TRILOGY Brain will select the appropriate model to process it.

### System Dashboard

The System Dashboard provides insights into the system's performance, including:
- Active models
- Response times
- Model usage statistics

### Model Selection

TRILOGY Brain automatically selects the best model for your query, but you can also manually select a model in the Settings tab.

### Memory Explorer

The Memory Explorer allows you to view past conversations and how TRILOGY Brain uses them for context.

## Configuration

You can configure TRILOGY Brain by modifying the files in the `config` directory:

- `models.yaml`: Define available models and their configurations
- `router.yaml`: Configure the routing logic
- `memory.yaml`: Configure the memory system

## Next Steps

- Explore the [API Reference](api_reference.md) for programmatic access
- Learn about [Model Integration](model_integration.md) to add custom models
- Check out [UI Customization](ui_customization.md) to adapt the interface to your needs 