# Model Integration Guide

TRILOGY Brain is designed to work with various AI models, both local and API-based. This guide explains how to integrate new models into the system.

## Supported Model Types

- **Local Ollama Models**: Run models locally with Ollama
- **Claude API**: Connect to Anthropic's Claude API
- **DeepSeek API**: Connect to DeepSeek's API
- **Custom Models**: Integrate your own model implementations

## Adding a New Model

### 1. Create a Model Implementation

First, create a new Python file in the `models` directory that implements the model interface:

```python
# Example: models/my_custom_model.py

import logging
from typing import Dict, Any, List, Optional

logger = logging.getLogger(__name__)

class MyCustomModel:
    """Custom model implementation"""
    
    def __init__(self, **config):
        """Initialize the model with configuration"""
        self.config = config
        logger.info(f"Initialized custom model with config: {config}")
        
    def is_available(self) -> bool:
        """Check if the model is available"""
        # Implement availability check
        return True
        
    def generate(self, 
                prompt: str, 
                **kwargs) -> Dict[str, Any]:
        """Generate a response from the model"""
        # Implement generation logic
        response = "This is a response from my custom model"
        
        return {
            "text": response,
            "model": "my_custom_model",
            "metadata": {
                "execution_time": 0.5,
                "total_tokens": 10
            }
        }
        
    def chat(self, 
            messages: List[Dict[str, str]], 
            **kwargs) -> Dict[str, Any]:
        """Chat with the model using a messages array"""
        # Implement chat logic
        return self.generate(" ".join([m["content"] for m in messages]))
```

### 2. Register the Model in the Registry

Next, update the model registry to include your new model:

```python
# In trilogy_app.py or where you initialize the system

# Import your custom model
from models.my_custom_model import MyCustomModel

# Register the model
model_registry.register_model(
    name="my_custom_model",
    model_type="custom",
    config={"param1": "value1"},
    initializer=lambda config: MyCustomModel(**config)
)
```

### 3. Add Model Strengths to the Router

To help the router make intelligent decisions, add your model to the strengths configuration:

```python
# In core/router.py

def _score_model_for_query(self, model_name: str, analysis: Dict[str, Any]) -> float:
    # Define model strengths by domain
    model_strengths = {
        # Existing models...
        "my_custom_model": {
            "general": 0.7,
            "coding": 0.6,
            "math": 0.8,
            # Add strengths for other domains
        }
    }
    # Rest of the method...
```

## Using the Model Registry YAML

Alternatively, you can define models in the `config/models.yaml` file:

```yaml
my_custom_model:
  type: custom
  config:
    param1: value1
    param2: value2
```

Then ensure your model class is imported and registered automatically by updating the ModelRegistry._load_config method.

## Testing Your Model

To test your model integration:

1. Start TRILOGY Brain with your new model registered
2. Go to the Settings tab
3. Select your model from the "Default Model" dropdown
4. Try sending queries in the Neural Interface tab

## Common Issues

### Missing Dependencies

Ensure all required dependencies for your model are installed:

```bash
pip install -r requirements.txt
```

### Model Not Appearing

If your model doesn't appear in the list:

1. Check the logs for registration errors
2. Verify that the model is properly registered
3. Ensure the model initialization doesn't throw exceptions

### Performance Tuning

To improve model performance:

1. Use caching for repeated operations
2. Optimize input/output processing
3. Consider batch processing for high-volume workloads

## API-based Models

When implementing API-based models, consider:

1. API key management (environment variables or secure storage)
2. Rate limiting and quota management
3. Error handling for network issues
4. Fallback mechanisms when the API is unavailable 