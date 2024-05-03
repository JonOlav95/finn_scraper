import random

from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from helpers import load_flags

from random import choice


def get_pc_options(width=1472, height=828, headless=True) -> ChromeOptions:
    """
    Generate default Chrome driver options
    :param width: int
    :param height: int
    :param headless: bool
    :return: Options
    """

    chrome_options = ChromeOptions()
    # chrome_options.page_load_strategy = 'none'

    if headless:
        chrome_options.add_argument("--headless=new")

    # return chrome_options

    chrome_options.add_argument(load_user_agent())

    chrome_options.add_argument("--enable-automation")
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument(f"--window-size={width}{height}")
    chrome_options.add_argument("--lang=en-GB")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-setuid-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-accelerated-2d-canvas")
    # chrome_options.add_argument("--proxy-server='direct://")
    # chrome_options.add_argument("--proxy-bypass-list=*")
    chrome_options.add_argument("--allow-running-insecure-content")
    chrome_options.add_argument("--disable-web-security")
    chrome_options.add_argument("--disable-client-side-phishing-detection")
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--mute-audio")
    chrome_options.add_argument("--ignore-certificate-errors")
    chrome_options.add_argument("--remote-allow-origins=*")


    # Disable downloads
    chrome_options.add_experimental_option(
        'prefs', {
            'safebrowsing.enabled': 'false',
            'download.prompt_for_download': False,
            'download.default_directory': '/dev/null',
            'download_restrictions': 3,
            'profile.default_content_setting_values.notifications': 2,
        }
    )

    return chrome_options


def load_user_agent():
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

    return choice(user_agents)


def get_raspberry_options():
    chrome_options = ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument(load_user_agent())
    chrome_options.add_argument("--lang=en-GB")

    if random.randint(0, 1) == 1:
        chrome_options.add_argument("--disable-client-side-phishing-detection")
        chrome_options.add_argument("--disable-notifications")

    if random.randint(0, 1) == 1:
        chrome_options.add_argument("--mute-audio")
        chrome_options.add_argument("--ignore-certificate-errors")

    return chrome_options


def load_driver():
    flags = load_flags()

    if flags['raspberry']:
        service = Service(executable_path='/usr/bin/chromedriver')
        options = get_raspberry_options()
    else:
        service = None
        options = get_pc_options(headless=flags['headless'])

    return webdriver.Chrome(options=options, service=service)
