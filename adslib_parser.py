import argparse
from time import sleep
from configparser import ConfigParser
from parser.loger import TxtLogger
from run_parse import test_driver, run_adslib_parser, get_ip
from parser.keywords import KeyWord

config_file_path = './conf.ini'
config = ConfigParser()
config.read(config_file_path)


parser = argparse.ArgumentParser(description='xxxx')
parser.add_argument('command', type=str, help='Запуск команды')
parser.add_argument('-proxy', type=str, default=None, help='Proxy id')
parser.add_argument('-country', type=str, default=None, help='Countryd')
parser.add_argument('-language', type=str, default=None, help='Language of keywords')


def run_parser(*args,**kwargs):
    print('RUN PARSER')
    print(args)
    print(kwargs)


def run_logee(*args,**kwargs):
    print('RUN loger')
    print(args)
    print(kwargs)


available_commands = {
    'parse': run_parser,
    'parse_stat': run_logee,
}
args = parser.parse_args()

txt_loger = TxtLogger()
if args.command == 'parse':
    INFINITY = True if config.get('AdsLibParser', 'infinity') == 'true' else False
    if not args.country:
        country = config.get('KeyWord', 'country')
    else:
        country = args.country
    if not args.language:
        language = config.get('KeyWord', 'language')
    else:
        language = args.language
    start_key = config.get('KeyWord', 'start_key')
    end_key = config.get('KeyWord', 'end_key')
    if args.proxy:
        try:
            proxy = config['Proxy'][args.proxy]
            proxy_change_ip_url = config['ProxyChangeIpUrl'][args.proxy]
        except KeyError:
            print('Incorrect proxy id')
            exit()
    else:
        proxy = None
        proxy_change_ip_url = None

    if not INFINITY:
        run_adslib_parser(txt_loger, country=country, language=language,   keys_range=(start_key, end_key),
                      proxy=proxy,proxy_change_ip_url=proxy_change_ip_url,

                )
    else:
        loop_count = 0
        while True:
            loop_count += 1
            print(f'InFY loop #{loop_count}')
            try:
                run_adslib_parser(txt_loger, country=country, language=language, keys_range=(start_key, end_key),
                                  proxy=proxy, proxy_change_ip_url=proxy_change_ip_url,
                                  )
            except Exception as error:
                print(error)
                print('LOOP EXCEPTION')
            sleep(60)
elif args.command == 'parse_stat':
    txt_loger.log_file_stat()

elif args.command == 'keys_stat':
    KeyWord().keys_stat()
elif args.command == 'test_proxy':
    if args.proxy:
        try:
            proxy = config['Proxy'][args.proxy]
        except KeyError:
            print('Incorrect proxy id')
            exit()
        test_driver(proxy=proxy)
    else:
        print('Chose proxy for test')
elif args.command == 'get_ip':
    if args.proxy:
        try:
            proxy = config['Proxy'][args.proxy]
        except KeyError:
            print('Incorrect proxy id')
            exit()
    else:
        proxy = None
        get_ip(proxy=proxy)

else:
    print('Incorrect command')
    print('Available_commands:', list(available_commands.keys()))




