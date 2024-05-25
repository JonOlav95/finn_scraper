import re
import logging

from datetime import datetime

from misc_helpers import get_sub_urls, load_xpath, init_logging, load_random_headers
from scrape_helpers import previously_scraped
from scrape_functions import scrape_single_page, scrape_pages


def main():
    curr_time = datetime.today().strftime('%Y_%m_%d')
    folder = 'finn'
    headers = load_random_headers()
    
    key_pattern = re.compile(r'finn\.no/\w+/(\w+)')
    page_pattern = re.compile(r'page=\d+')
    ad_pattern = re.compile(r'finnkode=\d+')
    id_pattern = re.compile(r'(?<=finnkode=)\d+')

    base_url = 'https://www.finn.no'
    daily_toggle = '&published=1'

    sub_urls = get_sub_urls()

    init_logging(f'logs/finn_{curr_time}.log')

    # Iterate the different subdomains used to scrape the daily ads
    for sub_url in sub_urls:
        logging.info(f'SCRAPING DOMAIN: {sub_url}')

        scraped_codes = previously_scraped(dirpath='finn', 
                                           column='finn_code', 
                                           n_files=50)

        page_iterator = lambda p : f'{base_url}/{sub_url}/search.html?page={p + 1}{daily_toggle}'
        
        scrape_pages(curr_time, folder, headers, page_iterator, scraped_codes,
                        page_pattern, ad_pattern, key_pattern, id_pattern)
        
        logging.info(f'FINISHED SCRAPING {sub_url}.')


if __name__ == "__main__":
    main()
