"""
Scraping module for soundfxcenter.
"""
import os
import csv
from hashlib import sha1

import requests
from bs4 import BeautifulSoup


SECTIONS = [
    dict(keywords='StarCraft SC',
         folder='soundfxcenter_starcraft',
         route='/sound-effects/starcraft/'),
]

DATA_PATH = 'data'


def download_html(section):
    i = 0
    while True:
        webpage = 'http://soundfxcenter.com' + section['route'] + str(i)
        response = requests.get(webpage)
        i += 10
        try:
            response.raise_for_status()
        except Exception as e:
            print(e)
            continue
        print('Saving %s...' % webpage)
        path = os.path.join(DATA_PATH, section['folder'], 'html', str(i))
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w') as fout:
            fout.write(response.text)
        if '>>>' not in response.text:
            break


def parse_html(section):
    section_path = os.path.join(DATA_PATH, section['folder'])
    html_path = os.path.join(section_path, 'html')
    with open(os.path.join(section_path, 'test.csv'), 'w') as fout:
        writer = csv.writer(fout)
        writer.writerow(['identifier', 'keywords', 'title',
                         'url', 'description'])
        keywords = section['keywords'].split()
        for fname in os.listdir(html_path):
            with open(os.path.join(html_path, fname)) as fin:
                text = fin.read()
            soup = BeautifulSoup(text, 'html.parser')
            for audio in soup.find_all('audio'):
                url = audio.attrs['src']
                identifier = sha1(url.encode('ascii')).hexdigest()
                title = audio.find_previous('table').find('strong').text
                if title.lower().endswith(' sound effect'):
                    title = title[:-len(' sound effect')]
                title = ' '.join(x for x in title.split()
                                 if x not in keywords)
                description = title
                writer.writerow([identifier, section['keywords'], title,
                                 url, description])


if __name__ == '__main__':
    for section in SECTIONS:
        parse_html(section)
