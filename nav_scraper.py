from datetime import datetime
from load_selenium import load_driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import selenium.common.exceptions

import re


def scrape_nav_page(driver):
    xpaths = {
        'title': '/html/body/div/div/main/div/article/div/div[1]/h1',
        'location': '/html/body/div/div/main/div/article/div/div[1]/section[1]/div[2]/p',
        'company': '/html/body/div/div/main/div/article/div/div[1]/section[1]/div[1]/p',
        'content': '/html/body/div/div/main/div/article/div/div[1]/div',
        'empolyer': '//h2[contains(text(), "Om arbeidsgiveren")]/..', #html,
        'about': '//h2[contains(text(), "Om stillingen")]/..',
        'deadline': '/html/body/div/div/main/div/article/div/div[2]/div/dl/dd/p',
        'source': '/html/body/div/div/main/div/article/div/div[2]/div/div'
    }

    result_dict = {
        'url': driver.current_url,
        'scrape_time': datetime.today().strftime('%Y-%m-%d %H:%M:%S'),
    }

    for k, value in xpaths.items():
        try:
            content = driver.find_element(By.XPATH, value).get_attribute('innerHTML')
        except selenium.common.exceptions.NoSuchElementException:
            content = ''

        result_dict[k] = content


    return result_dict


def main():

    driver = load_driver()

    driver.get('https://arbeidsplassen.nav.no/stillinger?published=now%2Fd')

    all_urls = driver.find_elements(By.TAG_NAME, 'a')
    all_urls = [u.get_attribute('href') for u in all_urls]

    ad_urls = [u for u in all_urls if re.compile(r'(\/stillinger\/stilling\/.+)').search(u)]

    print(ad_urls)

    for url in ad_urls:
        driver.get(url)
        result = scrape_nav_page(driver)



if __name__ == "__main__":
    main()
