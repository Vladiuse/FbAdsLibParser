from config import config

PC_NAME = config.get('Pc', 'name').upper()
COUNTRY = config.get('KeyWord', 'country').upper()


def set_country(country):
    global COUNTRY
    COUNTRY = country