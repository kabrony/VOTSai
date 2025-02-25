# Troubleshooting Guide

This guide helps resolve common issues with TRILOGY Brain.

## Installation Issues

### Module Not Found Errors

```
ModuleNotFoundError: No module named 'xyz'
```

**Solution**: Install the missing package:

```bash
pip install xyz
```

### Ollama Connection Issues

```
Ollama server not available
```

**Solutions**:

1. Check if Ollama is running:
   ```bash
   # Start Ollama
   ollama serve
   ```

2. Verify Ollama API is accessible:
   ```bash
   curl http://localhost:11434/api/tags
   ```

3. Check firewall settings that might block the connection

## Runtime Errors

### Model Initialization Failures

```
Error getting model: Model not found
```

**Solutions**:

1. Check if the model is available:
   ```bash
   ollama list  # For local models
   ```

2. Pull the required model:
   ```bash
   ollama pull llama2
   ```

3. Verify the model configuration in `config/models.yaml`

### Memory System Errors

```
Error saving memories: [Errno 2] No such file or directory
```

**Solutions**:

1. Create the directory structure:
   ```bash
   mkdir -p data/memories
   ```

2. Check file permissions:
   ```bash
   chmod 755 data
   chmod 755 data/memories
   ```

## Performance Issues

### Slow Response Times

**Solutions**:

1. Check system resources (CPU, memory)
2. Reduce model parameter size
3. Enable response streaming
4. Use a faster model for simpler queries

### High Memory Usage

**Solutions**:

1. Reduce the memory system's `max_items` parameter
2. Use smaller models
3. Implement memory flushing at regular intervals
4. Close unused model instances

## UI Issues

### Styling Not Applied

**Solutions**:

1. Clear browser cache
2. Ensure CSS is properly formatted
3. Check for JavaScript errors in browser console
4. Try a different browser

### Interface Responsiveness

**Solutions**:

1. Reduce animation effects
2. Optimize data loading
3. Implement pagination for large datasets
4. Use Streamlit caching

## API Integration Issues

### API Key Issues

```
Authentication error: Invalid API key
```

**Solutions**:

1. Verify API key is correct
2. Check if API key is expired
3. Use environment variables for API keys:
   ```bash
   export ANTHROPIC_API_KEY=your_key_here
   ```

### Rate Limiting

```
Rate limit exceeded
```

**Solutions**:

1. Implement backoff and retry logic
2. Reduce request frequency
3. Contact API provider for higher limits
4. Add request queuing

## Debug Mode

Enable debug mode to get more detailed logs:

```bash
export LOG_LEVEL=DEBUG
streamlit run trilogy_app.py
```

## Getting Help

If you encounter issues not covered in this guide:

1. Check the logs in `trilogy_brain.log`
2. Review the [documentation](README.md)
3. Create an issue on the GitHub repository
4. Contact VillageOfThousands.io support 