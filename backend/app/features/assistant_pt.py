"""
This module provides functionality for processing and analysing a user's input 
as either a 'reflection' or a 'normal message', and returns a response and an
evaluation based on pre-defined criteria if the input is a reflection.
"""

from ..utils.chat_completion_request import chat_completion_request
import logging
from typing import List, Dict, Any, Tuple, Optional

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s:%(levelname)s:%(message)s")


def assistant_pt(
    message: str, prevMessages: List[Dict[str, Any]] = []
) -> Tuple[Dict[str, Any], bool, Optional[Dict[str, Any]]]:
    """
    Analyses a message as either a 'reflection' or a 'normal message', and returns
    a response from an assistant, a boolean indicating whether the message is a
    reflection, and a JSON object with numeric evaluations if the message is a reflection.

    Args:
        reflection (str): The user's message to analyse.
        prevMessages (List[Dict[str, Any]]): A list of previous messages, if any.

    Returns:
        assistant_message (Dict[str, Any]): The assistant's response to the message.
        is_reflection (bool): A boolean indicating whether the message is a reflection.
        criteria_json (Optional[Dict[str, Any]]): A JSON object with numeric evaluations
        for various criteria if the message is a reflection, or None if not.
    """
    logging.info("Analysing message...")
    messages = [
        # System message to provide instructions to the AI assistant
        {
            "role": "system",
            "content": """
                Given a user's text input, classify it as either a 'reflection' or a 'normal message'. A reflection is a more detailed, introspective thought or contemplation that provides in-depth insights into the user's feelings, experiences, or thoughts. Normal messages are shorter, direct, and less introspective, such as simple greetings, questions, or direct instructions.

                Here are some examples for each category:

                1. 'Today I've been thinking about my work habits, and I realized that I'm far more productive in the mornings. I think I'll start shifting my schedule to start earlier and see if that helps my productivity.'
                True

                2. 'I'm feeling a bit overwhelmed by the new project. There's a lot to do and I'm unsure about where to begin.'
                True

                3. 'Good morning, how are you today?'
                False

                4. 'Could you help me understand how to solve this math problem?'
                False

                5. 'Last week we were talking about Python in class. I didn't really understand the topic because I never programmed before. I think want to improve on it in the future though!'
                True

                ONLY respond with True or False!
            """,
        },
        {
            "role": "user",
            "content": message,
        },
    ]
    is_reflection_response = chat_completion_request(messages=messages)
    is_reflection = bool(
        is_reflection_response.json()["choices"][0]["message"]["content"].lower()
        == "true"
    )
    logging.info(
        "ReflectionPT: "
        + ("Reflection detected" if is_reflection else "Message detected")
    )

    reflection_instruction = """
        Provide peronal feedback to the students reflection based on how well the student included the criteria: Emotion, Analysis, Description, Conclusion, Evaluation, Future Plan. 
                You shouldn't list each criteria, instead provide a nicely flowing text as response.
                Also focus on anaysing the reflection based on the criteria. Do not summarize the reflection.
    """
    messages = (
        [
            {
                "role": "system",
                "content": "You are a helpful chatbot that helps students to improve at uni."
                + (reflection_instruction if is_reflection else ""),
            }
        ]
        + prevMessages
        + [
            {
                "role": "user",
                "content": message,
            },
        ]
    )
    chat_response = chat_completion_request(messages=messages)
    assistant_message = chat_response.json()["choices"][0]["message"]
    messages.append(assistant_message)
    criteria_json = None
    if is_reflection:
        logging.info("Analysing numeric values for criteria...")
        request_numeric_values_message = {
            "role": "system",
            "content": """
                Please provide a JSON object that holds numeric values (0 to 5) representing how well the student integrated each critia into the reflection.
                Use the following keys for the JSON object: "emotion", "analysis", "description", "conclusion", "evaluation", "future".
                Only provide the JSON object.
            """,
        }
        messages.append(request_numeric_values_message)
        criteria_chat_response = chat_completion_request(messages=messages)
        logging.info("Finished analysing criteria.")
        criteria_json = criteria_chat_response.json()["choices"][0]["message"]
        logging.info("Finished analysing reflection.")
    return assistant_message, is_reflection, criteria_json
