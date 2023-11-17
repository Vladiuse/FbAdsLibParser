from datetime import datetime, timedelta
from time import sleep, time
from parser import get_driver, FbAdsLibParser
from parser.keywords import KeyWord
from selenium.common.exceptions import TimeoutException
from parser.exceptions import FbBlockLibError, MaxWaitCardLoadError, NoLoadCardBtnError, CriticalError
from parser.pinger import Pinger
from bs4 import BeautifulSoup
from config import config
from print_color import print as cprint


GLOBAL_ERRORS_LIMIT = 2
pinger = Pinger()


def run_adslib_parser(txt_loger,*,country, language, proxy=None, keys_range=(1,500)):
    print('\n','*'*30)
    print('PC:', config.get('Pc', 'name'))
    print('Country:',country, )
    print('Language:', language)
    print('Proxy:', proxy if proxy else '-')
    print('KeyRange:', keys_range)
    print('*'*30, end='\n\n')
    key_words = KeyWord()
    DRIVER = get_driver(proxy=proxy)
    fb_adslib_parser = FbAdsLibParser(DRIVER)
    print('Open main')
    fb_adslib_parser.open_main()
    pinger()
    while True:
        key = key_words.get_key(language=language, range=keys_range)
        print('Open key', key)
        fb_adslib_parser.open_lib(q=key, country=country)
        try:
            for links in fb_adslib_parser.parse():
                txt_loger.log_links_in_file(links)
                pinger()
                current_time = datetime.now().strftime('%H:%M:%S')
                links_len = len(links)
                print(f'Links: {links_len}, Key: {key}','Time:', current_time)
                if config.get('AdsLibParser', 'show_colors'):
                    if links_len > 25:
                        cprint('#' * len(links), color='green')
                    elif links_len >= 10:
                        cprint('#' * len(links), color='yellow')
                    else:
                        cprint('#' * len(links), color='red')
                else:
                    print('#' * len(links))
        except (MaxWaitCardLoadError, NoLoadCardBtnError) as error:
            print(key, '\n', error)
            error()
        except FbBlockLibError as error:
            error()
            sleep(10)
            DRIVER.quit()
            exit()
        except Exception as error:
            print('Exception\nException\nException\n')
            print(key, '\n', error)
            CriticalError()()
            DRIVER.quit()
            exit()


def test_driver(*,proxy):
    DRIVER = get_driver(proxy=proxy)
    fb_adslib_parser = FbAdsLibParser(DRIVER)
    fb_adslib_parser.open_my_ip()
    input('Press enter to exit ')
    DRIVER.quit()
    exit()


def get_ip(*,proxy):
    DRIVER = get_driver(proxy=proxy)
    DRIVER.get('https://api.ipify.org?format=html')
    soup = BeautifulSoup(DRIVER.page_source, 'lxml')
    print(soup.text)
    exit()

