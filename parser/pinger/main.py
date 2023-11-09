import requests as req
from config import config
from requests.exceptions import RequestException
from print_color import print as cprint

DOMAIN =  config.get('Pinger', 'domain')
URL = config.get('Pinger', 'ping_url')

class PingeReqError(Exception):

    TEXT_COLOR = 'red'

    PLAY_SOUND = config.get('AdsLibParser', 'play_sound')
    SHOW_COLORS = config.get('AdsLibParser', 'show_colors')

    def __init__(self, error_text):
        self.error_text = error_text

    def __call__(self):
        if PingeReqError.SHOW_COLORS == 'true':
            cprint(f'[Pinger] \n{self.error_text}', color=self.TEXT_COLOR)
        else:
            print(f'[Pinger] {self.error_text}')



class Pinger:
    IS_NEED_PING = config.get('Pinger', 'need_ping')
    PC_NAME = config.get('Pc', 'name')
    PING_URL = f'http://{DOMAIN}/{URL}/{PC_NAME}/'
    PING_TRY = int(config.get('Pinger', 'error_ping_count'))


    def __call__(self):
        if Pinger.IS_NEED_PING == 'true':
            for _ in range(Pinger.PING_TRY):
                try:
                    self.ping()
                except PingeReqError as error:
                    error()
                else:
                    break

    def ping(self):
        try:
            res = req.get(Pinger.PING_URL)
            if res.status_code == 200:
                print('[Pinger] success')
            else:
                raise PingeReqError('status code not 200')
        except RequestException as error:
            error_text = str(error)
            raise PingeReqError(error_text)


