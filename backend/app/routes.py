from flask import request, jsonify
from app import app
from .utils.create_event import create_event
from .features.assistant_pt import assistant_pt
from .features.wiki_pt import wiki_pt
from .features.event_pt import event_pt
import logging
import json
from datetime import datetime

MAX_MESSAGES_STORED = 8
prev_messages = []


@app.route("/api/chat", methods=["POST"])
def chat():
    # Analysing Reflection
    message = request.get_json()["message"]
    logging.info(f"Received user message:\n{message}")
    response, is_analysis, criteria = assistant_pt(message, prevMessages=prev_messages)
    logging.info(f"Generated assistant response:\n{response}\n{criteria}")

    add_message_to_prev_messages(message=message, role="user")
    add_message_to_prev_messages(message=response["content"], role=response["role"])

    if is_analysis:
        # Calling WikiPT
        logging.info("Calling WikiPT...")
        print(response)
        title, url = wiki_pt(message + response["content"])

        # Create Google Calendar event if there is an event in the message or response
        event = event_pt(message + response["content"])

        return (
            jsonify(
                {
                    "content": response["content"],
                    "role": response["role"],
                    "wikiEntry": {"title": title, "url": url},
                    "event": event,
                }
            ),
            200,
        )
    else:
        return (
            jsonify(
                {
                    "content": response["content"],
                    "role": response["role"],
                }
            ),
            200,
        )


@app.route("/api/create_event", methods=["POST"])
def event():
    data = request.get_json()
    message = json.loads(data["message"])
    logging.info(f"Create event:\n{message}")
    create_event(
        message["name"],
        start_date=datetime.strptime(message["startDate"], "%Y-%m-%dT%H:%M:%S"),
        end_date=datetime.strptime(message["endDate"], "%Y-%m-%dT%H:%M:%S"),
        all_day=message["allDay"],
    )
    return ("Created", 200)


def add_message_to_prev_messages(message: str, role: str):
    global prev_messages
    if len(prev_messages) > MAX_MESSAGES_STORED:
        prev_messages.pop(0)
    prev_messages += [{"content": message, "role": role}]
