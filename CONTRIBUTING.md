# Contributing Guide

Contributions are always welcome!

## Development Setup

1. Clone the repository
2. Create and activate a virtual environment (`python -m venv .venv && source .venv/bin/activate`)
3. Install package with dev dependencies:
   ```bash
   pip install -e ".[dev]"
   ```
4. Run tests:
   ```bash
   pytest
   ```
5. Ensure code coverage remains $\ge 80\%$.
