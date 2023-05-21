from utils.call_chatgpt_api import call_chatgpt_api
from utils.get_wiki_url import get_wiki_url

def call_wikiPT_api(text: str): 
    wikiPT_instruction = 'You are WikiPT, you reply to every message with a single term that you expect wikipedia to have an entry on and that is worth researching in the context of the message. Only respond with that term (not a full sentence).'
    term = call_chatgpt_api(user_msg=text, system_msg=wikiPT_instruction)
    url = get_wiki_url(term)
    return term, url
