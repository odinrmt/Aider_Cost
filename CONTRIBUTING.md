# Contributing to Aider Stats

Thank you for your interest in contributing!

## Development Setup

1. Fork the repository on GitHub.
2. Clone your fork locally.
3. Install the development environment using `uv`:
   ```bash
   uv sync --all-extras --dev
   ```

## Pre-Pull Request Checks

Before submitting a pull request, you must ensure that all code quality checks pass. Run the following commands locally:

```bash
uv run ruff check .
uv run ruff format --check .
uv run mypy src/
```
