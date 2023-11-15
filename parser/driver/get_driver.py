from .chrome import get_chrome_driver
from .firefox import get_firefox_driver

def get_driver(type='chrome', proxy=None):
    if type == 'chrome':
        return get_chrome_driver(proxy=proxy)
    elif type == 'firefox':
        return get_firefox_driver(proxy=proxy)