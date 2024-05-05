import logging
import os
import re
import sys
import yaml

from random import choice



def load_random_headers():
    user_agents = [
        'user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2859.0 Safari/537.36',
        'user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
        'user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.49 Safari/537.36',
        'user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:55.0) Gecko/20100101 Firefox/55.0',
        'user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2876.0 Safari/537.36',
        'user-agent=Mozilla/5.0 (X11; Linux i686 (x86_64)) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3187.0 Safari/537.366',
        'user-agent=Mozilla/5.0 (X11;Fedora; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3178.0 Safari/537.36',
        'user-agent=Mozilla/5.0 (X11; Linux x86_64; rv:55.0) Gecko/20100101 Firefox/55.0',
        'user-agent=Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:55.0) Gecko/20100101 Firefox/55.0',
    ]


    headers = {
        "User-Agent": choice(user_agents),
        "Accept-Language": "en-GB,en,q=0.5",
        "Referer": "https://google.com",
        "DNT": "1"
    }

    return headers
    


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



def load_xpath(key):

    default_housing = {
        "text": {
            'title': '//section[@data-testid="object-title"]//h1',
            'local_area_name': '//span[@data-testid="object-address"]',
            'pricing_inciactive': '//div[@data-testid="pricing-indicative-price"]//span[2]',
            'about': '//section[@data-testid="about-property"]',
            'location': '//span[@data-testid="object-address"]'
        },
        "html": {
            'cadastreinfo_part': '//h2[@id="cadastreinfo-part"]/following-sibling::div[1]',
            'key_info': '//section[@data-testid="key-info"]//dl',
            'facilities': '//section[@data-testid="object-facilities"]//div',
            'pricing_details': '//section[@data-testid="pricing-details"]//dl',
        }
    },


    default_work = {
        "text": {
            'title': "//div[@data-controller='storeVisitedAd trackAd']//section[1]//h1",
            'content': "//div[@class='import-decoration']//section",
            'keywords': "//*[contains(text(),'Nøkkelord')]/following-sibling::*"
        },
        "html": {
            'definition_1': "//div[@data-controller='storeVisitedAd trackAd']//section[2]//dl",
            'definition_2': "//dl[@class='definition-list definition-list--inline']",
        }
    }

    newbuildings = {
        "text": {
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
        "html": {

        }
    }

    xpaths = {
        "homes": {
            "text": {
                'title': '//section[@data-testid="object-title"]//h1',
                'local_area_name': '//span[@data-testid="object-address"]',
                'pricing_inciactive': '//div[@data-testid="pricing-incicative-price"]//span[2]', # Finn typo
                'about': '//section[@data-testid="about-property"]',
                'location': '//span[@data-testid="object-address"]'
            },
            "html": {
                'cadastreinfo_part': '//h2[@id="cadastreinfo-part"]/following-sibling::div[1]',
                'key_info': '//section[@data-testid="key-info"]//dl',
                'facilities': '//section[@data-testid="object-facilities"]//div',
                'pricing_details': '//section[@data-testid="pricing-details"]//dl',
            }
        },

        'positions': {
            "text": {
                'title': "//div[@data-testid='aggregated-ad-object']//div[1]//h1[1]",
                'content': "//div[@data-testid='aggregated-ad-object']//div[1]//section[1]",

            },
            "html": {
                'definition_1': "//div[@data-testid='aggregated-ad-object']//div[1]//dl[1]",
                'definition_2': "//div[@data-testid='aggregated-ad-object']//div[2]//dl[1]"
            }
       },

        'lettings': {
            "text": {
                'title': '//section[@data-testid="object-title"]//h1',
                'pricing_common_monthly_cost': '//div[@data-testid="pricing-common-monthly-cost"]//dd',
                'pricing_depositum': '//div[@data-testid="pricing-deposit"]//dd',
                'pricing_common_includes': '//div[@data-testid="pricing-common-includes"]//dd',
                'key_info': '//section[@data-testid="key-info"]//dl',
                'facilities': '//section[@data-testid="object-facilities"]//div',
                'about': '//section[@data-testid="about-property"]',
                'location': '//span[@data-testid="object-address"]'
            },
            "html": {
            }
        },

        'newbuildings': newbuildings,
        'nybygg': newbuildings,

        'leisuresale': default_housing,
        'abroad': default_housing,
        'plots': default_housing,
        'wanted': default_housing,
        'businesssale': default_housing,
        'businessrent': default_housing,
        'businessplots': default_housing,
        'companyforsale': default_housing,

        'fulltime': default_work,
        'management': default_work,
        'parttime': default_work,
    }

    if key not in xpaths.keys():
        return None

    return xpaths[key]



def get_sub_urls():
    return [
        'job/fulltime',
        'job/parttime',
        'job/management',
        'realestate/homes',

        'realestate/newbuildings',
        
        'realestate/plots',
        'realestate/leisureplots',
        'realestate/lettings',
        'realestate/wanted',
        'realestate/abroad',
        'realestate/leisuresale',
        'realestate/businesssale',
        'realestate/businessrent',
        'realestate/businessplots',
        'realestate/companyforsale',
    ]
