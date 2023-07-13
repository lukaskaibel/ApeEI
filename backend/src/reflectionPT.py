from utils.chat_completion_request import chat_completion_request
from utils.print_chat_conversation import print_chat_conversation
from utils.extract_json import extract_json
import logging


def analyse_reflection(reflection: str):
    logging.info("Analysing message...")
    messages = [
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
    ]
    is_reflection_response = chat_completion_request(messages=messages)
    is_reflection = bool(
        is_reflection_response.json()["choices"][0]["message"]["content"].lower()
        == "true"
    )
    print(
        "Is Reflection "
        + is_reflection_response.json()["choices"][0]["message"]["content"]
    )
    logging.info(
        "ReflectionPT: "
        + ("Reflection detected" if is_reflection else "Message detected")
    )

    reflection_instruction = f"""
        Provide peronal feedback to the students reflection based on how well the student included the criteria: Emotion, Analysis, Description, Conclusion, Evaluation, Future Plan. 
                You shouldn't list each criteria, instead provide a nicely flowing text as response.
                Also focus on anaysing the reflection based on the criteria. Do not summarize the reflection.
    """
    messages = [
        {
            "role": "system",
            "content": "You are a helpful chatbot that helps students to improve at uni."
            + (reflection_instruction if is_reflection else ""),
        },
        {
            "role": "user",
            "content": reflection,
        },
    ]
    chat_response = chat_completion_request(messages=messages)
    assistant_message = chat_response.json()["choices"][0]["message"]
    messages.append(assistant_message)
    criteria_json = None
    if is_reflection:
        logging.info("Analysing numeric values for criteria...")
        request_numeric_values_message = {
            "role": "system",
            "content": f"""
                Please provide a JSON object that holds numeric values (0 to 5) representing how well the student integrated each critia into the reflection.
                Use the following keys for the JSON object: "emotion", "analysis", "description", "conclusion", "evaluation", "future".
                Only provide the JSON object.
            """,
        }
        messages.append(request_numeric_values_message)
        criteria_chat_response = chat_completion_request(messages=messages)
        logging.info("Finshed analysing criteria.")
        criteria_json = criteria_chat_response.json()["choices"][0]["message"]
        logging.info("Finished analysing reflection.")
    return assistant_message, is_reflection, criteria_json
