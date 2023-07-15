"""
This module provides functionality for interaction with OpenAI's API.
It includes methods to make chat completion requests, using tenacity library
for retrying in case of failures.
"""

import logging
from typing import List, Optional, Dict, Any
import requests
from tenacity import retry, wait_random_exponential, stop_after_attempt
import openai

from .config_utils import get_api_key

# Setup logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

# Set the OpenAI API key
openai.api_key = get_api_key()

# Define the GPT model to use
GPT_MODEL = "gpt-3.5-turbo-0613"


@retry(wait=wait_random_exponential(min=1, max=40), stop=stop_after_attempt(3))
def chat_completion_request(
    messages: List[Dict[str, Any]],
    functions: Optional[List[Dict[str, Any]]] = None,
    function_call: Optional[Dict[str, Any]] = None,
    model: str = GPT_MODEL,
) -> Any:
    """
    Makes a chat completion request to OpenAI API.

    Args:
        messages (List[Dict[str, Any]]): A list of message objects.
        functions (Optional[List[Dict[str, Any]]]): A list of function objects.
        function_call (Optional[Dict[str, Any]]): The function call object.
        model (str): The model to be used for the completion request.

    Returns:
        response (Any): The API response.

    Raises:
        If the request fails, an exception will be logged and re-raised.
    """

    logging.info("Making chat completion request to API...")

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {openai.api_key}",
    }

    json_data = {
        "model": model,
        "messages": messages,
    }

    if functions is not None:
        json_data["functions"] = functions
    if function_call is not None:
        json_data["function_call"] = function_call

    try:
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers=headers,
            json=json_data,
        )
        response.raise_for_status()

        logging.info("Completion request successful!")
        return response

    except Exception as e:
        logging.error(f"Completion request failed with exception:\n{e}")
        raise
