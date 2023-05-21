import json

def get_api_key():
    with open('config.json') as config_file:
        config = json.load(config_file)
        return config['openai_key']
