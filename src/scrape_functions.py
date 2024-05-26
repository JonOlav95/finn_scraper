import os
import re
import time
import random
import logging
import requests
import pandas as pd

from lxml import etree
from datetime import datetime
from bs4 import BeautifulSoup
from xpaths import load_xpath


def store_data(page_ads, folder, curr_time):
    for xpath_key in page_ads.keys():

        filename = f'{folder}/{xpath_key}_{curr_time}.csv'
        value_df = pd.DataFrame(page_ads[xpath_key])

        if os.path.isfile(filename):
            scrape_df = pd.read_csv(filename, encoding='utf-8')
            value_df = pd.concat([scrape_df, value_df])

        value_df.to_csv(filename, index=False, encoding='utf-8')


def scrape_single_page(url, xpaths, scrape_key, headers, **kwargs):
    r = requests.get(url, headers=headers)

    if r.status_code != 200:
        logging.critical(f"SCRAPE PAGE RESPONSE CODE {r.status_code}, URL: {url}")
        return

    tree = etree.HTML(r.text)

    result_dict = {
        'url': url,
        'scrape_time': datetime.today().strftime('%Y-%m-%d %H:%M:%S'),
        **kwargs
    }

    if not xpaths:
        logging.info("NO XPATHS")
        logging.info(f'{scrape_key} URL: {url}')

        entire_html = etree.tostring(tree, encoding='unicode')
        result_dict["html"] = entire_html

        return result_dict

    for k, v in xpaths.items():
        content = tree.xpath(v)

        if not content:
            result_dict[k] = None
        else:
            result_dict[k] = etree.tostring(content[0], method='html', encoding='unicode')


    if 'title' in result_dict:
        title = etree.tostring(etree.fromstring(result_dict['title']), method="text", encoding="unicode")
        logging.info(f'{scrape_key} TITLE: {title.rstrip()}')
    else:
        logging.info(f'{scrape_key} URL: {url}')

    return result_dict


def iterate_pages(curr_time,
                  folder,
                  headers,
                  page_iterator,
                  scraped_codes,
                  ad_pattern,
                  xpath_key_pattern,
                  id_pattern):

    for page_number in range(100):
        logging.info(f'SCRAPING PAGE {page_number + 1}')

        time.sleep(random.uniform(0.75, 1.5))

        url = page_iterator(page_number)
        r = requests.get(url, headers=headers)

        if r.status_code == 400:
            return
        if r.status_code != 200:
            logging.critical(f"ITERATE PAGE RESPONSE CODE {r.status_code}, URL: {url}")
            continue

        headers['Referer'] = url
        soup = BeautifulSoup(r.text, "html.parser")

        a_tags = soup.find_all("a")
        all_urls = [u.get('href') for u in a_tags]

        ad_urls = [u for u in all_urls if ad_pattern.search(u)]

        if not ad_urls:
            logging.info('NO ADS ON PAGE')
            return

        page_ads = {}

        for url in ad_urls:
            idx = id_pattern.search(url).group(0)

            if idx in scraped_codes:
                continue

            scraped_codes.append(idx)

            xpath_key = xpath_key_pattern.findall(url)[0]
            xpaths = load_xpath(xpath_key)

            if not xpaths:
                xpath_key = 'other'

            result = scrape_single_page(url=url, headers=headers, scrape_key=xpath_key,
                                        xpaths=xpaths, idx=idx)

            if xpath_key in page_ads.keys():
                page_ads[xpath_key].append(result)
            else:
                page_ads[xpath_key] = [result]

            time.sleep(random.uniform(0.75, 1.5))

        store_data(page_ads, folder, curr_time)

        time.sleep(random.uniform(2.5, 5.5))
