import openai
import logging
from utils.config_utils import get_api_key

openai.api_key = get_api_key()

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s:%(levelname)s: %(message)s')

def call_chatgpt_api(user_msg, system_msg='You are a helpful assistant.') -> (str | None):
    logging.info('Calling Chat GPT API with user message: "%s"', user_msg)
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": system_msg
                },
                {
                    "role": "user",
                    "content": user_msg
                }
            ],
            max_tokens=50
        )
        logging.info('Chat GPT API call successful with response: "%s"', response['choices'][0]['message']['content'].strip())
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        logging.error('Error making the Chat GPT API call: %s', e)
        return None
