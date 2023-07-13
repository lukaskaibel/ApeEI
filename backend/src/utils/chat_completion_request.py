import openai
import requests
from tenacity import retry, wait_random_exponential, stop_after_attempt
from utils.config_utils import get_api_key
import logging

openai.api_key = get_api_key()

GPT_MODEL = "gpt-3.5-turbo-0613"


@retry(wait=wait_random_exponential(min=1, max=40), stop=stop_after_attempt(3))
def chat_completion_request(
    messages, functions=None, function_call=None, model=GPT_MODEL
):
    logging.info("Making chat completion request to API...")
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + openai.api_key,
    }
    json_data = {"model": model, "messages": messages}
    if functions is not None:
        json_data.update({"functions": functions})
    if function_call is not None:
        json_data.update({"function_call": function_call})
    try:
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers=headers,
            json=json_data,
        )
        logging.info("Completion request successful!")
        return response
    except Exception as e:
        logging.error(f"Completion request failed with exception:\n{e}")
        return e
