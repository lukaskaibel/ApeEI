"""
This module provides functionality for retrieving the OpenAI API key from a
configuration file.
"""

import json
from typing import Optional
import logging


def get_api_key(config_file: str = "config.json") -> Optional[str]:
    """
    Reads the OpenAI API key from a configuration file.

    Args:
        config_file (str): The path to the configuration file. Defaults to 'config.json'.

    Returns:
        The OpenAI API key, or None if the key does not exist in the configuration file.

    Raises:
        FileNotFoundError: If the configuration file does not exist.
        json.JSONDecodeError: If the configuration file is not valid JSON.
        KeyError: If the 'openai_key' field does not exist in the configuration file.
    """
    try:
        with open(config_file) as file:
            config = json.load(file)
            return config.get("openai_key")
    except FileNotFoundError:
        logging.error(f"Configuration file '{config_file}' not found.")
        raise
    except json.JSONDecodeError:
        logging.error(f"Configuration file '{config_file}' is not valid JSON.")
        raise
    except KeyError:
        logging.error(f"'openai_key' not found in configuration file '{config_file}'.")
        raise
