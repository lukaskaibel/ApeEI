"""
This module provides functionality for fetching a Wikipedia URL corresponding 
to a given search term using the Wikipedia opensearch API.
"""

import requests
import logging
from typing import Optional

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s:%(levelname)s:%(message)s")


def get_wiki_url(search_term: str) -> Optional[str]:
    """
    Fetches the Wikipedia URL for a given search term.

    Args:
        search_term (str): The term to search for on Wikipedia.

    Returns:
        The URL of the Wikipedia page for the search term, or None if no page is found
        or an error occurs.

    Logs:
        Information about the search term, the result of the search, and any errors that occur.
    """
    logging.info("Starting search on Wikipedia for term: %s", search_term)
    try:
        url = f"https://en.wikipedia.org/w/api.php?action=opensearch&search={search_term}&limit=1&namespace=0&format=json"
        response = requests.get(url)

        if response.status_code == 200:
            logging.info("Received response from Wikipedia API")
            data = response.json()

            if data[1]:
                logging.info("Found a matching Wikipedia page: %s", data[3][0])
                return data[3][0]
            else:
                logging.warning("No results found for search term: %s", search_term)
                return None
        else:
            logging.error(
                "An error occurred when calling the Wikipedia API: Received status code %s",
                response.status_code,
            )
            return None
    except Exception as e:
        logging.error("An error occurred: %s", e)
        return None
