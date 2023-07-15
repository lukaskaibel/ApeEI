"""
This module provides functionality for extracting a JSON5 or JavaScript object
from a string. It uses regular expressions to identify the object and the `json5`
library to parse it.
"""

import re
from json5 import loads
from typing import Optional, Dict, Any


def extract_json(input_string: str) -> Optional[Dict[str, Any]]:
    """
    Extracts the first JSON5 or JavaScript object from a string.

    Args:
        input_string (str): The string to extract the object from.

    Returns:
        The extracted object as a Python dict, or None if no valid object is found.

    Notes:
        Only the first valid object in the string is returned. If the string contains
        multiple objects, consider using `re.findall` instead of `re.search`, and
        parsing each match in a loop.
    """
    # Search for everything between {}
    match = re.search(r"\{.*\}", input_string, re.DOTALL)
    if match:
        # Extract matched string
        json_str = match.group()
        try:
            # Try to decode the JSON5 (or JavaScript) object
            json_obj = loads(json_str)
            return json_obj
        except Exception:
            # If the object cannot be parsed, return None
            return None
    else:
        # If no object is found, return None
        return None
