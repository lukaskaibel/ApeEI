from utils.call_chatgpt_api import call_chatgpt_api
from utils.get_wiki_url import get_wiki_url
import logging


def call_wikiPT_api(text: str):
    logging.info("WikiPT: Looking for helpful Wikipedia entry...")
    wikiPT_instruction = "You are WikiPT, you reply to every message with a single term that you expect wikipedia to have an entry on and that is worth researching in the context of the message. Only respond with that term (not a full sentence)."
    title = call_chatgpt_api(user_msg=text, system_msg=wikiPT_instruction)
    url = get_wiki_url(title)

    if title:
        logging.info(f"WikiPT: Found Wikipedia entry for {title} at {url}")
    else:
        logging.info("WikiPT: No related Wikipedia entry found")

    return title, url
