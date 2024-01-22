from .chrome import get_chrome_driver
from .firefox import get_firefox_driver
from config import config

def get_driver(type='chrome', proxy=None):
    driver_type = config.get('Driver', 'type')
    if driver_type == 'chrome':
        print('Open Chrome')
        return get_chrome_driver(proxy=proxy)
    elif driver_type == 'firefox':
        print('Open Firefox')
        return get_firefox_driver(proxy=proxy)
    else:
        raise TypeError('Incorrect driver type\nAvaible only "chrome" and "firefox"')
