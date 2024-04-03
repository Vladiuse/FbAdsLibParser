from datetime import datetime, timedelta
from time import sleep, time
from parser import get_driver, FbAdsLibParser
from parser.keywords import KeyWord
from selenium.common.exceptions import TimeoutException, WebDriverException
from parser.exceptions import FbBlockLibError, MaxWaitCardLoadError, NoLoadCardBtnError, CriticalError, FbLibEmptyQuery
from parser.pinger import Pinger
from bs4 import BeautifulSoup
from config import config
from print_color import print as cprint
from parser import change_proxy_ip
from parser.fbadslib_url import get_random_url
from settings import set_country


GLOBAL_ERRORS_LIMIT = 2
pinger = Pinger()

DROP_DRIVER = True if config.get('Driver', 'drop_driver_key') == 'true' else False
def run_adslib_parser(txt_loger,*,country, language, active_status,keys_range=(1,500),
                      proxy=None, proxy_change_ip_url=None,start_date=None,
                      ):
    # print('\n')
    # print('*'*30)
    # print('PC:', config.get('Pc', 'name'))
    # print('Country:',country, )
    # print('Language:', language)
    # print('KeyRange:', keys_range)
    # print('Proxy:', proxy if proxy else '-')
    # print('ProxyCIU:', proxy_change_ip_url if proxy_change_ip_url else '-')
    # print('Active status:', active_status)
    # print('Start date:',)
    # print('*'*30, end='\n\n')

    key_words = KeyWord()
    DRIVER = get_driver(proxy=proxy)
    fb_adslib_parser = FbAdsLibParser(DRIVER)
    fb_adslib_parser.open_main()
    while True:
        key,number_in_dict = key_words.get_key(language=language, range=keys_range)
        fblib_url = get_random_url()
        print(repr(fblib_url))
        fb_adslib_parser.open_lib(str(fblib_url))
        set_country(fblib_url.country)
        try:
            for links in fb_adslib_parser.parse():
                txt_loger.log_links_in_file(links,fblib_url)
                pinger()
        except (MaxWaitCardLoadError, NoLoadCardBtnError) as error:
            print( error)
            error()
            if DROP_DRIVER:
                DRIVER.quit()
                break
        except FbLibEmptyQuery as error:
            print(error)
            error()
        except FbBlockLibError as error:
            error()
            DRIVER.quit()
            if proxy:
                sleep(10)
                change_proxy_ip(proxy_change_ip_url)
                break
            else:
                exit()
        except WebDriverException as error:
            print('WebDriverException\nWebDriverException\nWebDriverException\n')
            print(error)
            CriticalError()()
            DRIVER.quit()
            break


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

