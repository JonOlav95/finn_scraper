import os
import random
import re
import time
import logging
import pandas as pd
import requests

from datetime import datetime
from lxml import etree
from bs4 import BeautifulSoup
from helpers import get_sub_urls, load_xpath, init_logging, extract_datetime


def scrape_page(key, xpaths, url):

    code = re.compile(r'(?<=finnkode=)\d+').search(url).group(0)


    r = requests.get(url)
    tree = etree.HTML(r.text)
        
    result_dict = {
        'finn_code': code,
        "key": key,
        "url": url,
        'scrape_time': datetime.today().strftime('%Y-%m-%d %H:%M:%S')
    }

    if not xpaths:
        logging.info("NO XPATHS")
        logging.info(f'{key} URL: {url}')
        return result_dict
        # result_dict['content_html'] = driver.find_element(By.TAG_NAME, "body").get_attribute("outerHTML")
        # result_dict['sub_domain'] = key

    text_xpaths = xpaths["text"]
    html_xpaths = xpaths["html"]

    for k, value in text_xpaths.items():
        content = tree.xpath(value)
        if not content:
            result_dict[k] = None
        else:
            result_dict[k] = etree.tostring(content[0], method='text', encoding='unicode')

    for k, value in html_xpaths.items():
        content = tree.xpath(value)
        if not content:
            result_dict[k] = None
        else:
            result_dict[k] = etree.tostring(content[0], method='html', encoding='unicode')


    if 'title' in result_dict:
        logging.info(f'{key} TITLE: {result_dict["title"]}')
    else:
        logging.info(f'{key} URL: {url}')

    return result_dict


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


def scrape_sub_url(curr_time, sub_url, scraped_urls):

    domain_url = BASE_URL + sub_url
    pattern = re.compile(r'finn\.no/(\w+)/(\w+)')

    # Iterate every page until the maximum of 50
    for current_page in range(1, 50):
        logging.info(f'Scraping page {current_page}')

        r = requests.get(f'{domain_url}/search.html?page={current_page}&published=1')

        html_content = r.text

        soup = BeautifulSoup(html_content, "html.parser")
        a_tags = soup.find_all("a")

        all_urls = [u.get("href") for u in a_tags]

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
            
            # Key may differ from suburl
            key = re.search(pattern, url).group(2)
            xpath = load_xpath(key)

            results = scrape_page(key, xpath, url)

            if not xpath:
                key = 'other'

            if key in page_ads.keys():
                page_ads[key].append(results)
            else:
                page_ads[key] = [results]

            time.sleep(random.uniform(0.5, 1.5))

        # Write result to file
        for key in page_ads.keys():
            filename = f'scrapes/{key}_{curr_time}.csv'
            value_df = pd.DataFrame(page_ads[key])

            if os.path.isfile(filename):
                scrape_df = pd.read_csv(filename, encoding='utf-8')
                value_df = pd.concat([scrape_df, value_df])

            value_df.to_csv(filename, index=False, encoding='utf-8')


        if f'{domain_url}/search.html?published=1&page={current_page + 1}' not in page_urls:
            logging.info(f'FINISHED SCRAPING {sub_url}.')
            return


def main():
    curr_time = datetime.today().strftime('%Y_%m_%d_%H_%M')
    init_logging(f'logs/{curr_time}.log')

    sub_urls = get_sub_urls()

    # Iterate the different subdomains used to scrape the daily ads
    for sub_url in sub_urls:
        logging.info(f'SCRAPING DOMAIN: {sub_url}')
        scraped_urls = previously_scraped()
        scrape_sub_url(curr_time, sub_url, scraped_urls)


if __name__ == "__main__":
    headers = {
        "User-Agent": "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2859.0 Safari/537.36",
        "Accept-Language": "en-GB,en,q=0.5",
        "Referer": "https://google.com",
        "DNT": "1"
    }
    BASE_URL = 'https://www.finn.no/'
    main()
