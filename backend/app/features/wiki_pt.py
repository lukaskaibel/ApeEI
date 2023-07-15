"""
This module provides functionality to find potential Wikipedia entries
related to the given text and returns the term and its corresponding Wikipedia URL.
"""

from ..utils.chat_completion_request import chat_completion_request
from ..utils.get_wiki_url import get_wiki_url
import logging
from typing import Tuple, Optional

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s:%(levelname)s:%(message)s")


def wiki_pt(text: str) -> Tuple[str, Optional[str]]:
    """
    Parses a given text to find a relevant Wikipedia entry.

    Args:
        text (str): The input text to be parsed.

    Returns:
        title (str): The title of the relevant Wikipedia entry.
        url (Optional[str]): The URL of the relevant Wikipedia entry or None if no entry is found.
    """

    logging.info("WikiPT: Looking for helpful Wikipedia entry...")
    wiki_pt_instruction = """
    Your task is to reply to every message with a single term that you expect wikipedia to have an entry on.
    The term should be worth researching in the context of the message. 
    Only respond with that term (not a full sentence).
    """

    messages = [
        {
            "content": wiki_pt_instruction,
            "role": "system",
        },
        {"content": text, "role": "user"},
    ]

    title = chat_completion_request(messages=messages).json()["choices"][0]["message"][
        "content"
    ]
    url = get_wiki_url(title)

    if url:
        logging.info(f"WikiPT: Found Wikipedia entry for {title} at {url}")
    else:
        logging.info("WikiPT: No related Wikipedia entry found")

    return title, url
