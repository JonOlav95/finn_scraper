import os
import random
import re
import time
import logging
import pandas as pd
import selenium.common.exceptions

from datetime import datetime
from logger import init_logging
from housing_xpaths import scraping_xpaths
from load_selenium import load_driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def scrape_page(driver, key):
    xpaths = scraping_xpaths[key]

    result_dict = {
        'url': driver.current_url,
        'scrape_time': datetime.today().strftime('%Y-%m-%d %H:%M:%S'),
    }

    if not xpaths:
        result_dict['content_html'] = driver.find_element(By.TAG_NAME, "main").get_attribute("outerHTML")

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
    try:
        WebDriverWait(driver, 3).until(
            EC.frame_to_be_available_and_switch_to_it((By.XPATH, '//*[@id="sp_message_iframe_987797"]')))
        WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.XPATH, '//button[@title="Godta alle"]'))).click()
        driver.switch_to.parent_frame()
    except selenium.common.exceptions.TimeoutException:
        logging.critical('Failed to accept cookie.')


def construct_metadata():
    metadata = []

    for (dirpath, direnames, filenames) in os.walk('housing'):
        for f in filenames:
            df = pd.read_csv(f'{dirpath}/{f}')

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
    metadata = construct_metadata()
    metadata = metadata[:30]
    files = [d['filename'] for d in metadata]

    if not files:
        return []

    previous_scrapes = pd.concat((pd.read_csv(f'housing/{f}') for f in files if os.path.isfile(f'housing/{f}')),
                                 ignore_index=True)

    scraped_urls = previous_scrapes['url'].to_list()

    return scraped_urls


def main():
    scraped_urls = previously_scraped()

    base_url = 'https://www.finn.no/realestate'
    driver = load_driver()
    driver.get(base_url)
    accept_cookie(driver)

    curr_time = datetime.today().strftime('%Y_%m_%d-%H:%M')
    init_logging(f'logs/housing_{curr_time}.log')

    for key in scraping_xpaths.keys():
        logging.info(f'STARTED SCRAPING {key}')

        filename = f'housing/{key}_{curr_time}.csv'

        if os.path.isfile(filename):
            scrape_df = pd.read_csv(filename)
        else:
            scrape_df = pd.DataFrame([])

        # Iterate every page until the maximum of 50
        for current_page in range(1, 50):
            logging.info(f'Scraping page {current_page}')

            driver.get(f'{base_url}/{key}/search.html?page={current_page}&published=1')

            all_urls = driver.find_elements(By.TAG_NAME, 'a')
            all_urls = [u.get_attribute('href') for u in all_urls]

            page_urls = [u for u in all_urls if re.compile(r'page=\d+').search(u) and key in u]
            ad_urls = [u for u in all_urls if re.compile(r'finnkode=\d+').search(u) and key in u]

            # Scrape every ad url on the given page
            for url in ad_urls:

                if url in scraped_urls:
                    logging.info(f'ALREADY SCRAPED: {url}')
                    continue

                driver.execute_script("window.open(arguments[0], '_blank');", url)
                driver.switch_to.window(driver.window_handles[1])

                results = scrape_page(driver, key)
                results_df = pd.DataFrame([results])

                scrape_df = pd.concat([scrape_df, results_df])
                scrape_df.to_csv(filename, index=False)

                driver.close()
                driver.switch_to.window(driver.window_handles[0])

                time.sleep(random.uniform(0.5, 1.5))

            if f'{base_url}/{key}/search.html?published=1&page={current_page + 1}' not in page_urls:
                logging.info(f'FINISHED SCRAPING {key}.')
                break


if __name__ == "__main__":
    main()
