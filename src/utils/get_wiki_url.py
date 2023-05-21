import requests
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')

def get_wiki_url(search_term) -> (str | None):
    logging.info('Starting search on Wikipedia for term: %s', search_term)
    try:
        url = f"https://en.wikipedia.org/w/api.php?action=opensearch&search={search_term}&limit=1&namespace=0&format=json"
        response = requests.get(url)
        
        if response.status_code == 200:
            logging.info('Received response from Wikipedia API')
            data = response.json()

            if data[1]:
                logging.info('Found a matching Wikipedia page: %s', data[3][0])
                return data[3][0]
            else:
                logging.warning('No results found for search term: %s', search_term)
                return None
        else:
            logging.error('An error occurred when calling the Wikipedia API: Received status code %s', response.status_code)
            return None
    except Exception as e:
        logging.error('An error occurred: %s', e)
        return None
