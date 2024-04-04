import sqlite3
import os
from config import config
import random as r
from settings import USE_DOT


class KeyWord:

    def __init__(self):
        self.db_path = config.get('DB', 'db_file_path')

        self._check_db()

    def _check_db(self):
        if not os.path.exists(self.db_path):
            raise ValueError('Db no exists')

    def get_key(self, language, range):
        start, end = range
        con = sqlite3.connect(self.db_path)
        cursor = con.cursor()
        command = f"SELECT * FROM keyword WHERE number_in_dict BETWEEN {start} AND {end} AND language = '{language}' ORDER BY RANDOM() LIMIT 1"
        cursor.execute(command)
        row = cursor.fetchone()
        pk, word, lang, number_in_dict = row
        return word,number_in_dict

    def keys_stat(self):
        con = sqlite3.connect(self.db_path)
        cursor = con.cursor()
        command = """
        SELECT language,COUNT(*) FROM keyword GROUP BY language;
        """
        cursor.execute(command)
        rows = cursor.fetchall()
        for row in rows:
            lang, count = row
            print(lang, count)

number_keywords = [str(i) for i in range(10)]
chars_keywords = ['!', '?', '%', '$']
DOT = '.'

def get_random_keyword():
    keywords = number_keywords + chars_keywords
    if USE_DOT:
        if r.randint(0,1):
            return DOT
    return r.choice(keywords)


