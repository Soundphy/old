"""
Scraping module for soundfxcenter.
"""
import os
import csv
from hashlib import sha1

import requests
from bs4 import BeautifulSoup


def download_html(route, output_directory):
    webpage = 'http://dota2.gamepedia.com'
    response = requests.get(webpage + route)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'html.parser')
    heroes = soup.find_all('div', attrs={'style': 'position: relative;'})

    for hero in heroes:
        page = hero.find('a').attrs['href']
        name = hero.find('a').attrs['title']
        response = requests.get(webpage + page + '/Responses')
        try:
            response.raise_for_status()
        except Exception:
            continue
        print('Saving %s...' % name)
        path = os.path.join(output_directory, name)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w') as fout:
            fout.write(response.text)


def parse_html(html_directory, csv_path, keywords):
    with open(csv_path, 'w') as fout:
        writer = csv.writer(fout)
        writer.writerow(['identifier', 'url', 'title', 'description'])
        kwlist = [x.strip() for x in keywords.split(',')]
        for name in os.listdir(html_directory):
            with open(os.path.join(html_directory, name)) as fin:
                text = fin.read()

            soup = BeautifulSoup(text, 'html.parser')
            links = soup.find_all('a', attrs={'title': 'Play'})

            urls = [link.attrs['href'] for link in links]
            titles = [link.parent.text.strip(' Play ') for link in links]

            for url, title in zip(urls, titles):
                identifier = sha1(url.encode('ascii')).hexdigest()
                full_title = kwlist[0] + ' ' + name + ' ' + title
                description = ' '.join(kwlist + [name, title])
                writer.writerow([identifier, url, full_title, description])
