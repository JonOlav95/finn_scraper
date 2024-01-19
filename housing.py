import os
import re
from datetime import datetime

import pandas as pd
from selenium.webdriver.common.by import By

from load_selenium import load_driver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def scrape_one(driver):
    scrape_path = {
        'title': '//section[@data-testid="object-title"]//h1',
        'local_area_name': '//div[@data-testid="local-area-name"]',
        'pricing_inciactive': '//div[@data-testid="pricing-incicative-price"]//span[2]',
        'pricing_details': '//section[@data-testid="pricing-details"]//dl',
        'key_info': '//section[@data-testid="key-info"]//dl',
        'facilities': '//section[@data-testid="object-facilities"]//div',
        'about': '//div[@data-testid="om boligen"]//div',
        'location': '//span[@data-testid="object-address"]'
    }

    result_dict = {
        'url': driver.current_url,
        'scrape_time': datetime.today().strftime('%Y-%m-%d %H:%M:%S')
    }

    for key, value in scrape_path.items():
        try:
            content = driver.find_element(By.XPATH, value).text
        except:
            content = ''

        result_dict[key] = content

    try:
        result_dict['content_html'] = driver.page_source
    except:
        result_dict['content_html'] = ''

    return result_dict


def accept_cookie(driver):
    try:
        WebDriverWait(driver, 3).until(
            EC.frame_to_be_available_and_switch_to_it((By.XPATH, '//*[@id="sp_message_iframe_987797"]')))
        WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, '//button[@title="Godta alle"]'))).click()
        driver.switch_to.parent_frame()
    except:
        return


def save_result(filename, results):
    if os.path.isfile(f'finn_ads/{filename}'):
        df = pd.read_csv(f'finn_ads/{filename}')
    else:
        df = pd.DataFrame([])

    results_df = pd.DataFrame([results])
    df = pd.concat([df, results_df])
    df.to_csv(f'{filename}', index=False)


def main():
    base_url = 'https://www.finn.no/realestate'
    end_url = 'search.html?page=1&published=1'

    subsites = {
        'homes': f'{base_url}/homes/{end_url}',
        'newbuildings': f'{base_url}/newbuildings/{end_url}',
        'plots': f'{base_url}/plots/{end_url}',
        'leisuresale': f'{base_url}/leisuresale/{end_url}',
        'leisureplots': f'{base_url}/leisureplots/{end_url}',
        'lettings': f'{base_url}/lettings/{end_url}',
        'wanted': f'{base_url}/wanted/{end_url}',
        'businesssale': f'{base_url}/businesssale/{end_url}',
        'businessrent': f'{base_url}/businessrent/{end_url}',
        'businessplots': f'{base_url}/businessplots/{end_url}',
        'companyforsale': f'{base_url}/companyforsale/{end_url}',
        'abroad': f'{base_url}/abroad/{end_url}'
    }

    curr_time = datetime.today().strftime('%Y_%m_%d-%H:%M')
    filename = f'housing/housing_{curr_time}.csv'

    driver = load_driver()
    driver.get('https://www.finn.no/realestate/')
    accept_cookie(driver)

    current_page = 1

    while True:
        driver.get(f'https://www.finn.no/realestate/homes/search.html?page={current_page}&published=1')

        all_urls = driver.find_elements(By.TAG_NAME, 'a')
        all_urls = [u.get_attribute('href') for u in all_urls]

        page_urls = [u for u in all_urls if re.compile(r'page=\d+').search(u) and 'homes' in u]
        ad_urls = [u for u in all_urls if re.compile(r'finnkode=\d+').search(u) and 'homes' in u]

        for url in ad_urls:
            driver.get(url)
            results = scrape_one(driver)
            save_result(filename, results)

        current_page += 1

        if f'https://www.finn.no/realestate/homes/search.html?page={current_page}&published=1' not in page_urls:
            break


if __name__ == "__main__":
    main()
