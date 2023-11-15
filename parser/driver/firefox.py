from selenium import webdriver
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from seleniumwire import webdriver as wire_webdriver
from config import config

def firefox_driver(proxy=None):

PROXY = 'http://kEJANU:AN6rAD6ur3Ca@lu.mobileproxy.space:1249'
seleniumwire_options = {
'proxy': {
    'http': PROXY,
    'https': PROXY,
    }
}


firefox_profile = FirefoxProfile()
#firefox_profile.set_preference("javascript.enabled", False)

service = webdriver.FirefoxService(
    service_args=['--profile-root', './firefox_profile'],
)

options = webdriver.FirefoxOptions()
#options.binary_location = '/usr/local/bin/geckodriver'
options.profile = firefox_profile
driver = wire_webdriver.Firefox(
    service=service,
    seleniumwire_options=seleniumwire_options,
)
driver.get('https://google.com/')
input()

# 119.0.1
