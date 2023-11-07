from configparser import ConfigParser

conf_file_path = './conf.ini'
config = ConfigParser()
config.read(conf_file_path, encoding='utf-8')

