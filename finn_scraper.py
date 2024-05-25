import requests
import logging
import re

from bs4 import BeautifulSoup
from datetime import datetime

from misc_helpers import get_sub_urls, init_logging, load_random_headers
from scrape_helpers import previously_scraped
from scrape_functions import scrape_pages


def main():
    folder = 'finn'
    curr_time = datetime.today().strftime('%Y_%m_%d')
    headers = load_random_headers()
    
    key_pattern = re.compile(r'finn\.no/\w+/(\w+)')
    page_pattern = re.compile(r'page=\d+')
    ad_pattern = re.compile(r'finnkode=\d+')
    id_pattern = re.compile(r'(?<=finnkode=)\d+')

    base_url = 'https://www.finn.no'

    sub_urls = get_sub_urls()

    init_logging(f'logs/finn_{curr_time}.log')

    for sub_url in sub_urls:
        logging.info(f'SCRAPING DOMAIN: {sub_url}')

        scraped_codes = previously_scraped(dirpath='finn', 
                                           column='finn_code', 
                                           n_files=50)

        if False:
            toggles = ['&published=1']
        else:
            url = f'{base_url}/{sub_url}/search.html'
            r = requests.get(url, headers=headers)

            soup = BeautifulSoup(r.text, "html.parser")
            divs = soup.find_all("div", {"class": "input-toggle"})
            toggle_inputs = [div.find("input", {"type": "checkbox"}) for div in divs]
            toggles = [u.get("id") for u in toggle_inputs]

        for t in toggles:
            page_iterator = lambda p : f'{base_url}/{sub_url}/search.html?page=&{p + 1}{t}'
                
            scrape_pages(curr_time, folder, headers, page_iterator, scraped_codes,
                            page_pattern, ad_pattern, key_pattern, id_pattern)
        
        logging.info(f'FINISHED SCRAPING {sub_url}.')


if __name__ == "__main__":
    main()
