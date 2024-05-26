import requests
import logging
import re
import yaml

from bs4 import BeautifulSoup
from datetime import datetime

from misc_helpers import init_logging, load_random_headers
from scrape_helpers import previously_scraped
from scrape_functions import iterate_pages


def get_sub_urls():
    # List of sub urls to scrape. Might be moved to parameters
    return [
        'realestate/homes',
        'realestate/newbuildings',
        'realestate/plots',
        'realestate/leisureplots',
        'realestate/lettings',
        'realestate/wanted',
        'realestate/abroad',
        'realestate/leisuresale',
        'realestate/businesssale',
        'realestate/businessrent',
        'realestate/businessplots',
        'realestate/companyforsale',

        'job/fulltime',
        'job/parttime',
        'job/management',
    ]


def main():
    with open('parameters.yml', 'r') as file:
        flags = yaml.safe_load(file)

    folder = 'finn'
    curr_time = datetime.today().strftime('%Y_%m_%d')
    headers = load_random_headers()

    xpath_key_pattern = re.compile(r'finn\.no/\w+/(\w+)')
    ad_pattern = re.compile(r'finnkode=\d+')
    id_pattern = re.compile(r'(?<=finnkode=)\d+')

    base_url = 'https://www.finn.no/'

    sub_urls = get_sub_urls()

    init_logging(f'logs/finn_{curr_time}.log')

    for sub_url in sub_urls:
        logging.info(f'SCRAPING DOMAIN: {sub_url}')

        scraped_codes = previously_scraped(dirpath='finn',
                                           identifier='idx',
                                           n_files=50)

        if flags['daily_scrape']:
            toggles = ['&published=1']
        else:
            url = f'{base_url}/{sub_url}/search.html'
            r = requests.get(url, headers=headers)

            soup = BeautifulSoup(r.text, "html.parser")
            divs = soup.find_all("div", {"class": "input-toggle"})
            toggle_inputs = [div.find("input", {"type": "checkbox"}) for div in divs]
            toggles = [u.get("id") for u in toggle_inputs]

        for t in toggles:
            page_iterator = lambda p: f'{base_url}{sub_url}/search.html?{t}&page={p + 1}'

            iterate_pages(curr_time=curr_time,
                          folder=folder,
                          headers=headers,
                          page_iterator=page_iterator,
                          scraped_codes=scraped_codes,
                          ad_pattern=ad_pattern,
                          xpath_key_pattern=xpath_key_pattern,
                          id_pattern=id_pattern)

        logging.info(f'FINISHED SCRAPING {sub_url}.')


if __name__ == "__main__":
    main()
