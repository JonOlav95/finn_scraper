
import re
import logging

from datetime import datetime

from scrape_helpers import previously_scraped
from scrape_functions import scrape_pages
from misc_helpers import load_random_headers, init_logging


def main():
    curr_time = datetime.today().strftime('%Y_%m_%d')
    folder = 'nav'
    headers = load_random_headers()

    key_pattern = re.compile(r'nav')
    page_pattern = re.compile(r'from=\d+')
    ad_pattern = re.compile(r'(\/stillinger\/stilling\/.+)')
    id_pattern = re.compile(r'[a-f0-9]{8}-[a-f0-9]{4}-4[a-f0-9]{3}-[89ab][a-f0-9]{3}-[a-f0-9]{12}')

    base_url = 'https://arbeidsplassen.nav.no'
    daily_toggle = '&published=now%2Fd'
    init_logging(f'logs/nav_{curr_time}.log')

    logging.info(f'SCRAPING NAV')

    scraped_urls = previously_scraped(dirpath='nav', column='url', n_files=30)
    page_iterator = lambda p : f'{base_url}/stillinger?from={p + 25}{daily_toggle}'
    
    scrape_pages(curr_time, folder, headers, page_iterator, scraped_urls,
                    page_pattern, ad_pattern, key_pattern, id_pattern,
                    base_url=base_url)
    
    logging.info(f'FINISHED SCRAPING NAV')



if __name__ == "__main__":
    main()
