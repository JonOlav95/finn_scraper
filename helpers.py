import logging
import os
import re
import sys
from datetime import datetime

import yaml


def extract_datetime(filename):
    date_and_time = re.search(r'(\d{4}_\d{2}_\d{2}-\d{2}_\d{2})', filename)

    if not date_and_time:
        return None
    
    parsed_datetime = datetime.strptime(date_and_time[0], '%Y_%m_%d-%H_%M')
    parsed_datetime = parsed_datetime.strftime('%Y_%m_%d-%H_%M')

    return parsed_datetime



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
            'pricing_inciactive': '//div[@data-testid="pricing-incicative-price"]//span[2]', # Finn typo
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
        'newbuildings': {
            'title': '//h1[@class="mb-16 text-34"]',
            'sub_title': '//h2[@class="mb-16 text-22"]',
            'stpe': '//div[@class=" w-full flex"]',
            'price': '//p[contains(text(), "Pris")]/following-sibling::p[1]',
            'total_price': '//p[contains(text(), "Totalpris")]/following-sibling::p[1]',
            'joint_debt': '//p[contains(text(), "Fellesgjeld")]/following-sibling::p[1]',
            'local_area_name': '//svg[@alt="Beliggenhet ikon"]/following-sibling::p[1]',
            'keywords': "//h3[contains(text(),'Nøkkelord') or contains(text(), 'Nøkkelinfo')]/following-sibling::div[1]",
            'short_about': '//h3[contains(text(), "Kort om prosjektet")]/following-sibling::p[1]',
            'facilities': '//h3[contains(text(),"Fasiliteter")]/following-sibling::div[1]',
            'units_in_project': '//table[@class="w-full"]',
            'about': '//h3[contains(text(),"Beskrivelse")]/following-sibling::div[1]',
            'location': '//h3[@id="beliggenhet"]/following-sibling::div[1]'
        },
        'nybygg': {
            'title': '//h1[@class="mb-16 text-34"]',
            'sub_title': '//h2[@class="mb-16 text-22"]',
            'stpe': '//div[@class=" w-full flex"]',
            'price': '//p[contains(text(), "Pris")]/following-sibling::p[1]',
            'total_price': '//p[contains(text(), "Totalpris")]/following-sibling::p[1]',
            'joint_debt': '//p[contains(text(), "Fellesgjeld")]/following-sibling::p[1]',
            'local_area_name': '//svg[@alt="Beliggenhet ikon"]/following-sibling::p[1]',
            'keywords': "//h3[contains(text(),'Nøkkelord') or contains(text(), 'Nøkkelinfo')]/following-sibling::div[1]",
            'short_about': '//h3[contains(text(), "Kort om prosjektet")]/following-sibling::p[1]',
            'facilities': '//h3[contains(text(),"Fasiliteter")]/following-sibling::div[1]',
            'units_in_project': '//table[@class="w-full"]',
            'about': '//h3[contains(text(),"Beskrivelse")]/following-sibling::div[1]',
            'location': '//h3[@id="beliggenhet"]/following-sibling::div[1]'
        },
        'leisuresale': {
            'title': '//section[@data-testid="object-title"]//h1',
            'local_area_name': '//div[@data-testid="local-area-name"]',
            'pricing_inciactive': '//div[@data-testid="pricing-indicative-price"]//span[2]', # Finn no typo
            'pricing_details': '//section[@data-testid="pricing-details"]//dl',
            'key_info': '//section[@data-testid="key-info"]//dl',
            'facilities': '//section[@data-testid="object-facilities"]//div',
            'about': '//section[@data-testid="about-property"]',
            'location': '//span[@data-testid="object-address"]'
        },

        'abroad': {
            'title': '//section[@data-testid="object-title"]//h1',
            'local_area_name': '//div[@data-testid="local-area-name"]',
            'pricing_inciactive': '//div[@data-testid="pricing-indicative-price"]//span[2]',  # Finn no typo
            'pricing_details': '//section[@data-testid="pricing-details"]//dl',
            'key_info': '//section[@data-testid="key-info"]//dl',
            'facilities': '//section[@data-testid="object-facilities"]//div',
            'about': '//section[@data-testid="about-property"]',
            'location': '//span[@data-testid="object-address"]'
        },

        'plots': {
            'title': '//section[@data-testid="object-title"]//h1',
            'local_area_name': '//div[@data-testid="local-area-name"]',
            'pricing_inciactive': '//div[@data-testid="pricing-indicative-price"]//span[2]',  # Finn no typo
            'pricing_details': '//section[@data-testid="pricing-details"]//dl',
            'key_info': '//section[@data-testid="key-info"]//dl',
            'facilities': '//section[@data-testid="object-facilities"]//div',
            'about': '//section[@data-testid="about-property"]',
            'location': '//span[@data-testid="object-address"]'
        },

        'wanted': {
            'title': '//section[@data-testid="object-title"]//h1',
            'pricing_inciactive': '//div[@data-testid="letting-wanted-price"]',  # Finn no typo
            'pricing_details': '//section[@data-testid="pricing-details"]//dl',
            'key_info': '//section[@data-testid="key-info"]//dl',
            'region_info': '//section[@data-testid="region-info"]//dl',
            'facilities': '//section[@data-testid="object-facilities"]//div',
            'about': '//section[@data-testid="about-property"]',
            'location': '//span[@data-testid="object-address"]'
        },

        'businesssale': {
            'title': '//section[@data-testid="object-title"]//h1',
            'local_area_name': '//div[@data-testid="local-area-name"]',
            'pricing_inciactive': '//div[@data-testid="pricing-indicative-price"]//span[2]',  # Finn no typo
            'pricing_details': '//section[@data-testid="pricing-details"]//dl',
            'key_info': '//section[@data-testid="key-info"]//dl',
            'facilities': '//section[@data-testid="object-facilities"]//div',
            'about': '//section[@data-testid="about-property"]',
            'location': '//span[@data-testid="object-address"]'
        },

        'businessrent': {
            'title': '//section[@data-testid="object-title"]//h1',
            'local_area_name': '//div[@data-testid="local-area-name"]',
            'pricing_inciactive': '//div[@data-testid="pricing-indicative-price"]//span[2]',  # Finn no typo
            'pricing_details': '//section[@data-testid="pricing-details"]//dl',
            'key_info': '//section[@data-testid="key-info"]//dl',
            'facilities': '//section[@data-testid="object-facilities"]//div',
            'about': '//section[@data-testid="about-property"]',
            'location': '//span[@data-testid="object-address"]'
        },

        'businessplots': {
            'title': '//section[@data-testid="object-title"]//h1',
            'local_area_name': '//div[@data-testid="local-area-name"]',
            'pricing_inciactive': '//div[@data-testid="pricing-indicative-price"]//span[2]',  # Finn no typo
            'pricing_details': '//section[@data-testid="pricing-details"]//dl',
            'key_info': '//section[@data-testid="key-info"]//dl',
            'facilities': '//section[@data-testid="object-facilities"]//div',
            'about': '//section[@data-testid="about-property"]',
            'location': '//span[@data-testid="object-address"]'
        },

        'companyforsale': {
            'title': '//section[@data-testid="object-title"]//h1',
            'local_area_name': '//div[@data-testid="local-area-name"]',
            'pricing_inciactive': '//div[@data-testid="pricing-indicative-price"]//span[2]',  # Finn no typo
            'pricing_details': '//section[@data-testid="pricing-details"]//dl',
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
            'definition_1': "//div[@data-testid='aggregated-ad-object']//div[1]//dl[1]",
            'title': "//div[@data-testid='aggregated-ad-object']//div[1]//h1[1]",
            'content': "//div[@data-testid='aggregated-ad-object']//div[1]//section[1]",
            'definition_2': "//div[@data-testid='aggregated-ad-object']//div[2]//dl[1]"
        }
    }


def get_sub_urls():
    return [
        'job/fulltime',
        'job/parttime',
        'job/management',
        'realestate/homes',
        'realestate/plots',
        'realestate/leisureplots',
        'realestate/lettings',
        'realestate/wanted',
        'realestate/abroad',
        'realestate/leisuresale',
        'realestate/newbuildings',
        'realestate/businesssale',
        'realestate/businessrent',
        'realestate/businessplots',
        'realestate/companyforsale',
    ]
