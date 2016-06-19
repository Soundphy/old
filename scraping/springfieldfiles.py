"""
Scraping module for springfieldfiles.
"""
import os
import re
import csv
from hashlib import sha1

import requests
from bs4 import BeautifulSoup


def download_html(route, output_directory):
    webpage = 'http://www.springfieldfiles.com/'
    response = requests.get(webpage + route)
    response.raise_for_status()
    for line in response.text.split('\n'):
        aux = re.findall('<td width=..%.*<font size=3>([^<]*)<.*', line)
        if not aux:
            aux = re.findall('<td width=20%>([^<]*)</td>', line)
        if aux:
            name = aux[0]
            continue
        aux = re.findall('<td width=..%><a href="([^"]*)"', line)
        if not aux:
            continue
        url = aux[0]
        response = requests.get(webpage + url)
        try:
            response.raise_for_status()
        except Exception as e:
            print(e)
            continue
        fname = name + '_' + url.split('sounds/')[-1]
        print('Saving %s...' % name)
        path = os.path.join(output_directory, fname)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w') as fout:
            fout.write(response.text)


def parse_html(html_directory, csv_path, keywords):
    webpage = 'http://www.springfieldfiles.com/'
    with open(csv_path, 'w') as fout:
        writer = csv.writer(fout)
        writer.writerow(['identifier', 'url', 'title', 'description'])
        kwlist = [x.strip() for x in keywords.split(',')]
        for fname in os.listdir(html_directory):
            with open(os.path.join(html_directory, fname)) as fin:
                text = fin.read()
            lines = text.split('\n')[::-1]
            while len(lines):
                line = lines.pop()
                sound = re.findall('href="(sounds[^"]*.mp3)">.*', line)
                if not sound:
                    continue
                line = lines.pop()
                title = BeautifulSoup(line, 'html.parser').text
                if not title:
                    continue
                title = title.strip('"')
                url = webpage + sound[0]
                identifier = sha1(url.encode('ascii')).hexdigest()
                for keyword in kwlist:
                    if title.lower().startswith(keyword.lower() + ' '):
                        title = title[len(keyword):].strip()
                character = fname.split('_')[0]
                if not title.lower().startswith(character):
                    title = character + ' ' + title
                full_title = kwlist[0] + ' ' + title
                description = ' '.join(kwlist + [title])
                writer.writerow([identifier, url, full_title, description])
