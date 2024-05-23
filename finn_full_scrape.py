import requests
from bs4 import BeautifulSoup
from lxml import etree
from datetime import datetime

from misc_helpers import get_sub_urls, load_xpath, init_logging, load_random_headers
from scrape_helpers import previously_scraped
from scrape_functions import scrape_page
from finn_scraper import scrape_sub_url


def main():
    sub_urls = get_sub_urls()
    curr_time = datetime.today().strftime('%Y_%m_%d')
    headers = load_random_headers()
    BASE_URL = 'https://www.finn.no/'

    curr_time = datetime.today().strftime('%Y_%m_%d')
    init_logging(f'logs/finn_{curr_time}.log')

    for sub_url in sub_urls:
        scraped_codes = previously_scraped(dirpath='finn', 
                                           column='finn_code', 
                                           n_files=50)
        

        url = f'{BASE_URL}{sub_url}/search.html'
        r = requests.get(url, headers=headers)

        soup = BeautifulSoup(r.text, "html.parser")
        divs = soup.find_all("div", {"class": "input-toggle"})
        toggle_inputs = [div.find("input", {"type": "checkbox"}) for div in divs]
        toggles = [u.get("id") for u in toggle_inputs]

        for t in toggles:
            print(f"scraping {sub_url} with {t}")
            scrape_sub_url(curr_time, scraped_codes, BASE_URL + sub_url, t, headers)
            print("finished scraping")



if __name__ == "__main__":
    main()
