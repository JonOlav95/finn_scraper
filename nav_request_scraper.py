import requests
import re
import time
from lxml import etree
from bs4 import BeautifulSoup


def scrape_nav_page(url):
    r = requests.get(url)
    tree = etree.HTML(r.text)


    text_xpaths = {
        'title': '//*[@id="main-content"]/article/h1',
        'company': '//*[@id="main-content"]/article/section[1]/div[1]/p',
        'location': '//*[@id="main-content"]/article/section[1]/div[2]/p',
        'content': '//*[@id="main-content"]/article/section[2]',
        'contact_person': '//h2[contains(text(), "Kontaktperson for stillingen")]/..',
        'employer': '//h2[contains(text(), "Om bedriften")]/..',
        'deadline': '/html/body/div/div/main/div/article/div/div[2]/div/dl/dd/p',
    }

    html_xpaths = {
        'about': '//h2[contains(text(), "Om jobben")]/..',
        'ad_data': '//h2[contains(text(), "Annonsedata")]/..',
        'source': '/html/body/div/div/main/div/article/div/div[2]/div/div',
    }

        
    result_dict = {}

    for k, v in text_xpaths.items():    
        content = tree.xpath(v)

        if not content:
            continue
    
        result_dict[k] = etree.tostring(content[0], method='text', encoding='unicode')

    for k, v in html_xpaths.items():    
        content = tree.xpath(v)

        if not content:
            continue

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
            break

        for url in ad_urls:
            page = BASE_URL + url
            scrape_nav_page(page)

            time.sleep(1)

        page += 1


if __name__ == "__main__":
    headers = {
        "User-Agent": "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2859.0 Safari/537.36",
        "Accept-Language": "en-GB,en,q=0.5",
        "Referer": "https://google.com",
        "DNT": "1"
    }

    BASE_URL = "https://arbeidsplassen.nav.no"
    main()
