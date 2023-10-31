import os
from selenium import webdriver
# from seleniumwire import webdriver
from requests.models import PreparedRequest
from time import sleep
from selenium.webdriver.common.by import By
from .cards import CardSearch
import time
from selenium.common.exceptions import NoSuchElementException
from datetime import datetime, timedelta
from playsound import playsound
from print_color import print as cprint
from .exceptions import *
from .loger import log_links_in_file

NEXT_KEY = """
##############
#  NEXT KEY  #
##############
"""

class FbAdsLibUrl:
    FB_ADSLIB_MAIN_PAGE = 'https://web.facebook.com/ads/library'

    URL_PARAMS = {'active_status': 'active',
                  # 'ad_type': 'political_and_issue_ads',
                  'ad_type': 'all',
                  'country': None,
                  'q': None,
                  'sort_data[direction]': 'desc',
                  'sort_data[mode]': 'relevancy_monthly_grouped',
                  'search_type': 'keyword_unordered',
                  'media_type': 'all',
                  'start_date[min]': None,
                  'start_date[max]': '',
                  'publisher_platforms[0]': 'facebook',
                  }

    FB_LIB_URL = 'https://www.facebook.com/ads/library/'

    def __init__(self, *, q, country, start_date=None):
        self.q = q
        self.country = country
        self.start_date = start_date if start_date else str(datetime.now().date() - timedelta(days=1))

    def _get_params(self):
        params = self.URL_PARAMS
        params['q'] = self.q
        params['country'] = self.country
        params['start_date[min]'] = self.start_date
        return params

    def _prepare_url(self):
        prepare = PreparedRequest()
        prepare.prepare_url(self.FB_LIB_URL, self._get_params())
        return prepare.url

    @property
    def url(self):
        return self._prepare_url()

class FbAdsLibParser:

    def __init__(self, driver):
        self.driver = driver

    PAGES_FOR_KEY_WORD = 200

    MAX_WAIT_TIME_CARDS_LOAD = 30

    # TODO add cards count
    # TODO add get payment data
    # TODo добавить голосовое сколько прошло времени - час два (мб нужно будет менять айпи)

    def open_main(self):
        self.driver.get(FbAdsLibUrl.FB_ADSLIB_MAIN_PAGE)

    def open_lib(self, *,q, country,**kwargs):
        fb_lib_url = FbAdsLibUrl(q=q, country=country,**kwargs)
        self.driver.get(fb_lib_url)


    def remove_all_cards(self):
        """Удалить все карточки со страницы"""
        self.driver.execute_script("""
var cards = document.querySelectorAll('div.xrvj5dj.xdq2opy.xexx8yu.xbxaen2.x18d9i69.xbbxn1n.xdoe023.xbumo9q.x143o31f.x7sq92a.x1crum5w > div.xh8yej3')
for (let i=0; i < cards.length; i++){
    var card = cards[i]
    card.remove()
};
""")

    def click_load_new_js(self):
        """Клик на кнопку загрузки новых карт"""
        self.driver.execute_script("""
var load_new_button = document.querySelector('a._8n_3')
load_new_button.click()
                """)

    def click_load_new_cards(self):
        """ожидать кнопку загрузки новыз карточек"""
        for _ in range(20):
            self._is_fb_block_loading()
            sleep(1)  # 1 is old value
            if self.cards_count():  # не кликать кнопку - если карточки стали загружаться автоматически
                return
            try:
                button = self.driver.find_element(By.CSS_SELECTOR, 'a._8n_3')
                sleep(0.5)  # 1 is old value
                if button:
                    if self.cards_count():  # не кликать кнопку - если карточки стали загружаться автоматически
                        return
                    self.click_load_new_js()
                    return
            except NoSuchElementException as error:
                pass
        raise NoLoadCardBtnError

    def hide_cards_media(self):
        """Скрить медиа контент у карточек"""
        self.driver.execute_script("""
const styleNoMedia = document.createElement("style")
styleNoMedia.textContent = "div.xrvj5dj.xdq2opy.xexx8yu.xbxaen2.x18d9i69.xbbxn1n.xdoe023.xbumo9q.x143o31f.x7sq92a.x1crum5w > div.xh8yej3  ._7jyg._7jyh{display:none;}"
document.head.appendChild(styleNoMedia)
        """)

    def cards_count(self):
        """Посчитать сколько карточек на странице"""
        cards = self.driver.find_elements(By.CSS_SELECTOR,
                                     'div.xrvj5dj.xdq2opy.xexx8yu.xbxaen2.x18d9i69.xbbxn1n.xdoe023.xbumo9q.x143o31f.x7sq92a.x1crum5w > div.xh8yej3')
        return len(cards)

    def get_links(self):
        """Достать ссылки на группы из верски"""
        html = str(self.driver.page_source)
        cards_searcher = CardSearch(html)
        return cards_searcher.links

    def parse(self):
        self.hide_cards_media()
        while True:
            self._wait_cards_load()
            links = self.get_links()
            log_links_in_file(links)
            current_time = datetime.now().strftime('%H:%M:%S')
            print(f'Links count: {len(links)}', current_time)
            print('#' * len(links))
            self.remove_all_cards()
            self.click_load_new_cards()

    def _wait_cards_load(self):
        """Ждать появления карточек"""
        start = time.time()
        while True:
            self._is_fb_block_loading()
            cards_count = self.cards_count()
            if cards_count:
                sleep(0.5)
                break
            else:
                if time.time() - start > self.MAX_WAIT_TIME_CARDS_LOAD:
                    raise MaxWaitCardLoadError
                else:
                    sleep(0.1)
                    continue

    def _is_fb_block_loading(self):
        """Проверить не поялился ли блок 'Слишком много запросов' """
        try:
            info_block = self.driver.find_element(By.CSS_SELECTOR,
                                             'div.x11408do.xr1yuqi.xkrivgy.x4ii5y1.x1gryazu.xw5ewwj.xh8yej3.x2b8uid')
            if info_block:
                raise FbBlockLibError
        except NoSuchElementException:
            pass


# PROXY = 'http://MeHeS7:Eb1Empua4ES6@nproxy.site:14569/'
# options = {
# 	'proxy': {
#         'https':PROXY,
# 	}
# }


options = webdriver.ChromeOptions()
# options.add_argument('--headless')
DRIVER = webdriver.Chrome(
    options=options,
    # seleniumwire_options=options
)
DRIVER.maximize_window()
def parse_by_keys(keys, country):
    DRIVER.get(FbAdsLibUrl.FB_ADSLIB_MAIN_PAGE)
    DAYS_AGO = 1
    start_date = str(datetime.now().date() - timedelta(days=DAYS_AGO))
    global_errors_count = 0
    GLOBAL_ERRORS_LIMIT = 2
    fb_adslib = FbAdsLibParser(DRIVER)
    for key in keys:
        try:
            cprint(NEXT_KEY, color='green')
            fb_lib_url = FbAdsLibUrl(q=key, country=country, start_date=start_date).url
            DRIVER.get(fb_lib_url)
            # DRIVER.get(fb_lib_page.url)  # todo add timeout and check status code
            global_errors_count = 0
            fb_adslib.parse()
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

    DRIVER.quit()
