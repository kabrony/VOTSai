# Contributing to TRILOGY Brain

Thank you for your interest in contributing to TRILOGY Brain! This document provides guidelines and instructions for contributing.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Pull Request Process](#pull-request-process)
- [Coding Standards](#coding-standards)
- [Testing](#testing)
- [Documentation](#documentation)

## Code of Conduct

This project adheres to the [Contributor Covenant Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code.

## Getting Started

1. Fork the repository on GitHub
2. Clone your fork locally
   ```bash
   git clone https://github.com/yourusername/trilogy-brain.git
   cd trilogy-brain
   ```
3. Create a virtual environment and install dependencies
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```
4. Set up a development branch
   ```bash
   git checkout -b feature/your-feature-name
   ```

## Development Workflow

1. Make your changes in your feature branch
2. Add tests for your changes
3. Run the tests to ensure they pass
   ```bash
   pytest tests/
   ```
4. Update documentation if necessary
5. Commit your changes with a descriptive commit message
   ```bash
   git commit -m "Add feature: description of your changes"
   ```
6. Push to your fork
   ```bash
   git push origin feature/your-feature-name
   ```
7. Create a Pull Request from your fork to the main repository

## Pull Request Process

1. Update the README.md or documentation with details of changes if appropriate
2. Ensure all tests pass and your code has proper test coverage
3. Make sure your code follows the project's coding standards
4. Your PR will be reviewed by maintainers, who may request changes
5. Once approved, your PR will be merged

## Coding Standards

- Follow PEP 8 style guidelines for Python code
- Write docstrings for all functions, classes, and modules
- Use type hints where appropriate
- Keep functions and methods focused and small
- Use descriptive variable names
- Add comments for complex logic

## Testing

- Write unit tests for all new functionality
- Ensure existing tests pass
- Aim for high test coverage
- Run tests before submitting a PR:
  ```bash
  pytest tests/
  ```

## Documentation

- Update documentation when adding or changing features
- Use clear, concise language
- Include examples where appropriate
- Keep the README.md up to date

## Adding New Models

If you're adding a new model integration:

1. Create a new file in the `models/` directory
2. Implement the standard model interface
3. Add registration code to the appropriate initialization file
4. Add tests for your new model
5. Update documentation to include the new model

Thank you for contributing to TRILOGY Brain! 