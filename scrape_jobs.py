import os
import random
import math
import re
import time
import pandas as pd
import logging

from datetime import datetime
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from load_selenium import load_driver
from logger import init_logging


def store_other_ad(driver):
    job_ad = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid^='aggregated-ad-object']")))

    scrape = {
        'definition_1': "div[1]//dl[1]",
        'title': "div[1]//h1[1]",
        'content': "div[1]//section[1]",
        'definition_2': "div[2]//dl[1]"
    }

    result_dict = {
        'url': driver.current_url,
        'scrape_time': datetime.today().strftime('%Y-%m-%d %H:%M:%S')
    }

    for key, value in scrape.items():
        try:
            content = job_ad.find_element(By.XPATH, value).text
        except:
            content = ''

        result_dict[key] = content

    try:
        content = job_ad.find_element(By.XPATH, "div[1]//section[1]")
        result_dict['content_html'] = content.get_attribute("outerHTML")
    except:
        result_dict['content_html'] = ''

    source = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid^='sok-her-box'")))
    source = source.find_element(By.XPATH, 'span[1]').text
    result_dict['source'] = source

    return result_dict


def store_finn_ad(driver):
    job_ad = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "[data-controller^='storeVisitedAd trackAd']")))

    scrape = {
        'title': "section[1]",
        'definition_1': "section[2]",
        'content': "//div[@class='import-decoration']",
        'definition_2': "//dl[@class='definition-list definition-list--inline']",
        'keywords': "//*[contains(text(),'Nøkkelord')]/.."
    }

    result_dict = {
        'url': driver.current_url,
        'scrape_time': datetime.today().strftime('%Y-%m-%d %H:%M:%S'),
        'source': 'finn'
    }

    for key, value in scrape.items():
        try:
            content = job_ad.find_element(By.XPATH, value).text
        except Exception as e:
            content = ''

        result_dict[key] = content

    try:
        content = job_ad.find_element(By.XPATH, "//div[@class='import-decoration']")
        result_dict['content_html'] = content.get_attribute("outerHTML")
    except:
        result_dict['content_html'] = ''

    return result_dict


def get_ads_per_page(driver):
    section = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'page-results')))
    job_div = section.find_element(By.XPATH, './/div[position()=4]')
    jobs = job_div.find_elements(By.TAG_NAME, "article")

    jobs_on_page = len(jobs)

    return jobs_on_page


def collect_ads(driver, filename, ads_list, urls, finn_ad=True):
    ads_on_page = len(ads_list)

    if os.path.isfile(f'finn_ads/{filename}'):
        df = pd.read_csv(f'finn_ads/{filename}')
    else:
        df = pd.DataFrame([])

    for j in range(ads_on_page):

        article = ads_list[j]
        first_a = article.find_element(By.CSS_SELECTOR, 'a:first-child')
        ad_link = first_a.get_attribute('href')

        if ad_link in urls:
            logging.info(f'{ad_link} previously scraped.')
            continue

        urls.append(ad_link)

        driver.execute_script("window.open(arguments[0], '_blank');", ad_link)
        driver.switch_to.window(driver.window_handles[1])

        if finn_ad:
            ads_data = store_finn_ad(driver)
        else:
            ads_data = store_other_ad(driver)

        logging.info(f"Scarped ad title '{ads_data['title']}'")
        ads_data = pd.DataFrame([ads_data])
        df = pd.concat([df, ads_data])
        df.to_csv(f'finn_ads/{filename}', index=False)

        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        time.sleep(random.uniform(0.5, 1.5))


def construct_metadata():
    metadata = []

    for (dirpath, direnames, filenames) in os.walk('finn_ads'):
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

    previous_scrapes = pd.concat((pd.read_csv(f'finn_ads/{f}') for f in files if os.path.isfile(f'finn_ads/{f}')),
                                 ignore_index=True)

    scraped_urls = previous_scrapes['url'].to_list()

    return scraped_urls


def main():
    curr_time = datetime.today().strftime('%Y_%m_%d-%H:%M')
    filename = f'finn_{curr_time}.csv'

    init_logging(f'logs/finn_{curr_time}.log')
    logging.info(f'Initiated scrape at {curr_time} under filename {filename}')

    urls = previously_scraped()

    driver = load_driver()

    driver.get("https://www.finn.no/job/fulltime/search.html?published=1")

    n_jobs_info = driver.find_element(By.CLASS_NAME, "flex-shrink-0").text
    n_jobs_info = n_jobs_info.replace(' ', '')

    n_ads = int(re.search(r'(\d+)annonser', n_jobs_info).group(1))

    n_pages = int(math.ceil(n_ads / get_ads_per_page(driver)))
    logging.info(f'{n_pages} pages to scrape.')

    for i in range(1, n_pages + 1):
        driver.get(f"https://www.finn.no/job/fulltime/search.html?page={i}&published=1")
        section = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'page-results')))
        div_list = section.find_elements(By.XPATH, "./*")

        # Select div with jobs
        main_ads = div_list[3]
        main_ads = main_ads.find_elements(By.TAG_NAME, "article")

        collect_ads(driver, filename, main_ads, urls)

        # If length 5, page contains non-finn adds
        if len(div_list) == 5:
            extra_ads = div_list[4]
            extra_ads = extra_ads.find_elements(By.TAG_NAME, "article")
            collect_ads(driver, filename, extra_ads, urls, finn_ad=False)

        logging.info(f'Scraped page {i} out of {n_pages}')


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logging.exception("main crashed. Error: %s", e)
