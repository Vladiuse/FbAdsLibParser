import os
from selenium import webdriver
from requests.models import PreparedRequest
from time import sleep
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from .cards import CardSearch
import time
from selenium.common.exceptions import NoSuchElementException
from datetime import datetime, timedelta
from .exceptions import *
from config import config

NEXT_KEY = """
##############
#  NEXT KEY  #
##############
"""

class FbAdsLibUrl:
    FB_ADSLIB_MAIN_PAGE = 'https://web.facebook.com/ads/library'
    ACTIVE = 'active'
    INACTIVE = 'inactive'
    ACTIVE_STATUS = (ACTIVE, INACTIVE)

    URL_PARAMS = {'active_status': None,
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

    def __init__(self, *, q, country, start_date=None, active_status=ACTIVE):
        self.q = q
        self.country = country
        self.start_date = start_date if start_date else str(datetime.now().date() - timedelta(days=1))
        self.active_status = active_status
        print(self.active_status, 'xxx')

    def _get_params(self):
        params = self.URL_PARAMS
        params['q'] = self.q
        params['country'] = self.country
        params['active_status'] = self.active_status
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

    MAX_WAIT_TIME_CARDS_LOAD = float(config.get('AdsLibParser', 'card_load_timeout_sec'))
    NEW_CARDS_BNT_WAIT = float(config.get('AdsLibParser', 'new_cards_btn_timeout_sec'))

    # TODO add cards count
    # TODO add get payment data
    # TODo добавить голосовое сколько прошло времени - час два (мб нужно будет менять айпи)

    def open_main(self):
        """Открыть главную страницу библиотеки"""
        print('Open main')
        try:
            self.driver.get(FbAdsLibUrl.FB_ADSLIB_MAIN_PAGE)
        except TimeoutException as error:
            print(error)
            print('TimeOut')

    def open_lib(self, *,q, country,active_status,**kwargs):
        """Открыть страницу с карточками"""
        print(f'Open key: {q}')
        fb_lib_url = FbAdsLibUrl(q=q, country=country,active_status=active_status,**kwargs).url
        try:
            self.driver.get(fb_lib_url)
        except TimeoutException as error:
            print(error)
            print('TimeOut')

    def open_my_ip(self):
        self.driver.get('https://2ip.ru/')

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
        start = time.time()
        """ожидать кнопку загрузки новыз карточек"""
        while True:
            if time.time() - start > FbAdsLibParser.NEW_CARDS_BNT_WAIT:
                raise NoLoadCardBtnError
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
            yield links
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

    # TODO is cards exists on page
