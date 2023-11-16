from selenium import webdriver
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.firefox.options import Options
from seleniumwire import webdriver as wire_webdriver
from pathlib import Path
import os
from config import config


curr_file_path = Path(__file__).parent.absolute()
FIREFOX_PROFILE_DIR_PATH = os.path.join(curr_file_path, 'firefox_profile')

def get_firefox_driver(proxy=None):
    service = webdriver.FirefoxService(
        service_args=['--profile-root', FIREFOX_PROFILE_DIR_PATH],
    )
    options = Options()
    if config.get('Driver', 'headless') == 'true':
        options.add_argument('--headless')
    if proxy:
        seleniumwire_options = {
        'proxy': {
            'http': proxy,
            'https': proxy,
            }
        }

        DRIVER = wire_webdriver.Firefox(
            service=service,
            seleniumwire_options=seleniumwire_options,
            options=options,
        )
    else:
        DRIVER = webdriver.Firefox(
            service=service,
            options=options,
        )

    return DRIVER

if __name__ == '__main__':
    driver = get_firefox_driver(
        #proxy='http://kEJANU:AN6rAD6ur3Ca@lu.mobileproxy.space:1249'
    )
    driver.get('https://api.ipify.org?format=html')
    print(driver.page_source)
    input()
# 119.0.1

