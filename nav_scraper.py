
import re
import logging

from datetime import datetime

from scrape_helpers import previously_scraped
from scrape_functions import iterate_pages
from xpaths import load_random_headers, init_logging


def nav_xpaths():
    xpaths = {
        'title': '//*[@id="main-content"]/article/div/h1',
        'company': '//*[@id="main-content"]/article/div/section[1]/div[1]/p',
        'location': '//*[@id="main-content"]/article/div/section[1]/div[2]/p',
        'job_content': '//div[contains(@class, "job-posting-text")]',
        'employer': '//h2[contains(text(), "Om bedriften")]/../div',
        'deadline': '//h2[contains(text(), "Søk på jobben")]/../p',
        'about': '//h2[contains(text(), "Om jobben")]/../../dl',
        'contact_person': '//h2[contains(text(), "Kontaktperson for stillingen") or contains(text(), "Kontaktpersoner for stillingen")]/..',
        'ad_data': '//h2[contains(text(), "Annonsedata")]/../dl'
    }

    return xpaths


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

    scraped_urls = previously_scraped(dirpath='nav', identifier='url', n_files=30)
    page_iterator = lambda p : f'{base_url}/stillinger?from={p + 25}{daily_toggle}'
    
    iterate_pages(curr_time, folder, headers, page_iterator, scraped_urls,
                    page_pattern, ad_pattern, key_pattern, id_pattern,
                    base_url=base_url)
    
    logging.info(f'FINISHED SCRAPING NAV')



if __name__ == "__main__":
    main()
