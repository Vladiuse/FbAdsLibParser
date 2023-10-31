from selenium import webdriver
from seleniumwire import webdriver as webdriver_wire


def get_driver(*,proxy=None):
    pass
    if not proxy:
        options = webdriver.ChromeOptions()

        DRIVER = webdriver.Chrome(
            options=options,
        )
        DRIVER.maximize_window()
    else:
        PROXY = 'http://MeHeS7:Eb1Empua4ES6@nproxy.site:14569/'
        options = {
        	'proxy': {
                'https':PROXY,
        	}
        }
        DRIVER = webdriver_wire.Chrome(
            seleniumwire_options=options
        )
    DRIVER.maximize_window()
    # options.add_argument('--headless')
    return DRIVER



if __name__ == '__main__':
    driver = get_driver(proxy='1')
    driver.get('https://google.com/')
    input('Exit?')
    driver.quit()
