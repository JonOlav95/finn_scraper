

def work_xpaths(key):

    default_work = {
        'title': "//div[@data-controller='storeVisitedAd trackAd']//section[1]//h1",
        'content': "//div[@class='import-decoration']//section",
        'keywords': "//*[contains(text(),'Nøkkelord')]/following-sibling::*",
        'definition_1': "//div[@data-controller='storeVisitedAd trackAd']//section[2]//dl",
        'definition_2': "//dl[@class='definition-list definition-list--inline']",
        'last_edited': '//*[text()="Sist endret"]/following-sibling::*[1]'

    }
    xpaths = {
        'positions': {
            'title': "//div[@data-testid='aggregated-ad-object']//div[1]//h1[1]",
            'content': "//div[@data-testid='aggregated-ad-object']//div[1]//section[1]",
            'definition_1': "//div[@data-testid='aggregated-ad-object']//div[1]//dl[1]",
            'definition_2': "//div[@data-testid='aggregated-ad-object']//div[2]//dl[1]",
            'last_edited': '//*[text()="Sist endret"]/following-sibling::*[1]'
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
    last_edited = {'last_edited': '//tr[th[text()="Sist endret"]]/td'}

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
            'pricing_indicative': '//div[@data-testid="pricing-incicative-price"]//span[1]//span[2]',  # Different structure
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

        'plots': {
            **title,
            **pricing_indicative,
            **about,
            **address,
            **cadastreinfo_part,
            **key_info,
            **pricing_details,
            **facilities
        },

        'businessrent': {
            **title,
            **pricing_indicative,
            **about,
            **address,
            **cadastreinfo_part,
            **key_info,
            **pricing_details
        },


        "homes": default_housing,
        'leisuresale': default_housing,
        'businesssale': default_housing,
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
