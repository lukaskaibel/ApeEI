from utils.call_chatgpt_api import call_chatgpt_api
from utils.create_event import create_event
from utils.extract_json import extract_json
from datetime import datetime
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s:%(levelname)s: %(message)s")


def call_eventPT_api(text: str):
    logging.info("EventPT: Looking for events in text...")
    eventPT_instruction = f"""
        You are EventPT. 
        Your task is to find any possible calendar occurance.
        Please infer the date if its implied like 'tomorrow' or 'next Tuesday'. Today is the { datetime.now().strftime("%Y-%m-%d %H:%M:%S") }.
        When you find such an entry return a JSON object like this {{ name: <string>, startDate: <%Y-%m-%%dT%H:%M:%S>, endDate: <%Y-%m-%%dT%H:%M:%S>, allDay: <bool> }}. 
        If there is no specific time mentioned, assume that the event is all day and set endDate = startDate. 
        If there is a start date, but no end date, assume that the event lasts an hour.
        Make sure to respond with only the JSON obejct.
    """
    response_text = call_chatgpt_api(user_msg=text, system_msg=eventPT_instruction)
    event = extract_json(response_text)
    if event:
        logging.info("EventPT: Successfully created event: %s", event)
        logging.info("EventPT: Adding event to calendar...")
        return create_event(
            name=event["name"],
            start_date=datetime.strptime(event["startDate"], "%Y-%m-%dT%H:%M:%S"),
            end_date=datetime.strptime(event["endDate"], "%Y-%m-%dT%H:%M:%S"),
            all_day=event["allDay"],
        )
    else:
        logging.info("EventPT: No event found in text")
        return None
