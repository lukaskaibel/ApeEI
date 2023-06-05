import re
from json5 import loads
from typing import Optional, Dict, Any


def extract_json(input_string: str) -> Optional[Dict[str, Any]]:
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
            return None
    else:
        return None
