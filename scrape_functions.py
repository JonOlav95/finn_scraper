import requests
import logging

from datetime import datetime
from lxml import etree


def scrape_page(url, xpaths, scrape_key, headers, **kwargs):
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
