import logging
import os
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



def work_xpaths(key):
    
    default_work = {
        'title': "//div[@data-controller='storeVisitedAd trackAd']//section[1]//h1",
        'content': "//div[@class='import-decoration']//section",
        'keywords': "//*[contains(text(),'Nøkkelord')]/following-sibling::*",
        'definition_1': "//div[@data-controller='storeVisitedAd trackAd']//section[2]//dl", # html
        'definition_2': "//dl[@class='definition-list definition-list--inline']", # html
    }
    xpaths = {
        'positions': {
            'title': "//div[@data-testid='aggregated-ad-object']//div[1]//h1[1]",
            'content': "//div[@data-testid='aggregated-ad-object']//div[1]//section[1]",
            'definition_1': "//div[@data-testid='aggregated-ad-object']//div[1]//dl[1]", # html
            'definition_2': "//div[@data-testid='aggregated-ad-object']//div[2]//dl[1]" # html
        
        },
        
        'fulltime': default_work,
        'management': default_work,
        'parttime': default_work,
    }

    if key not in xpaths.keys():
        return None

    return xpaths[key]


def housing_xpaths(key):

    # Common xpaths
    title = {'title': '//section[@data-testid="object-title"]//h1'}
    local_area_name = {'local_area_name': '//div[@data-testid="local-area-name"]'}
    about = {'about': '//section[@data-testid="about-property"]'}
    address = {'address': '//span[@data-testid="object-address"]'}
    cadastreinfo_part = {'cadastreinfo_part': '//h2[@id="cadastreinfo-part"]/following-sibling::div[1]'}
    key_info = {'key_info': '//section[@data-testid="key-info"]//dl'}
    facilities = {'facilities': '//section[@data-testid="object-facilities"]//div'}
    pricing_details = {'pricing_details': '//section[@data-testid="pricing-details"]//dl'}
    pricing_indicative = {'pricing_indicative': '//div[contains(@data-testid, "pricing-indicative-price") \
                          or contains(@data-testid, "pricing-incicative-price")]//span[2]'}
    
    # Uncommon xpaths
    sub_title = {'sub_title': '//section[@data-testid="object-title"]//h1'}

    default_housing = {
        **title,
        **local_area_name,
        **pricing_indicative,
        **about,
        **address,
        **cadastreinfo_part,
        **key_info,
        **pricing_details,
        **facilities 
    }

    xpaths = {
        'lettings': {
            **title,
            **key_info,
            **address,  
            **facilities,
            **about,
            **pricing_details
        },

        'planned': {
            **title,
            **key_info,
            **address,
            **about,
            **sub_title
        },

        'project': {
            **title,
            **key_info,
            **address,
            **about,
            **facilities,
            **sub_title,
            'pricing_indicative': '//div[@data-testid="pricing-incicative-price"]//span[1]//span[2]', # Different structure
        },

        'projectsingle': {
            **title,
            **key_info,
            **address,
            **about,
            **facilities,
            **sub_title,
            **pricing_details,
            **local_area_name,
            **pricing_indicative
        },

        'projectleisure': {
            **title,
            **key_info,
            **address,
            **about,
            **facilities,
            **sub_title,
            **pricing_details,
            **local_area_name,
            **pricing_indicative,
        },

        'wanted': {
            **title,
            **key_info,
            **about,
            'max_rent': '//div[@data-testid="letting-wanted-price"]//dd',
        },

        'abroad': {
            **title,
            **key_info,
            **address,
            **about,
            **facilities,
            **pricing_indicative,
            **pricing_details,
        },


        "homes": default_housing,
        'leisuresale': default_housing,
        'plots': default_housing,
        'businesssale': default_housing,
        'businessrent': default_housing,
        'businessplots': default_housing,
        'companyforsale': default_housing
    }
    
    if key not in xpaths.keys():
        return None

    return xpaths[key]




def load_xpath(key):

    if key in ['fulltime', 'positions', 'management', 'parttime']:
        return work_xpaths(key)
    
    return housing_xpaths(key)


def get_sub_urls():
    return [
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

        'job/fulltime',
        'job/parttime',
        'job/management',
    ]
