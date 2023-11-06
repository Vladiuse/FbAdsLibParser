from datetime import datetime, timedelta
from time import sleep, time
from parser import get_driver, FbAdsLibParser
from parser.keywords import KeyWord
from parser.exceptions import FbBlockLibError, MaxWaitCardLoadError, NoLoadCardBtnError, CriticalError

DB_PATH = './keyword.db'
GLOBAL_ERRORS_LIMIT = 2



def run_adslib_parser(txt_loger,*,country, language, proxy=None, keys_range=(1,500)):
    print(txt_loger,country, language, proxy,keys_range )
    key_words = KeyWord(db_path=DB_PATH)
    DRIVER = get_driver(proxy=proxy)
    fb_adslib_parser = FbAdsLibParser(DRIVER)
    fb_adslib_parser.open_main()
    while True:
        key = key_words.get_key(language=language, range=keys_range)
        fb_adslib_parser.open_lib(q=key, country=country)
        global_errors_count = 0
        try:
            for links in fb_adslib_parser.parse():
                txt_loger.log_links_in_file(links)
                current_time = datetime.now().strftime('%H:%M:%S')
                print(f'Links: {len(links)},','Time:', current_time)
                print('#' * len(links))
        except FbBlockLibError as error:
            error()
            sleep(10)
            DRIVER.quit()
            exit()
        except (MaxWaitCardLoadError, NoLoadCardBtnError) as error:
            print(key, '\n', error)
            error()
        except Exception as error:
            print(key, '\n', error)
            CriticalError()()
            global_errors_count += 1
            if global_errors_count >= GLOBAL_ERRORS_LIMIT:
                DRIVER.quit()
                exit()


def test_driver(txt_loger,*,country, language, proxy=None, keys_range):
    DRIVER = get_driver(proxy=proxy)
    fb_adslib_parser = FbAdsLibParser(DRIVER)
    fb_adslib_parser.open_my_ip()
    input('Exit?')
