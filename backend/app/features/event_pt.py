"""
This module provides functionality to find potential calendar occurrences
from a given text and return a JSON object of the event details.
"""

from ..utils.chat_completion_request import chat_completion_request
from ..utils.extract_json import extract_json
from datetime import datetime
import logging
from typing import Dict, Any, Optional

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s:%(levelname)s: %(message)s")


def event_pt(text: str) -> Optional[Dict[str, Any]]:
    """
    Parses a given text to find possible calendar events and return them in JSON format.

    Args:
        text (str): The input text to be parsed.

    Returns:
        event (Optional[Dict[str, Any]]): JSON object containing event details, or None if no event is found.
    """
    logging.info("EventPT: Looking for events in text...")

    # Instructions for EventPT
    event_pt_instruction = f"""
        Your task is to find any possible calendar occurance.
        Please infer the date if its implied like 'tomorrow' or 'next Tuesday'. Today is the { datetime.now().strftime("%Y-%m-%d %H:%M:%S") }.
        When you find such an entry return a JSON object like this {{ name: <string>, startDate: <%Y-%m-%%dT%H:%M:%S>, endDate: <%Y-%m-%%dT%H:%M:%S>, allDay: <bool> }}. 
        If there is no specific time mentioned, assume that the event is all day and set endDate = startDate. 
        If there is a start date, but no end date, assume that the event lasts an hour.
        Make sure to respond with only the JSON obejct.
    """

    # Construct the list of messages
    messages = [
        {
            "content": event_pt_instruction,
            "role": "system",
        },
        {
            "content": text,
            "role": "user",
        },
    ]

    # Get response from chat completion request
    response_text = chat_completion_request(messages=messages).json()["choices"][0][
        "message"
    ]["content"]

    # Extract JSON object from the response
    event = extract_json(response_text)

    if event:
        logging.info("EventPT: Found event: %s", event)
        return event
    else:
        logging.info("EventPT: No event found in text")
        return None
