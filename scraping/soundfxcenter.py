"""
Scraping module for soundfxcenter.
"""
import os
import re
import csv
from hashlib import sha1

import requests
from bs4 import BeautifulSoup


def pages(route):
    webpage = 'http://soundfxcenter.com' + route
    response = requests.get(webpage + '0')
    response.raise_for_status()
    last = int(re.findall('\/([0-9]*)">>>', response.text)[-1])
    for i in range(0, last + 10, 10):
        yield str(i), webpage + str(i)


def parse_html(html_directory, csv_path, keywords):
    with open(csv_path, 'w') as fout:
        writer = csv.writer(fout)
        writer.writerow(['identifier', 'url', 'title', 'description'])
        kwlist = [x.strip() for x in keywords.split(',')]
        for fname in os.listdir(html_directory):
            with open(os.path.join(html_directory, fname)) as fin:
                text = fin.read()
            soup = BeautifulSoup(text, 'html.parser')
            for audio in soup.find_all('audio'):
                url = audio.attrs['src']
                identifier = sha1(url.encode('ascii')).hexdigest()
                title = audio.find_previous('table').find('strong').text
                if title.lower().endswith(' sound effect'):
                    title = title[:-len(' sound effect')]
                for keyword in kwlist:
                    if title.lower().startswith(keyword.lower() + ' '):
                        title = title[len(keyword):].strip()
                full_title = kwlist[0] + ' ' + title
                description = ' '.join(kwlist + [title])
                writer.writerow([identifier, url, full_title, description])
