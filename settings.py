from config import config

PC_NAME = config.get('Pc', 'name').upper()
COUNTRY = config.get('KeyWord', 'country').upper()
USE_DOT = True if config.get('KeyWord', 'use_dot') == 'true' else False

def set_country(country):
    global COUNTRY
    COUNTRY = country