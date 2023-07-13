from flask import Flask, request, jsonify
from flask_cors import CORS
from reflectionPT import analyse_reflection
from wikiPT import call_wikiPT_api
from eventPT import call_eventPT_api
from utils.create_event import create_event
import logging
import json
from datetime import datetime

app = Flask(__name__)
CORS(app, resources=r"/api/*")

logging.getLogger().setLevel(logging.INFO)


@app.route("/api/chat", methods=["POST"])
def chat():
    # Analysing Reflection
    message = request.get_json()["message"]
    logging.info(f"Received user message:\n{message}")
    response, is_analysis, criteria = analyse_reflection(message)
    logging.info(f"Generated assistant response:\n{response}\n{criteria}")

    if is_analysis:
        # Calling WikiPT
        logging.info("Calling WikiPT...")
        print(response)
        title, url = call_wikiPT_api(message + response["content"])

        # Create Google Calendar event if there is an event in the message or response
        event = call_eventPT_api(message + response["content"])

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


if __name__ == "__main__":
    app.run(debug=True)
