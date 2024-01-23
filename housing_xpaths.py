scraping_xpaths = {
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
    'newbuildings': {
        'step': '//div[@class="styles__StepColor-sc-8clrzb-0 hzAclB"]',
    },
    'plots': {},
    'leisuresale': {},
    'leisureplots': {},
    'wanted': {},
    'businessale': {},
    'businessrent': {},
    'businessplots': {},
    'companyforsale': {},
    'abroad': {},
}
