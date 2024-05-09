import requests
import re
import random
import time
import os
import logging
import pandas as pd

from datetime import datetime
from bs4 import BeautifulSoup

from scrape_helpers import previously_scraped
from scrape_functions import scrape_page
from misc_helpers import load_random_headers, init_logging


def main():
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

    curr_time = datetime.today().strftime('%Y_%m_%d_%H_%M')
    init_logging(f'logs/nav_{curr_time}.log')

    filename = f'nav/nav_{curr_time}.csv'

    scraped_urls = previously_scraped(dirpath='nav', column='url', n_files=30)

    for page_number in range(100):
        url = f"{BASE_URL}/stillinger?from={page_number * 25}&published=now%2Fd"

        time.sleep(random.uniform(0.75, 1.5))
        r = requests.get(url, headers=HEADERS)

        soup = BeautifulSoup(r.text, "html.parser")
        a_tags = soup.find_all('a')

        all_urls = [u.get('href') for u in a_tags]
        ad_urls = [u for u in all_urls if re.compile(r'(\/stillinger\/stilling\/.+)').search(u)]

        if not ad_urls:
            return
        
        ads = []

        for url in ad_urls:
            url = BASE_URL + url
            
            if url in scraped_urls:
                continue

            scraped_urls.append(url)

            result = scrape_page(xpaths=xpaths, url=url, scrape_key='nav', headers=HEADERS)

            ads.append(result)

            time.sleep(random.uniform(0.75, 1.5))

        value_df = pd.DataFrame(ads)

        if os.path.isfile(filename):
            scrape_df = pd.read_csv(filename, encoding='utf-8')
            value_df = pd.concat([scrape_df, value_df])

        value_df.to_csv(filename, index=False, encoding='utf-8')
        
        time.sleep(random.uniform(2.5, 5.5))


if __name__ == "__main__":
    HEADERS = load_random_headers()
    BASE_URL = "https://arbeidsplassen.nav.no"

    main()
