import os
import random
import re
import time
import logging
import pandas as pd
import selenium.common.exceptions

from datetime import datetime

from pandas.errors import EmptyDataError

from load_selenium import load_driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from scrape_helpers import get_sub_urls, load_xpaths, init_logging


def scrape_page(driver, key, xpaths):

    result_dict = {
        'url': driver.current_url,
        'scrape_time': datetime.today().strftime('%Y-%m-%d %H:%M:%S'),
    }

    if not xpaths:
        result_dict['content_html'] = driver.find_element(By.TAG_NAME, "body").get_attribute("outerHTML")
        result_dict['sub_domain'] = key
    else:
        for k, value in xpaths.items():
            try:
                content = driver.find_element(By.XPATH, value).text
            except selenium.common.exceptions.NoSuchElementException:
                content = ''

            result_dict[k] = content

    if 'title' in result_dict:
        logging.info(f'{key} TITLE: {result_dict["title"]}')
    else:
        logging.info(f'{key} URL: {driver.current_url}')

    return result_dict


def accept_cookie(driver):

    # Trigger cookie
    driver.get('https://www.finn.no/realestate/homes/search.html?published=1')

    try:
        WebDriverWait(driver, 3).until(
            EC.frame_to_be_available_and_switch_to_it((By.XPATH, '//*[@id="sp_message_iframe_987797"]')))
        WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.XPATH, '//button[@title="Godta alle"]'))).click()
        driver.switch_to.parent_frame()
    except selenium.common.exceptions.TimeoutException:
        logging.critical('Failed to accept cookie.')


def construct_metadata(folder):
    metadata = []

    for (dirpath, direnames, filenames) in os.walk(folder):
        for f in filenames:

            try:
                df = pd.read_csv(f'{dirpath}/{f}')
            except EmptyDataError:
                continue

            n_ads = len(df.index)

            if n_ads == 0:
                os.remove(f'{dirpath}/{f}')
                continue

            date_and_time = re.search(r'(\d{4}_\d{2}_\d{2}-\d{2}:\d{2})', f)

            if not date_and_time:
                continue

            parsed_datetime = datetime.strptime(date_and_time[0], '%Y_%m_%d-%H:%M')
            parsed_datetime = parsed_datetime.strftime('%Y_%m_%d-%H:%M')

            row = {
                'filename': f,
                'datetime': parsed_datetime,
                'n_ads': n_ads
            }

            metadata.append(row)

    metadata.sort(key=lambda x: x['datetime'])

    return metadata


def previously_scraped():
    folder = 'scrapes'

    metadata = construct_metadata(folder)
    metadata = metadata[:30]
    files = [d['filename'] for d in metadata]

    if not files:
        return []

    previous_scrapes = pd.concat((pd.read_csv(f'{folder}/{f}') for f in files if os.path.isfile(f'{folder}/{f}')),
                                 ignore_index=True)

    scraped_urls = previous_scrapes['url'].to_list()

    return scraped_urls


def scrape_sub_url(driver, curr_time, sub_url, scraped_urls, xpaths):

    domain_url = BASE_URL + sub_url
    pattern = re.compile(r'finn\.no/(\w+)/(\w+)')

    # Iterate every page until the maximum of 50
    for current_page in range(1, 50):
        logging.info(f'Scraping page {current_page}')

        driver.get(f'{domain_url}/search.html?page={current_page}&published=1')

        all_urls = driver.find_elements(By.TAG_NAME, 'a')
        all_urls = [u.get_attribute('href') for u in all_urls]

        page_urls = [u for u in all_urls if re.compile(r'page=\d+').search(u) and sub_url in u]
        ad_urls = [u for u in all_urls if re.compile(r'finnkode=\d+').search(u)]

        page_ads = {}

        # Scrape every ad url on the given page
        for url in ad_urls:

            if url in scraped_urls:
                logging.info(f'ALREADY SCRAPED: {url}')
                continue

            scraped_urls.append(url)

            key = re.search(pattern, url).group(2)

            if key in xpaths.keys():
                key_xpaths = xpaths[key]
                filename_key = key
            else:
                key_xpaths = None
                filename_key = 'other'

            driver.execute_script("window.open(arguments[0], '_blank');", url)
            driver.switch_to.window(driver.window_handles[1])

            results = scrape_page(driver, key, key_xpaths)

            driver.close()
            driver.switch_to.window(driver.window_handles[0])

            if filename_key in page_ads.keys():
                page_ads[filename_key].append(results)
            else:
                page_ads[filename_key] = [results]


            time.sleep(random.uniform(0.5, 1.5))


        for filename_key, value in page_ads.items():
            filename = f'scrapes/{filename_key}_{curr_time}.csv'
            value_df = pd.DataFrame(value)

            if os.path.isfile(filename_key):
                scrape_df = pd.read_csv(filename)
                value_df = pd.concat([scrape_df, value_df])

            value_df.to_csv(filename, index=False)


        if f'{domain_url}/search.html?published=1&page={current_page + 1}' not in page_urls:
            logging.info(f'FINISHED SCRAPING {sub_url}.')
            break


def main():
    driver = load_driver()
    driver.get(BASE_URL)
    accept_cookie(driver)

    xpaths = load_xpaths()
    sub_urls = get_sub_urls()
    curr_time = datetime.today().strftime('%Y_%m_%d-%H:%M')

    init_logging(f'logs/{curr_time}.log')

    for sub_url in sub_urls:
        logging.info(f'SCRAPING DOMAIN: {sub_url}')
        scraped_urls = previously_scraped()
        scrape_sub_url(driver, curr_time, sub_url, scraped_urls, xpaths)


if __name__ == "__main__":
    BASE_URL = 'https://www.finn.no/'
    main()
