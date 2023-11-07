from print_color import print as cprint
import os
from pathlib import Path
from playsound import playsound
from config import config


curr_file_path = Path(__file__).parent.absolute()
MEDIA_FILES_DIR = 'media'
MEDIA_FILES_DIR_PATH = os.path.join(curr_file_path, MEDIA_FILES_DIR)

class ParserError(Exception):
    TEXT = ''
    error_sound_path = ''
    TEXT_COLOR = 'red'

    PLAY_SOUND = config.get('AdsLibParser', 'play_sound')
    SHOW_COLORS = config.get('AdsLibParser', 'show_colors')

    @classmethod
    def __call__(cls):
        if ParserError.SHOW_COLORS == 'true':
            cprint(cls.TEXT, color=cls.TEXT_COLOR)
        else:
            print(cls.TEXT)
        if ParserError.PLAY_SOUND == 'true':
            media_path = os.path.join(MEDIA_FILES_DIR_PATH, cls.error_sound_path)
            playsound(media_path)

NEXT_KEY = """
##############
#  NEXT KEY  #
##############
"""


class FbBlockLibError(ParserError):
    """Блокировка фейсбуком запросов в библеотеку"""
    TEXT = """
############################
#                          #
#  FACEBOOK BLOCK LIBRARY  #
#                          #
############################
"""
    error_sound_path = 'fb_block_lib.mp3'
    TEXT_COLOR = 'red'


class MaxWaitCardLoadError(ParserError):
    """Превышено время ожидания карточек"""

    TEXT = """
#######################
#                     #
#  CARD WAIT TIMEOUT  #
#                     #
#######################
    """
    error_sound_path = 'card_wait_timeout.mp3'
    TEXT_COLOR = 'yellow'


class NoLoadCardBtnError(ParserError):
    """Кнопка загрузки новых карточек не найдена"""
    TEXT = """
###########################
#                         #
#  LOAD BTN WAIT TIMEOUT  #
#                         #
###########################
        """
    error_sound_path = 'load_btn_not_found.mp3'
    TEXT_COLOR = 'yellow'


class UnKnownError(ParserError):
    TEXT = """
    ###################
    #                 #
    #  UNKNOWN ERROR  #
    #                 #
    ###################
    """
    error_sound_path = 'unknown_error.mp3'
    TEXT_COLOR = 'yellow'

class CriticalError(ParserError):
    TEXT = """
    ####################
    #                  #
    #  CRITICAL ERROR  #
    #                  #
    ####################
    """
    error_sound_path = 'critical_error.mp3'
    TEXT_COLOR = 'red'


if __name__ == '__main__':
    # try:
    #     raise FbBlockLibError
    # except FbBlockLibError as error:
    #     error()
    FbBlockLibError()()