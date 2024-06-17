import requests
import logging
import re
import yaml

from bs4 import BeautifulSoup
from datetime import datetime

from misc_helpers import init_logging, load_random_headers
from scrape_helpers import previously_scraped
from scrape_functions import iterate_pages


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

    init_logging(f'logs/finn_{curr_time}.log')

    try:
        for sub_url in flags['finn_sub_urls']:

            if flags['daily_scrape']:
                toggles = ['published=1']
            else:
                url = f'{base_url}/{sub_url}/search.html'
                r = requests.get(url, headers=headers)

                if r.status_code != 200:
                    logging.error(f"Not 200 status code {r.status_code}, URL: {url}")
                    continue

                soup = BeautifulSoup(r.text, "html.parser")
                divs = soup.find_all("div", {"class": "input-toggle"})
                toggle_inputs = [div.find("input", {"type": "checkbox"}) for div in divs]
                toggles = [u.get("id") for u in toggle_inputs]
                toggles = [t.replace("-", "=") for t in toggles]

            for t in toggles:
                logging.info(f'SCRAPING {sub_url} WITH {t}')
                page_iterator = lambda p: f'{base_url}{sub_url}/search.html?{t}&page={p + 1}'

                scraped_codes = previously_scraped(dirpath='finn',
                                                   identifier='idx',
                                                   n_files=100)

                iterate_pages(curr_time=curr_time,
                              folder=folder,
                              headers=headers,
                              page_iterator=page_iterator,
                              scraped_codes=scraped_codes,
                              ad_pattern=ad_pattern,
                              xpath_key_pattern=xpath_key_pattern,
                              id_pattern=id_pattern)

            logging.info(f'FINISHED SCRAPING {sub_url}.')

    except Exception as e:
        logging.error(f'MAIN CRASHED WITH {e}')


if __name__ == "__main__":
    main()
