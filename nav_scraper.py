import requests
import re
import random
import time
import os
import logging
import pandas as pd

from datetime import datetime
from lxml import etree
from bs4 import BeautifulSoup

from scrape_helpers import previously_scraped
from misc_helpers import load_random_headers, init_logging


def scrape_nav_page(url):
    r = requests.get(url, headers=HEADERS)
    tree = etree.HTML(r.text)
        
    result_dict = {
        'url': url,
        'scrape_time': datetime.today().strftime('%Y-%m-%d %H:%M:%S')
    }

    for k, v in text_xpaths.items():    
        content = tree.xpath(v)

        if not content:
            result_dict[k] = None
        else:
            result_dict[k] = etree.tostring(content[0], method='text', encoding='unicode')

    for k, v in html_xpaths.items():    
        content = tree.xpath(v)

        if not content:
            result_dict[k] = None
        else:
            result_dict[k] = etree.tostring(content[0], method='html', encoding='unicode')


    if 'title' in result_dict:
        logging.info(f'TITLE: {result_dict["title"]}')
    else:
        logging.info(f'URL: {url}')

    return result_dict


def main():
    curr_time = datetime.today().strftime('%Y_%m_%d_%H_%M')
    init_logging(f'logs/nav_{curr_time}.log')

    filename = f'nav/nav_{curr_time}.csv'

    scraped_urls = previously_scraped('nav', 'url', 30)
    page = 0

    while True:
        url = f"{BASE_URL}/stillinger?from={page * 25}&published=now%2Fd"

        r = requests.get(url, headers=HEADERS)
        html_content = r.text

        soup = BeautifulSoup(html_content, "html.parser")
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

            result = scrape_nav_page(url)
            ads.append(result)

            time.sleep(random.uniform(0.75, 1.5))


        if os.path.isfile(filename):
            scrape_df = pd.read_csv(filename, encoding='utf-8')

        if ads:
            value_df = pd.DataFrame(ads)
            value_df = pd.concat([scrape_df, value_df])
            value_df.to_csv(filename, index=False, encoding='utf-8')

        page += 1


if __name__ == "__main__":
    HEADERS = load_random_headers()

    text_xpaths = {
        'title': '//*[@id="main-content"]/article/h1',
        'company': '//*[@id="main-content"]/article/section[1]/div[1]/p',
        'location': '//*[@id="main-content"]/article/section[1]/div[2]/p',
        'job_posting_text': '//div[contains(@class, "job-posting-text")]',
        'employer': '//h2[contains(text(), "Om bedriften")]/../div',
        'deadline': '//h2[contains(text(), "Søk på jobben")]/../p',
    }

    html_xpaths = {
        'about': '//h2[contains(text(), "Om jobben")]/../../dl',
        'contact_person': '//h2[contains(text(), "Kontaktperson for stillingen") or contains(text(), "Kontaktpersoner for stillingen")]/..',
        'ad_data': '//h2[contains(text(), "Annonsedata")]/../dl'
    }

    BASE_URL = "https://arbeidsplassen.nav.no"
    
    main()
