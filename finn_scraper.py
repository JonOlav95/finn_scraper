import os
import re
import time
import random
import logging
import requests
import pandas as pd

from datetime import datetime
from bs4 import BeautifulSoup
from misc_helpers import get_sub_urls, load_xpath, init_logging, load_random_headers
from scrape_helpers import previously_scraped
from scrape_functions import scrape_page


def scrape_sub_url(curr_time, scraped_codes, base_url, toggle, headers):

    pattern = re.compile(r'finn\.no/(\w+)/(\w+)')

    # Iterate every page until the maximum of 50
    for page_number in range(1, 50):
        logging.info(f'Scraping page {page_number}')

        time.sleep(random.uniform(0.75, 1.5))

        url = f'{base_url}/search.html?page={page_number}&{toggle}'
        r = requests.get(url, headers=headers)

        if r.status_code != 200:
            logging.critical(f"ITERATE PAGE RESPONSE CODE {r.status_code}, URL: {url}")
            continue

        soup = BeautifulSoup(r.text, "html.parser")
        a_tags = soup.find_all("a")

        all_urls = [u.get("href") for u in a_tags]

        page_urls = [u for u in all_urls if re.compile(r'page=\d+').search(u)]
        ad_urls = [u for u in all_urls if re.compile(r'finnkode=\d+').search(u)]

        if not ad_urls:
            logging.info('NO ADS ON PAGE')
            return

        page_ads = {}

        # Scrape every ad url on the given page.
        # Scraping is done by opening up the ad in a new tab, then downloading the data.
        # The tab is then closed, and selenium returns to the initial page tab without
        # making a new request.
        for url in ad_urls:

            finn_code = re.compile(r'(?<=finnkode=)\d+').search(url).group(0)
            finn_code = int(finn_code)

            if finn_code in scraped_codes:
                logging.info(f'ALREADY SCRAPED: {url}')
                continue
            
            scraped_codes.append(finn_code)
            
            # Key may differ from suburl
            key = re.search(pattern, url).group(2)
            xpath = load_xpath(key)

            results = scrape_page(url=url, headers=headers, scrape_key=key, 
                                  xpaths=xpath, finn_code=finn_code)

            if not xpath:
                key = 'other'

            if key in page_ads.keys():
                page_ads[key].append(results)
            else:
                page_ads[key] = [results]

            time.sleep(random.uniform(0.75, 1.5))

        # Write result to file
        for key in page_ads.keys():
            
            if not page_ads[key]:
                continue

            filename = f'finn/{key}_{curr_time}.csv'
            value_df = pd.DataFrame(page_ads[key])

            if os.path.isfile(filename):
                scrape_df = pd.read_csv(filename, encoding='utf-8')
                value_df = pd.concat([scrape_df, value_df])

            value_df.to_csv(filename, index=False, encoding='utf-8')
    
        if f'page={page_number + 1}' not in '\t'.join(page_urls):
            return

        time.sleep(random.uniform(2.5, 5.5))


def main():
    curr_time = datetime.today().strftime('%Y_%m_%d')
    init_logging(f'logs/finn_{curr_time}.log')

    sub_urls = get_sub_urls()
    daily_toggle = 'published=1'
    headers = load_random_headers()

    # Iterate the different subdomains used to scrape the daily ads
    for sub_url in sub_urls:
        logging.info(f'SCRAPING DOMAIN: {sub_url}')

        scraped_codes = previously_scraped(dirpath='finn', 
                                           column='finn_code', 
                                           n_files=50)
        
        base_url = 'https://www.finn.no/' + sub_url
        
        scrape_sub_url(curr_time, scraped_codes, base_url, daily_toggle, headers)
        logging.info(f'FINISHED SCRAPING {sub_url}.')


if __name__ == "__main__":
    
    main()
