import os
import re
import sys
import sqlite3
import requests


def create_database(db_name):
    db_connection = sqlite3.connect(db_name)
    cursor = db_connection.cursor()
    NAME = 'test'
    COLUMNS = 'url TEXT PRIMARY KEY, description TEXT'
    query = 'CREATE TABLE IF NOT EXISTS {} ({})'.format(NAME, COLUMNS)
    cursor.execute(query)
    db_connection.commit()


def download_instantsfun_es(db_name):
    WEBPAGE = 'http://www.instantsfun.es'
    response = requests.get(WEBPAGE)
    response.raise_for_status()

    buttons = [x for x in response.text.split('\n') if 'type="audio' in x]
    descriptions = [re.findall('title="([^"]*)', x)[0] for x in buttons]
    urls = [WEBPAGE + re.findall('source src="([^"]*mp3)', x)[0]
            for x in buttons]

    db_connection = sqlite3.connect(db_name)
    cursor = db_connection.cursor()
    NAME = 'test'
    for x in zip(urls, descriptions):
        marks = ','.join(['?'] * len(x))
        query = 'INSERT OR REPLACE INTO {} VALUES ({})'.format(NAME, marks)
        cursor.execute(query, x)
    db_connection.commit()


def create_and_fill_database(db_name):
    create_database(db_name)
    download_instantsfun_es(db_name)


def print_database(db_name):
    create_database(db_name)
    db_connection = sqlite3.connect(db_name)
    cursor = db_connection.cursor()
    for row in cursor.execute('SELECT * FROM test'):
        print(row)
    db_connection.commit()


if __name__ == '__main__':
    DB_NAME = 'local.db'
    create_and_fill_database(DB_NAME)
    print_database(DB_NAME)
