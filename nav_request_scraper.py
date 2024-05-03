import requests
import re
import time

from datetime import datetime
from lxml import etree
from bs4 import BeautifulSoup


def scrape_nav_page(url):
    r = requests.get(url)
    tree = etree.HTML(r.text)
        
    result_dict = {
        "url": url,
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


    return result_dict


def main():

    page = 0

    while True:
        url = f"{BASE_URL}/stillinger?from={page * 25}&published=now%2Fd"

        r = requests.get(url, headers=headers)
        html_content = r.text

        soup = BeautifulSoup(html_content, "html.parser")
        a_tags = soup.find_all("a")

        all_urls = [u.get("href") for u in a_tags]
        
        ad_urls = [u for u in all_urls if re.compile(r'(\/stillinger\/stilling\/.+)').search(u)]

        if not ad_urls:
            return

        for url in ad_urls:
            url = BASE_URL + url
            
            scrape_nav_page(url)

            time.sleep(1)

        page += 1


if __name__ == "__main__":
    headers = {
        "User-Agent": "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2859.0 Safari/537.36",
        "Accept-Language": "en-GB,en,q=0.5",
        "Referer": "https://google.com",
        "DNT": "1"
    }

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
        'contact_person': '//h2[contains(text(), "Kontaktperson for stillingen")]/..',
        'ad_data': '//h2[contains(text(), "Annonsedata")]/../dl'
    }

    BASE_URL = "https://arbeidsplassen.nav.no"
    main()
