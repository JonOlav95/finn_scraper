
import re
import logging
import time
import random
import requests
import yaml

from datetime import datetime

from misc_helpers import load_random_headers, init_logging
from scrape_helpers import previously_scraped
from scrape_functions import scrape_single_page, store_data

from bs4 import BeautifulSoup


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


def iterate_pages_nav(curr_time,
                      folder,
                      headers,
                      scraped_codes,
                      ad_pattern,
                      id_pattern,
                      base_url,
                      toggle):
    """
    Iterate pages goes through all pages and extract ads
    to scrape. If no ads are found on the page, the function
    returns. The function stores all data in batches at the
    end of the page scrape.

    Args:
        curr_time: Start time of scrape, used for filename.
        folder: Where to store the data.
        headers: Request headers.
        ad_pattern: Regex pattern for finding ads in urls.
        xpath_key_pattern: Regex pattern for finding correct xpaths.
        id_pattern: Regex pattern for finding id in url.
        toggle: Current button toggle for search.
    """

    headers['Referer'] = 'https://www.google.com'

    for page_number in range(100):
        logging.info(f'SCRAPING PAGE {page_number + 1}')

        time.sleep(random.uniform(1.5, 2.5))

        if page_number == 0:
            url = f'{base_url}/stillinger?size=100&{toggle}&v=2'
        else:
            url = f'{base_url}/stillinger?from={page_number * 100}&size=100&{toggle}&v=2'

        r = requests.get(url, headers=headers)

        if r.status_code == 400:
            return
        elif r.status_code != 200:
            logging.error(f"ITERATE PAGE RESPONSE CODE {r.status_code}, URL: {url}")
            continue

        headers['Referer'] = url
        soup = BeautifulSoup(r.text, "html.parser")

        a_tags = soup.find_all("a")
        all_urls = [u.get('href') for u in a_tags]

        ad_urls = [base_url + u for u in all_urls if ad_pattern.search(u)]

        if not ad_urls:
            logging.info('NO ADS ON PAGE')
            return

        page_ads = {}

        for url in ad_urls:
            idx = id_pattern.search(url).group(0)

            # Check if ad has been scraped before.
            if idx in scraped_codes:
                logging.info(f'ALREADY SCRAPED: {url}')
                continue

            scraped_codes.append(idx)

            # Search for the correct xpaths given the 'xpath key'
            # which is identified by the url.
            xpath_key = 'nav'
            xpaths = nav_xpaths()

            result = scrape_single_page(url=url,
                                        headers=headers,
                                        scrape_key=xpath_key,
                                        xpaths=xpaths,
                                        idx=idx)

            if not result:
                continue

            # Store the ad temporarliy in a dictionary. A finn page
            # may contain ads of different type. E.g. 'home' ads may contain
            # 'project' ads.
            if xpath_key in page_ads.keys():
                page_ads[xpath_key].append(result)
            else:
                page_ads[xpath_key] = [result]

            time.sleep(random.uniform(0.75, 1.5))

        store_data(page_ads, folder, curr_time)


def main():
    with open('parameters.yml', 'r') as file:
        flags = yaml.safe_load(file)

    curr_time = datetime.today().strftime('%Y_%m_%d')
    folder = 'nav'
    headers = load_random_headers()

    ad_pattern = re.compile(r'(\/stillinger\/stilling\/.+)')
    id_pattern = re.compile(r'[a-f0-9]{8}-[a-f0-9]{4}-4[a-f0-9]{3}-[89ab][a-f0-9]{3}-[a-f0-9]{12}')

    base_url = 'https://arbeidsplassen.nav.no'
    init_logging(f'logs/nav_{curr_time}.log')

    try:
        if flags['daily_scrape']:
            toggles = ['&published=now%2Fd']
        else:
            url = f'{base_url}/stillinger'
   
            try:
                r = requests.get(url, headers=headers)
            except requests.exceptions.ConnectionError as e:
                logging.error(f'ConnectionError for {e}')
                return

            soup = BeautifulSoup(r.text, "html.parser")
            inputs = soup.find_all("input")
            inputs = [input_tag for input_tag in inputs
                      if 'checkbox' or 'radio' in input_tag.get('id', '')]

            toggles = [f'{input.get("name")}={input.get("value")}'
                       for input in inputs]

            if 'q=' in toggles:
                toggles.remove('q=')

        for t in toggles:

            logging.info(f'SCRAPING NAV WITH {t}')
            scraped_urls = previously_scraped(dirpath='nav', identifier='idx', n_files=50)
            iterate_pages_nav(curr_time=curr_time,
                              folder=folder,
                              headers=headers,
                              ad_pattern=ad_pattern,
                              id_pattern=id_pattern,
                              scraped_codes=scraped_urls,
                              base_url=base_url,
                              toggle=t)

            logging.info(f'FINISHED SCRAPING NAV WITH {t}')

    except Exception as e:
        logging.error(f'MAIN CRASHED WITH {e}')


if __name__ == "__main__":
    main()
