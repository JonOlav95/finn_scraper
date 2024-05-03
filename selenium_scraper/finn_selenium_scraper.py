import os
import random
import re
import time
import logging
import pandas as pd
import selenium.common.exceptions

from datetime import datetime
from selenium_scraper.load_selenium import load_driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from helpers import get_sub_urls, load_xpaths, init_logging, extract_datetime


def scrape_page(driver, key, xpaths):
    """ Scrapes the page using selenium and spesifications from the key (ad type) and the corresponding xpaths.

    If the xpath config is not present for the given key, the HTML code is downloaded instead.

    :param driver: Selenium webdriver.
    :param key: The key, or ad type, which informs which type of ad the page consists of.
    :param xpaths: Dictionary pointing to the xpaths given the ad type. None if the xpath is not set for the ad type.
    :return: The scraped data as dictionary. The keys of the dictionary depends on the ad type.
    """
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
                content = driver.find_element(By.XPATH, value).get_attribute('innerHTML') # TODO
            except selenium.common.exceptions.NoSuchElementException:
                content = ''

            result_dict[k] = content

    if 'title' in result_dict:
        logging.info(f'{key} TITLE: {result_dict["title"]}')
    else:
        logging.info(f'{key} URL: {driver.current_url}')

    return result_dict


def accept_cookie(driver):
    """When scraping housing, accepting a cookie is required at the initial link."""

    # Trigger cookie
    driver.get('https://www.finn.no/realestate/homes/search.html?published=1')

    try:
        WebDriverWait(driver, 3).until(
            EC.frame_to_be_available_and_switch_to_it((By.XPATH, '//*[@title="SP Consent Message"]')))
        WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.XPATH, '//button[@title="Godta alle"]'))).click()
        driver.switch_to.parent_frame()
    except selenium.common.exceptions.TimeoutException:
        logging.critical('Failed to accept cookie.')


def previously_scraped():
    dirpath = 'scrapes'
    n_files = 30

    metadata = []

    filenames = os.listdir(dirpath)
    filenames = sorted(filenames, key=extract_datetime)
    filenames = filenames[-n_files:]

    for f in filenames:

        with open(f'{dirpath}/{f}', encoding='utf-8') as file:
            n_ads = sum(1 for _ in file)

        if n_ads == 0:
            os.remove(f'{dirpath}/{f}')
            continue

        row = {
            'filename': f,
            'datetime': extract_datetime(f),
            'n_ads': n_ads
        }

        metadata.append(row)

    # No previous scrapes
    if not metadata:
        return []

    files = [d['filename'] for d in metadata]

    previous_scrapes = pd.concat(
        (pd.read_csv(f'{dirpath}/{f}', encoding='utf-8') for f in files if os.path.isfile(f'{dirpath}/{f}')),
        ignore_index=True)

    scraped_urls = previous_scrapes['url'].to_list()

    return scraped_urls


def scrape_sub_url(driver, curr_time, sub_url, scraped_urls, xpaths):
    """ Scrape a subdomain. This can for example be finn.com/housing/homes. Though the subdomain in the
    example is homes, other keys can be present on the page, such as newbuildings.

    The function scrapes through all ads which has been uploaded within 24 hours.

    :param driver: Selenium web driver.
    :param curr_time: Time and the intiation of the process. Used for filenames.
    :param sub_url: The current sub url which is being scraped. E.g. /homes, /fulltime.
    :param scraped_urls: List of previously scraped URLs to reduce repeat scrapes.
    :param xpaths: Xpath spesifications for the different type of ads.
    """
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

        # Scrape every ad url on the given page.
        # Scraping is done by opening up the ad in a new tab, then downloading the data.
        # The tab is then closed, and selenium returns to the initial page tab without
        # making a new request.
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


        # Write the scraped data to CSV files corresponding to their ad type.
        # TODO: Write only once
        for filename_key, value in page_ads.items():
            filename = f'scrapes/{filename_key}_{curr_time}.csv'
            value_df = pd.DataFrame(value)

            if os.path.isfile(filename):
                scrape_df = pd.read_csv(filename, encoding='utf-8')
                value_df = pd.concat([scrape_df, value_df])

            value_df.to_csv(filename, index=False, encoding='utf-8')


        if f'{domain_url}/search.html?published=1&page={current_page + 1}' not in page_urls:
            logging.info(f'FINISHED SCRAPING {sub_url}.')
            break


def main():
    curr_time = datetime.today().strftime('%Y_%m_%d-%H_%M')
    init_logging(f'logs/{curr_time}.log')

    driver = load_driver()
    driver.get(BASE_URL)
    accept_cookie(driver)

    xpaths = load_xpaths()
    sub_urls = get_sub_urls()

    # Iterate the different subdomains used to scrape the daily ads
    for sub_url in sub_urls:
        logging.info(f'SCRAPING DOMAIN: {sub_url}')
        scraped_urls = previously_scraped()
        scrape_sub_url(driver, curr_time, sub_url, scraped_urls, xpaths)


if __name__ == "__main__":
    BASE_URL = 'https://www.finn.no/'
    main()
