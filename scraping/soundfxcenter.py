"""
Scraping module for soundfxcenter.
"""
import os
import csv
from hashlib import sha1

import requests
from bs4 import BeautifulSoup


def download_html(route, output_directory):
    i = 0
    while True:
        webpage = 'http://soundfxcenter.com' + route + str(i)
        response = requests.get(webpage)
        i += 10
        try:
            response.raise_for_status()
        except Exception as e:
            print(e)
            continue
        print('Saving %s...' % webpage)
        path = os.path.join(output_directory, str(i))
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w') as fout:
            fout.write(response.text)
        if '>>>' not in response.text:
            break


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
                for kw in kwlist:
                    if title.lower().startswith(kw.lower() + ' '):
                        title = title[len(kw):].strip()
                full_title = kwlist[0] + ' ' + title
                description = ' '.join(kwlist + [title])
                writer.writerow([identifier, url, full_title, description])
