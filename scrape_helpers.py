import logging
import os
import sys

import yaml


def init_logging(filename):
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')

    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setLevel(logging.DEBUG)
    stdout_handler.setFormatter(formatter)

    file_handler = logging.FileHandler(filename)
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(stdout_handler)



def load_flags():
    location = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    f = open(os.path.join(location, "parameters.yml"), "r")
    flags = yaml.safe_load(f)
    f.close()

    return flags


def load_xpaths():
    return {
        'homes': {
            'title': '//section[@data-testid="object-title"]//h1',
            'local_area_name': '//div[@data-testid="local-area-name"]',
            'pricing_inciactive': '//div[@data-testid="pricing-incicative-price"]//span[2]',
            'pricing_details': '//section[@data-testid="pricing-details"]//dl',
            'key_info': '//section[@data-testid="key-info"]//dl',
            'facilities': '//section[@data-testid="object-facilities"]//div',
            'about': '//section[@data-testid="about-property"]',
            'location': '//span[@data-testid="object-address"]'
        },
        'lettings': {
            'title': '//section[@data-testid="object-title"]//h1',
            'pricing_common_monthly_cost': '//div[@data-testid="pricing-common-monthly-cost"]//dd',
            'pricing_depositum': '//div[@data-testid="pricing-deposit"]//dd',
            'pricing_common_includes': '//div[@data-testid="pricing-common-includes"]//dd',
            'key_info': '//section[@data-testid="key-info"]//dl',
            'facilities': '//section[@data-testid="object-facilities"]//div',
            'about': '//section[@data-testid="about-property"]',
            'location': '//span[@data-testid="object-address"]'
        },

        'fulltime': {
            'title': "//div[@data-controller='storeVisitedAd trackAd']//section[1]",
            'definition_1': "//div[@data-controller='storeVisitedAd trackAd']//section[2]",
            'content': "//div[@class='import-decoration']",
            'definition_2': "//dl[@class='definition-list definition-list--inline']",
            'keywords': "//*[contains(text(),'Nøkkelord')]/.."
        },
        'management': {
            'title': "//div[@data-controller='storeVisitedAd trackAd']//section[1]",
            'definition_1': "//div[@data-controller='storeVisitedAd trackAd']//section[2]",
            'content': "//div[@class='import-decoration']",
            'definition_2': "//dl[@class='definition-list definition-list--inline']",
            'keywords': "//*[contains(text(),'Nøkkelord')]/.."
        },
        'parttime': {
            'title': "//div[@data-controller='storeVisitedAd trackAd']//section[1]",
            'definition_1': "//div[@data-controller='storeVisitedAd trackAd']//section[2]",
            'content': "//div[@class='import-decoration']",
            'definition_2': "//dl[@class='definition-list definition-list--inline']",
            'keywords': "//*[contains(text(),'Nøkkelord')]/.."
        },
        'positions': {
            'definition_1': "div[1]//dl[1]",
            'title': "div[1]//h1[1]",
            'content': "div[1]//section[1]",
            'definition_2': "div[2]//dl[1]"
        }
    }


def get_sub_urls():
    return [
        'job/fulltime',
        'job/parttim/',
        'realestate/homes',
        'realestate/newbuildings',
        'realestate/plots',
        'realestate/leisuresale',
        'realestate/leisureplots',
        'realestate/lettings',
        'realestate/wanted',
        'realestate/businesssale',
        'realestate/businessrent',
        'realestate/businessplots',
        'realestate/companyforsale',
        'realestate/abroad'
    ]