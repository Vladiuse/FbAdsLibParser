from datetime import datetime, timedelta
from time import sleep
from parser import get_driver, FbAdsLibParser
from parser.keywords import KeyWord
from parser.exceptions import FbBlockLibError, MaxWaitCardLoadError, NoLoadCardBtnError, CriticalError

DB_PATH = './keyword.db'
GLOBAL_ERRORS_LIMIT = 2
COUNTRY = 'US'
LANGUAGE = 'en'

key_words = KeyWord(db_path=DB_PATH)
DRIVER = get_driver()
fb_adslib_parser = FbAdsLibParser(DRIVER)
fb_adslib_parser.open_main()
while True:
    key = key_words.get_key(language=LANGUAGE, range=(1, 500))
    fb_adslib_parser.open_lib(q=key, country=COUNTRY)
    global_errors_count = 0
    try:
        fb_adslib_parser.parse()
    except FbBlockLibError as error:
        error()
        sleep(15)
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
