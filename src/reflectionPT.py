from utils.chat_completion_request import chat_completion_request
from utils.print_chat_conversation import print_chat_conversation
from utils.extract_json import extract_json


def analyse_reflection(reflection: str):
    messages = [
        {
            "role": "system",
            "content": f"""
                You are a helpful chatbot that helps students to improve at uni.
                Provide peronal feedback to the students reflection based on how well the student included the criteria: Emotion, Analysis, Description, Conclusion, Evaluation, Future Plan. 
                You shouldn't list each criteria, instead provide a nicely flowing text as response.
                Also focus on anaysing the reflection based on the criteria. Do not summarize the reflection.
            """,
        },
        {
            "role": "user",
            "content": reflection,
        },
    ]
    chat_response = chat_completion_request(messages=messages)
    assistant_message = chat_response.json()["choices"][0]["message"]
    messages.append(assistant_message)
    request_numeric_values_message = {
        "role": "system",
        "content": f"""
            Please provide a JSON object that holds numeric values (0 to 5) representing how well the student integrated each critia into the reflection.
            Use the following keys for the JSON object: "emotion", "analysis", "description", "conclusion", "evaluation", "future".
        """,
    }
    messages.append(request_numeric_values_message)
    criteria_chat_response = chat_completion_request(messages=messages)
    criteria_json = criteria_chat_response.json()["choices"][0]["message"]
    print_chat_conversation(messages)
    print(criteria_json)
