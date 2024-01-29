import re
import os
from config import config
from datetime import datetime

PC_NAME = config.get('Pc', 'name').upper()
COUNTRY = config.get('KeyWord', 'country').upper()
def _k(num):
    if num > 1000:
        num = round(num / 1000, 1)
        return str(num) + 'k'
    return str(num)


class TxtLogger:
    TXT_LOG_DIR = config.get('Loger', 'log_dir_path')
    LOF_FILE_NANE = f'{PC_NAME}_{COUNTRY}_links.txt'

    def __init__(self):
        self.log_file_path = f'{TxtLogger.TXT_LOG_DIR}/{TxtLogger.LOF_FILE_NANE}'

    def log_links_in_file(self, links):
        """Записать ссылки из карточек в лог файл"""
        with open(self.log_file_path, 'a', encoding='utf-8') as file:
            current_time = datetime.now().strftime('%H:%M:%S')
            head = f'\n##### Links count: {len(links)}, Time: {current_time}\n'
            file.write(head)
            for link in links:
                file.write(link + '\n')

    @staticmethod
    def _get_fbgroup_id_from_url(url: str) -> str:
        url = url.strip()
        url = url.replace(' ', '')
        url = url.replace('\n', '')
        url = url.replace('http://', 'https://')
        url = url.replace('://www.', '://')
        if not url.endswith('/'):
            url = url + '/'
        patterns = [
            r'^https://facebook.com/\d{3,30}/$',
            r'^https://facebook.com/.{3,80}/$',
            r'^https://fb.com/page-\d{3,30}/$',
        ]
        for pattern in patterns:
            if re.match(pattern, url):
                url = url[:-1]
                url = url.replace('https://facebook.com/', '')
                url = url.replace('https://fb.com/page-', '')
                return url
        return ''

    def get_links_from_file(self):
        group_links = []
        with open(self.log_file_path, encoding='utf-8') as file:
            for line in file:
                group_link = TxtLogger._get_fbgroup_id_from_url(line)
                if group_link:
                    group_links.append(group_link)
        return group_links

    def log_file_stat(self):
        links = self.get_links_from_file()
        total_links_count = len(links)
        unique_links_count = len(set(links))
        unique_percent = round(unique_links_count / total_links_count * 100)

        print('\n')
        print(PC_NAME)
        print('File: ', os.path.basename(self.log_file_path))
        print(f'Total: {_k(total_links_count)}')
        print(f'Unique: {_k(unique_links_count)} ({unique_percent}%)')
