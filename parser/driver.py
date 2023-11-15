from selenium import webdriver
from seleniumwire import webdriver as webdriver_wire
from config import config


def get_driver(*,proxy=None):
    options = webdriver.ChromeOptions()

    if not proxy:
        if config.get('Driver', 'headless') == 'true':
            options.add_argument('--headless')
        DRIVER = webdriver.Chrome(
            options=options,
        )
        DRIVER.maximize_window()
    else:
        options = {
        	'proxy': {
                'https':proxy,
        	}
        }

        chrome_options = webdriver.ChromeOptions()
        if config.get('Driver', 'headless') == 'true':
            chrome_options.add_argument('--headless')
        if config.get('Driver', 'no_sandbox') == 'true':
            chrome_options.add_argument('--no-sandbox')
        DRIVER = webdriver_wire.Chrome(
            seleniumwire_options=options,
            options=chrome_options,
        )
    if config.get('Driver', 'max_window') == 'true':
        DRIVER.maximize_window()
    return DRIVER



if __name__ == '__main__':
    driver = get_driver(proxy='1')
    driver.get('https://google.com/')
    input('Exit?')
    driver.quit()
