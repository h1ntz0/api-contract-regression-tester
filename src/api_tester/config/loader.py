import os
from pathlib import Path
from typing import Optional, Dict, Any
import yaml

from api_tester.config.models import ProjectConfig
from api_tester.core.exceptions import ConfigurationError


def load_config(config_path: Optional[str] = None) -> ProjectConfig:
    """Load and validate configuration YAML file if provided, otherwise returns defaults."""
    if not config_path:
        return ProjectConfig()

    path = Path(config_path)
    if not path.exists():
        raise ConfigurationError(f"Configuration file not found: {config_path}")

    try:
        content = path.read_text(encoding="utf-8")
        data = yaml.safe_load(content) or {}
    except Exception as e:
        raise ConfigurationError(f"Failed to parse configuration file '{config_path}': {e}") from e

    try:
        return ProjectConfig.model_validate(data)
    except Exception as e:
        raise ConfigurationError(f"Invalid configuration parameters: {e}") from e
